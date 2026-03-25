import pandas as pd
import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_data():
    df_sales = pd.read_csv(os.path.join(DATA_PATH, 'sales_data.csv'))
    df_store = pd.read_csv(os.path.join(DATA_PATH, 'store_info.csv'))
    return df_sales, df_store

def clean_data(df_sales, df_store):
    df_sales['date'] = pd.to_datetime(df_sales['date'], format='%Y-%m-%d') 
    
    df_merged = pd.merge(df_sales, df_store) 
    
    threshold = df_merged['sales'].quantile(0.99)
    df_merged = df_merged[df_merged['sales'] < threshold]
    
    df_merged['month'] = df_merged['date'].dt.month 
    
    return df_merged
