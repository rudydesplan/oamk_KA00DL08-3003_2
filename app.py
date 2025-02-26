# app.py
import streamlit as st
from streamlit_lottie import st_lottie
import json

# Load Lottie animation
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

st.set_page_config(
    page_title="Food Product Analysis",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🍏 Open Food Facts Nutritional & Environmental Analysis")
    
    # Add animated header
    lottie_food = load_lottie("food_animation.json")  # Get free animations from LottieFiles
    st_lottie(
        lottie_food,
        speed=1,
        reverse=False,
        loop=True,
        quality="medium",
        height=200,
    )
    
    st.markdown("""
    Welcome to our interactive food product analysis tool. Explore nutritional and environmental impacts of 500,000 food products!
    """)

if __name__ == "__main__":
    main()