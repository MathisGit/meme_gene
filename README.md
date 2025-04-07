# Générateur de Mèmes Intelligent

Un générateur de mèmes qui utilise l'IA pour créer des mèmes personnalisés à partir d'un prompt texte.

## Fonctionnalités

- Sélection intelligente de templates de mèmes basée sur le contexte
- Génération de texte adapté au format du mème
- Support de différents formats de mèmes (top/bottom, 2 panels, etc.)
- Interface simple et intuitive

## Installation

1. Clonez le repository
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```
3. Configurez votre clé API Mistral dans un fichier `.env` :
```
MISTRAL_API_KEY=votre_clé_api
```

## Utilisation

```python
from src.main import generate_meme

meme = generate_meme("quand tu pushes en prod un vendredi")
meme.show()  # Affiche le mème généré
```

## Structure du Projet

- `data/` : Contient les templates de mèmes et leurs métadonnées
- `src/` : Code source principal
  - `main.py` : Point d'entrée principal
  - `meme_processor.py` : Traitement des images et ajout de texte
  - `meme_selector.py` : Sélection du template approprié
- `utils/` : Fonctions utilitaires
  - `image_utils.py` : Fonctions de manipulation d'images
