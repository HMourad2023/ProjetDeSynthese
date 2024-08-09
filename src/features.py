import pandas as pd
import yaml
import os

# Charger les paramètres depuis params.yaml
with open('params.yaml', 'r') as file:
    params = yaml.safe_load(file)

# Extraire les chemins des fichiers depuis les paramètres
features_path = params['data']['features']['file_path']
features_data_path = params['data']['features']
X_train_data_path = params["data"]["splitted_data"]["X_train"]
X_test_data_path = params["data"]["splitted_data"]["X_test"]

os.makedirs(os.path.dirname(features_data_path['X_train_selected']), exist_ok=True)

# Lire les noms de features depuis le fichier features.txt
with open(features_path, 'r') as file:
    features = [line.strip() for line in file if line.strip()]

# Lire les fichiers CSV d'origine
try:
    df_train = pd.read_csv(X_train_data_path)
    df_test = pd.read_csv(X_test_data_path)
except FileNotFoundError as e:
    print(f"Erreur: {e}")
    exit(1)

# Sélectionner les colonnes spécifiées dans features.txt
df_train_selected = df_train[features]
df_test_selected = df_test[features]

# Enregistrer les fichiers CSV avec les colonnes sélectionnées
df_train_selected.to_csv(features_data_path['X_train_selected'], index=False)
df_test_selected.to_csv(features_data_path['X_test_selected'], index=False)


