from duckduckgo_search import DDGS
import json
from playwright.sync_api import sync_playwright
import json
import time
import sys
import os

# 🔹 Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("❌ Erreur : Aucun terme de recherche fourni. Exécution : python docget_duck3.py 'votre requête'")
    sys.exit(1)



# 🔹 Récupérer la requête depuis l'argument
SEARCH_QUERY = sys.argv[1]
MAX_RESULTS = 50  # Nombre de résultats à récupérer
JSON_FILE = "json\scraped_data_duck.json"

def scrape_duckduckgo(query, max_results):
    """Effectue une recherche sur DuckDuckGo et récupère plusieurs résultats."""
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"],
                "summary": r["body"]
            })

    return results

# 🔹 Sauvegarde des résultats en JSON
def save_to_json(data, filename=JSON_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Données sauvegardées dans {filename}")

if __name__ == "__main__":
    scraped_data = scrape_duckduckgo(SEARCH_QUERY, MAX_RESULTS)
    if scraped_data:
        save_to_json(scraped_data)
        print(f"✅ {len(scraped_data)} résultats récupérés !")
    else:
        print("❌ Aucun résultat trouvé.")

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    # DUCK_PATH = os.path.join(BASE_DIR, "scraper_duck2.py")

    # print("📄 Scrapping all link founds and Génération du PDF...")
    # os.system(f'python "{DUCK_PATH}"')
    # print("✅ Finish.")