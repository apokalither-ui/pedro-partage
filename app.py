import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Pédro-Partage", page_icon="📚", layout="centered")

# --- BARRE LATÉRALE (MENU) ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Aller vers :", ["📖 Espace d'étude", "📸 Partager un sujet (Photo)"])

# Liste complète des matières (adaptée pour tout le secondaire)
matieres_ci = [
    "Philosophie", 
    "Histoire-Géographie", 
    "Français", 
    "Anglais", 
    "Espagnol", 
    "Allemand", 
    "EDHC", 
    "Mathématiques",
    "SVT",
    "Physique-Chimie"
]

# Liste complète des classes de la 6e à la Terminale en Côte d'Ivoire
classes_ci = [
    "6ème",
    "5ème",
    "4ème",
    "3ème",
    "2nde A",
    "2nde C",
    "1ère A",
    "1ère C",
    "1ère D",
    "Terminale A1",
    "Terminale A2",
    "Terminale C",
    "Terminale D"
]

# --- PAGE 1 : ESPACE D'ÉTUDE ---
if page == "📖 Espace d'étude":
    st.title("📚 Pédro-Partage : Le site d'entraide")
    st.write("Bienvenue ! Ici, on partage nos devoirs pour progresser ensemble les amis.")
    
    st.divider() # Crée une ligne de séparation propre
    
    # Section Profil de l'utilisateur
    st.markdown("### 👤 Qui es-tu ?")
    nom = st.text_input("Entre ton nom ou pseudonyme :")
    classe = st.selectbox("Ta classe / Niveau :", classes_ci) # Utilisation de la nouvelle liste de classes
    
    # Section d'entraide par matière
    st.markdown("### 📖 Espace d'étude")
    matiere = st.selectbox("Choisis la matière que tu veux réviser :", matieres_ci)
    
    # Zone interactive (Bouton)
    if st.button("Afficher les ressources disponibles"):
        if nom:
            st.success(f"Bon courage {nom} ! Voici les sujets disponibles pour la classe de {classe} en {matiere} :")
            
            # Exemples de contenu selon la matière sélectionnée
            if matiere == "Philosophie" and "Terminale" in classe:
                st.info("📝 Sujet de dissertation récent : La liberté est-elle une illusion ?")
            elif matiere == "Histoire-Géographie":
                st.info("🌍 Fiche de révision : Le développement économique de la Côte d'Ivoire.")
            elif matiere == "EDHC":
                st.info("🛡️ Cours : Les valeurs civiques et les droits de l'homme en Côte d'Ivoire.")
            elif matiere == "Mathématiques" and "3ème" in classe:
                st.info("📐 Exercice Brevet : Calcul littéral et propriétés de Thalès.")
            else:
                st.warning(f"Aucun devoir n'a encore été partagé pour le niveau {classe} en {matiere}. Sois le premier !")
        else:
            st.error("S'il te plaît, entre ton nom ci-dessus avant de valider.")

# --- PAGE 2 : APPAREIL PHOTO ---
elif page == "📸 Partager un sujet (Photo)":
    st.title("📸 Partager un sujet d'examen")
    st.write("Prends une photo nette de ta feuille de papier (sujet, exercice, résumé) pour l'envoyer à tes camarades.")
    
    st.divider()
    
    # Sélection des détails du sujet
    st.markdown("### 📝 Infos sur le document")
    classe_photo = st.selectbox("Pour quelle classe est ce sujet ?", classes_ci) # Ajout de la classe pour la photo
    matiere_photo = st.selectbox("De quelle matière s'agit-il ?", matieres_ci)
    commentaire = st.text_input("Ajoute un petit titre ou commentaire (ex: Devoir de Math Lycée San-Pedro) :")
    
    # Zone de l'appareil photo
    st.markdown("### 📷 Active ton appareil photo")
    image_cliquee = st.camera_input("Place ta feuille bien en face de l'objectif")
    
    # Si l'utilisateur a pris une photo
    if image_cliquee is not None:
        st.success("📷 Photo capturée avec succès !")
        
        # Aperçu de l'image
        st.image(image_cliquee, caption="Aperçu de ton document avant envoi", use_container_width=True)
        
        # Bouton d'envoi final
        if st.button("🚀 Publier le sujet sur le site"):
            st.balloons() # Animation festive !
            st.success(f"Parfait ! Le sujet de {matiere_photo} ({classe_photo}) a été partagé avec succès. Merci pour l'entraide !")