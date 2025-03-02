import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import sys
import os


# 🔹 Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("❌ Erreur : https://docs.ansible.com/ansible/latest/getting_started/index.html : python docget_duck.py 'votre requête'")
    sys.exit(1)

# 🔹 Récupérer la requête depuis l'argument
BASE_URL = sys.argv[1]
JSON_FILE = "lib\scrap\scrapped_menu_links_doc.json"

def get_full_menu_links():
    """Utilise Playwright pour ouvrir les sous-menus et extraire tous les liens."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Mettre True pour ne pas afficher
        page = browser.new_page()
        page.goto(BASE_URL, timeout=60000)

        # Attendre le menu latéral
        page.wait_for_selector("div.toctree-wrapper", timeout=20000)

        # Déployer tous les sous-menus en cliquant sur les flèches
        submenu_buttons = page.query_selector_all("button.toctree-expand")
        for button in submenu_buttons:
            button.click()
            time.sleep(0.5)

        # Récupérer le HTML après expansion
        html_content = page.content()
        browser.close()

    # Analyse avec BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    menu_links = []
    for link in soup.select("div.toctree-wrapper a"):
        href = link.get("href")
        if href and not href.startswith("http"):
            full_url = BASE_URL.rsplit("/", 1)[0] + "/" + href  # Correction des URLs
            menu_links.append({"title": link.text.strip(), "url": full_url})

    print(f"✅ {len(menu_links)} liens récupérés !")

    # Sauvegarder en JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(menu_links, f, indent=4, ensure_ascii=False)

    print(f"✅ Liens enregistrés dans {JSON_FILE}")

if __name__ == "__main__":
    get_full_menu_links()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    DOC_PATH = os.path.join(BASE_DIR, "scraper_ansible.py")

    print("📄 Scrapping all link founds and Génération du PDF...")
    os.system(f'python "{DOC_PATH}"')
    print("✅ Finish.")
