#!/usr/bin/env python3
"""
Test script to verify the ProductHit attribute fixes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_product_finder import ProductHit

def test_product_hit_attributes():
    """Test that ProductHit has the correct attributes"""
    print("Testing ProductHit attributes...")
    
    # Create a ProductHit instance
    hit = ProductHit(
        name="Test Product",
        price=25000.0,
        brand="TestBrand",
        url="https://example.com",
        image_url="https://example.com/image.jpg",
        description="Test description",
        rating=4.5,
        reviews_count=1250
    )
    
    # Test all attributes
    print(f"✓ name: {hit.name}")
    print(f"✓ price: {hit.price}")
    print(f"✓ brand: {hit.brand}")
    print(f"✓ url: {hit.url}")
    print(f"✓ image_url: {hit.image_url}")
    print(f"✓ description: {hit.description}")
    print(f"✓ rating: {hit.rating}")
    print(f"✓ reviews_count: {hit.reviews_count}")
    print(f"✓ specifications: {hit.specifications}")
    
    # Test that invalid attributes don't exist
    invalid_attrs = ['seller_rating', 'product_rating', 'review_count', 'best_choice_reason']
    for attr in invalid_attrs:
        if hasattr(hit, attr):
            print(f"❌ ERROR: ProductHit should not have attribute '{attr}'")
        else:
            print(f"✓ Correctly missing invalid attribute: {attr}")
    
    print("\nProductHit attribute test completed!")
    return True

if __name__ == "__main__":
    test_product_hit_attributes()