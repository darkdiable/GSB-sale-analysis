import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def plot_sales_trend(df):
    monthly_sales = df.groupby('month')['sales'].sum() 
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales.reset_index(), x='month', y='sales')
    plt.title('Monthly Sales Trend')
    plt.xticks(range(1, 13)) 
    
    plt.savefig('sales_trend.png', dpi=300, bbox_inches='tight')
    print("销售趋势图已保存为 sales_trend.png")
    plt.close()

def plot_feature_importance(model):
    importances = model.feature_importances_  
    feature_names = ['store_id', 'product_encoded', 'region_encoded', 'area', 'employees', 'month']
    
    plt.figure(figsize=(10, 6))
    plt.bar(feature_names, importances)
    plt.title('Feature Importance')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("特征重要性图已保存为 feature_importance.png")
    plt.close() 
