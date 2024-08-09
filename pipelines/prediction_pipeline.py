import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import LabelEncoder
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

def predict(df):
    label_encoder = LabelEncoder()

    # Séparer les données catégorielles et numériques
    cat_data = df.select_dtypes(include='object')
    num_data = df.select_dtypes(exclude='object')

    # Transformation des données numériques
    num_data['Log_DISTANCE'] = np.log1p(num_data['DISTANCE'])
    num_data.drop(columns=['DISTANCE'], inplace=True)

    # Encodage des variables catégorielles
    for column in cat_data.columns:
        cat_data[column] = label_encoder.fit_transform(cat_data[column])
    
    # Fusionner les données transformées
    transformed_data = pd.concat([num_data, cat_data], axis=1)

    # Charger les noms des colonnes depuis un fichier ou les définir manuellement
    column_names = ['Log_DISTANCE', 'REGION', 'CARRIER_NAME', 'CARRIER_GROUP_NEW', 'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_WAC', 'DEST', 'DEST_CITY_NAME', 'YEAR', 'MONTH', 'DISTANCE_GROUP', 'CLASS']

    # Réorganiser les colonnes pour correspondre à celles utilisées lors de l'entraînement
    transformed_data = transformed_data.reindex(columns=column_names, fill_value=0)

    # Chargez le modèle depuis MLflow
    logged_model = 'runs:/ce7b5b0eb77a4c5a908b2a6620eb04e5/best_model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # Faire des prédictions
    prediction = loaded_model.predict(transformed_data)
    
    # Afficher les résultats de la prédiction
    prediction_original = np.exp(prediction)
    passengers = prediction_original[0][0]
    freight = prediction_original[0][1]
    mail = prediction_original[0][2]

    print(f"Le nombre de passagers prévu est : {math.floor(passengers)}")
    print(f"La quantité de Fret prévue : {math.floor(freight)}")
    print(f"La quantité de Courrier prévue est : {math.floor(mail)}")
    import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import LabelEncoder
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

def predict(df):
    label_encoder = LabelEncoder()

    # Séparer les données catégorielles et numériques
    cat_data = df.select_dtypes(include='object')
    num_data = df.select_dtypes(exclude='object')

    # Transformation des données numériques
    num_data['Log_DISTANCE'] = np.log1p(num_data['DISTANCE'])
    num_data.drop(columns=['DISTANCE'], inplace=True)

    # Encodage des variables catégorielles
    for column in cat_data.columns:
        cat_data[column] = label_encoder.fit_transform(cat_data[column])
    
    # Fusionner les données transformées
    transformed_data = pd.concat([num_data, cat_data], axis=1)

    # Charger les noms des colonnes depuis un fichier ou les définir manuellement
    column_names = ['Log_DISTANCE', 'REGION', 'CARRIER_NAME', 'CARRIER_GROUP_NEW', 'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_WAC', 'DEST', 'DEST_CITY_NAME', 'YEAR', 'MONTH', 'DISTANCE_GROUP', 'CLASS']

    # Réorganiser les colonnes pour correspondre à celles utilisées lors de l'entraînement
    transformed_data = transformed_data.reindex(columns=column_names, fill_value=0)

    # Chargez le modèle depuis MLflow
    logged_model = 'runs:/ce7b5b0eb77a4c5a908b2a6620eb04e5/best_model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # Faire des prédictions
    prediction = loaded_model.predict(transformed_data)
    
    # Afficher les résultats de la prédiction
    prediction_original = np.exp(prediction)
    passengers = prediction_original[0][0]
    freight = prediction_original[0][1]
    mail = prediction_original[0][2]

    print(f"Le nombre de passagers prévu est : {math.floor(passengers)}")
    print(f"La quantité de Fret prévue : {math.floor(freight)}")
    print(f"La quantité de Courrier prévue est : {math.floor(mail)}")

    return passengers, freight, mail


    
