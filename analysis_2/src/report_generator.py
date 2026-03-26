import pandas as pd
import numpy as np
from datetime import datetime
import os


class ReportGenerator:
    def __init__(self, processor, output_dir='output'):
        self.processor = processor
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_summary_report(self):
        metrics = self.processor.calculate_basic_metrics()
        growth_rate = self.processor.calculate_growth_rate()

        report = []
        report.append("=" * 60)
        report.append("销售数据分析总结报告")
        report.append("=" * 60)
        report.append(f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("一、核心指标概览")
        report.append("-" * 60)
        report.append(f"总销售额：¥{metrics['总销售额']:,.2f}")
        report.append(f"总利润：¥{metrics['总利润']:,.2f}")
        report.append(f"平均订单金额：¥{metrics['平均订单金额']:,.2f}")
        report.append(f"总订单数：{metrics['总订单数']:,}")
        report.append(f"总销售数量：{metrics['总销售数量']:,}")
        report.append(f"平均客单价：¥{metrics['平均客单价']:,.2f}")

        if growth_rate:
            report.append(f"销售增长率：{growth_rate}%")

        report.append("")
        return "\n".join(report)

    def generate_category_report(self):
        category_stats = self.processor.get_category_analysis()

        report = []
        report.append("二、类别分析")
        report.append("-" * 60)

        total_sales = category_stats['总销售额'].sum()

        for category in category_stats.index:
            sales = category_stats.loc[category, '总销售额']
            profit = category_stats.loc[category, '总利润']
            avg_sale = category_stats.loc[category, '平均销售额']
            orders = category_stats.loc[category, '订单数']

            sales_pct = (sales / total_sales) * 100
            profit_margin = (profit / sales) * 100 if sales > 0 else 0

            report.append(f"\n【{category}】")
            report.append(f"  总销售额：¥{sales:,.2f} (占比 {sales_pct:.1f}%)")
            report.append(f"  总利润：¥{profit:,.2f} (利润率 {profit_margin:.1f}%)")
            report.append(f"  平均订单金额：¥{avg_sale:,.2f}")
            report.append(f"  订单数：{orders}")

        report.append("")
        return "\n".join(report)

    def generate_region_report(self):
        region_stats = self.processor.get_region_analysis()

        report = []
        report.append("三、区域分析")
        report.append("-" * 60)

        total_sales = region_stats['总销售额'].sum()

        for region in region_stats.index:
            sales = region_stats.loc[region, '总销售额']
            profit = region_stats.loc[region, '总利润']
            avg_sale = region_stats.loc[region, '平均销售额']
            orders = region_stats.loc[region, '订单数']

            sales_pct = (sales / total_sales) * 100
            profit_margin = (profit / sales) * 100 if sales > 0 else 0

            report.append(f"\n【{region}】")
            report.append(f"  总销售额：¥{sales:,.2f} (占比 {sales_pct:.1f}%)")
            report.append(f"  总利润：¥{profit:,.2f} (利润率 {profit_margin:.1f}%)")
            report.append(f"  平均订单金额：¥{avg_sale:,.2f}")
            report.append(f"  订单数：{orders}")

        report.append("")
        return "\n".join(report)

    def generate_channel_report(self):
        channel_stats = self.processor.get_channel_analysis()

        report = []
        report.append("四、销售渠道分析")
        report.append("-" * 60)

        total_sales = channel_stats['总销售额'].sum()

        for channel in channel_stats.index:
            sales = channel_stats.loc[channel, '总销售额']
            profit = channel_stats.loc[channel, '总利润']
            avg_sale = channel_stats.loc[channel, '平均销售额']
            orders = channel_stats.loc[channel, '订单数']

            sales_pct = (sales / total_sales) * 100
            profit_margin = (profit / sales) * 100 if sales > 0 else 0

            report.append(f"\n【{channel}】")
            report.append(f"  总销售额：¥{sales:,.2f} (占比 {sales_pct:.1f}%)")
            report.append(f"  总利润：¥{profit:,.2f} (利润率 {profit_margin:.1f}%)")
            report.append(f"  平均订单金额：¥{avg_sale:,.2f}")
            report.append(f"  订单数：{orders}")

        report.append("")
        return "\n".join(report)

    def generate_product_report(self):
        top_products = self.processor.get_top_products(15)

        report = []
        report.append("五、热销商品分析")
        report.append("-" * 60)
        report.append("\nTop 15 商品排名：\n")

        for i, product in enumerate(top_products.index, 1):
            sales = top_products.loc[product, '总销售额']
            profit = top_products.loc[product, '总利润']
            quantity = top_products.loc[product, '总销量']
            orders = top_products.loc[product, '订单数']

            report.append(f"{i}. {product}")
            report.append(f"   销售额：¥{sales:,.2f} | 利润：¥{profit:,.2f} | 销量：{quantity} | 订单数：{orders}")

        report.append("")
        return "\n".join(report)

    def generate_customer_report(self):
        customer_stats = self.processor.get_customer_analysis(15)

        report = []
        report.append("六、客户分析")
        report.append("-" * 60)
        report.append("\nTop 15 客户排名：\n")

        for i, customer in enumerate(customer_stats.index, 1):
            total_spent = customer_stats.loc[customer, '总消费额']
            avg_spent = customer_stats.loc[customer, '平均消费']
            orders = customer_stats.loc[customer, '订单数']
            profit = customer_stats.loc[customer, '总利润']

            report.append(f"{i}. {customer}")
            report.append(f"   总消费：¥{total_spent:,.2f} | 平均消费：¥{avg_spent:,.2f} | 订单数：{orders} | 贡献利润：¥{profit:,.2f}")

        report.append("")
        return "\n".join(report)

    def generate_employee_report(self):
        employee_stats = self.processor.get_employee_analysis(15)

        report = []
        report.append("七、员工绩效分析")
        report.append("-" * 60)
        report.append("\nTop 15 员工排名：\n")

        for i, employee in enumerate(employee_stats.index, 1):
            sales = employee_stats.loc[employee, '总销售额']
            avg_sale = employee_stats.loc[employee, '平均销售额']
            orders = employee_stats.loc[employee, '订单数']
            profit = employee_stats.loc[employee, '总利润']

            report.append(f"{i}. {employee}")
            report.append(f"   总销售额：¥{sales:,.2f} | 平均订单：¥{avg_sale:,.2f} | 订单数：{orders} | 总利润：¥{profit:,.2f}")

        report.append("")
        return "\n".join(report)

    def generate_insights(self):
        category_stats = self.processor.get_category_analysis()
        region_stats = self.processor.get_region_analysis()
        channel_stats = self.processor.get_channel_analysis()
        growth_rate = self.processor.calculate_growth_rate()

        report = []
        report.append("八、数据洞察与建议")
        report.append("-" * 60)

        best_category = category_stats.index[0]
        best_region = region_stats.index[0]
        best_channel = channel_stats.index[0]

        report.append(f"\n1. 表现最佳的类别是：{best_category}")
        report.append(f"   建议：加大 {best_category} 的库存和营销投入")

        report.append(f"\n2. 表现最佳的区域是：{best_region}")
        report.append(f"   建议：在 {best_region} 区域扩大市场份额")

        report.append(f"\n3. 表现最佳的销售渠道是：{best_channel}")
        report.append(f"   建议：优化 {best_channel} 渠道的用户体验")

        if growth_rate:
            if growth_rate > 0:
                report.append(f"\n4. 销售增长率为：+{growth_rate}%")
                report.append("   建议：保持当前增长策略，寻找新的增长点")
            else:
                report.append(f"\n4. 销售增长率为：{growth_rate}%")
                report.append("   建议：需要分析下降原因，调整销售策略")

        low_margin_categories = []
        for category in category_stats.index:
            sales = category_stats.loc[category, '总销售额']
            profit = category_stats.loc[category, '总利润']
            margin = (profit / sales) * 100 if sales > 0 else 0
            if margin < 15:
                low_margin_categories.append((category, margin))

        if low_margin_categories:
            report.append(f"\n5. 以下类别利润率较低，需要关注：")
            for cat, margin in low_margin_categories[:3]:
                report.append(f"   - {cat}: 利润率 {margin:.1f}%")

        report.append("")
        return "\n".join(report)

    def generate_full_report(self):
        full_report = []

        full_report.append(self.generate_summary_report())
        full_report.append(self.generate_category_report())
        full_report.append(self.generate_region_report())
        full_report.append(self.generate_channel_report())
        full_report.append(self.generate_product_report())
        full_report.append(self.generate_customer_report())
        full_report.append(self.generate_employee_report())
        full_report.append(self.generate_insights())

        report_text = "\n".join(full_report)

        report_path = os.path.join(self.output_dir, 'sales_analysis_report.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"\n完整报告已保存：{report_path}")
        return report_text

    def export_to_excel(self):
        output_path = os.path.join(self.output_dir, 'analysis_summary.xlsx')

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            category_stats = self.processor.get_category_analysis()
            category_stats.to_excel(writer, sheet_name='类别分析')

            region_stats = self.processor.get_region_analysis()
            region_stats.to_excel(writer, sheet_name='区域分析')

            time_stats = self.processor.get_time_analysis()
            time_stats.to_excel(writer, sheet_name='时间趋势')

            channel_stats = self.processor.get_channel_analysis()
            channel_stats.to_excel(writer, sheet_name='渠道分析')

            top_products = self.processor.get_top_products(10)
            top_products.to_excel(writer, sheet_name='热销商品')

            customer_stats = self.processor.get_customer_analysis(20)
            customer_stats.to_excel(writer, sheet_name='客户分析')

            employee_stats = self.processor.get_employee_analysis(15)
            employee_stats.to_excel(writer, sheet_name='员工绩效')

        print(f"Excel 报告已保存：{output_path}")
        return output_path
