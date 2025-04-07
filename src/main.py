from meme_selector import MemeSelector
from caption_generator import CaptionGenerator
from meme_finalizer import MemeFinalizer
from utils.image_utils import save_meme
from PIL import Image

def generate_meme(prompt: str) -> Image.Image:
    """
    Génère un mème à partir d'un prompt texte en trois étapes :
    1. Sélection du mème approprié
    2. Génération des textes adaptés au format
    3. Finalisation de l'image
    
    Args:
        prompt (str): Le prompt décrivant la situation pour le mème
        
    Returns:
        Image.Image: Le mème généré
    """
    # 1. Sélection du mème approprié
    selector = MemeSelector()
    meme_id, meme_info = selector.select_meme(prompt)
    
    # 2. Génération des textes adaptés au format
    caption_generator = CaptionGenerator()
    texts = caption_generator.generate_captions(prompt, meme_info)
    
    # 3. Finalisation de l'image
    finalizer = MemeFinalizer()
    meme = finalizer.finalize_meme(meme_id, texts)
    
    return meme

def main():
    """Fonction principale pour tester le générateur de mèmes."""
    # Exemple d'utilisation
    prompt = input("Entrez votre prompt pour le mème : ")
    
    try:
        meme = generate_meme(prompt)
        meme.show()
        
        # Sauvegarde optionnelle
        save = input("Voulez-vous sauvegarder le mème ? (o/n) : ")
        if save.lower() == 'o':
            filename = input("Nom du fichier (sans extension) : ")
            save_meme(meme, filename)
            
    except Exception as e:
        print(f"Erreur lors de la génération du mème : {str(e)}")

if __name__ == "__main__":
    main()
