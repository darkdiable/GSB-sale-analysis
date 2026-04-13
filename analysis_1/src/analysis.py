import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

def prepare_features(df):
    df_encoded = df.copy()
    le_product = LabelEncoder()
    le_region = LabelEncoder()
    df_encoded['product_encoded'] = le_product.fit_transform(df_encoded['product'])
    df_encoded['region_encoded'] = le_region.fit_transform(df_encoded['region'])
    
    features = df_encoded[['store_id', 'product_encoded', 'region_encoded', 'area', 'employees', 'month']]
    target = df_encoded['sales']
    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)
    
    model = xgb.XGBRegressor(n_estimators=100, max_depth=3) 
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"MAE: {mae}") 
    
    return model
