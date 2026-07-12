import os
import csv
montant = input("Entre le montant de la depense(en FCFA)")
categorie = input("Quelle est la categorie(ex: Aliments, transport) : ")
moyen_de_paiment = input("quel est le moyen de paiement(cash, wave): ")

nouvelle_depense = {"montant": montant, "categorie": categorie, "moyen": moyen_de_paiment} 

historique_depenses = []
historique_depenses.append(nouvelle_depense)
print("\n--- Résumé de ta dépense ---")
print(f"montant : {montant} FCFA")
print(f"categorie : {categorie}")
print(f"Payé par : {moyen_de_paiment}")
fichier_existe = os .path.exists("depenses.csv")

with open("depenses.csv", mode="a", newline="", encoding="utf-8") as fichier:
    champs = ["montant", "categorie", "moyen"]
    scripteur = csv. DictWriter(fichier, fieldnames=champs)

    if not fichier_existe:
        scripteur.writeheader()

    scripteur.writerow(nouvelle_depense)
total_depenses = 0

with open("depenses.csv", mode="r", encoding="utf-8") as fichier:
    lecteur = csv.DictReader(fichier)
    for line in lecteur:
        total_depenses += int(line["montant"])

print("\n===============")
print(f"TOTAL DE TES DEPENSES : {total_depenses} FCFA")
print("==================")         
