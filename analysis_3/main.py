import os
import sys
from datetime import datetime
import pandas as pd

from src.data_processor import DataProcessor
from src.data_analyzer import DataAnalyzer
from src.visualizer import SalesVisualizer


def main():
    print("=" * 60)
    print("Car Brand Sales Analysis System")
    print("=" * 60)
    
    output_dir = "reports"
    data_dir = "data"
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    print("\nLoading data files...")
    sales_df = pd.read_csv('data/sales_data.csv')
    customer_df = pd.read_csv('data/customer_data.csv')
    dealer_df = pd.read_csv('data/dealer_data.csv')
    
    print(f"Loaded {len(sales_df)} sales records")
    print(f"Loaded {len(customer_df)} customer records")
    print(f"Loaded {len(dealer_df)} dealer records")
    
    print("\n[1/6] Processing data...")
    processor = DataProcessor(sales_df, customer_df, dealer_df)
    
    cleaned_df = processor.clean_data()
    print(f"Cleaned data shape: {cleaned_df.shape}")
    
    merged_customer_df = processor.merge_customer_data()
    merged_dealer_df = processor.merge_dealer_data()
    
    df_with_features = processor.add_time_features(cleaned_df)
    
    metrics = processor.calculate_metrics(df_with_features)
    print(f"Total Revenue: ${metrics['total_revenue']:,.2f}")
    print(f"Total Quantity Sold: {metrics['total_quantity']:,}")
    
    brand_stats = processor.aggregate_by_brand(df_with_features)
    region_stats = processor.aggregate_by_region(df_with_features)
    time_stats = processor.aggregate_by_time(df_with_features, freq='M')
    
    print("\n[2/6] Analyzing data...")
    analyzer = DataAnalyzer(df_with_features)
    
    brand_performance = analyzer.brand_performance_analysis()
    print("\nBrand Performance Analysis:")
    print(brand_performance.head(10))
    
    regional_analysis = analyzer.regional_analysis()
    print("\nRegional Analysis:")
    print(regional_analysis)
    
    temporal_analysis = analyzer.temporal_analysis(freq='M')
    print("\nTemporal Analysis:")
    print(temporal_analysis.head(12))
    
    corr_matrix, high_correlations = analyzer.correlation_analysis()
    print("\nHigh Correlations:")
    print(high_correlations)
    
    trend_result = analyzer.trend_analysis(column='revenue')
    print(f"\nTrend Analysis: {trend_result['trend_direction']}")
    print(f"Trend Slope: {trend_result['trend_slope']}")
    print(f"R-squared: {trend_result['r_squared']}")
    print(f"P-value: {trend_result['p_value']}")
    print(f"Confidence Level: {trend_result['confidence_level']}")
    print(f"Statistically Significant: {trend_result['statistically_significant']}")
    
    segmented_df, segment_profile = analyzer.segmentation_analysis(n_clusters=5)
    print("\nCustomer Segmentation Profile:")
    print(segment_profile)
    
    salesperson_perf = analyzer.salesperson_performance()
    print("\nTop 10 Salespersons:")
    print(salesperson_perf.head(10))
    
    print("\n[3/6] Creating visualizations...")
    visualizer = SalesVisualizer(df_with_features, style='seaborn-v0_8')
    
    print("Generating brand comparison chart...")
    visualizer.plot_brand_comparison(metric='revenue', top_n=10, 
                                    save_path=f"{output_dir}/brand_comparison.png")
    
    print("Generating time series chart...")
    visualizer.plot_time_series(metric='revenue', freq='M', 
                               save_path=f"{output_dir}/time_series.png")
    
    print("Generating regional heatmap...")
    visualizer.plot_regional_heatmap(metric='revenue', 
                                    save_path=f"{output_dir}/regional_heatmap.png")
    
    print("Generating market share pie chart...")
    visualizer.plot_brand_market_share(save_path=f"{output_dir}/market_share.png")
    
    print("Generating monthly performance dashboard...")
    visualizer.plot_monthly_performance(save_path=f"{output_dir}/monthly_performance.png")
    
    print("Generating correlation matrix...")
    visualizer.plot_correlation_matrix(save_path=f"{output_dir}/correlation_matrix.png")
    
    print("Creating full dashboard...")
    visualizer.create_dashboard(save_path=f"{output_dir}/full_dashboard.png")
    
    print("\n[4/6] Generating summary report...")
    generate_summary_report(metrics, brand_stats, region_stats, output_dir)
    
    print("\n[5/6] Analysis complete!")
    print(f"Results saved to: {os.path.abspath(output_dir)}")
    print(f"Data files saved to: {os.path.abspath(data_dir)}")
    
    return df_with_features


def generate_summary_report(metrics, brand_stats, region_stats, output_dir):
    report = []
    report.append("=" * 60)
    report.append("CAR BRAND SALES ANALYSIS REPORT")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    report.append("")
    
    report.append("KEY METRICS")
    report.append("-" * 40)
    report.append(f"Total Revenue: ${metrics['total_revenue']:,.2f}")
    report.append(f"Total Quantity Sold: {metrics['total_quantity']:,}")
    report.append(f"Average Discount: {metrics['avg_discount']:.2%}")
    report.append(f"Average Price: ${metrics['avg_price']:,.2f}")
    report.append(f"Max Sale: ${metrics['max_sale']:,.2f}")
    report.append(f"Min Sale: ${metrics['min_sale']:,.2f}")
    report.append("")
    
    report.append("TOP 5 BRANDS BY PERFORMANCE")
    report.append("-" * 40)
    for idx, row in brand_stats.head(5).iterrows():
        report.append(f"{row['brand']}: Revenue=${row['revenue_sum']:,.2f}, "
                     f"Market Share={row['market_share']:.2f}%")
    report.append("")
    
    report.append("REGIONAL PERFORMANCE")
    report.append("-" * 40)
    for idx, row in region_stats.iterrows():
        report.append(f"{row['region']}: Revenue=${row['revenue_sum']:,.2f}")
    report.append("")
    
    report.append("=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)
    
    report_text = "\n".join(report)
    
    with open(f"{output_dir}/analysis_report.txt", 'w') as f:
        f.write(report_text)
    
    print(report_text)


if __name__ == "__main__":
    df = main()
