import streamlit as st
import pandas as pd
from handle import run_query

def search_page():
    """
    Professional search page for inventory with enhanced height filtering and styling.
    """
    # Custom CSS for enhanced professional design
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
    .stSlider .thumb {
        background-color: #007bff !important;
    }
    .stSlider .track {
        background-color: #b8daff !important;
    }

    /* Data Table Styling */
    .dataframe thead th {
        background-color: #007bff !important;
        color: white !important;
    }
    .dataframe td {
        vertical-align: middle !important;
    }
    .height-badge {
        padding: 4px 8px;
        border-radius: 12px;
        background-color: #e9ecef;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">Search Inventory</h1>', unsafe_allow_html=True)
    
    # Get available tree names and packaging types
    tree_names = [row["tree_common_name"] for row in run_query(
        "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;") or []
    ]
    packaging_types = [row["packaging_type"] for row in run_query(
        "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;") or []
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        selected_tree = st.selectbox("Select Tree Name", ["All"] + tree_names)
    with col2:
        selected_packaging = st.selectbox("Select Packaging Type", ["All"] + packaging_types)
    
    # Dynamic height range selection
    min_h, max_h = 0, 10  # Default values
    if selected_tree != "All":
        height_query = """
            SELECT MIN(min_height) as min_h, MAX(max_height) as max_h 
            FROM Trees 
            WHERE common_name = %s;
        """
        result = run_query(height_query, (selected_tree,))
    else:
        result = run_query("SELECT MIN(min_height) as min_h, MAX(max_height) as max_h FROM Trees;")
    
    if result:
        min_h = result[0]['min_h'] or 0
        max_h = result[0]['max_h'] or 10
    
    st.markdown("### Height Range Selector")
    selected_min, selected_max = st.slider(
        "Select height range (feet)",
        min_value=min_h,
        max_value=max_h,
        value=(min_h, max_h),
        help="Adjust to filter by typical tree height range"
    )
    
    if st.button("Search Inventory", use_container_width=True):
        conditions = []
        params = []
        
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
        if selected_packaging != "All":
            conditions.append("nti.packaging_type = %s")
            params.append(selected_packaging)
        
        # Add height condition
        conditions.append("t.min_height >= %s AND t.max_height <= %s")
        params.extend([selected_min, selected_max])
        
        query = f"""
            SELECT 
                nti.quantity_in_stock,
                nti.price,
                t.growth_rate,
                t.scientific_name,
                t.min_height,
                t.max_height,
                t.shape,
                t.watering_demand,
                t.main_photo_url,
                t.origin,
                t.soil_type,
                t.root_type,
                t.leafl_type,
                n.address
            FROM Nursery_Tree_Inventory nti
            JOIN Trees t ON nti.tree_common_name = t.common_name
            JOIN Nurseries n ON nti.nursery_name = n.nursery_name
            {'WHERE ' + ' AND '.join(conditions) if conditions else ''}
        """
        
        results = run_query(query, tuple(params))
        if results:
            df = pd.DataFrame(results)
            # Format height display
            df['Height Range'] = df.apply(
                lambda row: f"<span class='height-badge'>{row['min_height']} - {row['max_height']} ft</span>", 
                axis=1
            )
            # Reorder columns for better presentation
            df = df[['scientific_name', 'Height Range', 'growth_rate', 'shape', 
                    'watering_demand', 'quantity_in_stock', 'price']]
            
            # Convert to HTML for custom styling
            st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No matching results found. Showing all available entries.")
            fallback_query = """
                SELECT * FROM Nursery_Tree_Inventory
                JOIN Trees ON Nursery_Tree_Inventory.tree_common_name = Trees.common_name
                LIMIT 10
            """
            fallback_results = run_query(fallback_query)
            if fallback_results:
                df_fallback = pd.DataFrame(fallback_results)
                st.dataframe(df_fallback)
            else:
                st.warning("No inventory data available.")
        else:
            st.warning("Please select at least one filter criteria.")

if __name__ == "__main__":
    search_page()
