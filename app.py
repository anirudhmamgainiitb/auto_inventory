import streamlit as st
from PIL import Image

from utils.detection import detect_objects
from utils.inventory import (
    create_default_inventory,
    load_inventory,
    update_inventory,
    save_inventory,
    filter_counts_by_inventory
)

st.title("📦 Automatic Inventory Update System")

# -----------------------------
# 1. Load Inventory
# -----------------------------
uploaded_file = st.file_uploader("Upload Inventory CSV", type=["csv"])

if uploaded_file:
    df = load_inventory(uploaded_file)
else:
    df = create_default_inventory()

st.subheader("Current Inventory")
st.dataframe(df)

# -----------------------------
# 2. Upload Image
# -----------------------------
image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image")

    # -----------------------------
    # 3. Detection
    # -----------------------------
    with st.spinner("Detecting objects..."):
        counts, results = detect_objects(image, df["Item"].tolist())

    st.image(results[0].plot(), caption="Detections")
    st.write("Detected Counts:", counts)

    # -----------------------------
    # 4. Filter detections
    # -----------------------------
    counts = filter_counts_by_inventory(df, counts)

    # -----------------------------
    # 5. Update Inventory
    # -----------------------------
    df = update_inventory(df, counts)

    # -----------------------------
    # 6. Add Status
    # -----------------------------
    # df = add_status(df)

    st.subheader("Updated Inventory")
    st.dataframe(df)

    # -----------------------------
    # 7. Save
    # -----------------------------
    save_inventory(df)
    st.success("Updated inventory saved!")

  