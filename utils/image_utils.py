from PIL import Image
import os
from typing import Tuple

def ensure_meme_directory(meme_dir: str = "data/memes") -> None:
    """Vérifie que le répertoire des mèmes existe."""
    os.makedirs(meme_dir, exist_ok=True)
    
def save_meme(image: Image.Image, filename: str, output_dir: str = "output") -> str:
    """
    Sauvegarde un mème dans le répertoire de sortie.
    
    Args:
        image (Image.Image): L'image du mème
        filename (str): Le nom du fichier
        output_dir (str): Le répertoire de sortie
        
    Returns:
        str: Le chemin du fichier sauvegardé
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{filename}.jpg")
    image.save(filepath, "JPEG", quality=95)
    return filepath
    
def get_image_dimensions(image_path: str) -> Tuple[int, int]:
    """
    Récupère les dimensions d'une image.
    
    Args:
        image_path (str): Le chemin de l'image
        
    Returns:
        Tuple[int, int]: Les dimensions (largeur, hauteur)
    """
    with Image.open(image_path) as img:
        return img.size
        
def resize_image(image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    """
    Redimensionne une image en conservant ses proportions.
    
    Args:
        image (Image.Image): L'image à redimensionner
        max_size (Tuple[int, int]): La taille maximale (largeur, hauteur)
        
    Returns:
        Image.Image: L'image redimensionnée
    """
    width, height = image.size
    max_width, max_height = max_size
    
    # Calcule les nouvelles dimensions en conservant les proportions
    ratio = min(max_width / width, max_height / height)
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
