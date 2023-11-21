import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from process import data_cleaning_area, data_cleaning_quant

label_encoder_codigo = LabelEncoder()
label_encoder_unid = LabelEncoder()
label_encoder_tipologia = LabelEncoder()

def read_processed_data():
    df = pd.read_csv('datasets/processed/processed.csv',index_col=0).reset_index(drop = True)
    project_review_df = pd.read_csv('datasets/processed/project_review.csv', index_col=0).reset_index(drop = True)

    df = df.merge(project_review_df, how = 'left', on = 'Titulo')
    df['quantidade'] = df['quantidade'].apply(data_cleaning_quant)

    df = df.groupby(['codigo','unid','Titulo','Tipologia']).sum().reset_index()
    
    return df

def apply_label_encoder(df):
    df['codigo_le'] = label_encoder_codigo.fit_transform(df['codigo'])
    df['unid_le'] = label_encoder_unid.fit_transform(df['unid'])
    df['Tipologia_le'] = label_encoder_tipologia.fit_transform(df['Tipologia'])
    
    return df 

def data_prep(df, projeto):
    # nem todos os projetos passaram pelo mesmas etapas
    # insere as etapas que o projeto não participou e preenche com zero
    code_df = df[['codigo','unid']].drop_duplicates().reset_index(drop = True)
    print('saving codigo.csv ')
    code_df.to_csv('datasets/processed/codigo.csv')
    
    project_name = projeto['Titulo'].unique()[0]
    tipologia_name = projeto['Tipologia'].unique()[0]
    
    projeto_dc = code_df.merge(projeto, how = 'left', on = ['codigo','unid'])
    projeto_dc['Titulo'] = projeto_dc['Titulo'].fillna(project_name)
    projeto_dc['Tipologia'] = projeto_dc['Tipologia'].fillna(tipologia_name)
    projeto_dc = projeto_dc.fillna(0)
    
    return projeto_dc

def insert_values(df):
    projeto2 = df[df['Titulo'] == 'Projeto 2 - Ca']
    projeto1 = df[df['Titulo'] == 'Projeto 1 - Wa']
    projeto3 = df[df['Titulo'] == 'Projeto 3 - Je2']
    
    a = data_prep(df, projeto1)
    b = data_prep(df, projeto2)
    c = data_prep(df, projeto3)

    final_df = pd.concat([a,b,c])
    return final_df

def main():
    df = read_processed_data()
    df = apply_label_encoder(df)
    df = insert_values(df)
    df.to_csv('datasets/processed/features.csv')