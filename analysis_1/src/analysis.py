import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import xgboost as xgb

def prepare_features(df):
    features = df[['store_id', 'product', 'region', 'area', 'employees', 'month']]
    target = df['sales']
    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)
    
    model = xgb.XGBRegressor(n_estimators=100, max_depth=3) 
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"MAE: {mae}") 
    
    return model
