import pickle
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import numpy as np
from process import read_data_project, data_cleaning_area_columns
from features import label_encoder_codigo, label_encoder_unid, label_encoder_tipologia

def load_models():
    model1 = pickle.load(open('model/model1.sav', 'rb'))
    model2 = pickle.load(open('model/model2.sav', 'rb'))
    model3 = pickle.load(open('model/model3.sav', 'rb'))
    return model1, model2, model3

def read_data_to_predict():
    df_predict = read_data_project('datasets/raw/projeto_4.csv')
    df_predict = data_cleaning_area_columns(df_predict)
    return df_predict

def add_activity(df_predict):
    code_df = pd.read_csv('datasets/processed/codigo.csv',
                          index_col=0).reset_index(drop = True)
    
    code_df['Titulo'] = 'Projeto 4 - Je3'
    
    predict_df = code_df.merge(df_predict, how = 'left', on = 'Titulo')
    
    return predict_df

def label_encoder(df):
    df['codigo_le'] = label_encoder_codigo.transform(df['codigo'])
    df['unid_le'] = label_encoder_unid.transform(df['unid'])
    df['Tipologia_le'] = label_encoder_tipologia.transform(df['Tipologia'])
    return df



def main():
    df = read_data_to_predict()
    df = add_activity(df)
    df = label_encoder(df)
    
    model1, model2, model3 = load_models()
    
    X = df[['codigo_le',
        'unid_le',
        'Tipologia_le',
        'Área Terreno',
        'Área Construída',
        'Área Fundação',
        'Área Fachada',
        'Área Parede']]
    
    df['quantidade_pred'] = model1.predict(X)
    df['preco_material_unitario_pred'] = model2.predict(X)
    df['execucao_unitario_model'] = model3.predict(X)
    
    df.to_csv('datasets/predict/predict.csv')

   # return df 