from flask import Flask , request
import pandas as pd
import numpy as np
import json
import pickle
from sklearn.preprocessing import StandardScaler
import os



APP = Flask(__name__)


model = pickle.load( open( "model.p", "rb" ) )


def generate_df(ticker):
    macd = 'https://www.alphavantage.co/query?function=MACD&symbol=' + ticker + '&interval=daily&series_type=open&apikey=NXAA2P2XI1GQSYPG'
    response1 = requests.get(macd)
    df_macd = pd.DataFrame.from_dict(response1.json()['Technical Analysis: MACD']).T

    stoch = 'https://www.alphavantage.co/query?function=STOCH&symbol=' + ticker + '&interval=daily&apikey=NXAA2P2XI1GQSYPG'
    response2 = requests.get(stoch)
    df_stoch = pd.DataFrame.from_dict(response2.json()['Technical Analysis: STOCH']).T

    # rsi = 'https://www.alphavantage.co/query?function=RSI&symbol='+ticker+'&interval=daily&time_period=10&series_type=open&apikey=NXAA2P2XI1GQSYPG'
    # response3 = requests.get(rsi)
    # df_rsi = pd.DataFrame.from_dict(response3.json()['Technical Analysis: RSI']).T

    aroon = 'https://www.alphavantage.co/query?function=AROONOSC&symbol=' + ticker + '&interval=daily&time_period=10&apikey=NXAA2P2XI1GQSYPG'
    response4 = requests.get(aroon)
    df_aroon = pd.DataFrame.from_dict(response4.json()['Technical Analysis: AROONOSC']).T

    dx = 'https://www.alphavantage.co/query?function=DX&symbol=' + ticker + '&interval=daily&time_period=10&apikey=NXAA2P2XI1GQSYPG'
    response5 = requests.get(dx)
    df_dx = pd.DataFrame.from_dict(response5.json()['Technical Analysis: DX']).T

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&interval=5min&outputsize=full&apikey=NXAA2P2XI1GQSYPG'
    response6 = requests.get(url)
    df = pd.DataFrame.from_dict(response6.json()['Time Series (Daily)']).T

    # Join all the dataset
    df = df.join(df_macd)
    df = df.join(df_stoch)
    # df = df.join(df_rsi)
    df = df.join(df_aroon)
    df = df.join(df_dx)
    return df

def signal_class(p):
  if p>=0.05:
    r = 1
  elif p<=-0.05:
    r = -1
  else:
    r=0
  return r

def generate_target(df):
  df2 =df.copy()
  df2 = df.astype(float)
  df2['next_10day_close']=df2['4. close'].shift(10)
  df2['percentage_change']=(df2['next_10day_close']-df2['4. close'])/df2['4. close']
  df2['signal']=df2['percentage_change'].apply(signal_class)
  return df2

@APP.route('/')
def hello_world():
    input ="MU"
    market_df = generate_df(input)
    market_df = market_df.dropna()
    X = market_df[['5. volume', 'MACD', 'AROONOSC',
                   'MACD_Hist', 'MACD_Signal', 'DX', 'SlowD', 'SlowK']]
    #print(X[0])
    sc = StandardScaler()
    X = sc.fit_transform(X)
    y_prebro = model.predict_proba(X[0].reshape(1, -1))
    print(y_prebro)
    dict1 = {'TA': {'sell':y_prebro[0][0],'hold':y_prebro[0][1],'buy':y_prebro[0][2]}, 'Sentiment':{'sell':0.5,'hold':0.25,'buy':0.25}}
    json1 = json.dumps(dict1)
    response=json1
    print(response)


    return response
