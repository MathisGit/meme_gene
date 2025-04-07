import os
import json
from mistralai import Mistral
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class CaptionGenerator:
    def __init__(self):
        """Initialise le générateur de textes avec l'API Mistral."""
        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.client = Mistral(api_key=self.api_key)
        self.model = "mistral-large-latest"
        
    def _create_caption_prompt(self, prompt: str, meme_info: Dict) -> str:
        """Crée le prompt pour la génération des textes."""
        format_instructions = {
            "two_panels": """Génère EXACTEMENT deux textes courts et drôles qui contrastent bien.
Exemple de format pour two_panels:
{
    "texts": ["Texte du premier panneau", "Texte du deuxième panneau"]
}""",
            "three_panels": """Génère EXACTEMENT trois textes courts qui racontent une histoire.
Exemple de format pour three_panels:
{
    "texts": ["Texte du premier panneau", "Texte du deuxième panneau", "Texte du troisième panneau"]
}""",
            "top_bottom": """Génère EXACTEMENT deux textes courts : un accrocheur en haut et une punchline en bas.
Exemple de format pour top_bottom:
{
    "texts": ["Texte du haut", "Texte du bas"]
}"""
        }
        
        return f"""Tu es un expert en création de mèmes. Génère des textes drôles et pertinents pour le mème suivant.

Prompt utilisateur: "{prompt}"

Informations sur le mème:
- Description: {meme_info['description']}
- Format: {meme_info['format']}

{format_instructions[meme_info['format']]}

IMPORTANT:
- Génère EXACTEMENT le nombre de textes requis pour le format
- Les textes doivent être courts et percutants
- Utilise le format JSON exact comme dans les exemples
- Ne génère que les textes, pas d'explications ou de commentaires
"""
        
    def generate_captions(self, prompt: str, meme_info: Dict) -> List[str]:
        """
        Génère les textes pour un mème à partir d'un prompt.
        
        Args:
            prompt (str): Le prompt décrivant la situation
            meme_info (Dict): Les informations sur le mème sélectionné
            
        Returns:
            List[str]: Les textes générés
        """
        caption_prompt = self._create_caption_prompt(prompt, meme_info)
        
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": caption_prompt,
                },
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse la réponse JSON
        result = json.loads(response.choices[0].message.content)
        return result["texts"]
    
if __name__ == "__main__":
    generator = CaptionGenerator()
    prompt = "quand tu pushes en prod un vendredi"
    meme_info = {
        "description": "Un développeur qui pousse du code en prod un vendredi",
        "format": "two_panels"
    }
    texts = generator.generate_captions(prompt, meme_info)
    print(texts)

