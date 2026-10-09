import pymupdf as fitz
import json
import os
import re

pdf_path = "catlague.pdf"
doc = fitz.open(pdf_path)

output_dir = "images/products"
os.makedirs(output_dir, exist_ok=True)

# Curated page overrides for accurate branding and naming from catalogue
PAGE_METADATA = {
    2: {"name": "ASTER", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    3: {"name": "SWAN", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    4: {"name": "BIOCON", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    5: {"name": "INDUS", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    6: {"name": "SS LIZA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    7: {"name": "SIEMENS", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    8: {"name": "MARICO", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    9: {"name": "CLAVIS", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    10: {"name": "NVIDIA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    11: {"name": "AMOHA ITI", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    12: {"name": "SS LEICA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    13: {"name": "SS NEXA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    14: {"name": "BENIN", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    15: {"name": "CHILE", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    16: {"name": "EXXON", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    17: {"name": "TEXAS", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    18: {"name": "ACURA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    19: {"name": "META", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    20: {"name": "BOEING", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    21: {"name": "VISA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    22: {"name": "IONIQ", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    23: {"name": "NUCOR", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    24: {"name": "VISTA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    25: {"name": "DIOR", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    26: {"name": "ORACLE", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    27: {"name": "KROGER", "category": "Mortise Lock Set", "material": "Zinc Plate / Zinc Handles"},
    28: {"name": "NYRA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    29: {"name": "AMOHA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    30: {"name": "SEVYA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Stainless Steel Handles"},
    31: {"name": "GAVAM", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    32: {"name": "VIRAJA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    33: {"name": "AKASA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    34: {"name": "SRIDA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    35: {"name": "CITRA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    36: {"name": "GARUDA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    37: {"name": "JIVA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    38: {"name": "VISNUR", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    39: {"name": "KAPILA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    40: {"name": "SARVA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    41: {"name": "GIRIJA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    42: {"name": "VEDAS", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    43: {"name": "FLEXA", "category": "Mortise Lock Set", "material": "S.S. 202 Plate / Zinc Handles"},
    44: {"name": "SMALL BET (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    45: {"name": "BIG BET (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    46: {"name": "OREVA (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    47: {"name": "REGAL (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    48: {"name": "NEXA (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    49: {"name": "NIKE (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    50: {"name": "FLIP (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    51: {"name": "ELIZA (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    52: {"name": "ELICA (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    53: {"name": "ROYAL (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    54: {"name": "PRIME (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    55: {"name": "HEAVY MORTISE LOCK BODIES", "category": "Lock Bodies", "material": "Brass / Steel Bullet Construction"},
    56: {"name": "DOOR & DEAD LOCKS", "category": "Door & Dead Locks", "material": "Heavy Duty Steel Mechanism"},
    57: {"name": "PIN CYLINDERS & FURNITURE LOCKS", "category": "Cylinders & Furniture Locks", "material": "Solid Brass Pin Cylinder & Zinc Body"},
    58: {"name": "LIZA (SS-304)", "category": "Mortise Lock Set", "material": "AISI S.S. 304 Plate / Zinc Handles"},
    59: {"name": "SS PULL HANDLES (SERIES 1001-1005)", "category": "Stainless Steel Pull Handles", "material": "Stainless Steel 304/202 Grade"},
    60: {"name": "SS PULL HANDLES (SERIES 1006-1010)", "category": "Stainless Steel Pull Handles", "material": "Stainless Steel 304/202 Grade"},
    61: {"name": "SS PULL HANDLES (SERIES 1011-1016)", "category": "Stainless Steel Pull Handles", "material": "Stainless Steel 304/202 Grade"},
    62: {"name": "ALUMINUM PULL HANDLES (SERIES 120-129)", "category": "Aluminum Pull Handles", "material": "Extruded Solid Architectural Aluminum"},
    63: {"name": "ALUMINUM PULL HANDLES (SERIES 130-133)", "category": "Aluminum Pull Handles", "material": "Extruded Solid Architectural Aluminum"},
}

products = []

for page_num in range(1, 63):
    page = doc[page_num]
    page_index = page_num + 1
    text = page.get_text("text").strip()
    
    meta = PAGE_METADATA.get(page_index, {})
    name = meta.get("name", f"Vinayak Product Series {page_index}")
    category = meta.get("category", "Mortise Lock Set")
    material = meta.get("material", "S.S. 202 Plate / Zinc Handles")
    
    # Extract codes
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    tokens = re.findall(r'(?:VSPH|VPS|VPR|VAH|VPC|VPL|VS|VF|VL)\s*[-]?\s*[0-9]+[A-Z\s]*', text, re.IGNORECASE)
    cleaned_codes = []
    for t in tokens:
        c = re.sub(r'\s+', ' ', t).strip()
        if c and c not in cleaned_codes:
            cleaned_codes.append(c)
            
    # Finishes
    finishes = ["Satin", "Antique", "Black", "Matt Antique Gold"]
    if "aluminum" in category.lower():
        finishes = ["SS Finish", "Antique Finish", "Copper Finish"]
    elif "stainless steel pull" in category.lower():
        finishes = ["SS Finish", "Antique Finish", "Black Finish"]
    elif "cylinder" in category.lower() or "lock bodies" in category.lower() or "dead locks" in category.lower():
        finishes = ["Satin Brass", "Antique", "Silver Chrome", "Matte Black"]
        
    # Sizes if pull handle
    sizes = []
    if "pull handles" in category.lower():
        sizes_found = re.findall(r'(\d+["\']?)', text)
        if sizes_found:
            sizes = [f'{s.replace("\"", "").replace("\'", "")}"' for s in sizes_found if int(s.replace("\"", "").replace("\'", "")) < 30]
            sizes = list(dict.fromkeys(sizes))
            
    features = []
    if category == "Mortise Lock Set":
        features = [
            "Heavy-Duty Mortise Lock Mechanism",
            "Smooth Reversible Latch & Robust Deadbolt",
            f"Crafted with {material}",
            "Ultra-Durable Multi-Layer Anti-Corrosion Coating",
            "Universal compatibility with Wooden, Metal & Flush Doors"
        ]
    elif category == "Lock Bodies":
        features = [
            "Precision-Engineered Internal Lock Case",
            "Brass & Solid Steel Bullet Security Options",
            "Tested for 200,000+ Operational Cycles",
            "Smooth Double Throw Deadbolt"
        ]
    elif category == "Door & Dead Locks":
        features = [
            "High Security Interlocking Deadbolt System",
            "Hardened Steel Casing & Rust Protection",
            "Keyed Both Sides / Thumbturn Compatibility",
            "Ideal for Main Entrance & High-Security Areas"
        ]
    elif category == "Cylinders & Furniture Locks":
        features = [
            "Computerized High-Precision Pin Tumbler Core",
            "Anti-Pick, Anti-Bump & Anti-Drill Shield",
            "Supplied with Dimple / Computer Keys",
            "Smooth 360-degree Key Operation"
        ]
    elif "Pull Handles" in category:
        features = [
            "Architectural Grade Solid Construction",
            "Ergonomic Touch & Modern Designer Aesthetic",
            f"Available Sizes: {', '.join(sizes)}" if sizes else "Available in 4\", 6\", 8\", 10\", 12\", 18\" sizes",
            "Heavy Weight Load & Tensile Fatigue Resistant"
        ]

    desc = f"Vinayak Locks {name} ({category}) engineered with {material}. Ideal for luxury residential, commercial, and architectural projects."

    model_summary = ", ".join(cleaned_codes[:5]) + ("..." if len(cleaned_codes) > 5 else "") if cleaned_codes else f"VL-{page_index:03d}"

    item = {
        "id": f"VL-{page_index:03d}",
        "name": name,
        "category": category,
        "material": material,
        "models": cleaned_codes,
        "modelSummary": model_summary,
        "description": desc,
        "features": features,
        "finishes": finishes,
        "sizes": sizes,
        "image": f"images/products/product_page_{page_index}.jpg",
        "pageNumber": page_index
    }
    products.append(item)

print(f"Generated {len(products)} refined products.")

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print("Saved products.json successfully.")
