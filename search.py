import streamlit as st
import pandas as pd
from handle import run_query

def search_page():
    """
    Professional search page for inventory with advanced styling and user experience.
    """
    # Custom CSS for enhanced professional design and card styling
    st.markdown("""
    <style>
    /* Page Title Styling */
    .page-title {
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        padding-bottom: 15px;
        border-bottom: 2px solid #007bff;
        margin-bottom: 20px;
    }

    /* Selectbox Styling */
    .stSelectbox > div > div > div {
        background-color: #f8f9fa;
        border: 1.5px solid #ced4da;
        border-radius: 6px;
        padding: 10px;
        color: #495057;
        transition: all 0.3s ease;
    }
    .stSelectbox > div > div > div:hover {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25);
    }

    /* Slider Styling */
    .stSlider > div {
        padding: 10px 0;
    }

    /* Search Button Styling */
    .stButton > button {
        background-color: #007bff !important;
        color: white !important;
        border-radius: 6px;
        font-weight: 600;
        text-transform: uppercase;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0056b3 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Card Styling for Results */
    .result-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .result-card img {
        width: 120px;
        height: 120px;
        border-radius: 8px;
        object-fit: cover;
        margin-right: 15px;
    }
    .result-header {
        display: flex;
        align-items: center;
    }
    .result-header h3 {
        margin: 0;
        color: #2c3e50;
    }
    .result-header p {
        margin: 0;
        color: #495057;
    }
    </style>
    """, unsafe_allow_html=True)

    # Professional title with custom styling
    st.markdown('<h1 class="page-title">Search Inventory</h1>', unsafe_allow_html=True)
    
    # Dropdown for Tree Name from Nursery_Tree_Inventory
    query_tree_names = "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;"
    tree_names = [row["tree_common_name"] for row in run_query(query_tree_names) or []]
    
    # Dropdown for Packaging Type from Nursery_Tree_Inventory
    query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;"
    packaging_types = [row["packaging_type"] for row in run_query(query_packaging) or []]
    
    # Create two columns for dropdown selectors
    col1, col2 = st.columns(2)
    with col1:
        selected_tree = st.selectbox("Select Tree Name", ["All"] + tree_names)
    with col2:
        selected_packaging = st.selectbox("Select Packaging Type", ["All"] + packaging_types)
    
    # Dynamic Height Range Dashboard based on available data for the selected tree
    if selected_tree != "All":
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        height_range = run_query(height_range_query, (selected_tree,))
    else:
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory;"
        height_range = run_query(height_range_query)
        
    if height_range and height_range[0]['min_val'] is not None and height_range[0]['max_val'] is not None:
        slider_min = float(height_range[0]['min_val'])
        slider_max = float(height_range[0]['max_val'])
        selected_height_range = st.slider("Select Height Range (cm)", min_value=slider_min, max_value=slider_max, value=(slider_min, slider_max))
    else:
        selected_height_range = None

    # Search Button with Full Width
    if st.button("Search Inventory", use_container_width=True):
        conditions = []
        params = []
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
        if selected_packaging != "All":
            conditions.append("nti.packaging_type = %s")
            params.append(selected_packaging)
        # Modified height condition: allow near or exact matches by checking for any overlap.
        if selected_height_range:
            conditions.append("nti.max_height >= %s AND nti.min_height <= %s")
            params.extend([selected_height_range[0], selected_height_range[1]])
        
        if conditions:
            where_clause = " AND ".join(conditions)
            query = f"""
            SELECT nti.quantity_in_stock, nti.price, nti.min_height, nti.max_height,
                   t.growth_rate, t.scientific_name, t.shape, t.watering_demand, 
                   t.main_photo_url, t.origin, t.soil_type, t.root_type, t.leafl_type, 
                   n.address
            FROM Nursery_Tree_Inventory nti
            JOIN Trees t ON nti.tree_common_name = t.common_name
            JOIN Nurseries n ON nti.nursery_name = n.nursery_name
            WHERE {where_clause};
            """
            results = run_query(query, tuple(params))
            if results:
                for row in results:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">
                            <img src="{row['main_photo_url']}" alt="Tree Photo">
                            <div>
                                <h3>{row['scientific_name']}</h3>
                                <p>Growth Rate: {row['growth_rate']} cm/yr</p>
                            </div>
                        </div>
                        <hr style="border:none; border-top:1px solid #dee2e6; margin:10px 0;">
                        <p><strong>Quantity in Stock:</strong> {row['quantity_in_stock']}</p>
                        <p><strong>Price:</strong> {row['price']} IQD</p>
                        <p><strong>Height Range:</strong> {row['min_height']} cm - {row['max_height']} cm</p>
                        <p><strong>Shape:</strong> {row['shape']}</p>
                        <p><strong>Watering Demand:</strong> {row['watering_demand']}</p>
                        <p><strong>Origin:</strong> {row['origin']}</p>
                        <p><strong>Soil Type:</strong> {row['soil_type']}</p>
                        <p><strong>Root Type:</strong> {row['root_type']}</p>
                        <p><strong>Leaf Type:</strong> {row['leafl_type']}</p>
                        <p><strong>Address:</strong> {row['address']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No results found.")
        else:
            st.write("Please select at least one filter.")
