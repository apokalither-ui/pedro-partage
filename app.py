import streamlit as st
import time

# 1. CONFIGURATION DE LA PAGE (Look moderne et large)
st.set_page_config(
    page_title="Pedro Partage", 
    page_icon="📚", 
    layout="wide"
)

# 2. DESIGN EN DÉGRADÉ (Bleu et Rouge)
st.markdown("""
    <style>
    .main-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #911a1a 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 30px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    .main-banner h1 {
        color: white !important;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    .main-banner p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    </style>
    <div class="main-banner">
        <h1>📚 Pedro Partage</h1>
        <p>Le site officiel d'échange de sujets et corrigés</p>
    </div>
""", unsafe_allow_html=True)

# 3. MESSAGE D'ACCUEIL ANIMÉ (Effet machine à écrire)
welcome_text = "✨ Bienvenue sur Pedro Partage, le site ! Préparez vos examens ensemble. ✨"
animated_placeholder = st.empty()
current_text = ""

for char in welcome_text:
    current_text += char
    # On affiche le texte au fur et à mesure
    animated_placeholder.markdown(f"<h3 style='text-align: center; color: #2a5298;'>{current_text}</h3>", unsafe_allow_html=True)
    time.sleep(0.04) # Vitesse de l'écriture (plus le chiffre est petit, plus c'est rapide)

# Un petit trait de séparation élégant
st.divider()

# --- LA SUITE DE TON CODE ACTUEL COMMENCE ICI ---
st.write("Tu peux coller la suite de ton application juste en dessous...")
