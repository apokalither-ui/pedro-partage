import streamlit as st
import random
import time

# Configuration du titre et du format de la page Web
st.set_page_config(
    page_title="Jeu du Nombre Mystère",
    page_icon="🎯",
    layout="centered"
)

# Affichage de l'entête principal
st.title("🎯 Le Jeu du Nombre Mystère")
st.markdown("Bienvenue ! Devine le nombre secret choisi par l'ordinateur avant la fin du temps ou l'épuisement de tes essais.")

# Barre latérale pour la personnalisation des options
st.sidebar.header("⚙️ Configuration du Jeu")
nombre_min = st.sidebar.number_input("Nombre Minimum", value=1, step=1)
nombre_max = st.sidebar.number_input("Nombre Maximum", value=100, step=1)
max_tentatives = st.sidebar.slider("Nombre d'essais autorisés", min_value=3, max_value=15, value=7)
temps_limite = st.sidebar.number_input("Temps limite total (secondes)", value=60, min_value=10, step=5)

# Fonction pour réinitialiser les variables et relancer une partie
def reinitialiser_partie():
    st.session_state.nombre_mystere = random.randint(nombre_min, nombre_max)
    st.session_state.tentatives_restantes = max_tentatives
    st.session_state.temps_depart = time.time()
    st.session_state.victoire = False
    st.session_state.game_over = False
    st.session_state.temps_ecoule_message = ""
    st.session_state.historique = []

# Initialisation de la mémoire du jeu
if "nombre_mystere" not in st.session_state or st.sidebar.button("🔄 Nouvelle Partie"):
    reinitialiser_partie()

# Calcul du temps restant avant chaque action
temps_actuel = time.time()
temps_passe = int(temps_actuel - st.session_state.temps_depart)
temps_restant = max(0, temps_limite - temps_passe)

# Vérification si le temps est dépassé
if temps_restant <= 0 and not st.session_state.victoire and not st.session_state.game_over:
    st.session_state.game_over = True
    st.session_state.temps_ecoule_message = "💥 BOOM !! Le temps est fini pendant ta réflexion !"

# Affichage des indicateurs visuels (Temps restant et Essais restants)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="⏳ Temps restant", value=f"{temps_restant}s")
with col2:
    st.metric(label="🎯 Essais restants", value=st.session_state.tentatives_restantes)
with col3:
    st.metric(label="📊 Plage", value=f"{nombre_min} à {nombre_max}")

st.divider()

# Formulaire de saisie pour que le joueur entre sa proposition
if not st.session_state.game_over and not st.session_state.victoire:
    with st.form("form_devinette", clear_on_submit=True):
        proposition = st.number_input(
            f"Entre un nombre de votre choix ({nombre_min} à {nombre_max}) :",
            min_value=int(nombre_min),
            max_value=int(nombre_max),
            step=1,
            key="input_joueur"
        )
        bouton_valider = st.form_submit_button("Valider ma réponse 🚀")

    # Traitement de la réponse soumise par le joueur
    if bouton_valider:
        # Vérification du temps au moment exact de la validation
        if time.time() - st.session_state.temps_depart > temps_limite:
            st.session_state.game_over = True
            st.session_state.temps_ecoule_message = "💥 BOOM !! Le temps est fini pendant ta réflexion !"
        else:
            st.session_state.tentatives_restantes -= 1

            if proposition == st.session_state.nombre_mystere:
                st.session_state.victoire = True
                st.session_state.game_over = True
                st.session_state.historique.append((proposition, "🎉 Victoire ! Tu as trouvé le nombre mystère !"))
            elif proposition < st.session_state.nombre_mystere:
                st.session_state.historique.append((proposition, "plus haut"))
            else:
                st.session_state.historique.append((proposition, "plus bas"))

            # Vérification de l'épuisement des tentatives
            if st.session_state.tentatives_restantes <= 0 and not st.session_state.victoire:
                st.session_state.game_over = True

        st.rerun()

# Affichage des messages de fin de partie

# Cas 1 : VICTOIRE
if st.session_state.victoire:
    st.success(f"🎉 *Bravo, tu as trouvé le nombre mystère : {st.session_state.nombre_mystere} !*")
    st.balloons()

# Cas 2 : DÉFAITE (Temps écoulé ou plus de tentatives)
elif st.session_state.game_over:
    if st.session_state.temps_ecoule_message:
        st.error(f"{st.session_state.temps_ecoule_message}")
    else:
        st.error("❌ Tu as épuisé toutes tes tentatives !")
    
    # Affichage du nombre mystère en cas d'échec (comme dans ton correctif)
    st.warning(f"❌ Dommage ! Le nombre mystère était : *{st.session_state.nombre_mystere}*")

# Bouton pour rejouer
if st.session_state.game_over or st.session_state.victoire:
    if st.button("🎮 Rejouer une partie"):
        reinitialiser_partie()
        st.rerun()

# Journal des coups joués
if st.session_state.historique:
    st.subheader("📜 Historique de tes coups")
    for prop, indice in reversed(st.session_state.historique):
        if "Victoire" in indice:
            st.success(f"Proposition : *{prop}* ➔ {indice}")
        elif "plus haut" in indice:
            st.info(f"Proposition : *{prop}* ➔ {indice}")
        else:
            st.warning(f"Proposition : *{prop}* ➔ {indice}")
