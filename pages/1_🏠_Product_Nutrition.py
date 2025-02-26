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
    df_sampled = df.sample(30000, random_state=42)
    
    st.title("Nutritional Analysis")
    
    # Interactive 3D Scatter Plot
    st.header("Nutritional Landscape")
    fig = px.scatter_3d(
        df_sampled,
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

    # Section 2: Energy Content Analysis
    st.header("Energy Content Distribution")
    
    kcal_range = st.slider(
        "Select kcal range:",
        min_value=int(df_sampled['energy_kcal_100g'].min()),
        max_value=int(df_sampled['energy_kcal_100g'].max()),
        value=(0, 500)
    )
    
    filtered_df = df_sampled[(df_sampled['energy_kcal_100g'] >= kcal_range[0]) & 
                              (df_sampled['energy_kcal_100g'] <= kcal_range[1])]
    
    fig2 = px.density_hexbin(
        filtered_df,
        x='energy_kcal_100g',
        y='nutriscore_score',
        nbinsx=50,
        nbinsy=20,
        color_continuous_scale='Viridis',
        labels={
            'energy_kcal_100g': 'Calories per 100g',
            'nutriscore_score': 'Nutrition Score'
        }
    )
    fig2.update_layout(
        title='Relationship Between Calories and Nutrition Score',
        xaxis_range=kcal_range
    )
    st.plotly_chart(fig2, use_container_width=True)
    
if __name__ == "__main__":
    main()
