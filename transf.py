import pandas as pd
import numpy as np

data_path = r'C:\Users\xuchu\Downloads\USDJPY\DAT_MT_USDJPY_M1_2019.csv'
df1 = pd.read_csv(data_path,parse_dates=[[0,1]],index_col=0)

df5 = df1.resample('5min',closed='left',label='left').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).dropna()

output_path = r'C:\Users\xuchu\Downloads\USDJPY\DAT_MT_USDJPY_M5_2019.csv'
df5.to_csv(output_path,sep=',',index=True,header=True)