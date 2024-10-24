import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Add MSTR logo and a GME mania GIF
st.image("https://images.contentstack.io/v3/assets/bltb564490bc5201f31/blt095f79f0870f355f/65148375f8d6e8655c49519a/microstrategy-logo_red.svg", width=300)
st.markdown("<h1 style='text-align: center; color: red;'>MSTR Tracker App 🚀</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Track the madness of MSTR, BTC, and your portfolio</h3>", unsafe_allow_html=True)
st.image("https://media1.tenor.com/m/4z1chS4K7AYAAAAC/master-warning.gif", use_column_width=True)

# Fetch data
def get_mstr_data():
    mstr = yf.Ticker('MSTR')
    hist = mstr.history(period='1y')
    current_price = mstr.history(period='1d')['Close'].iloc[-1]
    return hist, current_price

def get_btc_data():
    btc = yf.Ticker('BTC-USD')
    btc_price = btc.history(period='1d')['Close'].iloc[-1]
    return btc_price

def calculate_nav_premium(mstr_price, btc_price, bitcoin_per_share):
    nav_per_share = bitcoin_per_share * btc_price
    nav_premium = ((mstr_price - nav_per_share) / nav_per_share) * 100
    return nav_premium

# Get data
mstr_hist, mstr_price = get_mstr_data()
btc_price = get_btc_data()
bitcoin_per_share = 0.75  # Update this with the latest value

# User inputs
st.sidebar.header("Input your portfolio details")
shares_owned = st.sidebar.number_input('Number of MSTR shares owned', value=1, min_value=1)
future_btc_price = st.sidebar.number_input('Future BTC Price', value=float(btc_price), min_value=float(1.0))
nav_premium_input = st.sidebar.number_input('NAV Premium (%)', value=float(calculate_nav_premium(mstr_price, btc_price, bitcoin_per_share)))

# Calculate future MSTR price and portfolio value
future_nav_per_share = future_btc_price * bitcoin_per_share
future_mstr_price = future_nav_per_share * (1 + (nav_premium_input / 100))
portfolio_value = future_mstr_price * shares_owned

# Display in a table
st.subheader("Current MSTR Data and Calculated Portfolio")
data = {
    'Metric': ['MSTR Price', 'Bitcoin Price', 'MSTR Market Cap', 'NAV Premium', 'Bitcoin per Share', 'Portfolio Value'],
    'Value': [mstr_price, btc_price, mstr_price * bitcoin_per_share, f"{nav_premium_input}%", bitcoin_per_share, portfolio_value]
}
df = pd.DataFrame(data)
st.table(df)

# Display the historical price chart
st.subheader('Historical Data')
fig = go.Figure()
fig.add_trace(go.Scatter(x=mstr_hist.index, y=mstr_hist['Close'], mode='lines', name='MSTR Price'))
fig.update_layout(title='MSTR Historical Price', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig)

# Add a flashy button
st.markdown("""
<div style="text-align: center;">
    <a href="https://www.microstrategy.com" target="_blank">
        <button style="background-color: #00BFFF; border-radius: 12px; padding: 15px 32px; font-size: 16px;">Visit MicroStrategy 🚀</button>
    </a>
</div>
""", unsafe_allow_html=True)

# Final touch with another meme GIF
st.image("https://media1.tenor.com/m/pS0e4-_PXXEAAAAC/do-something-michael-saylor.gif", use_column_width=True)
