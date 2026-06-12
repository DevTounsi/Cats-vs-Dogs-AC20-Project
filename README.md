---
title: AC20 Cats VS Dogs
emoji: 🐱🐶
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# Classification d'Images (Chien vs Chat) avec CNN - Projet AC20 UTBM

[![Hugging Face Spaces](https://img.shields.github.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/AbTounsi/AC20_Cats-VS-Dogs)
**Démo interactive en ligne :** [abtounsi-ac20-cats-vs-dogs.hf.space](https://abtounsi-ac20-cats-vs-dogs.hf.space)

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
├── scripts/                # Scripts python
├── README.md               # Description du projet
└── environnment.yml        # Liste des dépendances Python
```

## Installation et Reproductibilité

Ce projet utilise [Conda](https://docs.conda.io/en/latest/) pour garantir une gestion stricte des dépendances (Data Science / Deep Learning). L'environnement a été configuré pour des machines fonctionnant sous Windows (incluant les pilotes CUDA pour l'accélération GPU).

### 1. Cloner le dépôt
Ouvrez votre terminal et clonez ce projet en local :
```bash
git clone https://github.com/DevTounsi/Cats-vs-Dogs-AC20-Project.git
cd Cats-vs-Dogs-AC20-Project
```
### 2. Créer l'environnement virtuel
À la racine du projet, exécutez la commande suivante pour recréer l'environnement à partir du fichier de configuration :

```bash
conda env create -f environment.yml
```

### 3. Activer l'environnement
Une fois l'installation terminée, activez l'environnement :

```bash
conda activate ac20
```

### 4. Lancer le projet
Vous pouvez désormais démarrer l'interface de développement (Jupyter Lab est inclus dans l'environnement) :

```bash
jupyter lab
```

Le code est maintenant documenté de manière professionnelle. Puisqu'il s'agit d'un projet


##  Auteur
**Abd-Allah AMINI** - Étudiant à l'UTBM (TC04)
---
*Projet réalisé dans le cadre du cursus Ingénieur à l'UTBM.*