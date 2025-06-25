#!/usr/bin/env python3
"""
Test script to verify DHL CSV output format
"""

import pandas as pd

def test_dhl_output_format():
    print("🧪 Testing DHL CSV Output Format")
    print("=" * 50)
    
    # Sample input data
    sample_data = [
        {
            "SKU": "M46234",
            "Brand": "LV", 
            "Item Description": "LV SPEEDY BAG",
            "Quantity": 1,
            "Units": "EA",
            "Selling": 1200,
            "Currency": "GBP",
            "Commodity Code": "42022100",
            "Weight": 0.9,
            "Country of Origin": "CN"
        },
        {
            "SKU": "1234567",
            "Brand": "GUCCI",
            "Item Description": "GUCCI BELT", 
            "Quantity": 2,
            "Units": "EA",
            "Selling": 800,
            "Currency": "GBP",
            "Commodity Code": "4203301000",
            "Weight": 0.3,
            "Country of Origin": "IT"
        }
    ]
    
    # Create DHL format DataFrame
    dhl_columns = [
        "Unique Item Number", "Item", "Item Description", "Commodity Code", "Quantity",
        "Units", "Value", "Currency", "Weight", "Weight 2", "Country of Origin",
        "Reference Type", "Reference Details", "Tax Paid"
    ]
    
    export_df = pd.DataFrame(columns=dhl_columns)
    
    for i, row in enumerate(sample_data):
        export_df.loc[i] = [
            1,  # Unique Item Number
            "INV_ITEM",  # Item
            row["Item Description"],
            row.get("Commodity Code", ""),
            row["Quantity"],
            row["Units"],
            row["Selling"],
            row.get("Currency", "GBP"),
            row["Weight"],
            "",  # Weight 2 - always blank
            row["Country of Origin"],
            "", "", ""  # Reference Type / Details / Tax Paid
        ]
    
    print("\n📋 DHL CSV Output Format:")
    print("-" * 30)
    print("Column Headers:")
    for i, col in enumerate(dhl_columns, 1):
        print(f"{i:2d}. {col}")
    
    print("\n📄 Sample Output (CSV format):")
    print("-" * 30)
    csv_output = export_df.to_csv(index=False, header=False)
    print(csv_output)
    
    print("\n📊 DataFrame Preview:")
    print("-" * 30)
    print(export_df.to_string(index=False))
    
    print("\n✅ DHL CSV format test completed!")
    
    return export_df

if __name__ == "__main__":
    test_dhl_output_format() 