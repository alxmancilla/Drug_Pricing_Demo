#!/usr/bin/env python3
"""
Generate comprehensive datasets for Drug Pricing Demo
Creates 50+ records for both drug_pricing and customer_pricing collections
"""

import json
from datetime import datetime

# Drug pricing data - 52 records
drug_pricing_data = [
    # Metformin - 8 records
    {"drug": "Metformin", "generic": "Metformin", "location": "Houston", "pharmacy": "CVS", "price": 8.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Metformin", "generic": "Metformin", "location": "Houston", "pharmacy": "Walgreens", "price": 9.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Metformin", "generic": "Metformin", "location": "Houston", "pharmacy": "Walmart", "price": 7.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Metformin", "generic": "Metformin", "location": "Houston", "pharmacy": "Costco", "price": 6.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Metformin", "generic": "Metformin", "location": "Dallas", "pharmacy": "CVS", "price": 8.75, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Metformin", "generic": "Metformin", "location": "Dallas", "pharmacy": "Tom Thumb", "price": 9.25, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Metformin", "generic": "Metformin", "location": "Austin", "pharmacy": "H-E-B", "price": 7.25, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Metformin", "generic": "Metformin", "location": "San Antonio", "pharmacy": "Walgreens", "price": 8.25, "supply_days": 30, "customer_id": "bestcare123"},
    
    # Atorvastatin/Lipitor - 7 records
    {"drug": "Lipitor", "generic": "Atorvastatin", "location": "Chicago", "pharmacy": "CVS", "price": 15.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Lipitor", "generic": "Atorvastatin", "location": "Chicago", "pharmacy": "Walgreens", "price": 14.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Lipitor", "generic": "Atorvastatin", "location": "Chicago", "pharmacy": "Jewel-Osco", "price": 13.75, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Atorvastatin", "generic": "Atorvastatin", "location": "New York City", "pharmacy": "Walmart", "price": 12.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Atorvastatin", "generic": "Atorvastatin", "location": "New York City", "pharmacy": "CVS", "price": 13.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Atorvastatin", "generic": "Atorvastatin", "location": "New York City", "pharmacy": "Duane Reade", "price": 14.00, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Atorvastatin", "generic": "Atorvastatin", "location": "Brooklyn", "pharmacy": "Rite Aid", "price": 12.50, "supply_days": 30, "customer_id": "acmehealth123"},
    
    # Ozempic - 5 records
    {"drug": "Ozempic", "generic": "Semaglutide", "location": "Los Angeles", "pharmacy": "CVS", "price": 850.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Ozempic", "generic": "Semaglutide", "location": "Los Angeles", "pharmacy": "Walgreens", "price": 875.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Ozempic", "generic": "Semaglutide", "location": "Los Angeles", "pharmacy": "Costco", "price": 820.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Ozempic", "generic": "Semaglutide", "location": "San Diego", "pharmacy": "CVS", "price": 860.00, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Ozempic", "generic": "Semaglutide", "location": "San Francisco", "pharmacy": "Walgreens", "price": 890.00, "supply_days": 30, "customer_id": "bestcare123"},
    
    # Trulicity - 4 records
    {"drug": "Trulicity", "generic": "Dulaglutide", "location": "Atlanta", "pharmacy": "CVS", "price": 780.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Trulicity", "generic": "Dulaglutide", "location": "Atlanta", "pharmacy": "Walmart", "price": 760.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Trulicity", "generic": "Dulaglutide", "location": "Atlanta", "pharmacy": "Publix", "price": 770.00, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Trulicity", "generic": "Dulaglutide", "location": "Charlotte", "pharmacy": "CVS", "price": 785.00, "supply_days": 30, "customer_id": "bestcare123"},
    
    # Lisinopril - 5 records
    {"drug": "Lisinopril", "generic": "Lisinopril", "location": "Miami", "pharmacy": "CVS", "price": 6.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Lisinopril", "generic": "Lisinopril", "location": "Miami", "pharmacy": "Publix", "price": 5.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Lisinopril", "generic": "Lisinopril", "location": "Miami", "pharmacy": "Walgreens", "price": 6.25, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Lisinopril", "generic": "Lisinopril", "location": "Tampa", "pharmacy": "Walmart", "price": 5.75, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Lisinopril", "generic": "Lisinopril", "location": "Orlando", "pharmacy": "CVS", "price": 6.10, "supply_days": 30, "customer_id": "bestcare123"},
    
    # Levothyroxine/Synthroid - 4 records
    {"drug": "Synthroid", "generic": "Levothyroxine", "location": "Seattle", "pharmacy": "Walgreens", "price": 18.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Synthroid", "generic": "Levothyroxine", "location": "Seattle", "pharmacy": "Costco", "price": 16.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Levothyroxine", "generic": "Levothyroxine", "location": "Seattle", "pharmacy": "Fred Meyer", "price": 12.00, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Levothyroxine", "generic": "Levothyroxine", "location": "Portland", "pharmacy": "Walgreens", "price": 12.50, "supply_days": 30, "customer_id": "acmehealth123"},
    
    # Amoxicillin - 4 records
    {"drug": "Amoxicillin", "generic": "Amoxicillin", "location": "Boston", "pharmacy": "CVS", "price": 10.00, "supply_days": 10, "customer_id": "acmehealth123"},
    {"drug": "Amoxicillin", "generic": "Amoxicillin", "location": "Boston", "pharmacy": "Walgreens", "price": 11.00, "supply_days": 10, "customer_id": "acmehealth123"},
    {"drug": "Amoxicillin", "generic": "Amoxicillin", "location": "Boston", "pharmacy": "Stop & Shop", "price": 9.50, "supply_days": 10, "customer_id": "bestcare123"},
    {"drug": "Amoxicillin", "generic": "Amoxicillin", "location": "Cambridge", "pharmacy": "CVS", "price": 10.25, "supply_days": 10, "customer_id": "bestcare123"},
    
    # Omeprazole/Prilosec - 4 records
    {"drug": "Prilosec", "generic": "Omeprazole", "location": "Denver", "pharmacy": "Walmart", "price": 9.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Omeprazole", "generic": "Omeprazole", "location": "Denver", "pharmacy": "King Soopers", "price": 8.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Omeprazole", "generic": "Omeprazole", "location": "Denver", "pharmacy": "Walgreens", "price": 9.25, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Omeprazole", "generic": "Omeprazole", "location": "Colorado Springs", "pharmacy": "Safeway", "price": 8.75, "supply_days": 30, "customer_id": "bestcare123"},
    
    # Gabapentin - 4 records
    {"drug": "Gabapentin", "generic": "Gabapentin", "location": "Phoenix", "pharmacy": "CVS", "price": 11.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Gabapentin", "generic": "Gabapentin", "location": "Phoenix", "pharmacy": "Walgreens", "price": 10.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Gabapentin", "generic": "Gabapentin", "location": "Phoenix", "pharmacy": "Fry's", "price": 9.75, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Gabapentin", "generic": "Gabapentin", "location": "Tucson", "pharmacy": "Walmart", "price": 10.00, "supply_days": 30, "customer_id": "bestcare123"},
    
    # Amlodipine - 4 records
    {"drug": "Amlodipine", "generic": "Amlodipine", "location": "Philadelphia", "pharmacy": "CVS", "price": 7.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Amlodipine", "generic": "Amlodipine", "location": "Philadelphia", "pharmacy": "Rite Aid", "price": 7.00, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Amlodipine", "generic": "Amlodipine", "location": "Philadelphia", "pharmacy": "Giant", "price": 6.75, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Amlodipine", "generic": "Amlodipine", "location": "Pittsburgh", "pharmacy": "Walgreens", "price": 7.25, "supply_days": 30, "customer_id": "bestcare123"},
    
    # Losartan - 4 records
    {"drug": "Losartan", "generic": "Losartan", "location": "Detroit", "pharmacy": "CVS", "price": 9.50, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Losartan", "generic": "Losartan", "location": "Detroit", "pharmacy": "Meijer", "price": 8.75, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Losartan", "generic": "Losartan", "location": "Detroit", "pharmacy": "Walgreens", "price": 9.00, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Losartan", "generic": "Losartan", "location": "Grand Rapids", "pharmacy": "Walmart", "price": 8.50, "supply_days": 30, "customer_id": "bestcare123"},
]

# Add last_updated timestamp to all records
for record in drug_pricing_data:
    record["last_updated"] = {"$date": "2024-04-26T00:00:00.000Z"}

# Save drug_pricing data
with open("dataset/pricing_demo.drug_pricing.json", "w") as f:
    json.dump(drug_pricing_data, f, indent=2)

print(f"✅ Created drug_pricing dataset with {len(drug_pricing_data)} records")
print(f"   Saved to: dataset/pricing_demo.drug_pricing.json")

# Create customer_pricing data (same as drug_pricing, embeddings will be generated by setup_database.py)
# The customer_pricing collection is used for hybrid search (text + vector)
customer_pricing_data = [record.copy() for record in drug_pricing_data]

# Save customer_pricing data
with open("dataset/pricing_demo.customer_pricing.json", "w") as f:
    json.dump(customer_pricing_data, f, indent=2)

print(f"✅ Created customer_pricing dataset with {len(customer_pricing_data)} records")
print(f"   Saved to: dataset/pricing_demo.customer_pricing.json")
print(f"\n📝 Note: Embeddings will be generated when you run setup_database.py")

