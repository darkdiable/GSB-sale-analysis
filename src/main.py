import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, "..", "sales_data.csv")
        df = pd.read_csv(data_path)  
        df['order_date'] = pd.to_datetime(df['OrderDate'])  
    except Exception as e:
        print(f"加载数据失败: {e}")
        return None
    return df

def preprocess_data(df):
    if df is None:
        return None
    
    df_clean = df[df['Status'] != 'Cancelled'].copy()  
    
    df_clean['Revenue'] = df_clean['Amount'] * 0.9  
    
    category_sales = df_clean.groupby('ProductCategory')['Revenue'].sum().reset_index()
    
    return df_clean, category_sales

def visualize_data(df_clean, category_sales):
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    sales_trend = df_clean.groupby('order_date')['Revenue'].sum()
    sales_trend.plot()
    plt.xlabel("Date") 
    plt.ylabel("Revenue")
    plt.title("Daily Sales Trend")
    
    plt.subplot(1, 3, 2)
    category_sales.plot(kind='bar', x='ProductCategory', y='Revenue') 
    plt.title("Sales by Category")
    
    plt.subplot(1, 3, 3)
    sns.histplot(data=df_clean, x='Revenue', bins=10, kde=True)
    plt.title("Revenue Distribution")
    
    plt.tight_layout()
    plt.show()

def main():
    df = load_data()
    if df is not None:
        df_clean, category_sales = preprocess_data(df)
        if df_clean is not None and category_sales is not None:
            visualize_data(df_clean, category_sales)
        else:
            print("数据预处理失败！")
    else:
        print("数据加载失败！")

if __name__ == "__main__":
    main()
