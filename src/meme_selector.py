import os
from typing import Dict, Tuple
import json
from dotenv import load_dotenv
from mistralai import Mistral
from caption_generator import CaptionGenerator

load_dotenv()

class MemeSelector:
    def __init__(self):
        """Initialise le sélecteur de mèmes avec l'API Mistral."""
        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.client = Mistral(api_key=self.api_key)
        self.model = "mistral-large-latest"
        self.memes = self._load_memes()
        self.caption_generator = CaptionGenerator()

    def _load_memes(self) -> dict:
        """Charge les métadonnées des mèmes depuis le fichier JSON."""
        with open("data/memes.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def _create_selection_prompt(self, prompt: str) -> str:
        """Crée le prompt pour la sélection du mème."""
        memes_info = "\n".join([
            f"- {meme['id']}: {meme['description']} (format: {meme['format']})"
            for meme in self.memes.values()
        ])
        
        return f"""Tu es un expert en mèmes. Sélectionne le mème le plus approprié pour le prompt suivant.

Prompt utilisateur: "{prompt}"

Mèmes disponibles:
{memes_info}

Réponds directement avec l'id du mème sélectionné, sans aucun autre texte.
exemple:
"drake_approve"
"""

    def select_meme(self, prompt: str) -> Tuple[str, Dict]:
        """
        Sélectionne le mème le plus approprié pour un prompt.
        
        Args:
            prompt (str): Le prompt décrivant la situation
            
        Returns:
            Tuple[str, Dict]: L'ID du mème sélectionné et ses informations
        """
        selection_prompt = self._create_selection_prompt(prompt)
        
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": selection_prompt,
                },
            ]
        )
        
        meme_id = response.choices[0].message.content
        
        # Vérifie que le mème existe
        if meme_id not in self.memes:
            raise ValueError(f"Mème {meme_id} non trouvé")
            
        return meme_id, self.memes[meme_id]

    def get_template_info(self, template_id: str) -> Dict:
        """Récupère les informations d'un template spécifique."""
        return self.memes.get(template_id)


if __name__ == "__main__":
    selector = MemeSelector()
    prompt = "j'ai un problème avec mon code"
    meme_id, meme_info = selector.select_meme(prompt)
    print(meme_id, meme_info)