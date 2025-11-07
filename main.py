"""
Copyright (c) 2025 [A&E Coding]

Permission est accordée, gratuitement, à toute personne obtenant une copie
 de ce logiciel et des fichiers de documentation associés (le "IAScrapper.py"),
 de traiter le Logiciel sans restriction, y compris, sans s'y limiter, les droits
 d'utiliser, de copier, de modifier, de fusionner, de publier, de distribuer, de sous-licencier,
 et/ou de vendre des copies du Logiciel, et de permettre aux personnes à qui
 le Logiciel est fourni de le faire, sous réserve des conditions suivantes :

Le texte ci-dessus et cette autorisation doivent être inclus dans toutes les copies
 ou portions substantielles du Logiciel.

LE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE, EXPLICITE OU IMPLICITE,
Y COMPRIS MAIS SANS S'Y LIMITER, LES GARANTIES DE QUALITÉ MARCHANDE, D'ADÉQUATION
À UN USAGE PARTICULIER ET D'ABSENCE DE CONTREFAÇON. EN AUCUN CAS LES AUTEURS OU TITULAIRES
DU COPYRIGHT NE POURRONT ÊTRE TENUS RESPONSABLES DE TOUTE RÉCLAMATION, DOMMAGE OU AUTRE RESPONSABILITÉ,
QUE CE SOIT DANS UNE ACTION CONTRACTUELLE, DÉLICTUELLE OU AUTRE, DÉCOULANT DE,
OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU D'AUTRES INTERACTIONS AVEC LE LOGICIEL.
"""

"""

pip install beautifulsoup4 requests playwright json fpdf duckduckgo_search langchain-community os time langchain-community 
playwright install 

"""

import os
import json
import sys
import time


BANNER = """
 █████╗  ██████╗ ███████╗
██╔══██╗██╔════╝ ██╔════╝
███████║██║  ███╗█████╗  
██╔══██║██║   ██║██╔══╝  
██║  ██║╚██████╔╝███████╗
╚═╝  ╚═╝ ╚═════╝ ╚══════╝

        🚀 A&ECoding - AITrainer 🚀
     --------------------------------------
     > Generate a data with LanGChain to train your LLM Model !
     --------------------------------------
"""

def show_banner():
    os.system("cls" if os.name == "nt" else "clear")  # Nettoie la console
    print(BANNER)
    time.sleep(1)  # Petite pause pour l'effet visuel

show_banner()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = "output"  # Remplace par ton répertoire de sortie
MAX_REQUESTS_BEFORE_PAUSE = 4  # Nombre max avant pause
PAUSE_DURATION = 10  # Pause en secondes (ajuste selon besoin)

def lire_fichier_input(fichier):
    """Lit les requêtes depuis un fichier texte"""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            return [ligne.strip() for ligne in f.readlines() if ligne.strip()]
    except FileNotFoundError:
        print(f"❌ Le fichier `{fichier}` est introuvable. Assurez-vous qu'il existe.")
        return []

def execute_script(choix, queries):
    """Exécute un script selon le choix, en ajoutant une pause si besoin"""
    
    scripts = {
        "1": "lib/search_duck.py",
        "2": "lib/search_ansible.py",
        "3": "lib/stackflow.py",
        "4": "lib/llm_duck.py",
        "5": "lib/llm_duck_image.py",
        "6": "lib/llm_duck_videos.py",
        "7": "lib/llm_duck_wikipedia.py",
        "8": "lib/llm_duck_articles.py",
        "9": "lib/llm_duck_company.py",
        "10": "lib/generate_input.py",
    }

    if choix in scripts:
        script_path = scripts[choix]
        compteur = 0  # Compteur de requêtes

        for search_query in queries:
            print(f"\n🔍 Scraping `{search_query}` avec {script_path} en cours...")
            os.system(f'python {script_path} "{search_query}" "{BASE_DIR}"')
            print("✅ Scraping terminé, fichier JSON généré.\n")

            compteur += 1

            # Ajout d'une pause après un certain nombre de requêtes
            if compteur >= MAX_REQUESTS_BEFORE_PAUSE:
                print(f"⏸ Pause de {PAUSE_DURATION} secondes pour éviter les limitations...")
                time.sleep(PAUSE_DURATION)  # Pause automatique
                compteur = 0  # Réinitialisation du compteur

    elif choix == "0":
        print("👋 Good Bye. See you !")
        sys.exit(0)
    
    else:
        print("❌ Option invalide. Veuillez choisir une option valide.")

def afficher_menu():
    """Affiche le menu"""
    print("\n📌 MENU")
    print("1 - Recherche DuckDuckGo")
    print("2 - Scraper Documentation Ansible")
    print("3 - Recherche StackOverflow")
    print("4 - Best Practices (LLM Duck)")
    print("5 - Recherche d'images")
    print("6 - Recherche de vidéos")
    print("7 - Recherche Wikipedia")
    print("8 - Recherche d'articles")
    print("9 - Recherche d'entreprises")
    print("10 - Generate Input for LLM")
    print("0 - Quitter")

if __name__ == "__main__":
    fichier_input = "inputs.txt"
    
    while True:
        afficher_menu()
        choix = input("\nPrompt choice : ").strip()
        queries = lire_fichier_input(fichier_input)
        
        if queries:
            execute_script(choix, queries)
        else:
            print("📂 Aucune requête trouvée dans le fichier, saisissez-les dans `inputs.txt`.")