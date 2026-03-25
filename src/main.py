import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载数据（故意设计路径错误和列名不匹配）
def load_data():
    try:
        # Bug 1: 文件路径错误（实际文件在 data/ 目录下，但代码可能找不到）
        df = pd.read_csv("data/sales_data.csv")  
        # Bug 2: 列名拼写错误（假设数据中列名为 'OrderDate'，但代码写为 'order_date'）
        df['order_date'] = pd.to_datetime(df['OrderDate'])  
    except Exception as e:
        print(f"加载数据失败: {e}")
        return None
    return df

# 2. 数据预处理（故意设计逻辑错误和索引错误）
def preprocess_data(df):
    if df is None:
        return None
    
    # Bug 3: 错误的条件判断（假设需要过滤 'Cancelled' 订单，但条件写反）
    df_clean = df[df['Status'] != 'Cancelled']  
    
    # Bug 4: 错误的列名引用（假设数据中无 'TotalAmount' 列，但代码尝试使用）
    df_clean['Revenue'] = df_clean['Amount'] * 0.9  # 修正为使用存在的列 'Amount'
    
    # Bug 5: 错误的分组逻辑（按 'Category' 分组，但数据中列名为 'ProductCategory'）
    category_sales = df_clean.groupby('ProductCategory')['Revenue'].sum().reset_index()
    
    return df_clean, category_sales

# 3. 可视化（故意设计图表配置错误和轴标签缺失）
def visualize_data(df_clean, category_sales):
    plt.figure(figsize=(15, 5))
    
    # 销售额趋势图（Bug 6: 未设置x轴标签和标题）
    plt.subplot(1, 3, 1)
    sales_trend = df_clean.groupby('order_date')['Revenue'].sum()
    sales_trend.plot()
    plt.xlabel("Date")  # 修复：添加标签
    plt.ylabel("Revenue")
    plt.title("Daily Sales Trend")
    
    # 品类分布图（Bug 7: 错误的图表类型（应使用条形图但用了饼图））
    plt.subplot(1, 3, 2)
    category_sales.plot(kind='bar', x='ProductCategory', y='Revenue')  # 修复：改为条形图
    plt.title("Sales by Category")
    
    # 客户地域分布（Bug 8: 假设数据中无 'Country' 列，但代码尝试绘制）
    plt.subplot(1, 3, 3)
    # 修复：删除此图或使用存在的列（如 'ProductCategory' 替代）
    # 示例：绘制品类分布的另一种形式
    sns.histplot(data=df_clean, x='Revenue', bins=10, kde=True)
    plt.title("Revenue Distribution")
    
    plt.tight_layout()
    plt.show()

# 主函数
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
