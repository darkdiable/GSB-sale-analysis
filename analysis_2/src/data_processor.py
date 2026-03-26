import pandas as pd
import numpy as np
from datetime import datetime


class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None

    def load_data(self):
        self.df = pd.read_excel(self.data_path)
        self.df['日期'] = pd.to_datetime(self.df['日期'])
        return self.df

    def clean_data(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        original_count = len(self.df)

        self.df = self.df[self.df['数量'] > 0]
        self.df = self.df[self.df['单价'] > 0]

        self.df = self.df.dropna(subset=['类别', '区域', '销售额'])

        self.df = self.df[~self.df['区域'].isin(['未知', 'None', ''])]

        cleaned_count = len(self.df)
        print(f"数据清洗完成: {original_count} -> {cleaned_count} 条记录")
        print(f"删除了 {original_count - cleaned_count} 条无效记录")

        return self.df

    def calculate_basic_metrics(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        metrics = {
            '总销售额': self.df['销售额'].sum(),
            '总利润': self.df['利润'].sum(),
            '平均订单金额': self.df['销售额'].mean(),
            '总订单数': len(self.df),
            '总销售数量': self.df['数量'].sum(),
            '平均客单价': self.df.groupby('客户ID')['销售额'].sum().mean()
        }

        return metrics

    def get_category_analysis(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        category_stats = self.df.groupby('类别').agg({
            '销售额': ['sum', 'mean'],
            '利润': 'sum',
            '数量': 'sum',
            '订单ID': 'count'
        }).round(2)

        category_stats.columns = ['总销售额', '平均销售额', '总利润', '总数量', '订单数']
        category_stats = category_stats.sort_values('总销售额', ascending=False)

        return category_stats

    def get_region_analysis(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        region_stats = self.df.groupby('区域').agg({
            '销售额': ['sum', 'mean'],
            '利润': 'sum',
            '数量': 'sum',
            '订单ID': 'count'
        }).round(2)

        region_stats.columns = ['总销售额', '平均销售额', '总利润', '总数量', '订单数']
        region_stats = region_stats.sort_values('总销售额', ascending=False)

        return region_stats

    def get_time_analysis(self, freq='M'):
        if self.df is None:
            raise ValueError("请先加载数据")

        self.df['月份'] = self.df['日期'].dt.to_period(freq)

        time_stats = self.df.groupby('月份').agg({
            '销售额': 'sum',
            '利润': 'sum',
            '数量': 'sum',
            '订单ID': 'count'
        }).round(2)

        time_stats.columns = ['销售额', '利润', '销售数量', '订单数']

        return time_stats

    def get_channel_analysis(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        channel_stats = self.df.groupby('销售渠道').agg({
            '销售额': ['sum', 'mean'],
            '利润': 'sum',
            '订单ID': 'count'
        }).round(2)

        channel_stats.columns = ['总销售额', '平均销售额', '总利润', '订单数']
        channel_stats = channel_stats.sort_values('总销售额', ascending=False)

        return channel_stats

    def get_payment_analysis(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        payment_stats = self.df.groupby('支付方式').agg({
            '销售额': 'sum',
            '订单ID': 'count'
        }).round(2)

        payment_stats.columns = ['总销售额', '订单数']
        payment_stats = payment_stats.sort_values('总销售额', ascending=False)

        return payment_stats

    def get_top_products(self, n=10):
        if self.df is None:
            raise ValueError("请先加载数据")

        product_stats = self.df.groupby('商品名称').agg({
            '销售额': 'sum',
            '利润': 'sum',
            '数量': 'sum',
            '订单ID': 'count'
        }).round(2)

        product_stats.columns = ['总销售额', '总利润', '总销量', '订单数']
        top_products = product_stats.sort_values('总销售额', ascending=False).head(n)

        return top_products

    def get_customer_analysis(self, n=20):
        if self.df is None:
            raise ValueError("请先加载数据")

        customer_stats = self.df.groupby('客户ID').agg({
            '销售额': ['sum', 'mean', 'count'],
            '利润': 'sum'
        }).round(2)

        customer_stats.columns = ['总消费额', '平均消费', '订单数', '总利润']
        top_customers = customer_stats.sort_values('总消费额', ascending=False).head(n)

        return top_customers

    def get_employee_analysis(self, n=15):
        if self.df is None:
            raise ValueError("请先加载数据")

        employee_stats = self.df.groupby('员工ID').agg({
            '销售额': ['sum', 'mean', 'count'],
            '利润': 'sum'
        }).round(2)

        employee_stats.columns = ['总销售额', '平均销售额', '订单数', '总利润']
        top_employees = employee_stats.sort_values('总销售额', ascending=False).head(n)

        return top_employees

    def calculate_growth_rate(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        time_stats = self.get_time_analysis('M')
        if len(time_stats) < 2:
            return None

        first_month = time_stats.iloc[0]['销售额']
        last_month = time_stats.iloc[-1]['销售额']

        growth_rate = ((last_month - first_month) / first_month) * 100

        return round(growth_rate, 2)

    def get_category_region_matrix(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        matrix = self.df.pivot_table(
            values='销售额',
            index='类别',
            columns='区域',
            aggfunc='sum',
            fill_value=0
        ).round(2)

        return matrix

    def get_time_category_trend(self):
        if self.df is None:
            raise ValueError("请先加载数据")

        self.df['月份'] = self.df['日期'].dt.to_period('M')

        trend = self.df.pivot_table(
            values='销售额',
            index='月份',
            columns='类别',
            aggfunc='sum',
            fill_value=0
        )

        return trend
