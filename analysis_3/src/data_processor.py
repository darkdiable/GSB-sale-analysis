import pandas as pd
import numpy as np
from datetime import datetime


class DataProcessor:
    def __init__(self, sales_df, customer_df=None, dealer_df=None):
        self.sales_df = sales_df.copy()
        self.customer_df = customer_df.copy() if customer_df is not None else None
        self.dealer_df = dealer_df.copy() if dealer_df is not None else None
        
    def clean_data(self):
        self.sales_df = self.sales_df.drop_duplicates()
        
        self.sales_df = self.sales_df[self.sales_df['quantity'] > 0]
        self.sales_df = self.sales_df[self.sales_df['final_price'] > 0]
        
        self.sales_df['date'] = pd.to_datetime(self.sales_df['date'])
        
        # 使用正确的收入计算公式：quantity * final_price (final_price已经是折扣后的价格)
        self.sales_df['revenue'] = self.sales_df['quantity'] * self.sales_df['final_price']
        
        return self.sales_df
    
    def merge_customer_data(self):
        if self.customer_df is None:
            return self.sales_df
        
        # 从salesperson_id正确提取数字部分并格式化为customer_id
        def extract_customer_id(sp_id):
            if 'SP' in str(sp_id):
                num = str(sp_id).split('SP')[1]
                return f"CUST{int(num):05d}"
            else:
                return f"CUST{int(sp_id):05d}"
        
        self.sales_df['customer_id'] = self.sales_df['salesperson_id'].apply(extract_customer_id)
        
        merged_df = pd.merge(
            self.sales_df,
            self.customer_df,
            on='customer_id',
            how='left'  # 使用left join避免数据丢失
        )
        
        if len(merged_df) == 0:
            print("Warning: No data after merge - check customer_id mapping")
        
        return merged_df
    
    def merge_dealer_data(self):
        if self.dealer_df is None:
            return self.sales_df
        
        # 根据region匹配dealer_id，每个region可能有多个dealer，取第一个
        region_to_dealer = self.dealer_df.groupby('region')['dealer_id'].first().to_dict()
        
        self.sales_df['dealer_id'] = self.sales_df['region'].apply(
            lambda x: region_to_dealer.get(x, f"DLR{hash(x) % 100:03d}")
        )
        
        merged_df = pd.merge(
            self.sales_df,
            self.dealer_df,
            on='dealer_id',
            how='left',
            suffixes=('', '_dealer')
        )
        
        return merged_df
    
    def add_time_features(self, df=None):
        if df is None:
            df = self.sales_df
        else:
            df = df.copy()
        
        df['date'] = pd.to_datetime(df['date'])
        
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['dayofweek'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        df['week'] = df['date'].dt.isocalendar().week
        
        df['is_month_start'] = df['date'].dt.is_month_start.astype(int)
        df['is_month_end'] = df['date'].dt.is_month_end.astype(int)
        df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
        
        return df
    
    def calculate_metrics(self, df=None):
        if df is None:
            df = self.sales_df
        
        metrics = {
            'total_revenue': df['revenue'].sum(),
            'total_quantity': df['quantity'].sum(),
            'avg_discount': df['discount'].mean(),
            'avg_price': df['final_price'].mean(),
            'max_sale': df['revenue'].max(),
            'min_sale': df['revenue'].min()
        }
        
        return metrics
    
    def aggregate_by_brand(self, df=None):
        if df is None:
            df = self.sales_df
        
        brand_stats = df.groupby('brand').agg({
            'quantity': ['sum', 'mean', 'std'],
            'revenue': ['sum', 'mean', 'std'],
            'discount': ['mean', 'std'],
            'final_price': ['mean', 'std']
        })
        
        brand_stats.columns = ['_'.join(col).strip() for col in brand_stats.columns]
        brand_stats = brand_stats.reset_index()
        
        brand_stats['market_share'] = brand_stats['revenue_sum'] / brand_stats['revenue_sum'].sum() * 100
        
        return brand_stats
    
    def aggregate_by_region(self, df=None):
        if df is None:
            df = self.sales_df
        
        region_stats = df.groupby('region').agg({
            'quantity': ['sum', 'mean'],
            'revenue': ['sum', 'mean'],
            'discount': 'mean',
            'final_price': 'mean'
        })
        
        region_stats.columns = ['_'.join(col).strip() for col in region_stats.columns.values]
        region_stats = region_stats.reset_index()
        
        return region_stats
    
    def aggregate_by_time(self, df=None, freq='M'):
        if df is None:
            df = self.sales_df
        
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        if freq == 'M':
            aggregated = df.resample('M').agg({
                'quantity': 'sum',
                'revenue': 'sum',
                'discount': 'mean',
                'final_price': 'mean'
            })
        elif freq == 'W':
            aggregated = df.resample('W').agg({
                'quantity': 'sum',
                'revenue': 'sum',
                'discount': 'mean',
                'final_price': 'mean'
            })
        elif freq == 'Q':
            aggregated = df.resample('Q').agg({
                'quantity': 'sum',
                'revenue': 'sum',
                'discount': 'mean',
                'final_price': 'mean'
            })
        
        return aggregated.reset_index()
    
    def filter_data(self, conditions):
        filtered_df = self.sales_df.copy()
        
        for column, value in conditions.items():
            if isinstance(value, tuple):
                filtered_df = filtered_df[filtered_df[column].between(value[0], value[1])]
            elif isinstance(value, list):
                filtered_df = filtered_df[filtered_df[column].isin(value)]
            else:
                filtered_df = filtered_df[filtered_df[column] == value]
        
        return filtered_df
    
    def detect_outliers(self, column='revenue', method='iqr'):
        df = self.sales_df.copy()
        
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        elif method == 'zscore':
            mean = df[column].mean()
            std = df[column].std()
            
            z_scores = np.abs((df[column] - mean) / std)
            outliers = df[z_scores > 3]
        
        return outliers
