import pandas as pd
import os
import yaml

# Charger les paramètres depuis params.yaml
with open('params.yaml', 'r') as f:
    params = yaml.safe_load(f)

data_path = params['data']['source_path']
external_data_path = params['data']['external_data_path']

# Créer le dossier externe si nécessaire
os.makedirs(os.path.dirname(external_data_path), exist_ok=True)

def load_data(data_path):
    data = pd.read_csv(data_path,index_col=0)
    return data

data = load_data(data_path)
data.to_csv(external_data_path, index=False)

