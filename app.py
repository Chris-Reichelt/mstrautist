import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Page selection: First page for Current MSTR data, Second page for forecasting
page = st.sidebar.selectbox("Choose a page", ["Current MSTR Data", "MSTR Price Forecast"])

if page == "Current MSTR Data":
    # Layout for MicroStrategy logo and the button side by side
    col1, col2 = st.columns([3, 1])  # Adjust ratio as necessary
    
    # Add MSTR logo in the left column
    with col1:
        st.image("https://images.contentstack.io/v3/assets/bltb564490bc5201f31/blt095f79f0870f355f/65148375f8d6e8655c49519a/microstrategy-logo_red.svg", width=300)
    
    # Add the button in the right column
    with col2:
        st.markdown("""
        <div style="text-align: right;">
            <a href="https://www.microstrategy.com" target="_blank">
                <button style="background-color: #00BFFF; border-radius: 12px; padding: 15px 32px; font-size: 16px;">Visit MicroStrategy 🚀</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: red;'>🚀 THE Autist MSTR App 🚀</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Track the madness of MSTR, BTC, and your portfolio</h3>", unsafe_allow_html=True)
    st.image("https://media1.tenor.com/m/4z1chS4K7AYAAAAC/master-warning.gif", use_column_width=True)

    # Existing code for Current MSTR data (with table, historical price, etc.)
    # ...

    # Final touch with another meme GIF
    video_url = "https://www.youtube.com/embed/B5if2hthPCs?autoplay=1"
    st.markdown(f"""
        <iframe width="560" height="315" src="{video_url}" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

elif page == "MSTR Price Forecast":
    st.title("MSTR Price Forecast Based on Bitcoin or NAV Premium")

    # User inputs for future BTC price or NAV premium
    future_btc_price = st.number_input('Enter future Bitcoin price', value=btc_price_last)
    nav_premium_input = st.number_input('Enter future NAV Premium (%)', value=nav_premium_input)

    # Calculate future MSTR price based on future BTC price or NAV premium
    future_nav_per_share = future_btc_price * bitcoin_per_share
    future_mstr_price_btc = future_nav_per_share * (1 + (nav_premium_input / 100))

    st.write(f"Future MSTR price based on entered Bitcoin price and NAV premium: ${future_mstr_price_btc:,.2f}")
    
    # More forecasting logic, charts, or inputs as needed
