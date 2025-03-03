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
README:

Faire requirements.txt pîp voir 
- Gérér import AnythingLLM aprés workspace dédié pour ca et le créer 
- voir comment API + créer workspace + ansible 
- voir comment gérer pipenv et intégrer dans ansible 


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

# 🔹 Scripts disponibles
SCRIPTS = {
    "1": "Search/Scrap on DuckDuckGo.com",
    "2": "Search on Ansible Officiel Documentation",
    "3": "Search on stackoverflow.com",
    "4": "Search DuckDuckGoSearch with LLM Format Train",
    "5": "Search Image DuckDuckGoSearch with LLM Format Train",
    "6": "Search Videos DuckDuckGoSearch with LLM Format Train",
    "7": "Search Wikipedia DuckDuckGoSearch with LLM Format Train",
    "8": "Search Articles DuckDuckGoSearch with LLM Format Train",
    "9": "Search Company DuckDuckGoSearch with LLM Format Train"
}

def afficher_menu():
    """Affiche le menu pour sélectionner une action."""
    print("\n📌 Choose an action :")
    for key, value in SCRIPTS.items():
        print(f"{key}. {value}")
    print("0. Exit")

def execute_script(choix):
    """Exécute un script selon le choix."""
    if choix == "1":
        search_query = input("\n🔍 Entrez votre requête pour DuckDuckGo : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\search_duck.py "{search_query}" "{BASE_DIR}"')  # 🔥 Passe la requête comme argument
        print("✅ Scraping terminé, fichier JSON généré.")

    elif choix == "2":
        search_query = input("\n🔍 Entrez votre URL de documentation https://docs.ansible.com/ansible/latest/getting_started/index.html : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\search_ansible.py "{search_query}" "{BASE_DIR}"')  # 🔥 Passe la requête comme argument
        print("✅ Scraping terminé, fichier JSON généré.")

    elif choix == "3":
        search_query = input("\n🔍 Entrez votre requête pour StackOverFlow : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\stackflow.py "{search_query}" "{BASE_DIR}"')  # 🔥 Passe la requête comme argument
        print("✅ Scraping terminé, fichier JSON généré.")

    elif choix == "4":
        search_query = input("\n🔍 Give me the best practive of...  : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\llm_duck.py "{search_query}" "{BASE_DIR}"')  # Lance l'entraînement du modèle
        print("✅ Scraping terminé with LangChain, fichier JSON généré.")

    elif choix == "5":
        search_query = input("\n🔍 Search Image  ...  : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\llm_duck_image.py "{search_query}" "{BASE_DIR}"')  # Lance l'entraînement du modèle
        print("✅ Scraping terminé with LangChain, fichier JSON généré.")

    elif choix == "6":
        search_query = input("\n🔍 Search Videos  ...  : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\llm_duck_videos.py "{search_query}" "{BASE_DIR}"')  # Lance l'entraînement du modèle
        print("✅ Scraping terminé with LangChain, fichier JSON généré.")

    elif choix == "7":
        search_query = input("\n🔍 Search Wikipedia ...  : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\llm_duck_wikipedia.py "{search_query}" "{BASE_DIR}"')  # Lance l'entraînement du modèle
        print("✅ Scraping terminé with LangChain, fichier JSON généré.")

    elif choix == "8":
        search_query = input("\n🔍 Search Articles ...  : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\llm_duck_articles.py "{search_query}" "{BASE_DIR}"')  # Lance l'entraînement du modèle
        print("✅ Scraping terminé with LangChain, fichier JSON généré.")

    elif choix == "9":
        search_query = input("\n🔍 Search Company ...  : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\llm_duck_company.py "{search_query}" "{BASE_DIR}"')  # Lance l'entraînement du modèle
        print("✅ Scraping terminé with LangChain, fichier JSON généré.")

    elif choix == "0":
        print("👋 Good Bye. See you !")
        sys.exit(0)

    else:
        print("❌ Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    while True:
        afficher_menu()
        choix = input("\nPrompt choice : ")
        execute_script(choix)
