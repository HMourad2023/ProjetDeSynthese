import pandas as pd
import numpy as np
import mlflow
from mlflow.tracking import MlflowClient
import math
import yaml

# Charger les paramètres depuis params.yaml
with open('params.yaml', 'r') as f:
    params = yaml.safe_load(f)

# Extraire les chemins et les configurations depuis params.yaml
model_path = params['data']['model']['path']
metrics_path = params['data']['metrics']['path']
mlflow_tracking_uri = params['mlflow']['tracking_uri']
model_name = params['mlflow']['model_name']

# Définir l'URI de suivi MLflow
mlflow.set_tracking_uri(mlflow_tracking_uri)

def get_model_uri_from_stage(model_name, stage="Production"):
    client = MlflowClient()
    # Obtenir la dernière version du modèle dans le stage spécifié
    model_versions = client.get_latest_versions(model_name, stages=[stage])
    if not model_versions:
        raise ValueError(f"No version of model '{model_name}' found in stage '{stage}'.")
    
    # Obtenir l'URI du modèle
    latest_version = model_versions[0].version
    model_uri = f"models:/{model_name}/{latest_version}"
    return model_uri

def convert_input_example_to_serving_input(input_example):
    # Convertir DataFrame en tableau NumPy
    if isinstance(input_example, pd.DataFrame):
        input_example = input_example.values
    
    # Retourner comme liste de listes (tableau 2D)
    return input_example.tolist()

def validate_serving_input(model_uri, serving_payload):
    # Charger le modèle
    model = mlflow.pyfunc.load_model(model_uri)
    
    # Faire une prédiction
    prediction = model.predict(serving_payload)
    
    # Afficher la prédiction
    prediction_original = np.exp(prediction)
    passengers = prediction_original[0][0]
    freight = prediction_original[0][1]
    mail = prediction_original[0][2]

    print(f"Le nombre de passagers prévu est : {math.floor(passengers)}")
    print(f"La quantité de Fret prévue : {math.floor(freight)}")
    print(f"La quantité de Courrier prévue est : {math.floor(mail)}")

# Exemple de données d'entrée
INPUT_EXAMPLE = {
    "DISTANCE": 7.723120,
    "REGION": 1,
    "CARRIER_NAME": 7,
    "CARRIER_GROUP_NEW": 2,
    "ORIGIN": 326,
    "ORIGIN_WAC": 48,
    "DEST": 412,
    "DEST_CITY_NAME": 351,
    "YEAR": 2,
    "MONTH": 6,
    "DISTANCE_GROUP": 4,
    "CLASS": 0
}

# Convertir l'exemple d'entrée en DataFrame
input_df = pd.DataFrame([INPUT_EXAMPLE])

# Obtenir l'URI du modèle
model_uri = get_model_uri_from_stage(model_name, stage="Production")
print(f"Model URI in production: {model_uri}")

# Convertir l'exemple d'entrée en format pour la prédiction
serving_payload = convert_input_example_to_serving_input(input_df)

# Valider le modèle avec l'exemple d'entrée
validate_serving_input(model_uri, serving_payload)
