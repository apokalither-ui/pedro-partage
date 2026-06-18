import streamlit as st
import time
from PIL import Image
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Pedro Partage", 
    page_icon="📚", 
    layout="wide"
)

# 2. DESIGN EN DÉGRADÉ CUSTOMISÉ
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

# 3. MESSAGE D'ACCUEIL ANIMÉ (Corrigé : Ne se joue qu'une seule fois !)
if "animation_jouee" not in st.session_state:
    welcome_text = "✨ Bienvenue sur Pedro Partage, le site ! Préparez vos examens ensemble. ✨"
    animated_placeholder = st.empty()
    current_text = ""

    for char in welcome_text:
        current_text += char
        animated_placeholder.markdown(f"<h3 style='text-align: center; color: #2a5298;'>{current_text}</h3>", unsafe_allow_html=True)
        time.sleep(0.03)
    st.session_state.animation_jouee = True
else:
    # Si l'animation a déjà été jouée, on affiche le texte directement sans recharger
    st.markdown("<h3 style='text-align: center; color: #2a5298;'>✨ Bienvenue sur Pedro Partage, le site ! Préparez vos examens ensemble. ✨</h3>", unsafe_allow_html=True)

st.divider()

# --- 🛡️ FONCTION DE COMPRESSION ET CONVERSION EN PDF DOUBLE SÉCURITÉ ---
def images_vers_pdf_compresser(photo_recto, photo_verso=None):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    largeur_page, hauteur_page = letter

    photos = [photo_recto]
    if photo_verso is not None:
        photos.append(photo_verso)

    for photo in photos:
        img = Image.open(photo)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Compression forte et redimensionnement
        max_size = 900
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Sauvegarde temporaire propre pour ReportLab
        temp_img_buffer = io.BytesIO()
        img.save(temp_img_buffer, format="JPEG", quality=50)
        temp_img_buffer.seek(0)
        
        # Intégration sécurisée
        img_valide = Image.open(temp_img_buffer)
        c.drawInlineImage(img_valide, 10, 10, width=largeur_page-20, height=hauteur_page-20, preserveAspectRatio=True)
        c.showPage()

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue() # Sauvegarde stable des données

# 4. CRÉATION DES ONGLETS
onglet_prendre, onglet_poster, onglet_admin = st.tabs(["📚 Consulter les sujets", "📸 Poster un sujet (Recto/Verso PDF)", "⚙️ Gestion"])

# Initialisation de la liste des sujets
if "liste_sujets" not in st.session_state:
    st.session_state.liste_sujets = []

# --- PARTIE 1 : CONSULTER ---
with onglet_prendre:
    st.subheader("Fil d'actualité des sujets partagés")
    
    if not st.session_state.liste_sujets:
        st.info("Aucun sujet n'a encore été posté. Soyez le premier !")
    else:
        for sujet in reversed(st.session_state.liste_sujets):
            with st.container(border=True):
                st.markdown(f"### 📝 {sujet['titre']}")
                st.caption(f"Matière : *{sujet['matiere']}*")
                
                st.download_button(
                    label="📥 Télécharger le sujet complet (PDF)",
                    data=sujet['pdf'],
                    file_name=f"{sujet['titre']}.pdf",
                    mime="application/pdf",
                    key=f"dl_{sujet['titre']}_{time.time()}" # Clé unique pour éviter les conflits
                )
                st.divider()

# --- PARTIE 2 : POSTER ---
with onglet_poster:
    st.subheader("Partagez un nouveau sujet (Recto et Verso optionnel)")
    
    # Utilisation d'un formulaire pour bloquer le rechargement pendant la saisie
    with st.form("formulaire_partage", clear_on_submit=True):
        titre_sujet = st.text_input("Titre du sujet (ex: Régional Blanc Philo 2026)")
        
        liste_matieres = [
            "Philosophie", "Histoire-Géographie", "Français", "Anglais", "Espagnol", 
            "Allemand", "Mathématiques", "Sciences de la Vie et de la Terre (SVT)", 
            "Physique-Chimie", "EDHC", "Arts Plastiques", "Musique", "Éducation Physique et Sportive (EPS)"
        ]
        matiere_choisie = st.selectbox("Sélectionnez la matière", liste_matieres)
        
        col1, col2 = st.columns(2)
        with col1:
            photo_recto = st.file_uploader("📸 Photo Face RECTO (Obligatoire)", type=["png", "jpg", "jpeg"])
        with col2:
            photo_verso = st.file_uploader("📸 Photo Face VERSO (Optionnel)", type=["png", "jpg", "jpeg"])
        
        bouton_publier = st.form_submit_button("🚀 Compresser et Publier en PDF")
        
        if bouton_publier:
            if titre_sujet and photo_recto:
                with st.spinner("Création du PDF compressé..."):
                    pdf_ultra_leger = images_vers_pdf_compresser(photo_recto, photo_verso)
                    
                    nouveau_sujet = {
                        "titre": titre_sujet,
                        "matiere": matiere_choisie,
                        "pdf": pdf_ultra_leger
                    }
                    st.session_state.liste_sujets.append(nouveau_sujet)
                    st.success("Parfait ! Ton sujet a été compressé en PDF et publié avec succès ! Va dans l'onglet 'Consulter les sujets'.")
            else:
                st.error("Veuillez donner un titre et ajouter au moins la photo du Recto.")

# --- PARTIE 3 : OUTIL D'ADMINISTRATION ---
with onglet_admin:
    st.subheader("🛠️ Espace Contrôle Mémoire")
    nb_sujets = len(st.session_state.liste_sujets)
    st.metric(label="Nombre de PDF stockés en mémoire", value=nb_sujets)
    
    if st.button("🚨 Nettoyer et vider la mémoire du site"):
        st.session_state.liste_sujets = []
        st.success("Mémoire vidée !")
        time.sleep(0.5)
        st.rerun()
