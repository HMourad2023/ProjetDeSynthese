from src.transform_data import transform_data
from src.validate_model import get_model_uri_from_stage, convert_input_example_to_serving_input, validate_serving_input
import math
import numpy as np  # Ajout de l'importation pour numpy

def predict(df):
    # Transformer les données
    df_transformed = transform_data(df)

    model_uri = get_model_uri_from_stage()

    serving_payload = convert_input_example_to_serving_input(df)
    model = validate_serving_input(model_uri, serving_payload)
    prediction = model.predict(serving_payload)

    # Afficher la prédiction
    prediction_original = np.exp(prediction)
    passengers = prediction_original[0][0]
    freight = prediction_original[0][1]
    mail = prediction_original[0][2]

    print(f"Le nombre de passagers prévu est : {math.floor(passengers)}")
    print(f"La quantité de Fret prévue : {math.floor(freight)}")
    print(f"La quantité de Courrier prévue est : {math.floor(mail)}")

    # Faire des prédictions
    predictions = model.predict(df_transformed)
    
    return predictions
