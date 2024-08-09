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
mlflow_tracking_uri = params['mlflow']['tracking_uri']
model_name = params['mlflow']['model_name']

# Définir l'URI de suivi MLflow
mlflow.set_tracking_uri(mlflow_tracking_uri)

def get_best_model_uri_from_stage(model_name, stage="Production"):
    client = MlflowClient()
    
    # Obtenir toutes les versions du modèle
    latest_mv = client.get_latest_versions(model_name, stages=[stage])[0]
    client.set_registered_model_alias(model_name, alias, latest_mv.version)
    
    if not model_versions:
        raise ValueError(f"No version of model '{model_name}' found.")
    
    # Afficher les versions du modèle
    print(f"Versions trouvées pour le modèle '{model_name}':")
    for mv in model_versions:
        print(f"Version: {mv.version}, Stage: {mv.current_stage}")

    # Filtrer les versions pour obtenir celles dans le stage spécifié
    stage_versions = [mv for mv in model_versions if mv.current_stage == stage]
    
    if not stage_versions:
        raise ValueError(f"No version of model '{model_name}' found in stage '{stage}'.")
    
    # Trouver la version la plus récente
    best_version = max(stage_versions, key=lambda mv: int(mv.version))
    
    # Obtenir l'URI du modèle
    model_uri = f"models:/{model_name}/{best_version.version}"
    return model_uri


def convert_input_example_to_serving_input(input_example):
    if isinstance(input_example, pd.DataFrame):
        input_example = input_example.values
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

    return prediction_original
