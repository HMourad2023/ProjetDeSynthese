import pandas as pd
import yaml

# Charger les paramètres depuis params.yaml
with open('params.yaml', 'r') as file:
    params = yaml.safe_load(file)

# Extraire les chemins des fichiers depuis les paramètres
features_file = params['data']['features']['file_path']
train_file = params['data']['splitted_data']['X_train']
test_file = params['data']['splitted_data']['X_test']
train_selected_file = params['data']['features']['X_train_selected']
test_selected_file = params['data']['features']['X_test_selected']

# Lire les noms de features depuis le fichier features.txt
with open(features_file, 'r') as file:
    features = [line.strip() for line in file if line.strip()]

# Lire les fichiers CSV d'origine
try:
    df_train = pd.read_csv(train_file)
    df_test = pd.read_csv(test_file)
except FileNotFoundError as e:
    print(f"Erreur: {e}")
    exit(1)

# Sélectionner les colonnes spécifiées dans features.txt
df_train_selected = df_train[features]
df_test_selected = df_test[features]

# Enregistrer les fichiers CSV avec les colonnes sélectionnées
df_train_selected.to_csv(train_selected_file, index=False)
df_test_selected.to_csv(test_selected_file, index=False)

print(f"Fichiers créés: {train_selected_file}, {test_selected_file}")


