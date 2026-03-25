import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data():
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sales_data.csv")
        df = pd.read_csv(csv_path)  
        required_columns = ['OrderDate', 'Status', 'ProductCategory', 'Amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"数据文件缺少必要的列: {missing_columns}")
            return None
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
    try:
        plt.figure(figsize=(15, 5))
        
        ax1 = plt.subplot(1, 3, 1)
        sales_trend = df_clean.groupby('order_date')['Revenue'].sum()
        sales_trend.plot(ax=ax1)
        ax1.set_xlabel("Date") 
        ax1.set_ylabel("Revenue")
        ax1.set_title("Daily Sales Trend")
        plt.xticks(rotation=45)
        
        ax2 = plt.subplot(1, 3, 2)
        category_sales.plot(kind='bar', x='ProductCategory', y='Revenue', ax=ax2) 
        ax2.set_title("Sales by Category")
        plt.xticks(rotation=45)
        
        ax3 = plt.subplot(1, 3, 3)
        sns.histplot(data=df_clean, x='Revenue', bins=10, kde=True, ax=ax3)
        ax3.set_title("Revenue Distribution")
        
        plt.tight_layout()
        
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sales_analysis.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {output_path}")
        
        try:
            plt.show()
        except:
            print("注意: 当前环境不支持GUI显示，图表已保存为图片文件")
    except Exception as e:
        print(f"可视化失败: {e}")

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
