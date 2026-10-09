import fitz  # PyMuPDF
import json
import os
import re

pdf_path = "catlague.pdf"
doc = fitz.open(pdf_path)

output_dir = "images/products"
os.makedirs(output_dir, exist_ok=True)

products = []

print(f"Total pages: {len(doc)}")

# Let's inspect pages and extract images & info
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text").strip()
    page_index = page_num + 1
    
    # Render page thumbnail / image
    pix = page.get_pixmap(dpi=150)
    image_filename = f"product_page_{page_index}.jpg"
    image_path = os.path.join(output_dir, image_filename)
    pix.save(image_path)
    
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    # Process page types
    if page_index == 1:
        # Cover page
        continue
    elif page_index == 64:
        # Back cover / Contact
        continue
    
    # Let's determine category, name, material, codes, finishes, etc.
    # Default values
    name = f"Catalogue Item {page_index}"
    category = "Mortise Lock Set"
    material = "SS 202 Plate / Zinc Handles"
    models = []
    finishes = ["Satin", "Antique", "Black", "Matt Antique Gold"]
    description = ""
    specs = {}
    
    # Check category and details based on lines
    text_lower = text.lower()
    
    if "mortise lock set" in text_lower or "mortise lock" in text_lower:
        category = "Mortise Lock Set"
    elif "lock bodies" in text_lower:
        category = "Lock Bodies"
    elif "door locks" in text_lower or "dead locks" in text_lower:
        category = "Door & Dead Locks"
    elif "furniture locks" in text_lower or "pin cylinder" in text_lower:
        category = "Cylinders & Furniture Locks"
    elif "stainless steel pull handles" in text_lower:
        category = "Stainless Steel Pull Handles"
    elif "aluminum pull handles" in text_lower or "aluminium pull handles" in text_lower:
        category = "Aluminum Pull Handles"
        
    # Extract material
    if "s.s. 304" in text_lower or "ss 304" in text_lower or "ss-304" in text_lower:
        material = "AISI S.S. 304 Plate / Zinc Handles"
    elif "s.s. 202 plate / stainless steel handles" in text_lower or "stainless steel handles" in text_lower:
        material = "S.S. 202 Plate / Stainless Steel Handles"
    elif "zinc plate / zinc handles" in text_lower:
        material = "Zinc Plate / Zinc Handles"
    elif "s.s. 202 plate / zinc handles" in text_lower:
        material = "S.S. 202 Plate / Zinc Handles"
        
    # Extract model codes like VS 212, VPS 215, VPR 19, VSPH-1001, VAH-128, etc.
    code_pattern = r'\b(V[A-Z0-9\-\s]{2,12})\b'
    potential_codes = []
    for line in lines:
        # Check if line looks like product name or code
        tokens = re.findall(r'(?:VSPH|VPS|VPR|VAH|VPC|VPL|VS|VF|VL)\s*[-]?\s*[0-9]+[A-Z\s]*', line, re.IGNORECASE)
        for t in tokens:
            cleaned_token = t.strip()
            if cleaned_token not in potential_codes:
                potential_codes.append(cleaned_token)
                
    models = potential_codes
    
    # Extract product name
    # Usually page title has a number and a name (e.g., '1 ASTER', '2 SWAN', '3 BIOCON', 'OREVA 45', 'FLEXA 42', etc.)
    name_found = False
    for line in lines:
        # Match lines like '1 ASTER', '2 SWAN', 'REGAL 46', 'CHILE', 'SS LIZA'
        m = re.match(r'^(?:\d+\s+)?([A-Z\s\.\-]{3,25})(?:\s+\d+)?$', line)
        if m:
            candidate = m.group(1).strip()
            # filter out non-names
            if candidate not in ["MORTISE LOCK SET", "MORTISE LOCK", "LOCK BODIES", "DOOR LOCKS", 
                                 "DEAD LOCKS", "FURNITURE LOCKS", "PIN CYLINDER", 
                                 "STAINLESS STEEL PULL HANDLES", "ALUMINUM PULL HANDLES", 
                                 "PRODUCT CATALOGUE", "FINISH", "PRODUCTS", "PLATE"]:
                if not any(candidate.startswith(prefix) for prefix in ["VS", "VPS", "VPR", "VAH", "VSPH", "VPC", "VPL", "VL", "VF"]):
                    if len(candidate) > 2:
                        name = candidate
                        name_found = True
                        break
                        
    if not name_found:
        if category == "Stainless Steel Pull Handles":
            name = f"SS Pull Handles (Series {page_index})"
        elif category == "Aluminum Pull Handles":
            name = f"Aluminum Pull Handles (Series {page_index})"
        elif category == "Lock Bodies":
            name = f"Lock Bodies (Series {page_index})"
        elif category == "Door & Dead Locks":
            name = f"Door & Dead Locks (Series {page_index})"
        elif category == "Cylinders & Furniture Locks":
            name = f"Cylinders & Furniture Locks (Series {page_index})"
        else:
            name = f"Mortise Lock Set (Series {page_index})"

    # Handle Finishes
    if "FINISH" in text:
        for line in lines:
            if "FINISH" in line.upper():
                fin_part = line.split(":")[-1].strip() if ":" in line else line
                finishes = [f.strip() for f in fin_part.split(",") if f.strip()]
                
    # Build specifications and features
    features = []
    if "mortise" in category.lower():
        features.append("Heavy Duty Mortise Mechanism")
        features.append("Smooth Latch & Deadbolt Operation")
        features.append(f"Material: {material}")
        features.append("Corrosion Resistant Multi-Layer Coating")
        features.append("Suitable for Wooden, Metal & Flush Doors")
    elif "pull handle" in category.lower():
        features.append("Architectural Grade Solid Construction")
        features.append("Ergonomic Grip & Modern Aesthetics")
        features.append("High Tensile Strength & Durability")
        features.append("Available in multiple standard sizes")
    elif "lock bodies" in category.lower():
        features.append("Precision Engineered Internal Mechanism")
        features.append("Brass / Steel Bullet Construction")
        features.append("Reversible Latch Bolt")
        features.append("Standard Cutout Compatibility")
    elif "cylinders" in category.lower():
        features.append("High Security Pin Tumbler System")
        features.append("Computerized / Dimple Keys Available")
        features.append("Anti-Pick & Anti-Drill Protection")

    desc = f"Vinayak Locks {name} {category} manufactured with {material}. Designed for superior durability, security, and architectural elegance in residential and commercial spaces."
    
    product_item = {
        "id": f"VL-{page_index:03d}",
        "name": name,
        "category": category,
        "material": material,
        "models": models,
        "modelSummary": ", ".join(models[:4]) + ("..." if len(models) > 4 else "") if models else f"VL-{page_index:03d}",
        "description": desc,
        "features": features,
        "finishes": finishes,
        "image": f"images/products/{image_filename}",
        "pageNumber": page_index,
        "rawText": text
    }
    
    products.append(product_item)

print(f"Parsed {len(products)} products.")

# Save to products.json
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print("Saved to products.json successfully!")
