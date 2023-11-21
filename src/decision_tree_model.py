import numpy as np
import pandas as pd
import features
import pickle

from sklearn.tree import DecisionTreeRegressor

# treinando modelo usando a variável resposta quantidade

def exec_model1(df):

    y = df[['quantidade']]

    regressor = DecisionTreeRegressor()

    model = regressor.fit(X, y)
    
    filename = 'model/model1.sav'
    pickle.dump(model, open(filename, 'wb'))
    
    return model

def exec_model2(df):

    y = df[['preco_material_unitario']]

    regressor = DecisionTreeRegressor()

    model = regressor.fit(X, y)
    
    filename = 'model/model2.sav'
    pickle.dump(model, open(filename, 'wb'))
    
    return model

def exec_model3(df):

    y = df[['preco_execucao_unitario']]

    regressor = DecisionTreeRegressor()

    model = regressor.fit(X, y)
    
    filename = 'model/model3.sav'
    pickle.dump(model, open(filename, 'wb'))
    
    return model

def main():

    df = pd.read_csv('datasets/processed/features.csv',index_col=0).reset_index(drop = True)

    X = df[['codigo_le',
            'unid_le',
            'Tipologia_le',
            'Área Terreno',
            'Área Construída',
            'Área Fundação',
            'Área Fachada',
            'Área Parede']]

    model1 = exec_model1(df)
    model2 = exec_model2(df)
    model3 = exec_model3(df)