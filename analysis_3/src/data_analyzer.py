import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from scipy import stats


class DataAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
        self.label_encoders = {}
        
    def brand_performance_analysis(self):
        brand_analysis = self.df.groupby('brand').agg({
            'quantity': ['sum', 'mean', 'count'],
            'revenue': ['sum', 'mean', 'std'],
            'discount': ['mean', 'min', 'max'],
            'final_price': ['mean', 'min', 'max']
        }).round(2)
        
        brand_analysis.columns = ['_'.join(col).strip() for col in brand_analysis.columns]
        brand_analysis = brand_analysis.reset_index()
        
        brand_analysis['revenue_per_unit'] = (
            brand_analysis['revenue_sum'] / brand_analysis['quantity_sum']
        )
        
        brand_analysis.loc[brand_analysis['quantity_sum'] == 0, 'revenue_per_unit'] = 0
        
        brand_analysis['performance_score'] = (
            brand_analysis['revenue_sum'].rank(pct=True) * 0.45 +
            brand_analysis['quantity_sum'].rank(pct=True) * 0.35 +
            (1 - brand_analysis['discount_mean'].rank(pct=True)) * 0.25
        ) * 100
        
        return brand_analysis.sort_values('performance_score', ascending=True)
    
    def regional_analysis(self):
        regional_stats = self.df.groupby('region').agg({
            'quantity': ['sum', 'mean'],
            'revenue': ['sum', 'mean'],
            'brand': 'nunique',
            'salesperson_id': 'nunique'
        })
        
        regional_stats.columns = ['total_quantity', 'avg_quantity', 
                                 'total_revenue', 'avg_revenue',
                                 'brand_count', 'salesperson_count']
        regional_stats = regional_stats.reset_index()
        
        regional_stats['revenue_contribution'] = (
            regional_stats['total_revenue'] / regional_stats['total_revenue'].sum() * 100
        )
        
        return regional_stats
    
    def temporal_analysis(self, freq='M'):
        df = self.df.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        if freq == 'M':
            df['period'] = df['date'].dt.to_period('M')
        elif freq == 'W':
            df['period'] = df['date'].dt.to_period('W')
        elif freq == 'Q':
            df['period'] = df['date'].dt.to_period('Q')
        
        temporal_stats = df.groupby('period').agg({
            'quantity': 'sum',
            'revenue': 'sum',
            'discount': 'mean',
            'brand': 'nunique'
        })
        
        temporal_stats['growth_rate'] = temporal_stats['revenue'].pct_change() * 100
        temporal_stats['moving_avg_3'] = temporal_stats['revenue'].rolling(window=3, min_periods=1).mean()
        temporal_stats['moving_avg_6'] = temporal_stats['revenue'].rolling(window=6, min_periods=1).mean()
        
        return temporal_stats.reset_index()
    
    def correlation_analysis(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.df[numeric_cols].corr()
        
        high_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.3:
                    high_correlations.append({
                        'var1': correlation_matrix.columns[i],
                        'var2': correlation_matrix.columns[j],
                        'correlation': round(corr_value, 3),
                        'causation': 'possible' if abs(corr_value) > 0.7 else 'unlikely'
                    })
        
        return correlation_matrix, pd.DataFrame(high_correlations)
    
    def trend_analysis(self, column='revenue'):
        df = self.df.copy()
        df = df.sort_values('date')
        
        df['cumulative_' + column] = df[column].cumsum()
        
        df['rolling_avg_7'] = df[column].rolling(window=7, min_periods=1).mean()
        df['rolling_avg_30'] = df[column].rolling(window=30, min_periods=1).mean()
        
        # 按日期聚合数据，避免同一天多条记录影响趋势分析
        daily_data = df.groupby('date')[column].sum().reset_index()
        daily_data = daily_data.sort_values('date')
        
        X = np.arange(len(daily_data)).reshape(-1, 1)
        y = daily_data[column].values
        
        model = LinearRegression()
        
        if len(X) < 2:
            return {
                'trend_direction': 'insufficient_data',
                'trend_slope': 0,
                'r_squared': 0,
                'confidence_level': 'low',
                'statistically_significant': False,
                'p_value': 1.0,
                'data_with_trends': df
            }
        
        model.fit(X, y)
        
        # 计算t统计量和p值
        n = len(X)
        y_pred = model.predict(X)
        mse = np.sum((y - y_pred) ** 2) / (n - 2) if n > 2 else 0
        x_mean = np.mean(X)
        ss_x = np.sum((X.flatten() - x_mean) ** 2)
        
        if mse > 0 and ss_x > 0:
            se_slope = np.sqrt(mse / ss_x)
            t_stat = model.coef_[0] / se_slope if se_slope > 0 else 0
            # 使用t分布计算p值（简化计算）
            from scipy import stats as scipy_stats
            p_value = 2 * (1 - scipy_stats.t.cdf(abs(t_stat), n - 2)) if n > 2 else 1.0
        else:
            p_value = 1.0
        
        trend_slope = model.coef_[0]
        # 根据斜率相对于数据均值的比例来判断趋势方向
        mean_value = np.mean(y)
        relative_slope = trend_slope / mean_value if mean_value > 0 else 0
        
        trend_direction = 'increasing' if relative_slope > 0.01 else 'decreasing' if relative_slope < -0.01 else 'stable'
        r_squared = model.score(X, y)
        
        # 综合考虑R²和p值来判断可信度
        # 高可信度：R² > 0.7 且 p < 0.05
        # 中等可信度：R² > 0.4 且 p < 0.1
        # 低可信度：其他情况
        if r_squared > 0.7 and p_value < 0.05:
            confidence = 'high'
        elif r_squared > 0.4 and p_value < 0.1:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        # 统计显著性：R² > 0.3 且 p < 0.05
        is_significant = r_squared > 0.3 and p_value < 0.05
        
        return {
            'trend_direction': trend_direction,
            'trend_slope': round(trend_slope, 2),
            'relative_slope': round(relative_slope, 4),
            'r_squared': round(r_squared, 4),
            'p_value': round(p_value, 4),
            'confidence_level': confidence,
            'statistically_significant': is_significant,
            'sample_size': n,
            'data_with_trends': df
        }
    
    def segmentation_analysis(self, n_clusters=5):
        df = self.df.copy()
        
        brand_encoded = self._encode_column('brand')
        region_encoded = self._encode_column('region')
        
        features = df[['quantity', 'final_price', 'discount', 'revenue']].copy()
        features['brand_encoded'] = brand_encoded
        features['region_encoded'] = region_encoded
        
        # 使用固定的random_state确保结果稳定
        np.random.seed(42)
        
        # 使用k-means++初始化，设置固定的random_state
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, 
                       max_iter=300, random_state=42)
        
        df['segment'] = kmeans.fit_predict(features)
        
        segment_profile = df.groupby('segment').agg({
            'quantity': ['mean', 'std'],
            'revenue': ['mean', 'std'],
            'discount': 'mean',
            'brand': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
        })
        
        if len(df['segment'].unique()) < n_clusters:
            print(f"Warning: Only {len(df['segment'].unique())} clusters formed instead of {n_clusters}")
        
        return df, segment_profile
    
    def salesperson_performance(self):
        salesperson_stats = self.df.groupby('salesperson_id').agg({
            'quantity': ['sum', 'mean', 'count'],
            'revenue': ['sum', 'mean'],
            'discount': 'mean',
            'brand': 'nunique',
            'region': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
        })
        
        salesperson_stats.columns = ['total_quantity', 'avg_quantity', 'sales_count',
                                    'total_revenue', 'avg_revenue',
                                    'avg_discount', 'brands_sold', 'primary_region']
        salesperson_stats = salesperson_stats.reset_index()
        
        salesperson_stats['performance_rank'] = salesperson_stats['total_revenue'].rank(
            ascending=False, method='min'
        ).astype(int)
        
        salesperson_stats['efficiency_score'] = (
            salesperson_stats['total_revenue'] / salesperson_stats['sales_count']
        ) / salesperson_stats['avg_discount']
        
        return salesperson_stats.sort_values('performance_rank')
    
    def price_elasticity_analysis(self, brand=None):
        df = self.df.copy()
        
        if brand:
            df = df[df['brand'] == brand]
        
        price_groups = pd.qcut(df['final_price'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        
        elasticity = df.groupby(price_groups).agg({
            'quantity': 'sum',
            'revenue': 'sum'
        })
        
        elasticity['avg_quantity'] = elasticity['quantity'] / elasticity['revenue'].count()
        
        return elasticity
    
    def _encode_column(self, column_name):
        if column_name not in self.label_encoders:
            self.label_encoders[column_name] = LabelEncoder()
            return self.label_encoders[column_name].fit_transform(self.df[column_name])
        else:
            return self.label_encoders[column_name].transform(self.df[column_name])
    
    def statistical_summary(self, group_by='brand'):
        summary = self.df.groupby(group_by).agg({
            'quantity': [stats.describe, lambda x: stats.skew(x)],
            'revenue': [lambda x: stats.kurtosis(x), 'std'],
            'discount': ['mean', 'std']
        })
        
        return summary
