import matplotlib.pyplot as plt
import seaborn as sns

def plot_sales_trend(df):
    monthly_sales = df.groupby('month')['sales'].sum() 
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales.reset_index(), x='month', y='sales')
    plt.title('Monthly Sales Trend')
    plt.xticks(range(1, 13)) 
    
    plt.show()

def plot_feature_importance(model):
    importances = model.coef_  
    
    plt.bar(range(len(importances)), importances)
    plt.title('Feature Importance')
    plt.show() 
