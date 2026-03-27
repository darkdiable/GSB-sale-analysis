import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime


class SalesVisualizer:
    def __init__(self, df, style='seaborn-v0_8'):
        self.df = df.copy()
        plt.style.use(style)
        self.color_palette = sns.color_palette("husl", 10)
        
    def plot_brand_comparison(self, metric='revenue', top_n=10, save_path=None):
        brand_data = self.df.groupby('brand')[metric].sum().sort_values(ascending=False)
        
        plt.figure(figsize=(14, 7))
        bars = plt.bar(range(len(brand_data)), brand_data.values, color=self.color_palette)
        
        plt.xticks(range(len(brand_data)), brand_data.index, rotation=45)
        plt.xlabel('Brand')
        plt.ylabel(f'Total {metric}')
        plt.title(f'Top {top_n} Brands by {metric}')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_time_series(self, metric='revenue', freq='M', save_path=None):
        df = self.df.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        if freq == 'M':
            df['period'] = df['date'].dt.to_period('M')
        elif freq == 'W':
            df['period'] = df['date'].dt.to_period('W')
        elif freq == 'Q':
            df['period'] = df['date'].dt.to_period('Q')
        
        time_data = df.groupby('period')[metric].sum()
        
        plt.figure(figsize=(14, 7))
        plt.plot(time_data.index.astype(str), time_data.values, marker='o', linewidth=2)
        
        plt.xlabel('Period')
        plt.ylabel(f'Total {metric}')
        plt.title(f'{metric} Trend Over Time')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_regional_heatmap(self, metric='revenue', save_path=None):
        regional_data = self.df.pivot_table(
            values=metric, 
            index='brand', 
            columns='region', 
            aggfunc='sum'
        )
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(regional_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                   linewidths=.5, cbar_kws={"shrink": .5})
        
        plt.title(f'Regional Sales Heatmap by Brand ({metric})')
        plt.xlabel('Region')
        plt.ylabel('Brand')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_distribution(self, column='final_price', save_path=None):
        plt.figure(figsize=(10, 6))
        
        sns.histplot(data=self.df, x=column, kde=True, bins=30)
        
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.title(f'Distribution of {column}')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_brand_market_share(self, save_path=None):
        brand_revenue = self.df.groupby('brand')['revenue'].sum()
        
        plt.figure(figsize=(10, 10))
        plt.pie(brand_revenue.values, labels=brand_revenue.index, autopct='%1.1f%%',
               colors=self.color_palette, startangle=90)
        
        plt.title('Market Share by Brand')
        plt.axis('equal')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_quantity_vs_price(self, save_path=None):
        plt.figure(figsize=(10, 8))
        
        scatter = plt.scatter(self.df['final_price'], self.df['quantity'], 
                            c=self.df['revenue'], cmap='viridis', 
                            alpha=0.6, s=50)
        
        plt.xlabel('Final Price')
        plt.ylabel('Quantity')
        plt.title('Quantity vs Price (colored by Revenue)')
        
        plt.colorbar(scatter, label='Revenue')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_monthly_performance(self, save_path=None):
        df = self.df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        
        monthly_data = df.groupby('month').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'discount': 'mean'
        })
        
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        axes[0].bar(monthly_data.index, monthly_data['revenue'], color='steelblue')
        axes[0].set_ylabel('Revenue')
        axes[0].set_title('Monthly Revenue')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].bar(monthly_data.index, monthly_data['quantity'], color='coral')
        axes[1].set_ylabel('Quantity')
        axes[1].set_title('Monthly Quantity Sold')
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(monthly_data.index, monthly_data['discount'], 
                    marker='o', color='green', linewidth=2)
        axes[2].set_ylabel('Average Discount')
        axes[2].set_title('Monthly Average Discount')
        axes[2].grid(True, alpha=0.3)
        
        plt.xlabel('Month')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_top_salespersons(self, top_n=20, metric='revenue', save_path=None):
        salesperson_data = self.df.groupby('salesperson_id')[metric].sum().sort_values(ascending=False)
        
        plt.figure(figsize=(14, 7))
        bars = plt.bar(range(top_n), salesperson_data.head(top_n).values, color=self.color_palette)
        
        plt.xticks(range(top_n), salesperson_data.head(top_n).index, rotation=45)
        plt.xlabel('Salesperson ID')
        plt.ylabel(f'Total {metric}')
        plt.title(f'Top {top_n} Salespersons by {metric}')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_correlation_matrix(self, save_path=None):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='coolwarm', linewidths=.5, square=True)
        
        plt.title('Correlation Matrix')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_dashboard(self, save_path=None):
        fig = plt.figure(figsize=(20, 16))
        
        ax1 = plt.subplot(2, 3, 1)
        brand_data = self.df.groupby('brand')['revenue'].sum().sort_values(ascending=False).head(10)
        ax1.bar(range(len(brand_data)), brand_data.values, color=self.color_palette)
        ax1.set_xticks(range(len(brand_data)))
        ax1.set_xticklabels(brand_data.index, rotation=45)
        ax1.set_title('Top 10 Brands by Revenue')
        
        ax2 = plt.subplot(2, 3, 2)
        df = self.df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        monthly_revenue = df.groupby('month')['revenue'].sum()
        ax2.plot(monthly_revenue.index, monthly_revenue.values, marker='o')
        ax2.set_title('Monthly Revenue Trend')
        
        ax3 = plt.subplot(2, 3, 3)
        regional_data = self.df.groupby('region')['revenue'].sum()
        ax3.pie(regional_data.values, labels=regional_data.index, autopct='%1.1f%%')
        ax3.set_title('Regional Revenue Distribution')
        
        ax4 = plt.subplot(2, 3, 4)
        sns.boxplot(data=self.df, x='brand', y='final_price', ax=ax4)
        ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45)
        ax4.set_title('Price Distribution by Brand')
        
        ax5 = plt.subplot(2, 3, 5)
        color_data = self.df.groupby('color')['quantity'].sum()
        ax5.bar(range(len(color_data)), color_data.values)
        ax5.set_xticks(range(len(color_data)))
        ax5.set_xticklabels(color_data.index, rotation=45)
        ax5.set_title('Sales by Color')
        
        ax6 = plt.subplot(2, 3, 6)
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax6)
        ax6.set_title('Correlation Heatmap')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
