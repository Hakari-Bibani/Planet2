import streamlit as st
import pandas as pd
import handle

def inventory_page(pool):
    st.header("Manage Nursery Inventory")
    # Fetch existing nurseries and trees for dropdowns
    nurseries = handle.get_all_nurseries(pool)
    trees = handle.get_all_trees(pool)
    nursery_names = [n["name"] for n in nurseries]
    tree_names = [t["common_name"] for t in trees]
    packaging_types = handle.get_distinct_values(pool, table="Nursery_Tree_Inventory", column="Packaging_type")
    
    # Add inventory form
    with st.form("inv_form", clear_on_submit=True):
        nursery_choice = st.selectbox("Nursery", nursery_names)
        tree_choice = st.selectbox("Tree (Common Name)", tree_names)
        # Packaging with dynamic add-new
        pack_choice = st.selectbox("Packaging Type", list(packaging_types) + ["Other..."])
        packaging = st.text_input("New Packaging Type") if pack_choice == "Other..." else pack_choice
        quantity = st.number_input("Quantity in stock", min_value=0, step=1)
        height = st.number_input("Height (cm)", min_value=0.0, step=1.0)
        price = st.number_input("Price ($)", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Inventory Record")
    if submitted:
        # Map selected names to IDs
        nursery_id = next(n["id"] for n in nurseries if n["name"] == nursery_choice)
        tree_id = next(t["id"] for t in trees if t["common_name"] == tree_choice)
        handle.add_inventory(pool, nursery_id=nursery_id, tree_id=tree_id,
                              packaging=packaging, quantity=quantity, height=height, price=price)
        st.success(f"Added inventory: {nursery_choice} now has {quantity} of {tree_choice}.")
    
    # Bulk upload inventory
    st.subheader("Bulk Upload Inventory from CSV")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        # We assume CSV has columns: nursery_name, tree_common_name, packaging_type, quantity, height, price
        for _, row in df.iterrows():
            # Get corresponding IDs
            try:
                n_id = next(n["id"] for n in nurseries if n["name"] == row["nursery_name"])
                t_id = next(t["id"] for t in trees if t["common_name"] == row["tree_common_name"])
            except StopIteration:
                continue  # if nursery or tree not found, skip or handle error
            handle.add_inventory(pool, nursery_id=n_id, tree_id=t_id,
                                  packaging=row["Packaging_type"], quantity=row["Quantity_in_stock"],
                                  height=row.get("Height", 0), price=row.get("Price", 0.0))
        st.success("Inventory CSV uploaded.")
    
    # Edit/Delete inventory entries
    st.subheader("Existing Inventory Records")
    inventory = handle.get_all_inventory(pool)  # fetch joined data or base data
    # Create labels for inventory items (e.g., "Nursery - Tree")
    inv_labels = [f"{rec['nursery_name']} - {rec['tree_name']} ({rec['Packaging_type']})" for rec in inventory]
    choice = st.selectbox("Select Inventory Record", [""] + inv_labels)
    if choice:
        rec = inventory[inv_labels.index(choice)]
        st.write(f"Editing inventory for **{rec['nursery_name']} – {rec['tree_name']}**")
        new_qty = st.number_input("Quantity", value=rec["Quantity_in_stock"], min_value=0)
        new_price = st.number_input("Price ($)", value=float(rec["Price"]), step=0.01)
        new_height = st.number_input("Height (cm)", value=float(rec.get("Height", 0)), step=1.0)
        new_pack_choice = st.selectbox("Packaging Type", list(packaging_types) + ["Other..."], index= list(packaging_types).index(rec["Packaging_type"]) if rec["Packaging_type"] in packaging_types else len(packaging_types))
        new_pack = st.text_input("New Packaging Type") if new_pack_choice == "Other..." else new_pack_choice
        if st.button("Update Record"):
            handle.update_inventory(pool, inv_id=rec["id"], quantity=new_qty, price=new_price, height=new_height, packaging=new_pack)
            st.success("Inventory record updated.")
        if st.button("Delete Record"):
            handle.delete_inventory(pool, inv_id=rec["id"])
            st.warning("Inventory record deleted.")
