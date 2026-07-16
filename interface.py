import streamlit as st

def main():
    # Configuration de la page pour ton téléphone
    st.set_page_config(page_title="Mon Portefeuille", page_icon="💰", layout="centered")

    st.title("💰 Mon Portefeuille Magique")

    # --- ÉTAPE 1 : INITIALISATION DE LA MÉMOIRE PRIVÉE ---
    # Ces variables restent isolées sur chaque téléphone pour ne pas mélanger tes données et celles de tes amis
    if 'budget_initial' not in st.session_state:
        st.session_state.budget_initial = 0.0
    if 'solde_actuel' not in st.session_state:
        st.session_state.solde_actuel = 0.0
    if 'budget_enregistre' not in st.session_state:
        st.session_state.budget_enregistre = False

    # --- ÉTAPE 2 : ENREGISTRER LE BUDGET INITIAL ---
    st.subheader("📊 Configuration du Budget")
    
    if not st.session_state.budget_enregistre:
        # Case pour taper le budget de départ (Ex: 5000)
        budget_saisi = st.number_input("Entrez votre budget initial (FCFA) :", min_value=0.0, step=500.0, value=5000.0)
        
        # Bouton pour bloquer et enregistrer ce budget
        if st.button("💾 Enregistrer mon budget"):
            st.session_state.budget_initial = budget_saisi
            st.session_state.solde_actuel = budget_saisi
            st.session_state.budget_enregistre = True
            st.success(f"Budget initial de {budget_saisi:,.0f} FCFA enregistré avec succès ! 🎉")
            st.rerun()
    else:
        # Si le budget est déjà enregistré, on affiche le solde en gros et un bouton pour réinitialiser si besoin
        col1, col2 = st.columns([2, 1])
        with col1:
            st.metric(label="Budget Initial", value=f"{st.session_state.budget_initial:,.0f} FCFA")
        with col2:
            if st.button("🔄 Changer de budget"):
                st.session_state.budget_enregistre = False
                st.rerun()

    st.markdown("---")

    # --- ÉTAPE 3 : AFFICHAGE DU SOLDE EN TEMPS RÉEL ---
    st.subheader("📉 Solde Disponible")
    # C'est ce compteur qui va diminuer à chaque achat
    if st.session_state.solde_actuel > 0:
        st.metric(label="Argent restant", value=f"{st.session_state.solde_actuel:,.0f} FCFA")
    elif st.session_state.budget_enregistre and st.session_state.solde_actuel <= 0:
        st.metric(label="Argent restant", value=f"{st.session_state.solde_actuel:,.0f} FCFA", delta="- Budget Épuisé !", delta_color="inverse")
    else:
        st.info("Veuillez d'abord enregistrer un budget initial ci-dessus.")

    st.markdown("---")

    # --- ÉTAPE 4 : ENREGISTRER UNE TRANSACTION (ACHAT) ---
    st.subheader("🛒 Effectuer un achat")

    # Case pour taper le montant de la transaction
    montant_achat = st.number_input("Montant de l'achat (FCFA) :", min_value=0.0, step=100.0)

    # Affichage dynamique du montant en FCFA juste en dessous pour ton écran mobile
    if montant_achat > 0:
        st.info(f"Montant saisi : *{montant_achat:,.0f} FCFA*")

    nom_achat = st.text_input("Nature de la dépense (Optionnel) :", placeholder="Ex: Boutique, Transport...")

    # Bouton magique qui effectue la soustraction directe
    if st.button("🔴 Soustraire de mon budget"):
        if not st.session_state.budget_enregistre:
            st.error("🚨 Vous devez d'abord définir et enregistrer un budget initial en haut de la page !")
        elif montant_achat <= 0:
            st.warning("⚠️ Veuillez saisir un montant d'achat supérieur à 0 FCFA.")
        else:
            # L'opération mathématique : Budget initial (ou solde actuel) MOINS l'achat
            if montant_achat <= st.session_state.solde_actuel:
                st.session_state.solde_actuel -= montant_achat
                st.success(f"Retrait effectué ! {montant_achat:,.0f} FCFA retirés pour '{nom_achat if nom_achat else 'Achat'}'.")
                st.rerun()
            else:
                st.error("🚨 Transaction refusée ! Votre solde actuel est insuffisant pour effectuer cet achat.")

if _name_ == "_main_":
    main()
