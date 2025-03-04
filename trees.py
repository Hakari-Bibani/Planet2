import streamlit as st
import pandas as pd
import handle  # import database functions

def trees_page(pool):
    st.header("Manage Trees")
    # Form for adding/updating a tree
    with st.form("tree_form", clear_on_submit=True):
        common = st.text_input("Common Name *")
        scientific = st.text_input("Scientific Name *")
        growth_rate = st.selectbox("Growth Rate", ["Slow", "Medium", "Fast"])
        # Dynamic dropdowns for categorical fields:
        shapes = handle.get_distinct_values(pool, table="Trees", column="shape")
        shape_choice = st.selectbox("Shape", list(shapes) + ["Other..."])
        shape = st.text_input("New shape") if shape_choice == "Other..." else shape_choice
        origin_choice = st.selectbox("Origin", handle.get_distinct_values(pool, "Trees", "Origin") + ["Other..."])
        origin = st.text_input("New origin") if origin_choice == "Other..." else origin_choice
        # ... similarly for Soil_type, Root_type, Leaf_Type ...
        water = st.text_input("Watering Demand (e.g., 'Moderate')")
        photo = st.text_input("Main Photo URL")
        submitted = st.form_submit_button("Add/Update Tree")
    if submitted:
        # If it's an update vs new add can be decided by whether this tree exists
        handle.add_tree(pool, common_name=common, scientific_name=scientific,
                        shape=shape, watering=water, photo_url=photo,
                        origin=origin, soil=soil, root=root, leaf=leaf, growth=growth_rate)
        st.success(f"Tree '{common}' has been added/updated.")
    # Bulk upload
    st.subheader("Bulk Upload Trees from CSV")
    csv_file = st.file_uploader("Upload CSV", type=["csv"])
    if csv_file:
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            handle.add_tree(pool, **row.to_dict())
        st.success(f"Uploaded {len(df)} trees from CSV.")
    # Delete or edit existing
    st.subheader("Modify Existing Tree")
    all_trees = handle.get_all_trees(pool)
    tree_names = [f"{t['common_name']} ({t['scientific_name']})" for t in all_trees]
    choice = st.selectbox("Select Tree to Edit/Delete", [""] + tree_names)
    if choice:
        # Find the selected tree data
        idx = tree_names.index(choice)
        tree = all_trees[idx]
        st.write(f"**Editing Tree:** *{tree['common_name']}*")
        # Pre-fill form (could reuse the form above with state, or just show fields)
        new_common = st.text_input("Common Name", value=tree["common_name"])
        new_scientific = st.text_input("Scientific Name", value=tree["scientific_name"])
        # ... other fields similarly pre-filled ...
        if st.button("Update"):
            handle.update_tree(pool, tree_id=tree["id"], common_name=new_common, scientific_name=new_scientific, ...)
            st.success("Tree updated successfully.")
        if st.button("Delete"):
            handle.delete_tree(pool, tree_id=tree["id"])
            st.warning("Tree deleted.")

