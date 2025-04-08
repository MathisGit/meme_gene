import streamlit as st
from PIL import Image
import os
import sys
from io import StringIO
import contextlib

# Ajoute le répertoire courant au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
                
                # Charger et afficher l'image
                meme_image = Image.open(meme_path)
                st.image(meme_image, caption="Votre mème généré", use_container_width=True)
                
                # Message de succès et bouton de téléchargement après l'image
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.success("Mème généré avec succès !")
                with col2:
                    with open(meme_path, "rb") as file:
                        st.download_button(
                            label="Télécharger",
                            data=file,
                            file_name=os.path.basename(meme_path),
                            mime="image/jpeg"
                        )
                
                # Logs dans un expander en bas
                with st.expander("Voir les détails de génération", expanded=False):
                    st.code(logs.getvalue())
                    
            except Exception as e:
                st.error(f"Erreur lors de la génération du mème : {str(e)}")
                with st.expander("Voir les détails de l'erreur", expanded=True):
                    st.code(str(e))
    else:
        st.warning("Veuillez entrer une description pour générer un mème.")