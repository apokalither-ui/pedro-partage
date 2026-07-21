import random
import time 
valeur_max = 100
valeur_min = 1
tentatives_max = 7
temps_limite = 60
nombre_mystère = random.randint(valeur_min, valeur_max)
tentatives_restantes = tentatives_max  
temps_depart = time.time()
print("BOMBE ACTIVE")
print(f"trouvez le nombre caché entre {valeur_min} et {valeur_max}")
print(f"vous avez {tentatives_max}essais et {temps_limite}secondes avant le cataclisme !")
victoire = False 
while tentatives_restantes > 0 :
    temps_ecoulé = time.time() - temps_depart
    temps_restant = int(temps_limite - temps_ecoulé)
    if temps_restant <= 0:
        print("BOOM !!!! LA BOMBE A EXPLOSEE , le temps est ecoulé")
        break 
    print(f"Temps restant : {temps_restant}s , Essais restant : {tentatives_restantes}")
    try:
        proposition = int(input("entrez un nombre de votre choix :"))
    except ValueError:
        print("entrez un nombre valide !")
        continue
    if time.time() - temps_depart > temps_limite:
        print("BOOM !! le temps est fini pendant ta reflexion")
        break 
    tentatives_restantes -= 1
    if proposition == nombre_mystère:
        victoire = True
        break
    elif proposition < nombre_mystère:
        print("plus haut")
    else:
        print("plus bas")    
