import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders

import requests
import schedule
from datetime import datetime
import time
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()



def send_email(subject, body, filename):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")


    #comping the email
    message=MIMEMultipart()
    message['From']=sender_email
    message['reciever']=receiver_email
    message['Subject']=subject

    #attach body
    message.attach(MIMEText(body,'html'))


    #attach csv
    with open(filename, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        email.encoders.encode_base64(part)  # This line encodes the file in base64 (optional)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        message.attach(part)


    try:
        with smtplib.SMTP(smtp_server,smtp_port) as server:
            server.starttls()
            server.login(sender_email,email_password)
            server.sendmail(sender_email,receiver_email,message.as_string())
            print("Email Sent")
        

    except Exception  as e:
        print(f'Unable to send email {e}')

# getting crypto data
def get_crypto_data():
    # API information
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    param = {
        'vs_currency' : 'usd',
        'order' : 'market_cap_desc',
        'per_page': 250,
        'page': 1
    }

    # sending requests
    response = requests.get(url, params=param)

    if response.status_code == 200:
        print('Connection Successfull! \nGetting the data...')
        
        # storing the response into data
        data = response.json()
        
        # creating df dataframe
        df = pd.DataFrame(data)
        
        # selecting only columns we need -data cleaning
        df = df[[
            'id','current_price', 'market_cap', 'price_change_percentage_24h',
            'high_24h', 'low_24h','ath', 'atl',
        ]]
    
        #creating new columns
        today =  datetime.now().strftime('%d-%m-%Y %H-%M-%S')
        df['time_stamp'] = today
        
        # getting top 10
        top_negative_10 = df.nsmallest(10, 'price_change_percentage_24h')
        
        # # positive top
        top_positive_10 = df.nlargest(10, 'price_change_percentage_24h')
        
        # saving the data
        file_name = f'data/crypto_data {today}.csv'
        df.to_csv(file_name, index=False)
        
        print(f"Data saved successfull as {file_name}!")
        
        # call email function to send the reports
        
        subject = f"Top 10 crypto currency data to invest for {today}"
        body = f"""
            <html>
            <head>
                <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    background-color: #f9f9f9;
                    padding: 20px;
                }}
                h2 {{
                    color: #2e6da4;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: center;
                    padding: 8px;
                    font-size: 14px;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                </style>
            </head>
            <body>
                <h2>📊 Daily Crypto Market Report</h2>
                <p>Hello,</p>
                <p>Here's your latest crypto summary for <strong>{today}</strong>.</p>

                <h3>📈 Top 10 Cryptos with Highest Price Increase (24h)</h3>
                {top_positive_10.to_html(index=False, border=0)}

                <h3>📉 Top 10 Cryptos with Highest Price Decrease (24h)</h3>
                {top_negative_10.to_html(index=False, border=0)}

                <p>Best regards,<br>
                <em>Your Crypto Python App</em></p>
            </body>
            </html>
            """

         # sending mail
        send_email(subject, body, file_name)   
 
        
    else:
        print(f"Connection Failed Error Code {response.status_code}")

if __name__=='__main__':
    get_crypto_data()
    # schedule.every().day.at('17:57').do(get_crypto_data)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)