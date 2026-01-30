import time
import re
from typing import Dict, List
import pandas as pd
import requests
import urllib3

# Disable SSL warnings for the Land Registry endpoint if necessary
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- SPARQL endpoint ---
ENDPOINT = "https://landregistry.data.gov.uk/landregistry/sparql"

PREFIXES = """
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix sr: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
prefix ukhpi: <http://landregistry.data.gov.uk/def/ukhpi/>
prefix lrppi: <http://landregistry.data.gov.uk/def/ppi/>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix lrcommon: <http://landregistry.data.gov.uk/def/common/>
"""

BASE_QUERY = PREFIXES + """
SELECT ?paon ?saon ?street ?town ?county ?postcode ?amount ?date ?category
WHERE
{
  VALUES ?postcode {"%s"^^xsd:string}
  VALUES ?paon     {"%s"^^xsd:string}

  ?addr lrcommon:postcode ?postcode ;
        lrcommon:paon ?paon .

  ?transx lrppi:propertyAddress ?addr ;
          lrppi:pricePaid ?amount ;
          lrppi:transactionDate ?date ;
          lrppi:transactionCategory/skos:prefLabel ?category.

  OPTIONAL {?addr lrcommon:county ?county}
  OPTIONAL {?addr lrcommon:saon ?saon}
  OPTIONAL {?addr lrcommon:street ?street}
  OPTIONAL {?addr lrcommon:town ?town}
}
ORDER BY DESC(?date)
"""

SESSION = requests.Session()
SESSION.headers.update({
    "Accept": "application/sparql-results+json",
    "User-Agent": "lr-lookup-jupyter/1.0"
})

# --- Helper functions ---

def _normalize_postcode(pc: str) -> str:
    """Ensure postcode is in proper UK format (adds space before last 3 chars if missing)."""
    pc = re.sub(r"\s+", "", pc.upper())
    if len(pc) > 3:
        pc = pc[:-3] + " " + pc[-3:]
    return pc

def query_price_paid(postcode: str, paon: str, timeout: int = 30) -> List[Dict[str, str]]:
    """Run the SPARQL query for a given postcode+paon and return results (latest first)."""
    query = BASE_QUERY % (_normalize_postcode(postcode), paon.strip())
    resp = SESSION.post(ENDPOINT, data={"query": query}, timeout=timeout, verify=False)
    resp.raise_for_status()
    data = resp.json()
    
    out = []
    for b in data.get("results", {}).get("bindings", []):
        def val(key):
            return b.get(key, {}).get("value")
        
        out.append({
            "paon": val("paon"),
            "saon": val("saon"),
            "street": val("street"),
            "town": val("town"),
            "county": val("county"),
            "postcode": val("postcode"),
            "amount": val("amount"),
            "date": val("date"),
            "category": val("category"),
        })
    return out

def format_address(r: Dict[str, str]) -> str:
    """Build a human-friendly address string from components."""
    parts = [p for p in [
        r.get("saon"),
        r.get("paon"),
        r.get("street"),
        r.get("town"),
        r.get("county"),
        r.get("postcode")
    ] if p]
    return ", ".join(parts)

def process_dataframe(df: pd.DataFrame,
                      door_col: str = "door_number",
                      postcode_col: str = "postcode",
                      id_col: str = "property_id",
                      delay_sec: float = 0.5,
                      retries: int = 2) -> pd.DataFrame:
    """Take a DataFrame, query API per row, return results with latest match."""
    records = []
    for idx, row in df.iterrows():
        door = str(row[door_col]).strip()
        pc = str(row[postcode_col]).strip()
        pid = row[id_col]
        last_err = None
        results = None
        
        for attempt in range(retries + 1):
            try:
                results = query_price_paid(pc, door)
                break
            except Exception as e:
                last_err = e
                time.sleep(1.5)
        
        if results and len(results) > 0:
            match = results[0] # already DESC by date
            rec = {
                "property_id": pid,
                "input_door_number": door,
                "input_postcode": pc,
                "matched_address": format_address(match),
                "sold_value": float(match["amount"]) if match.get("amount") else None,
                "sold_date": match.get("date"),
                "category": match.get("category"),
                "status": "matched",
                "error": None,
            }
            print(rec)
        else:
            rec = {
                "property_id": pid,
                "input_door_number": door,
                "input_postcode": pc,
                "matched_address": None,
                "sold_value": None,
                "sold_date": None,
                "category": None,
                "status": "no_match" if results is not None else "error",
                "error": str(last_err) if last_err else None,
            }
        
        records.append(rec)
        time.sleep(delay_sec)
        
    return pd.DataFrame.from_records(records)

# --- Main Execution ---

# Load your Excel file
file_path = r"C:\Users\Land Registry Data\Input Data.xlsx"

# If you know the sheet name, add: sheet_name="Sheet1"
df_input = pd.read_excel(file_path)

# Check first few rows
print(df_input.head())

# Process the data
results = process_dataframe(df_input)

# Show and save results
print(results)
# results.to_excel("Output_Land_Registery_Check_2025.xlsx", index=False)
