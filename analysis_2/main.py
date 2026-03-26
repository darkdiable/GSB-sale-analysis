import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_processor import DataProcessor
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator


def check_data_file(data_path):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"数据文件不存在：{data_path}")
    print(f"数据文件检查通过：{data_path}")

def main():
    print("=" * 60)
    print("销售数据分析与可视化系统")
    print("=" * 60)
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    data_path = 'data/sales_data.xlsx'
    output_dir = 'output'

    check_data_file(data_path)

    print("\n[1/4] 加载和处理数据...")
    processor = DataProcessor(data_path)
    processor.load_data()
    processor.clean_data()

    print("\n[2/4] 生成可视化图表...")
    visualizer = Visualizer(output_dir)
    visualizer.create_all_charts(processor)

    print("\n[3/4] 生成分析报告...")
    report_generator = ReportGenerator(processor, output_dir)
    report = report_generator.generate_full_report()

    print("\n[4/4] 导出 Excel 报告...")
    report_generator.export_to_excel()

    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)
    print(f"\n输出目录：{os.path.abspath(output_dir)}")
    print("\n生成的文件:")
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} 字节)")

    print("\n程序执行完毕！")


if __name__ == '__main__':
    main()
