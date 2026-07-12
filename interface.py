import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
# Configuration de la page avec un titre et un emoji sympa
st.set_page_config(page_title="Mon Portefeuille Magique", page_icon="💸", layout="centered")

# --- STYLE ET COULEURS ---
# Un grand titre accrocheur
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💸 Mon Portefeuille Magique</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555555; font-size: 18px;'>Suivez vos dépenses au quotidien sans effort et avec style !</p>", unsafe_allow_html=True)
st.write("---")

# --- FORMULAIRE COLORÉ ---
# On crée un bloc visuel pour le formulaire
with st.container():
    st.markdown("<h3 style='color: #1E88E5;'>✍️ Enregistrer une nouvelle dépense</h3>", unsafe_allow_html=True)
    
    with st.form("form_depense", clear_on_submit=True):
        # Zone de saisie du montant
        montant = st.number_input("Combien as-tu dépensé ? (FCFA)", min_value=0, step=100)
        
        # Choix de la catégorie
        categorie = st.selectbox("Dans quelle catégorie ?", ["🍔 Nourriture", "🚗 Transport", "🎁 Cadeau", "🎮 Loisirs", "💡 Factures & Abonnements", "✨ Autre"])
        
        # Moyen de paiement
        moyen_paiement = st.selectbox("Comment as-tu payé ?", ["🧡 Orange Money", "🌊 Wave", "💛 MTN MoMo", "💵 Espèces"])
        
        # Description
        description = st.text_input("Ajoute un petit détail (ex: 'Achat de pain', 'Taxi école')")
        
        # Le bouton pour valider
        st.write("")
        bouton_valider = st.form_submit_button("🚀 ENREGISTRER LA DÉPENSE")

# --- LOGIQUE D'ENREGISTREMENT ---
if bouton_valider:
    if montant > 0:
        nouvelle_depense = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Montant": montant,
            "Catégorie": categorie,
            "Moyen de Paiement": moyen_paiement,
            "Description": description
        }
        
        try:
            df = pd.read_csv("depenses.csv")
            df = pd.concat([df, pd.DataFrame([nouvelle_depense])], ignore_index=True)
            df.to_csv("depenses.csv", index=False)
        except FileNotFoundError:
            df = pd.DataFrame([nouvelle_depense])
            df.to_csv("depenses.csv", index=False)
            
        # Message de succès avec une belle couleur VERTE
        st.balloons() # Petite animation festive avec des ballons !
        st.success(f"🎉 Super ! Une dépense de {montant} FCFA a été ajoutée en catégorie {categorie} !")
    else:
        # Message d'erreur avec une belle couleur ROUGE
        st.error("⚠️ Oups ! Le montant doit être supérieur à 0 FCFA pour être enregistré.")

# --- RÉCAPITULATIF VISUEL ---
st.write("---")
st.markdown("<h3 style='color: #4CAF50;'>📊 Vos dernières statistiques</h3>", unsafe_allow_html=True)

try:
    df_visualisation = pd.read_csv("depenses.csv")
    if not df_visualisation.empty:
        # Affichage du total dans un joli encadré coloré
        total_depenses = df_visualisation["Montant"].sum()
        st.metric(label="Dépenses Totales", value=f"{total_depenses} FCFA", delta="- Évolution active")
        
        # Affichage du tableau des dépenses récentes
        st.write("📋 Historique de vos transactions :")
        st.dataframe(df_visualisation.tail(5), use_container_width=True)
    else:
        st.info("💡 Aucune dépense enregistrée pour le moment. Votre portefeuille est plein !")
except FileNotFoundError:
    st.info("💡 Le fichier de données va se créer dès votre premier clic sur le bouton.")
# On crée une section pour notre outil JavaScript
st.markdown("---")
st.subheader("💡 Simulateur d'Épargne Interactif (Propulsé par JavaScript)")

# Code HTML/CSS/JS combiné
code_javascript = """
<div style="background-color: #1E1E2F; padding: 20px; border-radius: 10px; color: white; font-family: sans-serif; text-align: center;">
    <p style="margin-bottom: 10px; font-size: 1.1em;">Combien veux-tu économiser par mois (FCFA) ?</p>
    
    <!-- Zone de saisie -->
    <input type="number" id="montantMois" value="5000" style="padding: 8px; border-radius: 5px; border: none; width: 60%; text-align: center; font-size: 1.2em; font-weight: bold;">
    
    <div style="margin-top: 20px;">
        <span style="font-size: 1.2em; color: #FF4B4B;">💰 En 1 an, tu auras économisé :</span>
        <!-- C'est ici que JavaScript va injecter le résultat en temps réel -->
        <h2 id="resultatAnnee" style="color: #00FFCC; margin: 10px 0; font-size: 2em;">60 000 FCFA</h2>
    </div>
</div>

<script>
    // 1. On récupère les éléments de la page
    const inputMontant = document.getElementById('montantMois');
    const affichageResultat = document.getElementById('resultatAnnee');

    // 2. On crée la fonction JavaScript qui fait le calcul en direct
    function calculerEpargne() {
        const montant = parseFloat(inputMontant.value) || 0;
        const totalAnnee = montant * 12;
        
        // On met à jour le texte à l'écran avec un format propre
        affichageResultat.innerText = totalAnnee.toLocaleString() + " FCFA";
    }

    // 3. On écoute ce que fait l'utilisateur : dès qu'il tape une touche, on calcule !
    inputMontant.addEventListener('input', calculerEpargne);
</script>
"""

# 2. On demande à Streamlit d'afficher ce composant JavaScript
components.html(code_javascript, height=220)
