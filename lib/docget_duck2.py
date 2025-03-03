from langchain.tools import DuckDuckGoSearchResults
import json
import os
import sys

# 🔹 Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("❌ Erreur : Aucun terme de recherche fourni. Exécution : python docget_duck2.py 'votre requête'")
    sys.exit(1)

# 🔹 Récupérer la requête depuis l'argument
query = sys.argv[1]


# 🔹 Définition de la requête de recherche
#query = "Ansible Windows role best practices"

# 🔹 Initialisation du moteur de recherche DuckDuckGo
search = DuckDuckGoSearchResults()

# 🔹 Exécuter la recherche et récupérer les résultats
search_results = search.run(query)

# 🔹 Formater les résultats en JSON (LangChain format)
formatted_data = []
for i, result in enumerate(search_results):
    formatted_data.append({
        "prompt": f"Explique cette question d'Ansible : {query}",
        "completion": result
    })

# 🔹 Définir le nom du fichier de sortie
json_file = "json\formatted_duckduckgo_data.json"

# 🔹 Sauvegarder en JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(formatted_data, f, indent=4, ensure_ascii=False)

print(f"✅ Données sauvegardées dans {json_file}")
