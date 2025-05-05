import requests
import pandas as pd
from datetime import datetime

url = 'https://api.coingecko.com/api/v3/coins/markets'
param = {
    'vs_currency' : 'usd',
    'order' : 'market_cap_desc',
    'per_page': 250,
    'page': 1
}

response=requests.get(url,params=param)

if response.status_code==200:
    print("Connection Successful")
    data=response.json()

    df=pd.DataFrame(data)

    # print(df.columns)
    # print(df.head())

    df=df[['id','current_price', 'market_cap','price_change_percentage_24h','ath','atl']]

    today=datetime.now().strftime('%d-%m-%Y  %H-%M-%S')
    df['time_stamp']=today

    top_negative=df.sort_values(by='price_change_percentage_24h',ascending=True).head(10)
    top_negative.to_csv("top_negative_{}.csv".format(today),index=False)
    top_positive=df.sort_values(by='price_change_percentage_24h',ascending=False).head(10)
    top_positive.to_csv("top_positive_{}.csv".format(today),index=False)

    df.to_csv("crypto_{}.csv".format(today),index=False)
    print("Data Saved Successfully!!!")
else:
    print(f"Connection Failed,Error Code:{response.status_code}")




