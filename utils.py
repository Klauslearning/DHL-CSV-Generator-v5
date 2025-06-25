import csv
import os
import requests
import re

SKU_DB = "sku_reference_data.csv"
UK_TARIFF_API = "https://www.trade-tariff.service.gov.uk/api/v2/commodities?filter[description]={}"

def get_default_weight(item_description):
    """Estimate default weight based on item description keywords"""
    desc_lower = item_description.lower()
    
    # Weight categories in kg
    if any(word in desc_lower for word in ['shoe', 'boot', 'sneaker', 'footwear']):
        return 1.3
    elif any(word in desc_lower for word in ['jacket', 'coat', 'blazer']):
        return 1.5
    elif any(word in desc_lower for word in ['shirt', 'pants', 'dress', 'skirt', 'trouser', 'jeans', 'sweater', 'hoodie']):
        return 0.7
    elif any(word in desc_lower for word in ['belt', 'wallet', 'bag', 'purse', 'accessory', 'jewelry', 'watch']):
        return 0.3
    else:
        return 0.5  # Default fallback

def find_best_match(sku, brand, item_description, memory_data):
    """Find the best matching record using priority: Full SKU > Partial keyword > Brand"""
    desc_lower = item_description.lower()
    
    # Priority 1: Full SKU match
    for record in memory_data:
        if record['SKU'] and record['SKU'].strip() == sku.strip():
            return record
    
    # Priority 2: Partial keyword match in Item Description
    desc_words = re.findall(r'\b\w+\b', desc_lower)
    best_match = None
    best_score = 0
    
    for record in memory_data:
        if not record['Item Description']:
            continue
            
        record_desc_lower = record['Item Description'].lower()
        record_words = re.findall(r'\b\w+\b', record_desc_lower)
        
        # Calculate match score based on common words
        common_words = set(desc_words) & set(record_words)
        if len(common_words) > 0:
            score = len(common_words) / max(len(desc_words), len(record_words))
            if score > best_score and score > 0.3:  # Minimum 30% match threshold
                best_score = score
                best_match = record
    
    if best_match:
        return best_match
    
    # Priority 3: Brand match (least reliable)
    for record in memory_data:
        if record['Brand'] and record['Brand'].strip().lower() == brand.strip().lower():
            return record
    
    return None

def load_sku_memory():
    """Load memory database with enhanced format"""
    memory_data = []
    if os.path.exists(SKU_DB):
        with open(SKU_DB, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                memory_data.append({
                    'SKU': row.get('SKU', '').strip(),
                    'Brand': row.get('Brand', '').strip(),
                    'Item Description': row.get('Item Description', '').strip(),
                    'Commodity Code': row.get('Commodity Code', '').strip(),
                    'Weight': row.get('Weight', '').strip(),
                    'Country of Origin': row.get('Country of Origin', '').strip()
                })
    return memory_data

def save_sku_memory(sku, brand, item_description, commodity_code=None, weight=None, country=None):
    """Save memory with enhanced format including commodity code"""
    rows = []
    updated = False
    
    # Load existing data
    if os.path.exists(SKU_DB):
        with open(SKU_DB, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if this is the same item
                if (row.get('SKU', '').strip() == sku.strip() and 
                    row.get('Brand', '').strip() == brand.strip() and
                    row.get('Item Description', '').strip() == item_description.strip()):
                    
                    # Update existing record
                    if commodity_code:
                        row['Commodity Code'] = commodity_code
                    if weight:
                        row['Weight'] = weight
                    if country:
                        row['Country of Origin'] = country
                    updated = True
                
                rows.append(row)
    
    # Add new record if not found
    if not updated:
        rows.append({
            'SKU': sku,
            'Brand': brand,
            'Item Description': item_description,
            'Commodity Code': commodity_code or '',
            'Weight': weight or '',
            'Country of Origin': country or ''
        })
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(SKU_DB), exist_ok=True)
    
    # Write back to file
    with open(SKU_DB, "w", newline="", encoding="utf-8") as f:
        fieldnames = ['SKU', 'Brand', 'Item Description', 'Commodity Code', 'Weight', 'Country of Origin']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def get_memory_values(sku, brand, item_description):
    """Get memory values for an item using enhanced matching logic"""
    memory_data = load_sku_memory()
    match = find_best_match(sku, brand, item_description, memory_data)
    
    if match:
        return {
            'commodity_code': match.get('Commodity Code', ''),
            'weight': match.get('Weight', ''),
            'country': match.get('Country of Origin', '')
        }
    
    # Return default weight if no match found
    return {
        'commodity_code': '',
        'weight': str(get_default_weight(item_description)),
        'country': ''
    }

def exact_match_lookup(item_description):
    """Exact match lookup in SKU database"""
    if not os.path.exists(SKU_DB):
        return None
    with open(SKU_DB, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Item Description'].strip().lower() == item_description.strip().lower():
                return {
                    'Commodity Code': row.get('Commodity Code', '').strip(),
                    'Weight': row.get('Weight', '').strip(),
                    'Origin Country': row.get('Origin Country', '').strip()
                }
    return None

# 1. 本地模糊查找

def keyword_match(desc, ref_desc):
    # 简单关键词交集匹配
    desc_words = set(re.findall(r'\w+', desc.lower()))
    ref_words = set(re.findall(r'\w+', ref_desc.lower()))
    return len(desc_words & ref_words) > 0

def local_lookup(item_description):
    if not os.path.exists(SKU_DB):
        return None
    with open(SKU_DB, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if keyword_match(item_description, row['Item Description']):
                return {
                    'Commodity Code': row.get('Commodity Code', '').strip(),
                    'Weight': row.get('Weight', '').strip(),
                    'Origin Country': row.get('Origin Country', '').strip()
                }
    return None

# 2. UK Tariff API 查询

def query_uk_tariff_api(item_description):
    url = UK_TARIFF_API.format(requests.utils.quote(item_description))
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # 取第一个 commodity code
            if data.get('data') and len(data['data']) > 0:
                return data['data'][0]['id']
    except Exception as e:
        print(f"API error: {e}")
    return ''

# 3. 追加写入 SKU 数据库

def append_sku_record(item_description, commodity_code, weight, origin_country):
    # 先检查是否已存在
    exists = False
    if os.path.exists(SKU_DB):
        with open(SKU_DB, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Item Description'].strip().lower() == item_description.strip().lower():
                    exists = True
                    break
    if not exists:
        with open(SKU_DB, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Item Description", "Commodity Code", "Weight", "Origin Country"])
            if os.stat(SKU_DB).st_size == 0:
                writer.writeheader()
            writer.writerow({
                "Item Description": item_description,
                "Commodity Code": commodity_code,
                "Weight": weight,
                "Origin Country": origin_country
            })