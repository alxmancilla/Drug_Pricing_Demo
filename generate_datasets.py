#!/usr/bin/env python3
"""
Generate comprehensive datasets for Drug Pricing Demo
Creates 100+ records for both drug_pricing and customer_pricing collections
Includes prescription medications and over-the-counter (OTC) medications
"""

import json
from datetime import datetime

# Drug pricing data - 100+ records (Prescription + OTC medications)
drug_pricing_data = [
    # ========================================
    # PRESCRIPTION MEDICATIONS
    # ========================================

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

    # ========================================
    # OVER-THE-COUNTER (OTC) MEDICATIONS
    # ========================================

    # Ibuprofen (Advil/Motrin) - 8 records
    {"drug": "Advil", "generic": "Ibuprofen", "location": "Houston", "pharmacy": "CVS", "price": 12.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Advil", "generic": "Ibuprofen", "location": "Houston", "pharmacy": "Walgreens", "price": 11.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Ibuprofen", "generic": "Ibuprofen", "location": "Houston", "pharmacy": "Walmart", "price": 8.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Ibuprofen", "generic": "Ibuprofen", "location": "Houston", "pharmacy": "Costco", "price": 7.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Motrin", "generic": "Ibuprofen", "location": "Dallas", "pharmacy": "CVS", "price": 13.49, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Ibuprofen", "generic": "Ibuprofen", "location": "Dallas", "pharmacy": "Tom Thumb", "price": 10.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Ibuprofen", "generic": "Ibuprofen", "location": "Austin", "pharmacy": "H-E-B", "price": 9.49, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Ibuprofen", "generic": "Ibuprofen", "location": "San Antonio", "pharmacy": "Walgreens", "price": 11.49, "supply_days": 30, "customer_id": "bestcare123"},

    # Acetaminophen (Tylenol) - 8 records
    {"drug": "Tylenol", "generic": "Acetaminophen", "location": "Chicago", "pharmacy": "CVS", "price": 14.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Tylenol", "generic": "Acetaminophen", "location": "Chicago", "pharmacy": "Walgreens", "price": 13.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Acetaminophen", "generic": "Acetaminophen", "location": "Chicago", "pharmacy": "Jewel-Osco", "price": 10.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Acetaminophen", "generic": "Acetaminophen", "location": "New York City", "pharmacy": "Walmart", "price": 9.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Tylenol", "generic": "Acetaminophen", "location": "New York City", "pharmacy": "CVS", "price": 15.49, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Tylenol", "generic": "Acetaminophen", "location": "New York City", "pharmacy": "Duane Reade", "price": 14.49, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Acetaminophen", "generic": "Acetaminophen", "location": "Brooklyn", "pharmacy": "Rite Aid", "price": 11.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Acetaminophen", "generic": "Acetaminophen", "location": "Brooklyn", "pharmacy": "Costco", "price": 8.99, "supply_days": 30, "customer_id": "bestcare123"},

    # Aspirin (Bayer) - 6 records
    {"drug": "Bayer Aspirin", "generic": "Aspirin", "location": "Los Angeles", "pharmacy": "CVS", "price": 9.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Aspirin", "generic": "Aspirin", "location": "Los Angeles", "pharmacy": "Walgreens", "price": 7.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Aspirin", "generic": "Aspirin", "location": "Los Angeles", "pharmacy": "Costco", "price": 6.49, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Bayer Aspirin", "generic": "Aspirin", "location": "San Diego", "pharmacy": "CVS", "price": 10.49, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Aspirin", "generic": "Aspirin", "location": "San Francisco", "pharmacy": "Walgreens", "price": 8.49, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Aspirin", "generic": "Aspirin", "location": "San Francisco", "pharmacy": "Safeway", "price": 7.49, "supply_days": 30, "customer_id": "acmehealth123"},

    # Claritin (Loratadine) - 6 records
    {"drug": "Claritin", "generic": "Loratadine", "location": "Atlanta", "pharmacy": "CVS", "price": 18.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Claritin", "generic": "Loratadine", "location": "Atlanta", "pharmacy": "Walmart", "price": 15.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Loratadine", "generic": "Loratadine", "location": "Atlanta", "pharmacy": "Publix", "price": 12.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Loratadine", "generic": "Loratadine", "location": "Charlotte", "pharmacy": "CVS", "price": 13.49, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Claritin", "generic": "Loratadine", "location": "Charlotte", "pharmacy": "Walgreens", "price": 17.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Loratadine", "generic": "Loratadine", "location": "Charlotte", "pharmacy": "Costco", "price": 11.99, "supply_days": 30, "customer_id": "bestcare123"},

    # Zyrtec (Cetirizine) - 6 records
    {"drug": "Zyrtec", "generic": "Cetirizine", "location": "Miami", "pharmacy": "CVS", "price": 19.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Zyrtec", "generic": "Cetirizine", "location": "Miami", "pharmacy": "Publix", "price": 17.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Cetirizine", "generic": "Cetirizine", "location": "Miami", "pharmacy": "Walgreens", "price": 14.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Cetirizine", "generic": "Cetirizine", "location": "Tampa", "pharmacy": "Walmart", "price": 13.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Zyrtec", "generic": "Cetirizine", "location": "Orlando", "pharmacy": "CVS", "price": 20.49, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Cetirizine", "generic": "Cetirizine", "location": "Orlando", "pharmacy": "Costco", "price": 12.99, "supply_days": 30, "customer_id": "acmehealth123"},

    # Benadryl (Diphenhydramine) - 5 records
    {"drug": "Benadryl", "generic": "Diphenhydramine", "location": "Seattle", "pharmacy": "Walgreens", "price": 11.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Benadryl", "generic": "Diphenhydramine", "location": "Seattle", "pharmacy": "Costco", "price": 9.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Diphenhydramine", "generic": "Diphenhydramine", "location": "Seattle", "pharmacy": "Fred Meyer", "price": 8.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Diphenhydramine", "generic": "Diphenhydramine", "location": "Portland", "pharmacy": "Walgreens", "price": 9.49, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Benadryl", "generic": "Diphenhydramine", "location": "Portland", "pharmacy": "CVS", "price": 12.49, "supply_days": 30, "customer_id": "bestcare123"},

    # Tums (Calcium Carbonate) - 5 records
    {"drug": "Tums", "generic": "Calcium Carbonate", "location": "Boston", "pharmacy": "CVS", "price": 8.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Tums", "generic": "Calcium Carbonate", "location": "Boston", "pharmacy": "Walgreens", "price": 8.49, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Calcium Carbonate", "generic": "Calcium Carbonate", "location": "Boston", "pharmacy": "Stop & Shop", "price": 6.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Tums", "generic": "Calcium Carbonate", "location": "Cambridge", "pharmacy": "CVS", "price": 9.49, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Calcium Carbonate", "generic": "Calcium Carbonate", "location": "Cambridge", "pharmacy": "Costco", "price": 5.99, "supply_days": 30, "customer_id": "acmehealth123"},

    # Pepto-Bismol (Bismuth Subsalicylate) - 5 records
    {"drug": "Pepto-Bismol", "generic": "Bismuth Subsalicylate", "location": "Denver", "pharmacy": "Walmart", "price": 10.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Pepto-Bismol", "generic": "Bismuth Subsalicylate", "location": "Denver", "pharmacy": "King Soopers", "price": 11.49, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Bismuth Subsalicylate", "generic": "Bismuth Subsalicylate", "location": "Denver", "pharmacy": "Walgreens", "price": 9.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Pepto-Bismol", "generic": "Bismuth Subsalicylate", "location": "Colorado Springs", "pharmacy": "Safeway", "price": 11.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Bismuth Subsalicylate", "generic": "Bismuth Subsalicylate", "location": "Colorado Springs", "pharmacy": "CVS", "price": 10.49, "supply_days": 30, "customer_id": "acmehealth123"},

    # Mucinex (Guaifenesin) - 5 records
    {"drug": "Mucinex", "generic": "Guaifenesin", "location": "Phoenix", "pharmacy": "CVS", "price": 16.99, "supply_days": 14, "customer_id": "acmehealth123"},
    {"drug": "Mucinex", "generic": "Guaifenesin", "location": "Phoenix", "pharmacy": "Walgreens", "price": 15.99, "supply_days": 14, "customer_id": "acmehealth123"},
    {"drug": "Guaifenesin", "generic": "Guaifenesin", "location": "Phoenix", "pharmacy": "Fry's", "price": 12.99, "supply_days": 14, "customer_id": "bestcare123"},
    {"drug": "Guaifenesin", "generic": "Guaifenesin", "location": "Tucson", "pharmacy": "Walmart", "price": 11.99, "supply_days": 14, "customer_id": "bestcare123"},
    {"drug": "Mucinex", "generic": "Guaifenesin", "location": "Tucson", "pharmacy": "CVS", "price": 17.49, "supply_days": 14, "customer_id": "acmehealth123"},

    # Allegra (Fexofenadine) - 5 records
    {"drug": "Allegra", "generic": "Fexofenadine", "location": "Philadelphia", "pharmacy": "CVS", "price": 21.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Allegra", "generic": "Fexofenadine", "location": "Philadelphia", "pharmacy": "Rite Aid", "price": 20.99, "supply_days": 30, "customer_id": "acmehealth123"},
    {"drug": "Fexofenadine", "generic": "Fexofenadine", "location": "Philadelphia", "pharmacy": "Giant", "price": 16.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Fexofenadine", "generic": "Fexofenadine", "location": "Pittsburgh", "pharmacy": "Walgreens", "price": 17.99, "supply_days": 30, "customer_id": "bestcare123"},
    {"drug": "Allegra", "generic": "Fexofenadine", "location": "Pittsburgh", "pharmacy": "Costco", "price": 15.99, "supply_days": 30, "customer_id": "acmehealth123"},

    # Sudafed (Pseudoephedrine) - 4 records
    {"drug": "Sudafed", "generic": "Pseudoephedrine", "location": "Detroit", "pharmacy": "CVS", "price": 13.99, "supply_days": 14, "customer_id": "acmehealth123"},
    {"drug": "Sudafed", "generic": "Pseudoephedrine", "location": "Detroit", "pharmacy": "Meijer", "price": 12.99, "supply_days": 14, "customer_id": "acmehealth123"},
    {"drug": "Pseudoephedrine", "generic": "Pseudoephedrine", "location": "Detroit", "pharmacy": "Walgreens", "price": 11.99, "supply_days": 14, "customer_id": "bestcare123"},
    {"drug": "Pseudoephedrine", "generic": "Pseudoephedrine", "location": "Grand Rapids", "pharmacy": "Walmart", "price": 10.99, "supply_days": 14, "customer_id": "bestcare123"},
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

