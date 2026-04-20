# Classification d'Images (Chien vs Chat) avec CNN - Projet AC20 UTBM

##  Description du Projet
Ce dépôt contient le code source et les expériences liés à mon projet de l'Unité d'Enseignement **AC20** à l'**Université de Technologie de Belfort-Montbéliard (UTBM)**.

L'objectif de ce projet est d'étudier, d'implémenter et d'optimiser des **Réseaux de Neurones Convolutifs (CNN)** pour résoudre un problème de classification d'images binaire : distinguer des images de chiens et de chats (dataset Kaggle). L'ensemble des implémentations est réalisé avec le framework **PyTorch**.

##  Objectifs Pédagogiques et Techniques
- **Fondations :** Comprendre et implémenter une architecture CNN "From Scratch".
- **Pipeline de Données :** Mettre en place un pipeline complet de traitement d'images avec PyTorch (Datasets, DataLoaders, Transforms).
- **Analyse et Optimisation :** Analyser les courbes d'apprentissage, identifier le sur-apprentissage (Overfitting) et appliquer des techniques de régularisation (Data Augmentation, Dropout).
- **Transfer Learning :** Découvrir et évaluer l'apport de modèles pré-entraînés (état de l'art) sur ImageNet par rapport à une architecture artisanale.

##  Technologies Utilisées
- **Langage :** Python
- **Framework Deep Learning :** PyTorch & Torchvision
- **Traitement de Données :** NumPy, PIL
- **Visualisation :** Matplotlib, Seaborn

##  Structure du Projet (Prévisionnelle)
```text
├── data/                   # Dossier contenant le dataset (Kaggle Dogs vs Cats)
├── notebooks/              # Jupyter Notebooks pour l'exploration (EDA) et les expérimentations
├── models/                 # Poids des modèles sauvegardés (.pth)
├── results/                # Courbes d'apprentissage, matrices de confusion, visualisations
├── README.md               # Description du projet (ce fichier)
└── requirements.txt        # Liste des dépendances Python (à venir)
```

##  Auteur
**Abd-Allah AMINI** - Étudiant à l'UTBM (TC04)
---
*Projet réalisé dans le cadre du cursus Ingénieur à l'UTBM.*