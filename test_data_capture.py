#!/usr/bin/env python3
"""
Test script to verify data capture and processing
"""

import pandas as pd

def test_data_capture():
    print("🧪 Testing Data Capture and Processing")
    print("=" * 50)
    
    # Simulate the input data (like from Excel upload)
    input_data = {
        "SKU": ["M46234", "1234567", "NEW123"],
        "Brand": ["LV", "GUCCI", "PRADA"],
        "Item Description": ["LV SPEEDY BAG", "GUCCI BELT", "PRADA SHOULDER BAG"],
        "Quantity": [1, 2, 1],
        "Units": ["EA", "EA", "EA"],
        "Selling": [1200, 800, 950],
        "Currency": ["GBP", "GBP", "GBP"],
        "Commodity Code": ["42022100", "4203301000", ""],
        "Weight": [0.9, 0.3, 0.7],
        "Country of Origin": ["CN", "IT", "IT"]
    }
    
    df = pd.DataFrame(input_data)
    print("\n📥 Input Data:")
    print(df.to_string(index=False))
    
    # Simulate the export process
    dhl_columns = [
        "Unique Item Number", "Item", "Item Description", "Commodity Code", "Quantity",
        "Units", "Value", "Currency", "Weight", "Weight 2", "Country of Origin",
        "Reference Type", "Reference Details", "Tax Paid"
    ]
    
    export_df = pd.DataFrame(columns=dhl_columns)
    
    print("\n🔄 Processing Data:")
    for i, row in df.iterrows():
        # Extract values (simulating the app logic)
        item_number = i + 1
        item_description = str(row.get("Item Description", "")).strip()
        commodity_code = str(row.get("Commodity Code", "")).strip()
        quantity = row.get("Quantity", 0)
        units = str(row.get("Units", "")).strip()
        selling = row.get("Selling", 0)
        currency = str(row.get("Currency", "GBP")).strip()
        weight = row.get("Weight", 0)
        country = str(row.get("Country of Origin", "")).strip()
        
        print(f"Row {i+1}:")
        print(f"  Item Number: {item_number}")
        print(f"  Description: {item_description}")
        print(f"  Commodity Code: {commodity_code}")
        print(f"  Quantity: {quantity}")
        print(f"  Units: {units}")
        print(f"  Selling: {selling}")
        print(f"  Currency: {currency}")
        print(f"  Weight: {weight}")
        print(f"  Country: {country}")
        print()
        
        export_df.loc[i] = [
            item_number,
            "INV_ITEM",
            item_description,
            commodity_code,
            quantity,
            units,
            selling,
            currency,
            weight,
            "",  # Weight 2
            country,
            "", "", ""  # Reference fields
        ]
    
    print("📤 Final DHL CSV Output:")
    print("-" * 50)
    csv_output = export_df.to_csv(index=False, header=False)
    print(csv_output)
    
    print("\n📊 DataFrame Preview:")
    print("-" * 50)
    print(export_df.to_string(index=False))
    
    print("\n✅ Data capture test completed!")
    
    return export_df

if __name__ == "__main__":
    test_data_capture() 