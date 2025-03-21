import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import random
import quantstats as qs
import requests
from bs4 import BeautifulSoup
import time
from json import JSONDecodeError  
#Define Functions
  
def get_mstr_data():
    mstr = yf.Ticker('MSTR')
    mstr_btc=get_mstr_btc()

    try:
      current_price = mstr.history(period='7d')['Close'].iloc[-1]
    except: 
      current_price=311

    retries = 3
    for attempt in range(retries):
        try:
            # Try fetching the market cap
            mrkt_cap = mstr.fast_info.get('marketCap', 0)
            hist = mstr.history(period='5y')['Close']
            shares=mstr.info['impliedSharesOutstanding'] 

            if mrkt_cap:
                break  # Exit loop if successful
        except (KeyError, AttributeError, TypeError, ValueError, JSONDecodeError):
            time.sleep(2)  # Wait and retry
            shares=294063000 #-----------------------------UPDATE
            mrkt_cap = shares*current_price   #-----------------------------UPDATE

    insiders=mstr.insider_roster_holders
    employees=mstr.info['fullTimeEmployees']
    return hist, current_price,mrkt_cap,shares,mstr_btc,insiders, employees

def get_btc_data():
    btc = yf.Ticker('BTC-USD')
    btc_hist = btc.history(period='5y')['Close']
    btc_price = btc.history(period='1d')['Close'].iloc[-1]
    return btc_price,btc_hist

def calculate_nav_premium(mstr_price, btc_price_last, bitcoin_per_share):
    nav_per_share = bitcoin_per_share * btc_price_last
    nav_premium = (mstr_price  / nav_per_share) 
    return nav_premium

def calculate_mstr_price(btc_price, nav_premium, bitcoin_per_share):
    nav_per_share = btc_price * bitcoin_per_share
    future_mstr_price = nav_per_share *  nav_premium  # NAV premium as a percentage
    return future_mstr_price


def get_mstr_btc():
    url = "https://saylortracker.com/"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we handle HTTP errors

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Locate the table and find the BTC amount in the correct <td>
      mstr_btc = soup.find('span', id = "current-btc-amount") 
    except Exception as e:
        print(f"Error fetching BTC holdings: {e}")
    return int(mstr_btc.get('data-value'))      

# Calculate data used througout
mstr_hist, mstr_price,mrkt_cap,shares,mstr_btc,insiders,employees = get_mstr_data()
btc_price_last,btc_hist = get_btc_data()
bitcoin_per_share =  mstr_btc/shares  # Update this with the latest value
nav_premium=calculate_nav_premium(mstr_price, btc_price_last, bitcoin_per_share)
CAGR=qs.stats.cagr(mstr_hist)*100
sharpe=qs.stats.sharpe(mstr_hist)
sortino=qs.stats.sortino(mstr_hist)
common=qs.stats.common_sense_ratio(mstr_hist)
WIN=qs.stats.outlier_win_ratio(mstr_hist)

# Page selection: First page for Current MSTR data, Second page for forecasting
page = st.sidebar.selectbox("Choose a page", ["Current MSTR Data", "MSTR Price Forecast", "Balance Sheet","Income Statement","Cash Flow","Financials"],index=0)


