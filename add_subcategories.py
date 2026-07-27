#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, 'c:\\Electronicsmart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electronicsmart.settings')
django.setup()

from store.models import Category, SubCategory

# Mobiles
print("Adding Mobiles subcategories...")
mobiles = Category.objects.get(name='Mobiles')
subs = ['iPhone Series', 'Samsung Galaxy', 'OnePlus', 'Xiaomi Redmi', 'Vivo & Oppo']
for sub in subs:
    SubCategory.objects.get_or_create(name=sub, category=mobiles)
print("✓ Mobiles done!")

# Laptops
print("Adding Laptops subcategories...")
laptops = Category.objects.get(name='Laptops')
subs = ['Dell Laptops', 'HP Laptops', 'Lenovo Laptops', 'ASUS Laptops', 'MacBook']
for sub in subs:
    SubCategory.objects.get_or_create(name=sub, category=laptops)
print("✓ Laptops done!")

# Accessories
print("Adding Accessories subcategories...")
accessories = Category.objects.get(name='headphone')
subs = ['Wireless Headphones', 'Wired Earphones', 'Bluetooth Speakers', 'Gaming Headsets']
for sub in subs:
    SubCategory.objects.get_or_create(name=sub, category=accessories)
print("✓ Accessories done!")

# TV
print("Adding TV subcategories...")
tv = Category.objects.get(name='TV')
subs = ['32 inch', '43 inch', '55 inch', '65 inch', '4K Smart TV']
for sub in subs:
    SubCategory.objects.get_or_create(name=sub, category=tv)
print("✓ TV done!")

# AC
print("Adding AC subcategories...")
ac = Category.objects.get(name='AC')
subs = ['1 Ton AC', '1.5 Ton AC', '2 Ton AC', 'Split AC', 'Window AC']
for sub in subs:
    SubCategory.objects.get_or_create(name=sub, category=ac)
print("✓ AC done!")

print("\n✅ All subcategories created successfully!")

