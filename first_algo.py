from re import L
from turtle import pd

period_short=12
period_long=26
import pandas as pd
import datetime

multiplier26=2/(26+1)
multiplier12=2/(12+1)
main_df=pd.read_csv('ETHUSD.csv')

main_df['Time'] = pd.to_datetime(main_df['Time'],unit='s')
main_df=main_df.set_index('Time')
main_df = main_df['Price'].resample('15Min').ohlc(_method='ohlc')

main_df["EMA12"]="None"
main_df["EMA26"]="None"
main_df=main_df.dropna()
main_df=main_df.reset_index()
del main_df['open']
sma12=main_df.loc[0:11,'close'].mean()
sma26=main_df.loc[0:25,'close'].mean()

main_df.loc[0:11,"EMA12"]=sma12
main_df.loc[0:25,"EMA26"]=sma26

lst12 = list(range(0,11))
lst26 = list(range(0,26))
for index, row in  main_df.iterrows():
    if index in lst12:
        continue
    
    main_df.loc[index,"EMA12"]=row['close'] * multiplier12 + main_df.loc[index-1,'EMA12']*(1-multiplier12)

for index, row in  main_df.iterrows():
    if index in lst26:
        continue
    
    main_df.loc[index,"EMA26"]=row['close'] * multiplier26 + main_df.loc[index-1,'EMA26']*(1-multiplier26)




main_df['signal']=''
for index, row in  main_df.iterrows():
    if index in lst26:
        continue
    if row['EMA12']>row['EMA26'] and main_df.loc[index-1,'EMA12']<main_df.loc[index-1,'EMA26']:
        main_df.loc[index,"signal"]='buy'
    if row['EMA12']<row['EMA26'] and main_df.loc[index-1,'EMA12']>main_df.loc[index-1,'EMA26']:
        main_df.loc[index,"signal"]='sell'

signal_types=['buy','sell']

buy_sell_df=main_df.loc[main_df['signal'].isin(signal_types)]
buy_sell_df["AVG"]=(buy_sell_df['high']+buy_sell_df['low'])/2

buy_sell_df['profit']=""
buy_sell_df['saldo']=""

buy_sell_df=buy_sell_df.reset_index(drop=True)

buy_sell_df.loc[0,'saldo']=0
buy_sell_df.loc[0,'profit']=0

for index, row in buy_sell_df.iterrows():
    if index==0:
        continue
    profit=row['AVG']-buy_sell_df.loc[index-1,'AVG']
    if row['signal']=='buy':

        buy_sell_df.loc[index,'profit']=-profit

    if row['signal']=='sell':
        
        buy_sell_df.loc[index,'profit']=profit
 

    saldo=buy_sell_df.loc[index-1,'saldo']+buy_sell_df.loc[index,'profit']
    buy_sell_df.loc[index,'saldo']=saldo
df2=pd.DataFrame()
df2['profit']=buy_sell_df['profit']
df2['signal']=buy_sell_df['signal']

grouped_df=df2.groupby(df2['signal']).sum()
grouped_df2=df2.groupby(df2['signal']).mean()
grouped_df3=df2.groupby(df2['signal']).median()
print(grouped_df)
print(grouped_df2)
print(grouped_df3)

