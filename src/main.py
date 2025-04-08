from src.meme_selector import MemeSelector
from src.caption_generator import CaptionGenerator
from src.meme_finalizer import MemeFinalizer
from utils.image_utils import save_meme
from PIL import Image

def generate_meme(prompt: str) -> str:
    """
    Génère un mème à partir d'un prompt texte.
    
    Args:
        prompt (str): Le prompt décrivant la situation pour le mème
        
    Returns:
        str: Le chemin du fichier mème généré
    """
    # Génération du mème avec le MemeFinalizer
    finalizer = MemeFinalizer()
    meme_path = finalizer.create_meme(prompt)
    return meme_path

def main():
    """Fonction principale pour tester le générateur de mèmes."""
    # Exemple d'utilisation
    prompt = input("Entrez votre prompt pour le mème : ")
    
    try:
        meme_path = generate_meme(prompt)
        print(f"Mème généré avec succès : {meme_path}")
        
        # Ouvrir l'image pour la montrer
        Image.open(meme_path).show()
            
    except Exception as e:
        print(f"Erreur lors de la génération du mème : {str(e)}")

if __name__ == "__main__":
    main()
