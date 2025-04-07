import base64
import json
import os
from typing import Dict

from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()


def encode_image(image_path: str) -> str:
    """Encode l'image en base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Erreur lors de l'encodage de l'image {image_path}: {str(e)}")
        return None


def get_image_analysis(image_path: str, client: Mistral) -> Dict:
    """
    Analyse l'image avec l'API Mistral pour obtenir une description et des tags.
    """
    base64_image = encode_image(image_path)
    if not base64_image:
        return None

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Analyse cette image de mème et fournis les informations suivantes au format JSON:
                    1. Une description détaillée de ce qui est représenté
                    2. Le format du mème (top_bottom, two_panels, ou three_panels)
                    3. Une liste de tags pertinents (max 5)
                    
                    Format de réponse attendu:
                    {
                        "description": "description détaillée",
                        "format": "format du mème",
                        "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
                    }""",
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ]

    try:
        response = client.chat.complete(model="pixtral-12b-2409", messages=messages)

        # Extrait le JSON de la réponse
        content = response.choices[0].message.content
        # Trouve le premier { et le dernier }
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end != -1:
            json_str = content[start:end]
            return json.loads(json_str)
        else:
            print(f"Impossible de parser la réponse JSON pour {image_path}")
            return None

    except Exception as e:
        print(f"Erreur lors de l'analyse de l'image {image_path}: {str(e)}")
        return None


def create_meme_metadata(image_path: str, client: Mistral) -> Dict:
    """
    Crée les métadonnées pour un mème à partir de son image en utilisant l'API Mistral.
    """
    filename = os.path.basename(image_path)
    meme_id = os.path.splitext(filename)[0]

    # Analyse l'image avec Mistral
    analysis = get_image_analysis(image_path, client)
    if not analysis:
        # Fallback sur une description basique si l'analyse échoue
        return {
            "id": meme_id,
            "description": filename.replace("_", " ").title(),
            "format": "top_bottom",
            "tags": ["meme", "funny", "humor"],
        }

    return {
        "id": meme_id,
        "description": analysis["description"],
        "format": analysis["format"],
        "tags": analysis["tags"],
    }


def update_memes_json():
    """
    Met à jour le fichier memes.json avec les nouvelles images trouvées.
    """
    # Initialise le client Mistral
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("Erreur: MISTRAL_API_KEY non trouvée dans les variables d'environnement")
        return

    client = Mistral(api_key=api_key)

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
                    metadata = create_meme_metadata(image_path, client)
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
