import pandas as pd
import os
import yaml

# Charger les paramètres depuis params.yaml
with open('params.yaml', 'r') as f:
    params = yaml.safe_load(f)

external_data_path = params['data']['external_data_path']
prepared_data_path = params['data']['prepared_data_path']

# Créer le dossier préparé si nécessaire
os.makedirs(os.path.dirname(prepared_data_path), exist_ok=True)

def prepare_data(data):
    data.columns = data.columns.str.replace(' ', '', regex=False)
    colonnes_avec_ID = [col for col in data.columns if 'ID' in col]
    data.drop(columns=colonnes_avec_ID, axis=1, inplace=True)
    
    # Conversion des colonnes catégorielles en objets
    cat_columns = ['CARRIER_GROUP', 'CARRIER_GROUP_NEW', 'ORIGIN_WAC', 'DEST_WAC', 'YEAR', 'QUARTER', 'MONTH', 'DISTANCE_GROUP']
    data[cat_columns] = data[cat_columns].astype(object)
    
    # Suppression des lignes avec PASSENGERS, FREIGHT, et MAIL tous égaux à 0
    lignes_zero_valeurs = data[(data['PASSENGERS'] == 0) & (data['FREIGHT'] == 0) & (data['MAIL'] == 0)].index
    data.drop(lignes_zero_valeurs, inplace=True)
    
    # Suppression des valeurs manquantes
    data.dropna(inplace=True)
    
    return data

data = pd.read_csv(external_data_path)
prepared_data = prepare_data(data)
prepared_data.to_csv(prepared_data_path, index=False)

