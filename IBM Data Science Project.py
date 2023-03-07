#IBM Cert. Stock Tracker

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import packaging 

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#TSLA Stock Data Extraction
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
print(tesla_data.head(5))
   

#Start Webscraping for TSLA
#Downloads the website data
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

#Parses the html data
soup = BeautifulSoup(html_data, "html5lib")
soup.prettify() #We were supposed to print this, but I didn't to save space in my terminal window

#Finds the Quarterly Tesla Revenue
tesla_revenue = pd.DataFrame(columns= ["Date", "Revenue"])
for table in soup.find_all('table'):
    if table.find('th').getText().startswith('Tesla Quarterly Revenue'):
        for row in table.find('tbody').find_all('tr'):
            col = row.find_all('td')
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace('$', '').replace(',','')
#The following would be TSLA's revenue reports for a WHILE, so I didn't output it
            tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index = True)
                        
tesla_revenue.dropna(axis=0, how='all', subset=['Revenue']) #drop NaN values
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""] #drop empty string value
print(tesla_revenue.tail(5))

#GME Stock Extractor
gme = yf.Ticker('GME')
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)
print(gme_data.head(5))


#Start scraping for Quarterly GME data
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html5lib")
soup.prettify() #There would normally be a print here, but as previously mentioned, it's not needed

#Actual scraping for Quarterly GME Data
gme_revenue = pd.DataFrame(columns= ["Date", "Revenue"])
for table in soup.find_all('table'):
    if table.find('th').getText().startswith("GameStop Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
            
            gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
print(gme_revenue.tail(5))
        

#Create graphs
make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'GameStop')