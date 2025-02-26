# pages/1_🏠_Product_Nutrition.py (updated)
import streamlit as st
import pandas as pd
import plotly.express as px
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns 
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

    st.subheader("Understanding Nutrition Scores")
    st.markdown("""
    - 🟢 **Higher nutrition scores** mean healthier products  
    - 🔴 **Lower scores** indicate less nutritional value  
    - Compare calories vs nutrition - the ideal quadrant is **top-left** (high nutrition, low calories)
    """)
    
    # --------------------------
    #  Sliders for Each Numeric Column
    # --------------------------
    # Nutriscore
    min_nutri = int(df_sampled['nutriscore_score'].min())
    max_nutri = int(df_sampled['nutriscore_score'].max())
    selected_nutri = st.slider(
        "Select Nutriscore Range:",
        min_value=min_nutri,
        max_value=max_nutri,
        value=(min_nutri, max_nutri)
    )

    # Environmental Score
    min_env = int(df_sampled['environmental_score_score'].min())
    max_env = int(df_sampled['environmental_score_score'].max())
    selected_env = st.slider(
        "Select Environmental Score Range:",
        min_value=min_env,
        max_value=max_env,
        value=(min_env, max_env)
    )

    # Energy (kcal/100g)
    min_cal = int(df_sampled['energy_kcal_100g'].min())
    max_cal = int(df_sampled['energy_kcal_100g'].max())
    selected_cal = st.slider(
        "Select Calories Range:",
        min_value=min_cal,
        max_value=max_cal,
        value=(min_cal, max_cal)
    )

    # CO2 Total
    min_co2 = int(df_sampled['co2_total'].min())
    max_co2 = int(df_sampled['co2_total'].max())
    selected_co2 = st.slider(
        "Select CO2 Range:",
        min_value=min_co2,
        max_value=max_co2,
        value=(min_co2, max_co2)
    )

    # --------------------------
    #  Filter the DataFrame
    # --------------------------
    filtered_df = df_sampled[
        (df_sampled['nutriscore_score'].between(selected_nutri[0], selected_nutri[1])) &
        (df_sampled['environmental_score_score'].between(selected_env[0], selected_env[1])) &
        (df_sampled['energy_kcal_100g'].between(selected_cal[0], selected_cal[1])) &
        (df_sampled['co2_total'].between(selected_co2[0], selected_co2[1]))
    ]

    # --------------------------
    #  Plot 3D Scatter with Filters
    # --------------------------
    st.header("Nutritional Landscape (Filtered)")
    fig = px.scatter_3d(
        filtered_df,
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
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Nutrition ↑', autorange="reversed"),
            yaxis=dict(title='Calories →'),
            zaxis=dict(title='CO2 →')
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Section 2: Energy Content Analysis
    st.header("Calories vs. Nutrition Score (Log-Scaled 2D Histogram)")
    
    kcal_range = st.slider(
        "Select kcal range:",
        min_value=int(df_sampled['energy_kcal_100g'].min()),
        max_value=int(df_sampled['energy_kcal_100g'].max()),
        value=(0, 500)
    )
    
    filtered_df = df_sampled[(df_sampled['energy_kcal_100g'] >= kcal_range[0]) & 
                              (df_sampled['energy_kcal_100g'] <= kcal_range[1])]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    # norm=mcolors.LogNorm() applies a log scale on bin counts
    h = ax.hist2d(
        filtered_df['energy_kcal_100g'], 
        filtered_df['nutriscore_score'],
        bins=(50, 50),
        cmap='viridis',
        norm=mcolors.LogNorm()
    )
    
    # Add color bar
    cbar = plt.colorbar(h[3], ax=ax)
    cbar.set_label('Count (log scale)')
    
    ax.set_xlabel('Calories per 100g')
    ax.set_ylabel('Nutrition Score')
    ax.set_title('2D Histogram (Log-Scaled) of Calories vs Nutrition Score')
    st.pyplot(fig)
    
if __name__ == "__main__":
    main()
