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

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from duckduckgo_search import DDGS
import json
import os
import sys

# 🔹 Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("❌ Erreur : Aucun terme de recherche fourni. Exécution : python docget_duck2.py 'votre requête'")
    sys.exit(1)

# 🔹 Récupérer la requête depuis l'argument
SEARCH_QUERY = sys.argv[1]
MAX_RESULTS = 100  # Nombre de résultats à récupérer

with DDGS() as ddgs:
    results = ddgs.text(SEARCH_QUERY, max_results=MAX_RESULTS)

for result in results:
    print(result)

# Sauvegarde en JSON
structured_results = [
    {
        "title": result["title"],
        "url": result["href"],
        "snippet": result["body"]
    }
    for result in results
]

with open("search_results_clean.json", "w", encoding="utf-8") as f:
    json.dump(structured_results, f, indent=4, ensure_ascii=False)

print("Résultats sauvegardés dans search_results_clean.json")