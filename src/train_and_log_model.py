import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import yaml
import pandas as pd
import joblib  # Pour sauvegarder le modèle localement

def train_and_log_model(model_name, model, X_train_selected_path, X_test_selected_path, y_train_path, y_test_path, local_model_path, metrics_path):
    with mlflow.start_run(run_name=model_name):
        # Entraîner le modèle
        X_train_selected = pd.read_csv(X_train_selected_path)
        X_test_selected = pd.read_csv(X_test_selected_path)

        y_train = pd.read_csv(y_train_path)
        y_test = pd.read_csv(y_test_path)
        
        model.fit(X_train_selected, y_train)
        
        # Prédictions
        predictions = model.predict(X_test_selected)
        
        # Calculer l'erreur quadratique moyenne et R2
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)  # Calculer RMSE
        r2 = r2_score(y_test, predictions)
        
        # Loguer les paramètres et les résultats
        mlflow.log_params(model.get_params())
        mlflow.log_metric("mean_squared_error", mse)
        mlflow.log_metric("root_mean_squared_error", rmse)
        mlflow.log_metric("R2", r2)
        
        # Loguer le modèle avec MLflow
        mlflow.sklearn.log_model(model, model_name)
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
        
        # Sauvegarder le modèle localement pour DVC
        joblib.dump(model, local_model_path)
        
        # Sauvegarder les métriques dans un fichier
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        with open(metrics_path, 'w') as f:
            f.write(f"mean_squared_error: {mse}\n")
            f.write(f"root_mean_squared_error: {rmse}\n")
            f.write(f"R2: {r2}\n")
        
        return r2, rmse

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment('experience1')

    # Charger les paramètres depuis params.yaml
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)

    X_train_selected_path = params['data']['features']['X_train_selected']
    X_test_selected_path = params['data']['features']['X_test_selected']
    y_train_path = params['data']['splitted_data']['y_train']
    y_test_path = params['data']['splitted_data']['y_test']
    model_path = params['data']['model']['path']
    metrics_path = params['data']['metrics']['path']

    models = {
        'LinearRegression': LinearRegression(),
        'RandomForestRegressor': RandomForestRegressor(),
        'KNeighborsRegressor': KNeighborsRegressor(),
        'ExtraTreesRegressor': ExtraTreesRegressor()
    }

    best_model_name = None
    best_r2 = -np.inf
    best_rmse = np.inf

    for model_name, model in models.items():
        r2, rmse = train_and_log_model(model_name, model, X_train_selected_path, X_test_selected_path, y_train_path, y_test_path, model_path, metrics_path)   
        print(f"Modèle: {model_name}, R2: {r2:.4f}, RMSE: {rmse:.4f}")
        
        # Mettre à jour le meilleur modèle basé sur R2 et RMSE
        if r2 > best_r2 and rmse < best_rmse:
            best_r2 = r2
            best_rmse = rmse
            best_model_name = model_name

    if best_model_name:
        print(f"\nLe meilleur modèle est '{best_model_name}' avec R2 = {best_r2:.4f} et RMSE = {best_rmse:.4f}")

        # Enregistrer le meilleur modèle
        with mlflow.start_run(run_name="Best_Model_Production") as best_run:
            best_model = models[best_model_name]
            mlflow.sklearn.log_model(best_model, "best_model")
            mlflow.log_metric("R2", best_r2)
            mlflow.log_metric("root_mean_squared_error", best_rmse)
            
            # Sauvegarder le modèle localement
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(best_model, model_path)

            # Enregistrer le modèle dans le registre MLflow
            model_uri = f"runs:/{best_run.info.run_id}/best_model"
            mlflow.register_model(model_uri, "Best_Model")

            # Déplacer le modèle vers le stage de production
            client = MlflowClient()
            latest_version = client.get_latest_versions("Best_Model", stages=["None"])[0].version
            client.transition_model_version_stage(
                name="Best_Model",
                version=latest_version,
                stage="Production"
            )

        print(f"Le modèle '{best_model_name}' a été enregistré et mis en production.")
    else:
        print("Aucun modèle n'a été sélectionné.")
