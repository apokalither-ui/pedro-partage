import streamlit as st
import time

# 1. CONFIGURATION DE LA PAGE (Look moderne et large)
st.set_page_config(
    page_title="Pedro Partage", 
    page_icon="📚", 
    layout="wide"
)

# 2. DESIGN EN DÉGRADÉ CUSTOMISÉ (Bleu et Rouge dégradé)
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
    animated_placeholder.markdown(f"<h3 style='text-align: center; color: #2a5298;'>{current_text}</h3>", unsafe_allow_html=True)
    time.sleep(0.04) # Vitesse de l'écriture

# Un trait de séparation élégant
st.divider()

# 4. CRÉATION DES DEUX PARTIES (ONGLETS)
onglet_prendre, onglet_poster = st.tabs(["📚 Consulter les sujets", "📸 Poster un sujet (Photo)"])

# Initialisation de la liste des sujets dans la mémoire du site
if "liste_sujets" not in st.session_state:
    st.session_state.liste_sujets = []

# --- PARTIE 1 : PRENDRE/CONSULTER LES SUJETS ---
with onglet_prendre:
    st.subheader("Fil d'actualité des sujets partagés")
    
    if not st.session_state.liste_sujets:
        st.info("Aucun sujet n'a encore été posté. Soyez le premier !")
    else:
        # On affiche les sujets du plus récent au plus ancien
        for sujet in reversed(st.session_state.liste_sujets):
            with st.container(border=True):
                st.markdown(f"### 📝 {sujet['titre']}")
                st.caption(f"Matière : *{sujet['matiere']}*")
                
                # ICI : Affichage de la vraie photo prise par l'utilisateur
                st.image(sujet['image'], caption=sujet['titre'], use_container_width=True)
                st.divider()

# --- PARTIE 2 : POSTER LES SUJETS ---
with onglet_poster:
    st.subheader("Partagez un nouveau sujet avec vos camarades")
    
    # Formulaire de partage
    titre_sujet = st.text_input("Titre du sujet (ex: Régional Blanc Philo 2026)")
    
    # Liste complète de toutes les matières demandées
    liste_matieres = [
        "Philosophie", 
        "Histoire-Geography", 
        "Français", 
        "Anglais", 
        "Espagnol", 
        "Allemand", 
        "Mathématiques", 
        "Sciences de la Vie et de la Terre (SVT)", 
        "Physique-Chimie", 
        "EDHC", 
        "Arts Plastiques", 
        "Musique", 
        "Éducation Physique et Sportive (EPS)"
    ]
    matiere_choisie = st.selectbox("Sélectionnez la matière", liste_matieres)
    
    # Zone d'importation de la photo du sujet papier
    photo_sujet = st.file_uploader("Prenez ou choisissez une photo du sujet papier", type=["png", "jpg", "jpeg"])
    
    if st.button("🚀 Publier le sujet sur le site"):
        if titre_sujet and photo_sujet:
            # Enregistrement des données de l'image et du titre
            nouveau_sujet = {
                "titre": titre_sujet,
                "matiere": matiere_choisie,
                "image": photo_sujet
            }
            st.session_state.liste_sujets.append(nouveau_sujet)
            st.success("Félicitations ! Votre sujet a été publié avec succès. Allez dans l'onglet 'Consulter les sujets' pour le voir.")
        else:
            st.error("Veuillez donner un titre et ajouter une photo avant de publier.")
