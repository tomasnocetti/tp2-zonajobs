import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from normalize_data import getNormalizedDataset, getNormalizedDataset_2, normailize_df
from utils import target_encoding
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def pred_with_xgboost(df_train, df_test):
    
    df_train = normailize_df(df_train, True)
    df_test = normailize_df(df_test, False)
    cat_features = ['tipodepropiedad', 'provincia', 'ciudad']
        
    df_train.drop('precio_mt2', axis=1, inplace=True)
    df_train_enc, target_enc = target_encoding(df_train,'train')
    
    #Data de train y test
    X_test, target_enc = target_encoding(df_test, 'test', target_enc)
    X_train = df_train_enc
    y_train = df_train['precio']
    
    xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.8, learning_rate = 0.1, max_depth = 10, reg_alpha = 1.2, n_estimators = 500, reg_lambda = 1.4, subsample=0.8)
    xg_reg.fit(X_train,y_train)
    preds = xg_reg.predict(X_test)

    return preds


def pred_with_rf(df, df_test):
    
    #Obtener df normalizado y con feature engineering aplicado
    df_norm = normailize_df(df, True)
    df_test_norm = normailize_df(df, False)
    
    df_train, target_enc = target_encoding(df_norm,'train')
    
    #Data de train y test
    X_train = df_train
    y_train = df_norm['precio']
    X_test, target_enc = target_encoding(df_test_norm, 'test', target_enc)

    #Uso los hiperparametros que obtuve como resultado del random search
    #rf = RandomForestRegressor(n_estimators=743, min_samples_split=5, min_samples_leaf=2,\
    #                       max_features='sqrt', max_depth=60, bootstrap= False)
    
    rf = RandomForestRegressor(n_estimators=929, min_samples_split=2, min_samples_leaf=2,\
                           max_features='auto', max_depth=80, bootstrap= True)
    
    # Otros parametros realmente buenos para probar como resultado de la random search
    #{'n_estimators': 929,
    # 'min_samples_split': 2,
    # 'min_samples_leaf': 2,
    # 'max_features': 'auto',
    # 'max_depth': 80,
    # 'bootstrap': True}
    
    rf.fit(X_train,y_train)
    
    # Todos aquellos que sean de una categoria que yo no tenia en el set de datos, lo mando a la mas comun. #TODO
    X_test.ciudad.fillna(X_test.ciudad.value_counts().idxmax(), inplace=True)
    X_test.ciudad.fillna(X_test.provincia.value_counts().idxmax(), inplace=True)
    X_test.ciudad.fillna(X_test.tipodepropiedad.value_counts().idxmax(), inplace=True)

    pred = rf.predict(X_test)
    
    return pred






# Funciones para ensamblar y predecir en base a lo predecido (stacking)


def pred_with_xgboost_ensamb(df_train, df_test):
    
    df_train = normailize_df(df_train, True)
    df_test = normailize_df(df_test, False)
    cat_features = ['tipodepropiedad', 'provincia', 'ciudad']
        
    df_train.drop('precio_mt2', axis=1, inplace=True)
    df_train_enc, target_enc = target_encoding(df_train,'train')
    
    #Data de train y test
    X_test, target_enc = target_encoding(df_test, 'test', target_enc)
    X_train = df_train_enc
    y_train = df_train['precio']
    
    xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.8, learning_rate = 0.1, max_depth = 10, reg_alpha = 1.2, n_estimators = 500, reg_lambda = 1.4, subsample=0.8)
    xg_reg.fit(X_train,y_train)
    preds = xg_reg.predict(X_test)

    return preds, xg_reg, target_enc


def pred_with_rf_ensamb(df, df_test):
    
    #Obtener df normalizado y con feature engineering aplicado
    df_norm = getNormalizedDataset(df)
    df_test_norm = getNormalizedDataset(df_test, 'test')
    
    df_train, target_enc = target_encoding(df_norm,'train')
    
    #Data de train y test
    X_train = df_train
    y_train = df_norm['precio']
    X_test, target_enc = target_encoding(df_test_norm, 'test', target_enc)

    #Uso los hiperparametros que obtuve como resultado del random search
    rf = RandomForestRegressor(n_estimators=743, min_samples_split=5, min_samples_leaf=2,\
                           max_features='sqrt', max_depth=60, bootstrap= False)
    rf.fit(X_train,y_train)
    
    # Todos aquellos que sean de una categoria que yo no tenia en el set de datos, lo mando a la mas comun. #TODO
    X_test.ciudad.fillna(X_test.ciudad.value_counts().idxmax(), inplace=True)
    X_test.ciudad.fillna(X_test.provincia.value_counts().idxmax(), inplace=True)
    X_test.ciudad.fillna(X_test.tipodepropiedad.value_counts().idxmax(), inplace=True)

    X_test.fillna(0, inplace=True)
    
    pred = rf.predict(X_test)
    
    return pred, rf, target_enc



def pred_with_rf_ensamb_2(df, df_test):
    
    #Obtener df normalizado y con feature engineering aplicado
    df_norm = getNormalizedDataset_2(df)
    df_test_norm = getNormalizedDataset_2(df_test, 'test')
    
    df_train, target_enc = target_encoding(df_norm,'train')
    
    #Data de train y test
    X_train = df_train
    y_train = df_norm['precio']
    X_test, target_enc = target_encoding(df_test_norm, 'test', target_enc)

    #Uso los hiperparametros que obtuve como resultado del random search
    rf = RandomForestRegressor(n_estimators=929, min_samples_split=2, min_samples_leaf=2,\
                           max_features='auto', max_depth=80, bootstrap= True)
    rf.fit(X_train,y_train)
    
    # Todos aquellos que sean de una categoria que yo no tenia en el set de datos, lo mando a la mas comun. #TODO
    X_test.ciudad.fillna(X_test.ciudad.value_counts().idxmax(), inplace=True)
    X_test.ciudad.fillna(X_test.provincia.value_counts().idxmax(), inplace=True)
    X_test.ciudad.fillna(X_test.tipodepropiedad.value_counts().idxmax(), inplace=True)

    X_test.fillna(0, inplace=True)
    
    pred = rf.predict(X_test)
    
    return pred, rf, target_enc



def pred_with_xgboost_ensamb_2(df_train, df_test):
    
    df_train = getNormalizedDataset_2(df_train, True)
    df_test = getNormalizedDataset_2(df_test, False)

    df_train_enc, target_enc = target_encoding(df_train,'train')
    
    #Data de train y test
    X_test, target_enc = target_encoding(df_test, 'test', target_enc)
    X_train = df_train_enc
    y_train = df_train['precio']
    
    xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.8, learning_rate = 0.1, max_depth = 10, reg_alpha = 1.2, n_estimators = 500, reg_lambda = 1.4, subsample=0.8)
    xg_reg.fit(X_train,y_train)
    preds = xg_reg.predict(X_test)

    return preds, xg_reg, target_enc