import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import os


class Visualizer:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        import matplotlib
        matplotlib.use('Agg')
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        sns.set_style('whitegrid')

    def plot_category_sales(self, category_stats, save_name='category_sales.png'):
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        categories = category_stats.index.tolist()
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))

        axes[0, 0].bar(categories, category_stats['总销售额'], color=colors)
        axes[0, 0].set_title('各类别总销售额对比')
        axes[0, 0].set_xlabel('类别')
        axes[0, 0].set_ylabel('销售额')
        axes[0, 0].tick_params(axis='x', rotation=45)

        axes[0, 1].bar(categories, category_stats['总利润'], color=colors)
        axes[0, 1].set_title('各类别总利润对比')
        axes[0, 1].set_xlabel('类别')
        axes[0, 1].set_ylabel('利润')
        axes[0, 1].tick_params(axis='x', rotation=45)

        axes[1, 0].pie(category_stats['总销售额'], labels=categories, autopct='%1.1f%%')
        axes[1, 0].set_title('各类别销售额占比')

        axes[1, 1].bar(categories, category_stats['平均销售额'], color=colors)
        axes[1, 1].set_title('各类别平均订单金额对比')
        axes[1, 1].set_xlabel('类别')
        axes[1, 1].set_ylabel('平均销售额')
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_region_sales(self, region_stats, save_name='region_sales.png'):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        regions = region_stats.index.tolist()
        colors = plt.cm.Paired(np.linspace(0, 1, len(regions)))

        axes[0].bar(regions, region_stats['总销售额'], color=colors)
        axes[0].set_title('各区域总销售额对比')
        axes[0].set_xlabel('区域')
        axes[0].set_ylabel('销售额')
        axes[0].tick_params(axis='x', rotation=45)

        axes[1].pie(region_stats['总销售额'], labels=regions, autopct='%1.1f%%')
        axes[1].set_title('各区域销售额占比')

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_time_trend(self, time_stats, save_name='time_trend.png'):
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        periods = time_stats.index.astype(str).tolist()

        axes[0, 0].plot(periods, time_stats['销售额'], marker='o', linewidth=2, markersize=6)
        axes[0, 0].set_title('月度销售额趋势')
        axes[0, 0].set_xlabel('月份')
        axes[0, 0].set_ylabel('销售额')
        axes[0, 0].tick_params(axis='x', rotation=45)

        axes[0, 1].plot(periods, time_stats['利润'], marker='s', linewidth=2, markersize=6, color='green')
        axes[0, 1].set_title('月度利润趋势')
        axes[0, 1].set_xlabel('月份')
        axes[0, 1].set_ylabel('利润')
        axes[0, 1].tick_params(axis='x', rotation=45)

        axes[1, 0].bar(periods, time_stats['销售数量'], color='orange')
        axes[1, 0].set_title('月度销售数量趋势')
        axes[1, 0].set_xlabel('月份')
        axes[1, 0].set_ylabel('销售数量')
        axes[1, 0].tick_params(axis='x', rotation=45)

        axes[1, 1].plot(periods, time_stats['订单数'], marker='^', linewidth=2, markersize=6, color='red')
        axes[1, 1].set_title('月度订单数趋势')
        axes[1, 1].set_xlabel('月份')
        axes[1, 1].set_ylabel('订单数')
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_channel_analysis(self, channel_stats, save_name='channel_analysis.png'):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        channels = channel_stats.index.tolist()
        colors = plt.cm.Spectral(np.linspace(0, 1, len(channels)))

        axes[0].barh(channels, channel_stats['总销售额'], color=colors)
        axes[0].set_title('各销售渠道总销售额')
        axes[0].set_xlabel('销售额')
        axes[0].set_ylabel('销售渠道')

        axes[1].pie(channel_stats['订单数'], labels=channels, autopct='%1.1f%%')
        axes[1].set_title('各销售渠道订单数占比')

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_payment_analysis(self, payment_stats, save_name='payment_analysis.png'):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        payments = payment_stats.index.tolist()
        colors = plt.cm.Accent(np.linspace(0, 1, len(payments)))

        axes[0].bar(payments, payment_stats['总销售额'], color=colors)
        axes[0].set_title('各支付方式总销售额')
        axes[0].set_xlabel('支付方式')
        axes[0].set_ylabel('销售额')
        axes[0].tick_params(axis='x', rotation=45)

        axes[1].pie(payment_stats['订单数'], labels=payments, autopct='%1.1f%%')
        axes[1].set_title('各支付方式订单数占比')

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_top_products(self, top_products, save_name='top_products.png'):
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))

        products = top_products.index.tolist()
        colors = plt.cm.viridis(np.linspace(0, 1, len(products)))

        axes[0, 0].barh(products, top_products['总销售额'], color=colors)
        axes[0, 0].set_title('Top 10 商品总销售额')
        axes[0, 0].set_xlabel('销售额')
        axes[0, 0].set_ylabel('商品名称')

        axes[0, 1].barh(products, top_products['总利润'], color='green')
        axes[0, 1].set_title('Top 10 商品总利润')
        axes[0, 1].set_xlabel('利润')
        axes[0, 1].set_ylabel('商品名称')

        axes[1, 0].barh(products, top_products['总销量'], color='orange')
        axes[1, 0].set_title('Top 10 商品总销量')
        axes[1, 0].set_xlabel('销量')
        axes[1, 0].set_ylabel('商品名称')

        axes[1, 1].barh(products, top_products['订单数'], color='red')
        axes[1, 1].set_title('Top 10 商品订单数')
        axes[1, 1].set_xlabel('订单数')
        axes[1, 1].set_ylabel('商品名称')

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_category_region_heatmap(self, matrix, save_name='category_region_heatmap.png'):
        fig, ax = plt.subplots(figsize=(14, 10))

        sns.heatmap(matrix, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': '销售额'})

        plt.title('类别 - 区域 销售额热力图')
        plt.xlabel('区域')
        plt.ylabel('类别')

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_time_category_trend(self, trend, save_name='time_category_trend.png'):
        fig, ax = plt.subplots(figsize=(16, 8))

        categories = trend.columns.tolist()
        periods = trend.index.astype(str).tolist()

        for category in categories:
            ax.plot(periods, trend[category], marker='o', linewidth=2, markersize=6, label=category)

        ax.set_title('各类别月度销售趋势')
        ax.set_xlabel('月份')
        ax.set_ylabel('销售额')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def plot_customer_analysis(self, customer_stats, save_name='customer_analysis.png'):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        customers = customer_stats.index[:10].tolist()
        colors = plt.cm.tab20(np.linspace(0, 1, len(customers)))

        axes[0].barh(customers, customer_stats['总消费额'][:10], color=colors)
        axes[0].set_title('Top 10 客户总消费额')
        axes[0].set_xlabel('总消费额')
        axes[0].set_ylabel('客户 ID')

        axes[1].scatter(customer_stats['订单数'][:20], customer_stats['总消费额'][:20],
                       s=100, alpha=0.6, c=range(len(customer_stats[:20])), cmap='viridis')
        axes[1].set_title('客户订单数与消费额关系')
        axes[1].set_xlabel('订单数')
        axes[1].set_ylabel('总消费额')

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图表已保存：{save_path}")
        return save_path

    def create_all_charts(self, processor):
        print("\n开始生成可视化图表...")

        category_stats = processor.get_category_analysis()
        self.plot_category_sales(category_stats)

        region_stats = processor.get_region_analysis()
        self.plot_region_sales(region_stats)

        time_stats = processor.get_time_analysis()
        self.plot_time_trend(time_stats)

        channel_stats = processor.get_channel_analysis()
        self.plot_channel_analysis(channel_stats)

        payment_stats = processor.get_payment_analysis()
        self.plot_payment_analysis(payment_stats)

        top_products = processor.get_top_products(10)
        self.plot_top_products(top_products)

        matrix = processor.get_category_region_matrix()
        self.plot_category_region_heatmap(matrix)

        trend = processor.get_time_category_trend()
        self.plot_time_category_trend(trend)

        customer_stats = processor.get_customer_analysis()
        self.plot_customer_analysis(customer_stats)

        print("\n所有图表生成完成！")
