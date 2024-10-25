import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Add MSTR logo and a GME mania GIF
st.image("https://images.contentstack.io/v3/assets/bltb564490bc5201f31/blt095f79f0870f355f/65148375f8d6e8655c49519a/microstrategy-logo_red.svg", width=300)
st.markdown("<h1 style='text-align: center; color: red;'>🚀 THE Autist MSTR App 🚀</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Track the madness of MSTR, BTC, and your portfolio</h3>", unsafe_allow_html=True)
st.image("https://media1.tenor.com/m/4z1chS4K7AYAAAAC/master-warning.gif", use_column_width=True)

# Fetch data
def get_mstr_data():
    mstr = yf.Ticker('MSTR')
    mstr_btc=252220
    mrkt_cap=mstr.fast_info['marketCap']
    hist = mstr.history(period='5y')
    current_price = mstr.history(period='1d')['Close'].iloc[-1]
    shares=mstr.get_shares_full().iloc[-1]
    insiders=mstr.insider_roster_holders
    return hist, current_price,mrkt_cap,shares,mstr_btc,insiders

def get_btc_data():
    btc = yf.Ticker('BTC-USD')
    btc_hist = btc.history(period='5y')
    btc_price = btc.history(period='1d')['Close'].iloc[-1]
    return btc_price,btc_hist

def calculate_nav_premium(mstr_price, btc_price, bitcoin_per_share):
    nav_per_share = bitcoin_per_share * btc_price
    nav_premium = (mstr_price  / nav_per_share) 
    return nav_premium

# Get data
mstr_hist, mstr_price,mrkt_cap,shares,mstr_btc,insiders = get_mstr_data()
btc_price_last,btc_hist = get_btc_data()
btc_price=get_btc_data()
bitcoin_per_share =  mstr_btc/shares  # Update this with the latest value
nav_premium=calculate_nav_premium(mstr_price, btc_price_last, bitcoin_per_share)
# User inputs
st.sidebar.header("Input your portfolio details")
shares_owned = st.sidebar.number_input('Number of MSTR shares owned', value=1, min_value=1)
#future_btc_price = st.sidebar.number_input('Future BTC Price', value=float(btc_price), min_value=float(1.0))
nav_premium_input = st.sidebar.number_input('NAV Premium ', value=float(calculate_nav_premium(mstr_price, btc_price, bitcoin_per_share)))

# Calculate future MSTR price and portfolio value
#future_nav_per_share = future_btc_price * bitcoin_per_share
future_mstr_price = nav_premium * (1 + (nav_premium / 100))
portfolio_value = mstr_price * shares_owned

# Display in a table

data = {
    'Metric': ['MSTR Price (USD)', 
    'Bitcoin Price (USD)', 
    'MSTR Market Cap (USD)', 
    'MSTR Shares Outstanding',
    'MSTR BTC Treasury',
    'MSTR BTC Value',  
    'NAV Premium', 
    'Bitcoin per Share', 
    ],
        'Current Value': [
        f"${mstr_price:,.2f}",
        f"${btc_price_last:,.2f}",
        f"${mrkt_cap:,.2f}",
        f"{shares:,.0f}",
        f"{mstr_btc:,.0f}",
        f"${mstr_btc*btc_price_last:,.0f}",
        f"{nav_premium_input:.3f}",
        f"{bitcoin_per_share:,.6f}"
        
    ]
}
df = pd.DataFrame(data)

# Custom CSS for table styling: center headers and left-align the data
table_style = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        text-align: center;
        font-weight: bold;
        padding: 8px;
        
    }
    td {
        text-align: left;
        padding: 8px;
    }
    </style>
"""

# Convert DataFrame to HTML and apply the custom style
table_html = df.to_html(index=False, escape=False)

# Convert DataFrame to a dictionary format that doesn't include the index
st.subheader("Current MSTR Data")
st.write(table_style + table_html, unsafe_allow_html=True)

#Insider data
insiders = insiders.drop('URL', axis=1)

st.subheader("Current Insider Action")
st.write(table_style + insiders.to_html(index=False, escape=False), unsafe_allow_html=True)


# Display the historical price chart
st.subheader('Historical Data')
fig = go.Figure()
fig.add_trace(go.Scatter(x=mstr_hist.index, y=mstr_hist['Close'], mode='lines', name='MSTR Price'))
# Add BTC price trace
fig.add_trace(go.Scatter(x=btc_price.index, y=btc_hist['Close'], mode='lines', name='BTC Price', line=dict(color='orange')))
fig.update_layout(title='MSTR & BTC Price', xaxis_title='Date', yaxis_title='Price')
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
