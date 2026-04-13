from src.data_processing import load_data, clean_data
from src.analysis import prepare_features
from src.visualization import plot_sales_trend, plot_feature_importance

def main():
    df_sales, df_store = load_data()
    df_clean = clean_data(df_sales, df_store)
    model = prepare_features(df_clean)

    plot_sales_trend(df_clean)
    plot_feature_importance(model)

if __name__ == "__main__":
    main()