#-----------------PAGE 1------------------------------
if page == "Current MSTR Data":
  # Add MSTR logo and a GME mania GIF
  
  st.markdown("""
      <div style="text-align: center;">
          <a href="https://www.microstrategy.com" target="_blank">
              <img src="https://images.contentstack.io/v3/assets/bltb564490bc5201f31/blt095f79f0870f355f/65148375f8d6e8655c49519a/microstrategy-logo_red.svg" 
              alt="MicroStrategy Logo" style="width:400px;">
          </a>
      </div>
  """, unsafe_allow_html=True)  
  
  st.markdown("<h1 style='text-align: center; color: red;'>🚀 The Autist MSTR App 🚀</h1>", unsafe_allow_html=True)

  st.markdown("<h3 style='text-align: center;'>Track the madness of MSTR, BTC, and your tendies</h3>", unsafe_allow_html=True)
  st.image("https://media1.tenor.com/m/4z1chS4K7AYAAAAC/master-warning.gif", use_column_width=True)

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
      'CAGR (5y)',
      'Sharpe (5y)',
      'Sortino (5y)',
      'Common Sense Ratio',
      'Outlier Win Ratio' 
      ],
          'Current Value': [
          f"${mstr_price:,.2f}",
          f"${btc_price_last:,.2f}",
          f"${mrkt_cap:,.2f}",
          f"{shares:,.0f}",
          f"{mstr_btc:,.0f}",
          f"${mstr_btc*btc_price_last:,.0f}",
          f"{nav_premium:.3f}",
          f"{bitcoin_per_share:,.6f}",
          f"{CAGR:.2f}%",
          f"{sharpe:.2f}",
          f"{sortino:.2f}",
          f"{common:.2f}",
          f"{WIN:.2f}",
          
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
  st.markdown("<h2 style='color: red; text-align: center;'>Current MSTR Data</h2>", unsafe_allow_html=True)
  st.write(table_style + table_html, unsafe_allow_html=True)

  #Insider data
  insiders = insiders.drop('URL', axis=1)
  st.markdown("<h2 style='color: red; text-align: center;'>Current Insider Action</h2>", unsafe_allow_html=True)
  st.write("Total number of full time employees:", employees)
  st.write(table_style + insiders.to_html(index=False, escape=False), unsafe_allow_html=True)


  # Display the historical price chart for the aligned data
  # Ensure the 'Date' column is the index for both DataFrames
  mstr_hist.index = pd.to_datetime(mstr_hist.index)
  btc_hist.index = pd.to_datetime(btc_hist.index)

  # Use outer join to include all dates (even if one asset has missing data)
  aligned_data = pd.DataFrame({
    'MSTR_Close': mstr_hist, 
    'BTC_Close': btc_hist
})
  
  # Forward fill and backward fill to handle missing values
  aligned_data.fillna(method='ffill', inplace=True)
  aligned_data.fillna(method='bfill', inplace=True)

  # Plot with secondary y-axis
  fig = make_subplots(specs=[[{"secondary_y": True}]])

  # Add MSTR price trace (secondary y-axis)
  fig.add_trace(
      go.Scatter(x=aligned_data.index, y=aligned_data['MSTR_Close'], mode='lines', name='MSTR Price'),
      secondary_y=True
  )

  # Add BTC price trace (primary y-axis)
  fig.add_trace(
      go.Scatter(x=aligned_data.index, y=aligned_data['BTC_Close'], mode='lines', name='BTC Price', line=dict(color='orange')),
      secondary_y=False
  )

  # Update layout with titles
  fig.update_layout(
      title_text="MSTR & BTC Prices",
      xaxis_title="Date",
      yaxis_title="BTC Price",
      yaxis2_title="MSTR Price",  # Label for secondary y-axis
      legend_title="Assets",
      width=1000, 
      height=600  
  )

  # Update y-axes titles
  fig.update_yaxes(title_text="BTC Price", secondary_y=False)
  fig.update_yaxes(title_text="MSTR Price", secondary_y=True)

  # Display the plot
  st.plotly_chart(fig)

  st.markdown("<h4 style='text-align: center; color: red;'>Not financial advice. I smooth brain autist.</h4>", unsafe_allow_html=True)

  # Final touch with another meme GIF
  # Generate a random query string to force video reload
  random_suffix = random.randint(1, 10000)

  # Video URL with autoplay and random suffix to force reload
  video_url = f"https://www.youtube.com/embed/B5if2hthPCs?autoplay=1&rand={random_suffix}"

  # Center and embed the YouTube video with autoplay
  st.markdown(f"""
      <div style="text-align: center;">
          <iframe width="560" height="315" src="{video_url}" 
          frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
      </div>
  """, unsafe_allow_html=True)

#-------------------------------PAGE 2-------------------------
elif page == "MSTR Price Forecast":

  st.markdown("<h1 style='text-align: center; color: red;'>MSTR Price Forecast</h1>", unsafe_allow_html=True)

  # User inputs for future Bitcoin price and future NAV premium
  future_btc_price = st.number_input('Enter future Bitcoin price', value=btc_price_last, min_value=0.0)
  future_nav_premium = st.number_input('Enter future NAV Premium (%)', value=nav_premium, min_value=0.0)
  future_mstrBTC = st.number_input('Enter future MSTR Bitcoin held. My wifes boyfriend said this will go up.', value=mstr_btc, min_value=0)
  bitcoin_per_share =  future_mstrBTC/shares  # Update this with the latest value

  # Calculate future MSTR price based on the inputs
  future_mstr_price = calculate_mstr_price(future_btc_price, future_nav_premium, bitcoin_per_share)

  # Show the current MSTR price for reference
  st.write(f"**Current MSTR Price**: ${mstr_price:,.2f}")
    
  # Display the future MSTR price in big, orange text
  st.markdown(f"""
      <div style="text-align: center; color: orange; font-size: 48px;">
          <strong>Future MSTR Price: ${future_mstr_price:,.2f}</strong>
      </div>
  """, unsafe_allow_html=True)  
  
  # Final touch with another meme GIF
  # Generate a random query string to force video reload
  random_suffix = random.randint(1, 10000)

  # Video URL with autoplay and random suffix to force reload
  video_url = f"https://www.youtube.com/embed/wIhTGB3wqV0?autoplay=1&rand={random_suffix}"

  # Center and embed the YouTube video with autoplay
  st.markdown(f"""
      <div style="text-align: center;">
          <iframe width="560" height="315" src="{video_url}" 
          frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
      </div>
  """, unsafe_allow_html=True)


#-------------------------------PAGE 3-------------------------
elif page == "Balance Sheet":
  st.markdown("<h1 style='text-align: center; color: red;'>Balance Sheet</h1>", unsafe_allow_html=True)
  mstr = yf.Ticker('MSTR').quarterly_balance_sheet
  st.table(mstr)


#-------------------------------PAGE 4-------------------------
elif page == "Income Statement":
  st.markdown("<h1 style='text-align: center; color: red;'>Income Statement</h1>", unsafe_allow_html=True)
  mstr = yf.Ticker('MSTR').quarterly_income_stmt
  st.table(mstr)


#-------------------------------PAGE 5-------------------------
elif page == "Cash Flow":
  st.markdown("<h1 style='text-align: center; color: red;'>Cash Flow</h1>", unsafe_allow_html=True)
  mstr = yf.Ticker('MSTR').quarterly_cashflow
  st.table(mstr)


#-------------------------------PAGE 6-------------------------
elif page == "Financials":
  st.markdown("<h1 style='text-align: center; color: red;'>Financials</h1>", unsafe_allow_html=True)
  mstr = yf.Ticker('MSTR').quarterly_financials
  st.table(mstr)

