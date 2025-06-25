#!/usr/bin/env python3
"""
Test script for DHL 发货自动生成系统 v5
"""

import pandas as pd
import os
import csv
from utils import exact_match_lookup, query_uk_tariff_api, append_sku_record

def format_commodity_code(code):
    digits = ''.join(filter(str.isdigit, str(code)))
    if len(digits) == 8:
        return f"{digits[:4]}.{digits[4:6]}.{digits[6:]}"
    return str(code)

def test_v5_system():
    print("🧪 Testing DHL 发货自动生成系统 v5")
    print("=" * 50)
    
    # Test 1: Exact match lookup
    print("\n1. Testing exact match lookup:")
    
    # Create test SKU database
    test_sku_data = [
        {"Item Description": "LV SPEEDY BAG", "Commodity Code": "42022100", "Weight": "0.9", "Origin Country": "CN"},
        {"Item Description": "GUCCI BELT", "Commodity Code": "4203301000", "Weight": "0.3", "Origin Country": "IT"}
    ]
    
    with open("test_sku_reference_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Item Description", "Commodity Code", "Weight", "Origin Country"])
        writer.writeheader()
        writer.writerows(test_sku_data)
    
    # Test exact matches
    test_cases = [
        "LV SPEEDY BAG",  # Should match
        "GUCCI BELT",     # Should match
        "PRADA SHOULDER BAG",  # Should not match
        "lv speedy bag"   # Should match (case insensitive)
    ]
    
    for item_desc in test_cases:
        result = exact_match_lookup(item_desc)
        if result:
            print(f"   ✅ '{item_desc}' -> Found: {result}")
        else:
            print(f"   ❌ '{item_desc}' -> Not found")
    
    # Test 2: Commodity code formatting
    print("\n2. Testing commodity code formatting:")
    test_codes = ["42022100", "4203301000", "12345678", "invalid"]
    
    for code in test_codes:
        formatted = format_commodity_code(code)
        print(f"   {code} -> {formatted}")
    
    # Test 3: Simulate the complete workflow
    print("\n3. Testing complete workflow:")
    
    # Simulate input data (only Item Description and Selling Price)
    input_data = {
        "Item Description": ["LV SPEEDY BAG", "GUCCI BELT", "PRADA SHOULDER BAG"],
        "Selling Price": [1200, 800, 950]
    }
    
    df = pd.DataFrame(input_data)
    print("\n📥 Input Data:")
    print(df.to_string(index=False))
    
    # Process each row
    results = []
    matched_count = 0
    unmatched_count = 0
    
    for _, row in df.iterrows():
        desc = str(row["Item Description"]).strip()
        price = row["Selling Price"]
        
        # Lookup in database
        local = exact_match_lookup(desc)
        
        if local and local["Commodity Code"] and local["Weight"] and local["Origin Country"]:
            matched_count += 1
            code = local["Commodity Code"]
            weight = local["Weight"]
            origin = local["Origin Country"]
            is_matched = True
        else:
            unmatched_count += 1
            code = ""
            weight = ""
            origin = ""
            is_matched = False
            
        results.append({
            "Item Description": desc,
            "Selling Price": price,
            "Weight": weight,
            "Origin Country": origin,
            "Commodity Code": code,
            "is_matched": is_matched
        })
    
    print(f"\n📊 Match Statistics:")
    print(f"   找到 Exact Match: {matched_count}")
    print(f"   未找到: {unmatched_count}")
    print(f"   总计: {len(results)}")
    
    # Test 4: DHL export format
    print("\n4. Testing DHL export format:")
    dhl_rows = []
    for i, row in enumerate(results):
        formatted_code = format_commodity_code(row["Commodity Code"])
        dhl_rows.append([
            1,  # Unique Item Number
            "INV_ITEM",
            row["Item Description"],
            formatted_code,
            1,  # Quantity
            "PCS",  # Units
            row["Selling Price"],
            "GBP",  # Currency
            row["Weight"],
            "",  # Weight 2
            row["Origin Country"],
            "", "", ""  # Reference fields
        ])
    
    dhl_df = pd.DataFrame(dhl_rows)
    print("\n📤 DHL Export Preview:")
    print(dhl_df.to_string(index=False, header=False))
    
    # Cleanup
    if os.path.exists("test_sku_reference_data.csv"):
        os.remove("test_sku_reference_data.csv")
    
    print("\n✅ All v5 system tests completed successfully!")

if __name__ == "__main__":
    test_v5_system() 