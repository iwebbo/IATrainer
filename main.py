"""
Copyright (c) 2025 [A&E Coding]

Permission est accordée, gratuitement, à toute personne obtenant une copie
 de ce logiciel et des fichiers de documentation associés (le "IAtrainer.py"),
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

### NOTE A AJOUTER FINIR
https://pypi.org/project/duckduckgo-search/ ca exemple encore ... voir ce qu'on peut faire 
Si le temps et l'envie voir comment intégrer les sites de doc comme 
https://docs.python.org/fr/3/tutorial/index.html
https://learn.microsoft.com/fr-fr/cpp/cpp/comments-cpp?view=msvc-170 

Corriger mon BUG à moi pouir LLM pour pipenv pour mettre une autre version quelque part 
voir comment gérer pipenv et intégrer dans ansible 

++ Voir ajouter scrappe json langchain sso intranet site (pro plus tards)

pip install beautifulsoup4 requests playwright json fpdf duckduckgo_search langchain-community os time langchain-community
playwright install 

"""

import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔹 Scripts disponibles
SCRIPTS = {
    "1": "Scraper DuckDuckGo.com",
    "2": "Scraper la documentation Ansible",
    "3": "Scraper stackoverflow.com",
    "4": "Scraper DuckDuckGo.com with LLMChain"
}

def afficher_menu():
    """Affiche le menu pour sélectionner une action."""
    print("\n📌 Sélectionnez une action :")
    for key, value in SCRIPTS.items():
        print(f"{key}. {value}")
    print("0. Quitter")

def execute_script(choix):
    """Exécute un script selon le choix."""
    if choix == "1":
        search_query = input("\n🔍 Entrez votre requête pour DuckDuckGo : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\docget_duck3.py "{search_query}" "{BASE_DIR}"')  # 🔥 Passe la requête comme argument
        print("✅ Scraping terminé, fichier JSON généré.")

    elif choix == "2":
        search_query = input("\n🔍 Entrez votre URL de documentation https://docs.ansible.com/ansible/latest/getting_started/index.html : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\docget_ansible.py "{search_query}" "{BASE_DIR}"')  # 🔥 Passe la requête comme argument
        print("✅ Scraping terminé, fichier JSON généré.")

    elif choix == "3":
        search_query = input("\n🔍 Entrez votre requête pour StackOverFlow : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\docget_stackflow.py "{search_query}" "{BASE_DIR}"')  # 🔥 Passe la requête comme argument
        print("✅ Scraping terminé, fichier JSON généré.")

    elif choix == "4":
        search_query = input("\n🔍 Give me the best practive of...  : ")
        print(f"\n🔍 Scraping de `{search_query}` en cours...")
        os.system(f'python lib\docget_duck2.py "{search_query}" "{BASE_DIR}"')  # Lance l'entraînement du modèle
        print("✅ Scraping terminé with LangChain, fichier JSON généré.")

    elif choix == "0":
        print("👋 Fin du programme. À bientôt !")
        sys.exit(0)

    else:
        print("❌ Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    while True:
        afficher_menu()
        choix = input("\nEntrez votre choix : ")
        execute_script(choix)
