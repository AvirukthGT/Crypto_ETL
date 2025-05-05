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

    today=datetime.now().strftime('%d-%m-%Y')
    df['time_stamp']=today

    df.to_csv("crypto_{}.csv".format(today),index=False)
    print("Data Saved Successfully!!!")
else:
    print(f"Connection Failed,Error Code:{response.status_code}")




