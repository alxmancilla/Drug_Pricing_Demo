# Dataset Expansion - 50+ Records

## Summary

Successfully expanded the BPE Pricing Demo datasets from limited sample data to comprehensive datasets with **53 records each** for both collections.

## What Was Created

### 1. **New Dataset Files**

#### `dataset/pricing_demo.drug_pricing.json` - 53 records
- **8 Metformin** records (Houston, Dallas, Austin, San Antonio)
- **7 Atorvastatin/Lipitor** records (Chicago, New York City, Brooklyn)
- **5 Ozempic** records (Los Angeles, San Diego, San Francisco)
- **4 Trulicity** records (Atlanta, Charlotte)
- **5 Lisinopril** records (Miami, Tampa, Orlando)
- **4 Levothyroxine/Synthroid** records (Seattle, Portland)
- **4 Amoxicillin** records (Boston, Cambridge)
- **4 Omeprazole/Prilosec** records (Denver, Colorado Springs)
- **4 Gabapentin** records (Phoenix, Tucson)
- **4 Amlodipine** records (Philadelphia, Pittsburgh)
- **4 Losartan** records (Detroit, Grand Rapids)

#### `dataset/pricing_demo.customer_pricing.json` - 53 records
- Same data as drug_pricing
- Embeddings will be generated automatically by `setup_database.py`
- Used for hybrid search (text + vector search)

### 2. **Dataset Generator Script**

**`generate_datasets.py`** - Python script to generate the datasets
- Creates both drug_pricing and customer_pricing JSON files
- 53 records covering 11 different medications
- Multiple locations across the US
- Various pharmacy chains (CVS, Walgreens, Walmart, Costco, etc.)
- Realistic pricing data

## Dataset Coverage

### Medications (11 types)
1. **Metformin** - Diabetes medication (generic)
2. **Atorvastatin/Lipitor** - Cholesterol medication
3. **Ozempic** - Diabetes/weight loss medication (brand name, expensive)
4. **Trulicity** - Diabetes medication (brand name, expensive)
5. **Lisinopril** - Blood pressure medication (generic)
6. **Levothyroxine/Synthroid** - Thyroid medication
7. **Amoxicillin** - Antibiotic
8. **Omeprazole/Prilosec** - Acid reflux medication
9. **Gabapentin** - Nerve pain medication
10. **Amlodipine** - Blood pressure medication
11. **Losartan** - Blood pressure medication

### Locations (20+ cities)
- **Texas**: Houston, Dallas, Austin, San Antonio
- **Illinois**: Chicago
- **New York**: New York City, Brooklyn, Cambridge
- **California**: Los Angeles, San Diego, San Francisco
- **Georgia**: Atlanta
- **North Carolina**: Charlotte
- **Florida**: Miami, Tampa, Orlando
- **Washington**: Seattle, Portland
- **Massachusetts**: Boston, Cambridge
- **Colorado**: Denver, Colorado Springs
- **Arizona**: Phoenix, Tucson
- **Pennsylvania**: Philadelphia, Pittsburgh
- **Michigan**: Detroit, Grand Rapids

### Pharmacy Chains (15+)
- CVS
- Walgreens
- Walmart
- Costco
- Tom Thumb
- H-E-B
- Jewel-Osco
- Duane Reade
- Rite Aid
- Publix
- Fred Meyer
- Stop & Shop
- King Soopers
- Safeway
- Fry's
- Meijer
- Giant

### Customer IDs (2)
- `acmehealth123`
- `bestcare123`

## Price Ranges

- **Generic medications**: $5.50 - $18.00 (30-day supply)
- **Brand name diabetes medications**: $760.00 - $890.00 (30-day supply)
- **Antibiotics**: $9.50 - $11.00 (10-day supply)

## Files Modified

1. **`generate_datasets.py`** (NEW)
   - Python script to generate both datasets
   - 53 records with realistic pharmaceutical pricing data

2. **`setup_database.py`** (UPDATED)
   - Fixed environment variable name: `VOYAGE_API_KEY` (was `VOYAGE_KEY`)
   - Now checks both `VOYAGE_API_KEY` and `VOYAGE_KEY` for backward compatibility
   - Automatically generates embeddings for customer_pricing data

3. **`dataset/pricing_demo.drug_pricing.json`** (REPLACED)
   - Expanded from limited sample to 53 comprehensive records

4. **`dataset/pricing_demo.customer_pricing.json`** (REPLACED)
   - Expanded from limited sample to 53 comprehensive records

## How to Use

### Generate Datasets

```bash
python3 generate_datasets.py
```

**Output:**
```
✅ Created drug_pricing dataset with 53 records
   Saved to: dataset/pricing_demo.drug_pricing.json
✅ Created customer_pricing dataset with 53 records
   Saved to: dataset/pricing_demo.customer_pricing.json

📝 Note: Embeddings will be generated when you run setup_database.py
```

### Load Data into MongoDB

```bash
python3 setup_database.py
```

This will:
1. Load 53 records into `drug_pricing` collection
2. Load 53 records into `customer_pricing` collection
3. Generate embeddings for all customer_pricing records using Voyage AI
4. Create necessary indexes
5. Provide instructions for creating Atlas Search indexes

## Testing

### Verify Dataset Files

```bash
# Count records
python3 -c "import json; dp = json.load(open('dataset/pricing_demo.drug_pricing.json')); print(f'drug_pricing: {len(dp)} records')"
python3 -c "import json; cp = json.load(open('dataset/pricing_demo.customer_pricing.json')); print(f'customer_pricing: {len(cp)} records')"
```

### Sample Queries to Test

After running `setup_database.py` and creating Atlas Search indexes, try these queries in `app.py`:

```
What's the cheapest Metformin in Houston?
Find Ozempic prices in Los Angeles
Where can I get Lisinopril in Miami?
Show me Atorvastatin options in New York
What's the best price for Gabapentin in Phoenix?
```

## Benefits of Expanded Dataset

1. **Better Search Results**: More data means better hybrid search relevance
2. **Realistic Testing**: Covers multiple medications, locations, and pharmacies
3. **Diverse Queries**: Can test various search patterns and edge cases
4. **Price Comparison**: Multiple options for each medication in different locations
5. **Customer Segmentation**: Two different customer IDs for testing customer-specific pricing

## Next Steps

1. ✅ Generate datasets (53 records each)
2. ⏳ Run `setup_database.py` to load data and generate embeddings
3. ⏳ Create Atlas Search indexes (vector_search_index and text_search_index)
4. ⏳ Test the application with expanded dataset

## Notes

- The dataset uses MongoDB Extended JSON format (`{"$date": "..."}`)
- Embeddings are generated using Voyage AI via MongoDB AI endpoint
- The setup script handles both pre-embedded and non-embedded data
- All prices are in USD
- Supply days vary (10 days for antibiotics, 30 days for most medications)

