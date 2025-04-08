from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Ajoute le répertoire parent au path pour pouvoir importer utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_utils import ensure_meme_directory, save_meme
from src.meme_selector import MemeSelector
from src.caption_generator import CaptionGenerator

class MemeFinalizer:
    def __init__(self):
        """Initialise le finaliseur de mèmes."""
        self.meme_dir = "data/img"
        self.font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"  # Use system Arial font
        ensure_meme_directory(self.meme_dir)
        self.selector = MemeSelector()
        self.caption_generator = CaptionGenerator()
        
    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Charge la police avec la taille spécifiée."""
        try:
            print(f"   Tentative de chargement de la police depuis {self.font_path}")
            if not os.path.exists(self.font_path):
                raise FileNotFoundError(f"Le fichier de police {self.font_path} n'existe pas")
                
            # Essayer d'abord avec truetype
            try:
                return ImageFont.truetype(self.font_path, size)
            except Exception as e:
                print(f"   Erreur avec truetype: {str(e)}")
                
            # Si ça échoue, essayer avec load_path
            try:
                return ImageFont.load_path(self.font_path)
            except Exception as e:
                print(f"   Erreur avec load_path: {str(e)}")
                
            # Si tout échoue, utiliser une police par défaut
            print("   Utilisation de la police par défaut...")
            return ImageFont.load_default()
        except Exception as e:
            print(f"   Erreur lors du chargement de la police: {str(e)}")
            raise
        
    def _get_text_position(self, image: Image.Image, text: str, font: ImageFont.FreeTypeFont) -> tuple:
        """Calcule la position du texte en bas de l'image."""
        draw = ImageDraw.Draw(image)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Centre le texte en bas avec une marge proportionnelle à la hauteur de l'image
        margin = max(20, image.height // 15)  # Au moins 30px, ou plus pour les grandes images
        x = (image.width - text_width) // 2
        y = image.height - text_height - margin
        return x, y
            
    def _calculate_optimal_font_size(self, image: Image.Image, text: str, max_width_ratio: float = 0.95, max_height_ratio: float = 0.3) -> int:
        """
        Calcule la taille de police optimale pour que le texte rentre dans la zone désirée.
        
        Args:
            image: L'image sur laquelle le texte sera ajouté
            text: Le texte à ajouter
            max_width_ratio: Ratio maximum de la largeur de l'image que le texte peut occuper
            max_height_ratio: Ratio maximum de la hauteur de l'image que le texte peut occuper
            
        Returns:
            int: La taille de police optimale
        """
        max_width = int(image.width * max_width_ratio)
        max_height = int(image.height * max_height_ratio)
        
        # Calcul de la taille de départ en fonction de la taille de l'image
        # Plus l'image est grande, plus on commence avec une grande taille
        start_size = min(image.height // 6, image.width // 8)  # Taille proportionnelle à l'image
        start_size = max(start_size, 40)  # Au moins 40px
        font_size = start_size
        
        draw = ImageDraw.Draw(image)
        
        # Vérifie que le fichier de police existe
        if not os.path.exists(self.font_path):
            print("   Police non trouvée, utilisation de la police par défaut")
            return 40  # Taille par défaut
        
        while font_size > 20:  # Taille minimum de 20px
            try:
                font = ImageFont.truetype(self.font_path, font_size)
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                if text_width <= max_width and text_height <= max_height:
                    return font_size
                    
                font_size -= 2
            except Exception:
                font_size -= 2
                
        return 20  # Taille minimum si rien d'autre ne fonctionne
            
    def _add_text_to_image(self, image: Image.Image, text: str, font_size: int = None) -> Image.Image:
        """Ajoute du texte en bas de l'image."""
        try:
            print("   Création du contexte de dessin...")
            draw = ImageDraw.Draw(image)
            
            print("   Calcul de la taille de police optimale...")
            if font_size is None:
                font_size = self._calculate_optimal_font_size(image, text)
            print(f"   Taille de police choisie: {font_size}px")
            
            print("   Chargement de la police...")
            font = self._load_font(font_size)
            
            print("   Calcul de la position du texte...")
            # Position du texte
            x, y = self._get_text_position(image, text, font)
            
            print("   Ajout de l'ombre...")
            # Ajout d'une ombre portée
            shadow_offset = max(2, font_size // 30)  # Offset proportionnel à la taille de police
            shadow_color = (0, 0, 0, 180)  # Noir semi-transparent
            for offset_x in range(shadow_offset, shadow_offset * 2):
                for offset_y in range(shadow_offset, shadow_offset * 2):
                    draw.text((x + offset_x, y + offset_y), text, font=font, fill=shadow_color)
            
            print("   Ajout du contour noir...")
            # Ajout d'un contour noir plus épais pour la lisibilité
            outline_size = max(2, font_size // 25)  # Contour proportionnel à la taille de police
            for offset_x in range(-outline_size, outline_size + 1):
                for offset_y in range(-outline_size, outline_size + 1):
                    if abs(offset_x) + abs(offset_y) <= outline_size + 1:
                        draw.text((x + offset_x, y + offset_y), text, font=font, fill="black")
            
            print("   Ajout du texte principal...")
            # Texte principal en blanc
            draw.text((x, y), text, font=font, fill="white")
            
            return image
        except Exception as e:
            print(f"   Erreur lors de l'ajout du texte: {str(e)}")
            raise
        
    def create_meme(self, prompt: str, output_dir: str = "output") -> str:
        """
        Crée un mème complet à partir d'un prompt.
        
        Args:
            prompt (str): Le prompt décrivant la situation
            output_dir (str): Le répertoire de sortie
            
        Returns:
            str: Le chemin du mème généré
        """
        try:
            print("\n=== Détails de la génération du mème ===")
            print(f"Prompt reçu: '{prompt}'")
            
            # 1. Sélection du mème
            print("\n1. Sélection du mème...")
            meme_id, meme_info = self.selector.select_meme(prompt)
            print(f"   ID du mème: {meme_id}")
            print(f"   Description: {meme_info.get('description', 'Non disponible')}")
            print(f"   Format: {meme_info.get('format', 'Non disponible')}")
            
            # 2. Génération de la caption
            print("\n2. Génération de la caption...")
            texts = self.caption_generator.generate_captions(prompt, meme_info)
            if len(texts) != 1:
                raise ValueError(f"Ce module ne gère que les mèmes avec une seule caption (reçu {len(texts)} captions)")
            caption = texts[0]
            print(f"   Caption générée: '{caption}'")
            
            # 3. Chargement de l'image
            print("\n3. Chargement de l'image...")
            # Essayer d'abord avec .png, puis .jpg si non trouvé
            image_path = os.path.join(self.meme_dir, f"{meme_id}.png")
            if not os.path.exists(image_path):
                image_path = os.path.join(self.meme_dir, f"{meme_id}.jpg")
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"Image du mème {meme_id} non trouvée (ni en PNG ni en JPG)")
            
            print(f"   Chemin de l'image: {image_path}")
            
            try:
                image = Image.open(image_path)
                print(f"   Dimensions: {image.width}x{image.height}")
                print(f"   Format: {image.format}")
                print(f"   Mode: {image.mode}")
                
                # Convertir en RGB si nécessaire
                if image.mode != 'RGB':
                    print("   Conversion en RGB...")
                    image = image.convert('RGB')
            except Exception as e:
                raise ValueError(f"Erreur lors de l'ouverture de l'image {image_path}: {str(e)}")
            
            # 4. Ajout du texte
            print("\n4. Ajout du texte...")
            meme = self._add_text_to_image(image, caption)
            
            # 5. Sauvegarde
            print("\n5. Sauvegarde...")
            filename = f"meme_{prompt[:20].replace(' ', '_')}"
            output_path = save_meme(meme, filename, output_dir)
            print(f"   Mème sauvegardé: {output_path}")
            
            return output_path
        except Exception as e:
            print(f"\nErreur: {str(e)}")
            raise

def main():
    """Fonction de test."""
    finalizer = MemeFinalizer()
    prompt = "quand tu pushes en prod un vendredi"
    try:
        meme_path = finalizer.create_meme(prompt)
        print(f"Mème généré avec succès : {meme_path}")
    except Exception as e:
        print(f"Erreur lors de la génération du mème : {str(e)}")

if __name__ == "__main__":
    main()