#script pour séparer la data en 3 dossiers: train, val et test
import os
import shutil
import random

# ==========================================
# CONFIGURATION
# ==========================================
SOURCE_DATA_DIR = 'data/raw'               # Dossier où se trouvent actuellement 'Cat' et 'Dog'
TARGET_DATA_DIR = 'data/clean'         # Nouveau dossier racine qui contiendra la séparation
CLASSES = ['Cat', 'Dog']                  # Les classes de ton dataset
TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
# Le test ratio est implicitement ce qui reste (0.10)
SEED = 42                                 # Graine pour la reproductibilité

def prepare_split_structure(base_target_path, classes):
    #Crée l'arborescence des dossiers train/val/test pour chaque classe.
    splits = ['train', 'val', 'test']
    for split in splits:
        for cls in classes:
            folder_path = os.path.join(base_target_path, split, cls)
            # exist_ok=True évite que le script plante si le dossier existe déjà
            os.makedirs(folder_path, exist_ok=True)

def split_and_copy_data():
    #Mélange et répartit les images dans les dossiers correspondants.

    # 1. On fixe la graine une seule fois pour tout le script
    random.seed(SEED)

    # 2. On crée la structure de dossiers de destination
    prepare_split_structure(TARGET_DATA_DIR, CLASSES)
    print(f"Structure de dossiers créée dans {TARGET_DATA_DIR}")

    # 3. Boucle sur chaque classe pour garantir la stratification (50/50 partout)
    for cls in CLASSES:
        print(f"Traitement de la classe : {cls}")
        source_cls_dir = os.path.join(SOURCE_DATA_DIR, cls)

        # Récupère tous les fichiers
        files = [f for f in os.listdir(source_cls_dir)]
        total_files = len(files)

        # Mélange aléatoire (mais reproductible grâce au seed)
        random.shuffle(files)

        # Calcul des indices de coupure
        train_idx = int(total_files * TRAIN_RATIO)
        val_idx = train_idx + int(total_files * VAL_RATIO)

        # Découpage de la liste
        train_files = files[:train_idx]
        val_files = files[train_idx:val_idx]
        test_files = files[val_idx:]

        # Petit dictionnaire pour faciliter la boucle de copie
        split_dict = {
            'train': train_files,
            'val': val_files,
            'test': test_files
        }

        # 4. Copie physique des fichiers
        for split_name, file_list in split_dict.items():
            dest_cls_dir = os.path.join(TARGET_DATA_DIR, split_name, cls)

            for file_name in file_list:
                src_path = os.path.join(source_cls_dir, file_name)
                dest_path = os.path.join(dest_cls_dir, file_name)
                # On utilise copy2 pour conserver les métadonnées de l'image
                shutil.copy2(src_path, dest_path)

            print(f"{len(file_list):5d} images copiées dans {split_name}/{cls}")

    print("Séparation des données terminée avec succès !")

# Point d'entrée classique en Python
if __name__ == "__main__":
    # Petit check de sécurité avant de lancer
    if not os.path.exists(SOURCE_DATA_DIR):
        print(f"Erreur : Le dossier source '{SOURCE_DATA_DIR}' est introuvable.")
    else:
        split_and_copy_data()