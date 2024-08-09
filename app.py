import streamlit as st
import pandas as pd
from pipelines.prediction_pipeline import predict

# Interface utilisateur avec Streamlit
st.title('Application de Prédiction')

# Création d'un formulaire pour saisir les valeurs
with st.form(key='prediction_form'):
    distance = st.number_input('DISTANCE', value=0.0)
    region = st.text_input('REGION', '')
    carrier_name = st.text_input('CARRIER_NAME', '')
    carrier_group_new = st.text_input('CARRIER_GROUP_NEW', '')
    origin = st.text_input('ORIGIN', '')
    origin_city_name = st.text_input('ORIGIN_CITY_NAME', '')
    origin_wac = st.text_input('ORIGIN_WAC', '')
    dest = st.text_input('DEST', '')
    dest_city_name = st.text_input('DEST_CITY_NAME', '')
    year = st.number_input('YEAR', min_value=1900, max_value=2100, value=2024)
    month = st.number_input('MONTH', min_value=1, max_value=12, value=1)
    distance_group = st.text_input('DISTANCE_GROUP', '')
    class_ = st.text_input('CLASS', '')

    submit_button = st.form_submit_button(label='Faire une Prédiction')

if submit_button:
    # Créer un DataFrame avec les valeurs saisies
    data = {
        'DISTANCE': [distance],
        'REGION': [region],
        'CARRIER_NAME': [carrier_name],
        'CARRIER_GROUP_NEW': [carrier_group_new],
        'ORIGIN': [origin],
        'ORIGIN_CITY_NAME': [origin_city_name],
        'ORIGIN_WAC': [origin_wac],
        'DEST': [dest],
        'DEST_CITY_NAME': [dest_city_name],
        'YEAR': [year],
        'MONTH': [month],
        'DISTANCE_GROUP': [distance_group],
        'CLASS': [class_]
    }
    
    df = pd.DataFrame(data)
    
    # Faire des prédictions
    predictions = predict(df)
    
    # Afficher les prédictions
    st.write("Prédictions :")
    st.write(predictions)
