import streamlit as st
from PIL import Image
import os
import sys
from io import StringIO
import contextlib

# Ajoute le répertoire courant au path Python pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Capture des prints pour les logs
@contextlib.contextmanager
def capture_logs():
    log_output = StringIO()
    with contextlib.redirect_stdout(log_output):
        yield log_output

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Mèmes",
    page_icon="🎭",
    layout="centered"
)

# Titre et description
st.title("🎭 Générateur de Mèmes")
st.write("Générez des mèmes personnalisés à partir d'une description !")

# Zone de saisie du prompt
prompt = st.text_input(
    "Décrivez votre situation",
    placeholder="Ex: quand tu pushes en prod un vendredi",
    key="prompt_input"
)

# Bouton de génération
if st.button("Générer le mème", type="primary"):
    if prompt:
        with st.spinner("Génération du mème en cours..."):
            try:
                # Import ici pour éviter les problèmes de path
                from src.meme_finalizer import MemeFinalizer
                
                # Capture des logs
                with capture_logs() as logs:
                    # Génération du mème
                    finalizer = MemeFinalizer()
                    meme_path = finalizer.create_meme(prompt)
                
                # Affichage du mème généré
                st.success("Mème généré avec succès !")
                
                # Charger et afficher l'image
                meme_image = Image.open(meme_path)
                st.image(meme_image, caption="Votre mème généré", use_container_width=True)
                
                # Bouton de téléchargement
                with open(meme_path, "rb") as file:
                    st.download_button(
                        label="Télécharger le mème",
                        data=file,
                        file_name=os.path.basename(meme_path),
                        mime="image/jpeg"
                    )
                
                # Afficher les logs dans la sidebar
                with st.sidebar:
                    st.text("Logs de génération :")
                    st.code(logs.getvalue())
                    
            except Exception as e:
                st.error(f"Erreur lors de la génération du mème : {str(e)}")
                st.error("Détails de l'erreur :")
                st.code(str(e))
    else:
        st.warning("Veuillez entrer une description pour générer un mème.")