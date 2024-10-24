import yfinance as yf
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

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


st.title('MSTR Tracker App')

# Fetch data
mstr_hist, mstr_price = get_mstr_data()
btc_price = get_btc_data()
bitcoin_per_share = 0.75  # Update this with the latest value

# User inputs for MSTR shares owned and NAV Premium prediction
shares_owned = st.number_input('Number of MSTR shares owned', value=1, min_value=1)
future_btc_price = st.number_input('Future BTC Price', value=btc_price, min_value=1)
nav_premium_input = st.number_input('NAV Premium (%)', value=calculate_nav_premium(mstr_price, btc_price, bitcoin_per_share))

# Calculate future MSTR price and portfolio value
future_nav_per_share = future_btc_price * bitcoin_per_share
future_mstr_price = future_nav_per_share * (1 + (nav_premium_input / 100))
portfolio_value = future_mstr_price * shares_owned

# Display in a table
data = {
    'Metric': ['MSTR Price', 'Bitcoin Price', 'MSTR Market Cap', 'NAV Premium', 'Bitcoin per Share', 'Portfolio Value'],
    'Value': [mstr_price, btc_price, mstr_price * bitcoin_per_share, f"{nav_premium_input}%", bitcoin_per_share, portfolio_value]
}
df = pd.DataFrame(data)
st.table(df)

# Plot historical data
st.subheader('Historical Data')
fig = go.Figure()
fig.add_trace(go.Scatter(x=mstr_hist.index, y=mstr_hist['Close'], mode='lines', name='MSTR Price'))
fig.update_layout(title='MSTR Historical Price', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig)