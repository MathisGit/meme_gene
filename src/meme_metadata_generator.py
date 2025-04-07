import json
import os
import re
from typing import Dict, List

from PIL import Image


def get_image_format(image_path: str) -> str:
    """
    Détermine le format du mème basé sur l'analyse de l'image.
    Retourne un des formats suivants : 'top_bottom', 'two_panels', 'three_panels'
    """
    img = Image.open(image_path)
    width, height = img.size

    # Analyse basée sur les ratios et la structure de l'image
    ratio = width / height

    if ratio > 1.5:  # Image large
        if "distracted" in image_path.lower():
            return "three_panels"
        elif "drake" in image_path.lower():
            return "two_panels"
        else:
            return "top_bottom"
    else:
        return "top_bottom"


def generate_tags(image_path: str, description: str) -> List[str]:
    """
    Génère des tags pertinents basés sur le nom du fichier et la description.
    """
    tags = []

    # Tags basés sur le nom du fichier
    filename = os.path.basename(image_path).lower()
    words = re.findall(r"\w+", filename)
    tags.extend(words)

    # Tags basés sur la description
    desc_words = re.findall(r"\w+", description.lower())
    tags.extend([w for w in desc_words if len(w) > 3])  # Évite les mots trop courts

    # Tags communs pour les mèmes
    common_tags = ["meme", "funny", "humor"]
    tags.extend(common_tags)

    # Supprime les doublons et retourne une liste unique
    return list(set(tags))


def create_meme_metadata(image_path: str) -> Dict:
    """
    Crée les métadonnées pour un mème à partir de son image.
    """
    filename = os.path.basename(image_path)
    meme_id = os.path.splitext(filename)[0]

    # Génère une description basée sur le nom du fichier
    description = filename.replace("_", " ").title()

    # Détermine le format
    format_type = get_image_format(image_path)

    # Génère les tags
    tags = generate_tags(image_path, description)

    return {
        "id": meme_id,
        "description": description,
        "format": format_type,
        "tags": tags,
    }


def update_memes_json():
    """
    Met à jour le fichier memes.json avec les nouvelles images trouvées.
    """
    # Charge le fichier memes.json existant
    memes_path = "data/memes.json"
    if os.path.exists(memes_path):
        with open(memes_path, "r", encoding="utf-8") as f:
            memes = json.load(f)
    else:
        memes = {}

    # Parcourt le dossier img
    img_dir = "data/img"
    if not os.path.exists(img_dir):
        print(f"Le dossier {img_dir} n'existe pas.")
        return

    # Extensions d'images supportées
    image_extensions = (".png", ".jpg", ".jpeg", ".gif")

    # Traite chaque image
    for filename in os.listdir(img_dir):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(img_dir, filename)
            meme_id = os.path.splitext(filename)[0]

            # Ne traite que les nouvelles images
            if meme_id not in memes:
                try:
                    metadata = create_meme_metadata(image_path)
                    memes[meme_id] = metadata
                    print(f"Ajouté: {meme_id}")
                except Exception as e:
                    print(f"Erreur lors du traitement de {filename}: {str(e)}")

    # Sauvegarde les modifications
    with open(memes_path, "w", encoding="utf-8") as f:
        json.dump(memes, f, indent=4, ensure_ascii=False)

    print(f"Mise à jour terminée. {len(memes)} mèmes dans la base de données.")


if __name__ == "__main__":
    update_memes_json()
