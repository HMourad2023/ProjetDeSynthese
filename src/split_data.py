import pandas as pd
from sklearn.model_selection import train_test_split
import os
import yaml

# Charger les paramètres depuis params.yaml
with open('params.yaml', 'r') as f:
    params = yaml.safe_load(f)

transformed_data_path = params['data']['transformed_data_path']
splitted_data_paths = params['data']['splitted_data']

# Créer le dossier splité si nécessaire
os.makedirs(os.path.dirname(splitted_data_paths['X_train']), exist_ok=True)

def split_data(transformed_data):
    X = transformed_data.drop(columns=["Log_PASSENGERS", "Log_FREIGHT", "Log_MAIL"])
    y = transformed_data[["Log_PASSENGERS", "Log_FREIGHT", "Log_MAIL"]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=params['processing']['split_data']['test_size'], random_state=42)
    return X_train, X_test, y_train, y_test

transformed_data = pd.read_csv(transformed_data_path)
X_train, X_test, y_train, y_test = split_data(transformed_data)

X_train.to_csv(splitted_data_paths['X_train'], index=False)
X_test.to_csv(splitted_data_paths['X_test'], index=False)
y_train.to_csv(splitted_data_paths['y_train'], index=False)
y_test.to_csv(splitted_data_paths['y_test'], index=False)

