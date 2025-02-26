# pages/2_🌍_Environmental_Impact.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyarrow.parquet as pq

@st.cache_data
def load_data():
    table = pq.read_table("openfoodfacts-processed.parquet")
    df = table.to_pandas()  # Convert to Pandas DataFrame
    df = df.rename(columns={'energy-kcal_100g': 'energy_kcal_100g'})
    return df.dropna(subset=['environmental_score_score', 'co2_total'])

def main():
    df = load_data()
    
    st.title("Environmental Impact Analysis")
    st.markdown("Analyze the environmental footprint of food products")
    
    # Section 1: Environmental Impact vs CO2
    st.header("Environmental Impact vs Carbon Footprint")
    
    fig = px.scatter(
        df.sample(10000),  # Sample for better performance
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
        color_continuous_scale='RdYlGn',
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
    
    top_co2 = df.nlargest(20, 'co2_total')[['product_name', 'co2_total', 'environmental_score_score']]
    top_co2 = top_co2.sort_values('co2_total', ascending=True)
    
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
    - Products with higher environmental scores (worse) tend to have higher CO2 emissions
    - High-calorie products often correlate with higher environmental impact
    - Meat and dairy products typically appear in top CO2 emitters
    """)

if __name__ == "__main__":
    main()
