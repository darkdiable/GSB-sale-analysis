import pandas as pd
import numpy as np
from config import DATA_PATH

def load_data():
    df_sales = pd.read_csv('data/sales_data.csv')
    df_store = pd.read_csv('data/store_info.csv')
    return df_sales, df_store

def clean_data(df_sales, df_store):
    df_sales['date'] = pd.to_datetime(df_sales['date'], format='%Y-%m-%d') 
    
    df_merged = pd.merge(df_sales, df_store) 
    
    threshold = df_merged['sales'].quantile(0.99)
    df_merged = df_merged[df_merged['sales'] < threshold]
    
    df_merged['month'] = df_merged['date'].dt.month 
    
    return df_merged
