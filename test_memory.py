#!/usr/bin/env python3
"""
Test script for the enhanced field memory logic
"""

from utils import get_memory_values, save_sku_memory, get_default_weight
import pandas as pd

def test_memory_system():
    print("🧪 Testing Enhanced Field Memory System")
    print("=" * 50)
    
    # Test 1: Default weight estimation
    print("\n1. Testing default weight estimation:")
    test_items = [
        "LV SPEEDY BAG",
        "GUCCI BELT", 
        "NIKE SNEAKERS",
        "HERMES JACKET",
        "CHANEL DRESS"
    ]
    
    for item in test_items:
        weight = get_default_weight(item)
        print(f"   {item}: {weight} kg")
    
    # Test 2: Memory matching
    print("\n2. Testing memory matching:")
    
    # Test with existing data from memory database
    test_cases = [
        ("M46234", "LV", "LV SPEEDY BAG"),
        ("1234567", "GUCCI", "GUCCI BELT"),
        ("NEW123", "PRADA", "PRADA SHOULDER BAG"),
        ("", "HERMES", "HERMES BIRKIN BAG"),
    ]
    
    for sku, brand, desc in test_cases:
        values = get_memory_values(sku, brand, desc)
        print(f"   SKU: {sku}, Brand: {brand}, Desc: {desc}")
        print(f"   -> Commodity Code: {values['commodity_code']}")
        print(f"   -> Weight: {values['weight']}")
        print(f"   -> Country: {values['country']}")
        print()
    
    # Test 3: Save new memory
    print("3. Testing memory saving:")
    save_sku_memory(
        sku="TEST001",
        brand="TEST_BRAND", 
        item_description="TEST ITEM",
        commodity_code="12345678",
        weight="0.5",
        country="US"
    )
    print("   ✅ Saved new memory record")
    
    # Test 4: Verify saved memory
    print("\n4. Verifying saved memory:")
    values = get_memory_values("TEST001", "TEST_BRAND", "TEST ITEM")
    print(f"   Retrieved values: {values}")
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_memory_system() 