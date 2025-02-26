# pages/1_🏠_Product_Nutrition.py (updated)
import streamlit as st
import pandas as pd
import plotly.express as px
import pyarrow.parquet as pq
from st_aggrid import AgGrid, GridOptionsBuilder

@st.cache_data
def load_data():
    # Use pyarrow to read the Parquet file
    table = pq.read_table("openfoodfacts-processed.parquet")
    df = table.to_pandas()  # Convert to Pandas DataFrame
    df = df.rename(columns={'energy-kcal_100g': 'energy_kcal_100g'})
    return df.dropna(subset=['nutriscore_score', 'environmental_score_score', 'energy_kcal_100g', 'co2_total'])

def main():
    df = load_data()
    
    st.title("Nutritional Analysis")
    
    # Interactive 3D Scatter Plot
    st.header("Nutritional Landscape")
    fig = px.scatter_3d(
        df.sample(10000),
        x='nutriscore_score',
        y='energy_kcal_100g',
        z='co2_total',
        color='environmental_score_score',
        hover_name='product_name',
        labels={
            'nutriscore_score': 'Nutrition Score',
            'energy_kcal_100g': 'Calories/100g',
            'co2_total': 'CO2 Emissions',
            'environmental_score_score': 'Env. Impact'
        },
        color_continuous_scale='Portland',
        title='3D Nutritional Landscape'
    )
    fig.update_layout(scene=dict(
        xaxis=dict(title='Nutrition ↑', autorange="reversed"),
        yaxis=dict(title='Calories →'),
        zaxis=dict(title='CO2 →')
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive Data Grid
    st.header("Product Explorer")
    gb = GridOptionsBuilder.from_dataframe(df[['product_name', 'nutriscore_score', 'energy_kcal_100g']])
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='mean')
    grid_options = gb.build()
    
    AgGrid(
        df[['product_name', 'nutriscore_score', 'energy_kcal_100g']],
        gridOptions=grid_options,
        height=400,
        theme='streamlit',
        enable_enterprise_modules=False
    )

if __name__ == "__main__":
    main()