import pandas as pd
import numpy as np
import os
import yaml
from sklearn.preprocessing import LabelEncoder

# Charger les paramètres depuis params.yaml
with open('params.yaml', 'r') as f:
    params = yaml.safe_load(f)

prepared_data_path = params['data']['prepared_data_path']
transformed_data_path = params['data']['transformed_data_path']

# Créer le dossier transformé si nécessaire
os.makedirs(os.path.dirname(transformed_data_path), exist_ok=True)

def transform_data(prepared_data):
    label_encoder = LabelEncoder()
    cat_data = prepared_data.select_dtypes(include='object')
    num_data = prepared_data.select_dtypes(exclude='object')
    
    # Transformation logarithmique
    num_data['Log_PASSENGERS'] = np.log1p(num_data['PASSENGERS'])
    num_data['Log_FREIGHT'] = np.log1p(num_data['FREIGHT'])
    num_data['Log_MAIL'] = np.log1p(num_data['MAIL'])
    num_data['Log_DISTANCE'] = np.log1p(num_data['DISTANCE'])
    num_data.drop(columns=['PASSENGERS', 'FREIGHT', 'MAIL', 'DISTANCE'], inplace=True)
    
    # Encodage des variables catégorielles
    for column in cat_data.columns:
        cat_data[column] = label_encoder.fit_transform(cat_data[column])
    
    data = pd.concat([num_data, cat_data], axis=1)
    return data

prepared_data = pd.read_csv(prepared_data_path)
transformed_data = transform_data(prepared_data)
transformed_data.to_csv(transformed_data_path, index=False)

