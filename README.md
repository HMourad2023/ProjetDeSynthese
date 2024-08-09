# <span style="color:red">Plan de la présentation</span>

- Introduction au projet.
- Proposition de valeur (Proof Of Concept).
- Collection des données
- Conception de la solution IA
- Création de l’environnement 
- Création de la structure du projet avec Cookiecutter
- Création d’un dépôt Github 
- Analyse Exploratoire de données
- Extraction de données.
- Versionnement des données avec DVC.
- Préparation et transformation de données.
- Sélection des caractéristiques 
- Entraînement du modèle (Utilisation de MLflow).
- Création des pipelines
- Déploiement sur Streamlit.
- Surveillance du modèle avec EvidentlyAI.
- Difficultés | À effectuer.
- Conclusion 

# <span style="color:red">Introduction au Projet</span>

Dans ce projet, nous allons automatiser l'ensemble du cycle de vie d’un projet en apprentissage automatique en utilisant les outils MLOps.
L’ensemble de données utilisé est disponible sur le site officiel du ministère des Transports américain.
Le déploiement se fera à l'aide du cloud de la communauté Streamlit et de Github Actions.

Le suivi du modèle de production se fera à l'aide de l’outil EvidentlyAI.
Les outils utilisés tout au long du projet sont open source.

La solution conçue prédit le nombre de passagers, la quantité de fret et du courrier entre les aéroports américains et canadiens au profit des compagnies aériennes américaines.

# <span style="color:red">Stack Technologique</span>

- **Cookiecutter** : structure du projet.
- **Contrôle de version des données (DVC)** : contrôle de version des données et création de pipeline.
- **Github** : pour le contrôle de version du code.
- **Actions GitHub** : pour créer le pipeline CI-CD.
- **MLFlow** : pour le registre de modèles.
- **Streamlit** : pour créer une application Web.
- **EvidentlyAI** : pour évaluer et surveiller les modèles ML en production.
- **Pytest** : pour implémenter les tests unitaires.

# <span style="color:red">Approche Technologique</span>

## <span style="color:red">La Régression Multi-Outputs</span>

En apprentissage automatique, nous rencontrons souvent des régressions, ces problèmes impliquent la prédiction d'une variable cible continue.
Cependant, dans de nombreux scénarios du monde réel, nous devons prédire non seulement une seule mais plusieurs variables ensemble, c'est là que nous utilisons la régression à sorties multiples (Régression Multi-outputs).

La régression multi-outputs utilisant Scikit-learn peut être réalisée de trois manières :

# <span style="color:red">Conception de la solution IA</span>

## <span style="color:red">Création de la structure du projet avec Cookiecutter</span>
