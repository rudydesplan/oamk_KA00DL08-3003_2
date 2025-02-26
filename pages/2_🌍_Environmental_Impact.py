# pages/2_🌍_Environmental_Impact.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyarrow.parquet as pq
import config

@st.cache_data
def load_data():
    table = pq.read_table("openfoodfacts-processed.parquet")
    df = table.to_pandas()  # Convert to Pandas DataFrame
    df = df.rename(columns={'energy-kcal_100g': 'energy_kcal_100g'})
    return df.dropna(subset=['environmental_score_score', 'co2_total','energy_kcal_100g'])

def main():
    df = load_data()
    
    st.title("Environmental Impact Analysis")
    
    st.subheader("Reading Environmental Scores")
    st.markdown("""
    - 🌱 **Lower environmental scores** are better (0-100 scale)
    - CO2 emissions are measured per 100g of product
    - Hover over bubbles to see product details
    """)
    
    # Section 1: Environmental Impact vs CO2
    st.header("Environmental Impact vs Carbon Footprint")
    
    fig = px.scatter(
        df.sample(30000, random_state=42),  # Sample for better performance
        x='environmental_score_score',
        y='co2_total',
        color='nutriscore_score',
        size='energy_kcal_100g',
        hover_name='product_name',
        labels={
            'environmental_score_score': 'Environmental Score (Lower is better)',
            'co2_total': 'CO2 Emissions (g)',
            'nutriscore_score': 'Nutrition Score',
            'energy_kcal_100g': 'Calories'
        },
        color_continuous_scale=config.ENV_COLORS,
        title='Environmental Impact vs CO2 Emissions'
    )
    fig.update_layout(
        plot_bgcolor='#f0f0f0',
        xaxis=dict(autorange="reversed"),
        coloraxis_colorbar=dict(title="Nutrition Score")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Section 2: Top CO2 Emitters
    st.header("Highest CO2 Emission Products")
    
    top_co2 = (
    df.groupby("product_name", as_index=False)
    .agg({"co2_total": "mean", "environmental_score_score": "mean"})
    )
    
    top_co2 = top_co2.nlargest(20, "co2_total").sort_values("co2_total", ascending=True)
    
    fig2 = go.Figure(go.Bar(
        x=top_co2['co2_total'],
        y=top_co2['product_name'],
        orientation='h',
        marker_color='#e74c3c',
        hovertemplate="<b>%{y}</b><br>CO2: %{x}g<extra></extra>"
    ))
    
    fig2.update_layout(
        title='Top 20 Products by CO2 Emissions',
        xaxis_title="CO2 Emissions (g)",
        yaxis_title="Product Name",
        height=600,
        margin=dict(l=150)
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Key Insights
    st.markdown("""
    ## Key Insights
    - Meat and dairy products typically appear in top CO2 emitters
    """)

if __name__ == "__main__":
    main()
