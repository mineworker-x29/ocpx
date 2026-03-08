Large semiconductor OCPM demo dataset

Files:
- raw_df_large_demo.csv
- events_large_demo.csv
- objects_large_demo.csv
- relations_link_large_demo.csv
- relations_ext_large_demo.csv
- summary.json

Summary:
{
  "lots": 120,
  "slots_per_lot": 24,
  "unique_products": 2880,
  "raw_rows": 17580,
  "events_rows": 35160,
  "objects_rows": 2894,
  "relations_link_rows": 122160,
  "relations_ext_rows": 122160
}

Notes:
- 120 lots x 24 slots = 2,880 unique wafer products.
- Product oid format: LOTID_SLOTNO e.g. L1001_01
- Includes common LP purge / chamber clean events with no product.
- Injected slowdowns:
  * lots 31-40: PM2 recipe durations slower
  * lots 81-90: LLM1 / transfer congestion slower
