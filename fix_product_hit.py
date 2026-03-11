#!/usr/bin/env python3
"""
Fix ProductHit class to add missing best_choice_reason attribute
"""

# Read the current smart_product_finder.py file
with open('smart_product_finder.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the malformed line
content = content.replace('reviews_count: int = 0`n    best_choice_reason: str = ""', 
                         'reviews_count: int = 0\n    best_choice_reason: str = ""')

# Write the corrected content back
with open('smart_product_finder.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed ProductHit class with proper best_choice_reason attribute")

# Verify the fix by reading the class
with open('smart_product_finder.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
print("\nProductHit class attributes:")
in_class = False
for line in lines:
    if 'class ProductHit:' in line:
        in_class = True
    elif in_class and line.strip().startswith('def '):
        break
    elif in_class and ':' in line and '=' in line:
        print(f"  {line.strip()}")