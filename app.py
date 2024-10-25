import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Page selection: First page for Current MSTR data, Second page for forecasting
page = st.sidebar.selectbox("Choose a page", ["Current MSTR Data", "MSTR Price Forecast"])

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

  def calculate_nav_premium(mstr_price, btc_price_last, bitcoin_per_share):
      nav_per_share = bitcoin_per_share * btc_price_last
      nav_premium = (mstr_price  / nav_per_share) 
      return nav_premium

  # Get data
  mstr_hist, mstr_price,mrkt_cap,shares,mstr_btc,insiders = get_mstr_data()
  btc_price_last,btc_hist = get_btc_data()
  btc_price=get_btc_data()
  bitcoin_per_share =  mstr_btc/shares  # Update this with the latest value
  nav_premium=calculate_nav_premium(mstr_price, btc_price_last, bitcoin_per_share)

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
          f"{nav_premium:.3f}",
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


  # Display the historical price chart for the aligned data
  # Ensure the 'Date' column is the index for both DataFrames
  mstr_hist.index = pd.to_datetime(mstr_hist.index)
  btc_hist.index = pd.to_datetime(btc_hist.index)

  # Use outer join to include all dates (even if one asset has missing data)
  aligned_data = mstr_hist[['Close']].join(btc_hist[['Close']], lsuffix='_MSTR', rsuffix='_BTC', how='outer')

  # Forward fill and backward fill to handle missing values
  aligned_data.fillna(method='ffill', inplace=True)
  aligned_data.fillna(method='bfill', inplace=True)

  # Plot with secondary y-axis
  fig = make_subplots(specs=[[{"secondary_y": True}]])

  # Add MSTR price trace (secondary y-axis)
  fig.add_trace(
      go.Scatter(x=aligned_data.index, y=aligned_data['Close_MSTR'], mode='lines', name='MSTR Price'),
      secondary_y=True
  )

  # Add BTC price trace (primary y-axis)
  fig.add_trace(
      go.Scatter(x=aligned_data.index, y=aligned_data['Close_BTC'], mode='lines', name='BTC Price', line=dict(color='orange')),
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

  # Add a flashy button
  #st.markdown("""
  #<div style="text-align: center;">
  #    <a href="https://www.microstrategy.com" target="_blank">
  #        <button style="background-color: #00BFFF; border-radius: 12px; padding: 15px 32px; font-size: 16px;">Visit MicroStrategy 🚀</button>
  #    </a>
  #</div>
  #""", unsafe_allow_html=True)

  # Final touch with another meme GIF
  # Embed YouTube video with autoplay
  video_url = "https://www.youtube.com/embed/B5if2hthPCs?autoplay=1"

  # Use HTML to embed the video in an iframe
  st.markdown(f"""
      <iframe width="560" height="315" src="{video_url}" 
      frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  """, unsafe_allow_html=True)
# The second page for forecasting MSTR price
elif page == "MSTR Price Forecast":
    st.title("MSTR Price Forecast Based on Bitcoin or NAV Premium")
