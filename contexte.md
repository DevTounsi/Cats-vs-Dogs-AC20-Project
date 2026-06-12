# Contexte du Projet AC20 / TZ20 - UTBM

## Informations Générales
- **Étudiant :** Abd-Allah AMINI
- **Enseignant Responsable :** Abdeljalil ABBAS-TURKI (abdeljalil.abbas-turki@utbm.fr)
- **Cadre :** Unité de Valeur AC20 (souvent couplée/assimilée aux exigences TZ20 pour la charge de travail), catégorie Connaissances Scientifiques (CS).
- **Charge de travail estimée :** 150 heures (dont 136h de travail personnel et 14h d'encadrement).

## Sujet du Projet
**Titre :** Étude et Implémentation de Réseaux de Neurones Convolutifs (CNN)
**Problématique :** Comment construire, entraîner et optimiser un réseau de neurones convolutif (CNN) à partir de zéro, et quel est l'apport réel du Transfer Learning par rapport à une architecture artisanale sur un problème de classification binaire (Chien vs Chat) ?

## Objectifs Pédagogiques
1. **Compréhension théorique et pratique :** Maîtriser les concepts des CNN par une implémentation "from scratch".
2. **Maîtrise du pipeline de données :** Gérer le nettoyage, la standardisation et la normalisation des images.
3. **Analyse expérimentale :** Interprétation des courbes d'apprentissage (Loss/Accuracy) et gestion de l'overfitting.
4. **Transfer Learning :** Appréhender l'extraction de caractéristiques avec des modèles pré-entraînés (état de l'art).
5. **Déploiement (Mise en production) :** Rendre le modèle accessible via une interface web simple pour des tests en conditions réelles.

## Méthodologie et Déroulement (sur 14 semaines)
Le projet suit une démarche incrémentale sur le dataset public Kaggle "Dogs vs Cats" (25 000 images) :
- **Phase A (S1-S6) :** Exploration des données (EDA), prétraitement et implémentation d'une architecture Baseline ("From Scratch"). [Terminé]
- **Phase B (S7-S9) :** Optimisation et Régularisation (mise en place de la Data Augmentation et du Dropout). [Terminé]
- **Phase C (S10-S11) :** Approche par Transfer Learning (ex: ResNet50) et fine-tuning. [Terminé]
- **Phase D (S12-S14) :** Analyse des erreurs, déploiement web, rédaction du rapport et préparation de la soutenance.

## Livrables Attendus
- **Code source structuré :** Notebooks Python ou scripts validés et commentés.
- **Application Web Déployée :** Interface Gradio hébergée (ex: Hugging Face Spaces) permettant de tester le modèle.
- **Rapport de projet complet :** Document d'une quarantaine de pages justifiant les choix architecturaux et analysant techniquement les résultats.
- **Soutenance orale :** Présentation devant au moins deux enseignants pour défendre la démarche scientifique adoptée.

---

## État d'avancement (Journal de bord)
- [x] Analyse initiale des documents (AC20 descriptif, Fiche Projet TZ20, Fiche sujet).
- [x] Rédaction du `contexte.md` et définition du plan d'action.
- [x] Initialisation de la structure du projet avec la création d'un `README.md`.
- [x] Configuration de l'environnement Git (création du fichier `.gitignore` spécifique à PyTorch/Machine Learning).
- [x] Création de l'environnement virtuel avec Conda et installation des dépendances.
- [x] Préparation du fichier `environment.yml` (l'équivalent Conda du requirements.txt).
- [x] Initialisation du rapport (Page de garde, sommaire, et configuration environnement) dans le dossier non-versionné.
- [x] Étape 1 : Téléchargement et préparation du Dataset Kaggle (EDA).
- [x] Étape 1.5 : Séparation physique des données (Train/Val/Test) via un script de prétraitement (scripts/prepare_data.py) pour garantir un split stratifié et reproductible. Les données sont maintenant structurées dans data/clean/.
- [x] Étape 2 : Création des DataLoaders PyTorch à partir du dossier data/clean/ et application des transformations (Resize à 256x256, ToTensor, Normalisation).
- [x] Étape 3 : Implémentation de l'architecture CNN Baseline (calcul des dimensions et définition des couches).
- [x] Étape 4 : Mise en place de la boucle d'entraînement (Loss, Optimiseur, suivi de l'Accuracy, Early Stopping).
- [x] Validation de la Baseline (Phase A) : Entraînement terminé, détection d'overfitting à partir de l'époque 4 (Val Acc: 89.55%).
- [x] Étape 5 : Création du notebook `03_optimization_cnn.ipynb` et implémentation de la Phase B (Optimisation).
- [x] Validation de l'Optimisation (Phase B) : Mise en place de la Data Augmentation (Flip, Rotation, Jitter), du Dropout (0.5) et de la Batch Normalization. Résultat : 95.76% d'accuracy sur le set de validation (Early Stopping à l'époque 29).
- [x] Étape 6 : Comparaison des modèles (Baseline vs Optimized) sur le set de test dans `04_model_comparison.ipynb`.
- [x] Résultats de la comparaison :
    - Baseline : 89.81% Accuracy | ~7.8 ms/image
    - Optimized : 95.76% Accuracy | ~7.2 ms/image
    - Conclusion : Le modèle optimisé est non seulement plus précis (+6%), mais aussi légèrement plus rapide grâce à la Batch Normalization qui stabilise l'apprentissage et l'inférence.
- [x] Étape 7 : Approche par Transfer Learning (Phase C) avec ResNet50 dans le notebook 05_transfer_learning.ipynb. Résultat : ~99.2% accuracy en validation.
- [x] Étape 8 : Évaluation finale sur le set de test et comparaison tri-modèles.
- [ ] Étape 9 : Création de l'interface de démonstration (Gradio) et déploiement.
- [ ] Étape 10 : Rédaction finale des parties théoriques du rapport et conclusion.