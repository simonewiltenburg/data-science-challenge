import pandas as pd
import numpy as np

projeto1 = 'datasets/raw/amostra_projeto1.csv'
projeto2 = 'datasets/raw/amostra_projeto_2.csv'
projeto3 = 'datasets/raw/amostra_projeto_3.csv'
projeto4 = 'datasets/raw/projeto_4.csv'

def read_data_project(project_name):
    '''
    lê as primeiras nove linhas do csv para pegar os dados sobre o projeto
    '''
    
    dfdados = pd.read_csv(project_name)#[1:9]
    columns = dfdados.iloc[:8,0].to_list()
    row = dfdados.iloc[:8,1].to_list()
    
    new_df = pd.DataFrame(row).T
    new_df.columns = columns
    
    return new_df

def read_dataset(project_name):
    '''
    Cria o df de orçamento do projeto
    '''
    df_orcamento_columns = ['item',
  'referencia',
  'tipo',
  'codigo',
  'descricao',
  'unid',
  'quantidade',
  'bdi',
  'preco_material_unitario',
  'preco_material_total',
  'preco_execucao_unitario',
  'preco_execucao_total',
  'preco_unitario',
  'preço_total']

    df_orcamento = pd.read_csv(project_name)[12:].reset_index(drop = True)
    df_orcamento.columns = df_orcamento_columns
    
    return df_orcamento

def read_data_sep(project_name):
    df_data_project = read_data_project(project_name)
    df_orcamento = read_dataset(project_name)
    df_orcamento['Titulo'] = str(df_data_project['Titulo'][0])
    return df_data_project, df_orcamento

def to_int(number):
    try:
        int_value = int(str(number))
    except:
        int_value = 0
    return int_value

def real_prefix_tofloat(txt):
    try: 
        text = txt.split('R$ ')
        text = text[1].replace('.','')
        text = text.replace(',','.')
        float_number = float(text)
    except:
        float_number = 0
    
    return float_number

def split_item_columns(df_orcamento):
    '''
    Divide a coluna item em 3 colunas separadas
    '''
    
    cols_to_int = ['primeiro', 'segundo','terceiro']
    
    df_orcamento[cols_to_int] = df_orcamento['item'].str.split('.', expand=True)
    

    for count in range(len(cols_to_int)):
        col = cols_to_int[count]
        df_orcamento[col] = df_orcamento[col].apply(to_int)
        
    return df_orcamento

def data_cleaning_area(area_value):
    '''
    Replace "," to "."
    '''
    try: 
        area_value = area_value.replace(',','.')
        area_value = float(area_value)
    except:
        area_value
    return area_value

def data_cleaning_area_columns(dfdados):
    area_columns = ['Área Terreno', 'Área Construída','Área Fundação', 'Área Fachada', 'Área Parede', 'Qtde BWCs']
    
    for count in range(len(area_columns)):
        column = area_columns[count]
        dfdados[column] = dfdados[column].apply(data_cleaning_area)
        
    return dfdados
    
    
def data_cleaning_price_columns(df_orcamento1):
    price_columns = ['preco_material_unitario',
          'preco_material_total',
          'preco_execucao_unitario',
          'preco_execucao_total',
          'preco_unitario',
          'preço_total']
    
    for count in range(len(price_columns)):
        col = price_columns[count]
        df_orcamento1[col] = df_orcamento1[col].apply(real_prefix_tofloat)
    
    return df_orcamento1

def process(project_name):
    
    dfdados, df_orcamento = read_data_sep(project_name)
    dfdados = data_cleaning_area_columns(dfdados)
    df_orcamento1 = split_item_columns(df_orcamento)
    df_orcamento1 = data_cleaning_price_columns(df_orcamento)
    
    return dfdados, df_orcamento

def data_cleaning_quant(object_value):
    object_value = data_cleaning_area(object_value)
    float_value = float(object_value)
        
    return float_value

def main(projeto1,projeto2,projeto3):

    dfdados3, df_orcamento3 = process(projeto3)
    dfdados2, df_orcamento2 = process(projeto2)
    dfdados1, df_orcamento1 = process(projeto1)
    
    df_orcamento_total = pd.concat([df_orcamento3, df_orcamento2, df_orcamento1])
    final_df = df_orcamento_total[df_orcamento_total['terceiro'] > 0]
    final_df.to_csv('datasets/processed/processed.csv')
    
    df_projetos_review = pd.concat([dfdados1, dfdados2, dfdados3])
    df_projetos_review.to_csv('datasets/processed/project_review.csv')