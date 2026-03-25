import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_sales_trend(df):
    monthly_sales = df.groupby('month')['sales'].sum()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales.reset_index(), x='month', y='sales')
    plt.title('Monthly Sales Trend')
    plt.xticks(range(1, 13))
    
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sales_trend.png')
    plt.savefig(output_path)
    print(f"Sales trend plot saved to: {output_path}")
    plt.close()

def plot_feature_importance(model):
    importances = model.feature_importances_
    feature_names = ['store_id', 'product_encoded', 'region_encoded', 'area', 'employees', 'month']
    
    plt.figure(figsize=(10, 6))
    plt.bar(feature_names, importances)
    plt.title('Feature Importance')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'feature_importance.png')
    plt.savefig(output_path)
    print(f"Feature importance plot saved to: {output_path}")
    plt.close() 
