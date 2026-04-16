import pandas as pd

# -----------------------------
# 1. Create default inventory
# -----------------------------
def create_default_inventory():
    return pd.DataFrame({
        "Item": ["bottle", "notebook", "marker pen"],
        "Count": [0, 0, 0]
    })


# -----------------------------
# 2. Load inventory from CSV
# -----------------------------
def load_inventory(file):
    df = pd.read_csv(file)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Debug print (keep for now)
    print("Columns found:", df.columns.tolist())

    # Map variations
    mapping = {
        "item": "Item",
        "items": "Item",
        "product": "Item",
        "name": "Item",

        "count": "Count",
        "quantity": "Count",
        "qty": "Count"
    }

    df = df.rename(columns=mapping)

    # If still missing → raise clear error
    if "Item" not in df.columns or "Count" not in df.columns:
        raise ValueError(
            f"CSV format incorrect. Found columns: {list(df.columns)}.\n"
            f"Expected something like: Item, Count"
        )

    # Normalize values
    df["Item"] = df["Item"].astype(str).str.lower().str.strip()

    return df


# -----------------------------
# 3. Update inventory with detections
# -----------------------------
def update_inventory(df, counts):
   

    # Ensure normalization
    df["Item"] = df["Item"].str.lower().str.strip()

    # Map detected counts
    df["Detected"] = df["Item"].map(counts).fillna(0).astype(int)

    # Compute difference
    df["Difference"] = df["Detected"] - df["Count"]

    return df


# -----------------------------
# 4. Add status (decision layer)
# -----------------------------


# -----------------------------
# 5. Save updated inventory
# -----------------------------
def save_inventory(df, path="updated_inventory.csv"):
    df.to_csv(path, index=False)


# -----------------------------
# 6. Convert to text (for VLM/LLM)
# -----------------------------
def inventory_to_text(df):
    return df.to_string(index=False)


# -----------------------------
# 7. Optional: filter only relevant detections
# -----------------------------
def filter_counts_by_inventory(df, counts):
    valid_items = set(df["Item"].tolist())

    filtered_counts = {
        k: v for k, v in counts.items() if k in valid_items
    }

    return filtered_counts