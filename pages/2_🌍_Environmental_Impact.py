import streamlit as st
import pandas as pd
import plotly.express as px
import pyarrow.parquet as pq
from streamlit_plotly_events import plotly_events
from streamlit_extras.metric_cards import style_metric_cards

@st.cache_data
def load_data():
    table = pq.read_table("openfoodfacts-processed.parquet")
    df = table.to_pandas()  # Convert to Pandas DataFrame
    df = df.rename(columns={'energy-kcal_100g': 'energy_kcal_100g'})
    # Drop rows with NaN values in relevant columns
    df = df.dropna(subset=['environmental_score_score', 'co2_total', 'energy_kcal_100g'])
    return df

def main():
    df = load_data()
    
    st.title("Environmental Impact Analysis")
    
    # Interactive Scatter Plot with Selection
    st.header("Product Impact Explorer")
    
    # Ensure energy_kcal_100g has no NaN values
    df = df[df['energy_kcal_100g'].notna()]
    
    fig = px.scatter(
        df,  # Sample for better performance
        x='environmental_score_score',
        y='co2_total',
        color='nutriscore_score',
        size='energy_kcal_100g',
        hover_name='product_name',
        labels={
            'environmental_score_score': 'Environmental Impact Score (Lower is better) →',
            'co2_total': 'CO2 Emissions (g) →',
            'nutriscore_score': 'Nutrition Score →',
            'energy_kcal_100g': 'Calories →'
        },
        color_continuous_scale='tealrose',
    )
    fig.update_layout(
        dragmode='select',
        hovermode='closest',
        plot_bgcolor='#f8f9fa',
        xaxis=dict(autorange="reversed")
    )
    
    selected_points = plotly_events(fig, click_event=True)
    
    if selected_points:
        selected_index = selected_points[0]['pointIndex']
        selected_product = df.iloc[selected_index]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Product", selected_product['product_name'])
        col2.metric("CO2 Emissions", f"{selected_product['co2_total']}g")
        col3.metric("Environmental Score", selected_product['environmental_score_score'])
        style_metric_cards(border_left_color="#2ecc71")
    
    # Animated Radial Chart
    st.header("Environmental Impact Profile")
    avg_values = df[['environmental_score_score', 'co2_total', 'nutriscore_score']].mean()
    
    fig = px.line_polar(
        pd.DataFrame(dict(
            r=avg_values.values,
            theta=avg_values.index
        )),
        r='r',
        theta='theta',
        line_close=True,
        color_discrete_sequence=['#2ecc71'],
        template='plotly_dark'
    )
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
