import json
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import time
import os
import sys
from playwright.sync_api import sync_playwright
import random


# 🔹 Récupération du BASE_DIR depuis `main.py`
BASE_DIR = sys.argv[2] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

# 🔹 Correction des chemins relatifs en utilisant BASE_DIR
FONT_PATH = os.path.join(BASE_DIR, "pdf", "DejaVuSans.ttf")  # Police TTF
PDF_DIR = os.path.join(BASE_DIR, "pdf")  # Dossier PDF
JSON_FILE = os.path.join(BASE_DIR, "scrap", "scraped_data_stackflow.json")  # JSON
PDF_FILE = "StackOverFlow.pdf"

# ✅ Assurer l'existence du dossier PDF
os.makedirs(PDF_DIR, exist_ok=True)

def scrape_page(url):
    """Scrape le contenu principal d'une page donnée."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"❌ Erreur lors du chargement de {url}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # Sélection du contenu principal
    content = soup.select_one("article") or soup.select_one("div.body") or soup.select_one("main")  # Essaye différents conteneurs
    if not content:
        print(f"❌ Impossible d'extraire le contenu de {url}")
        return ""

    return content.get_text(separator="\n", strip=True)


class PDF(FPDF):
    """Classe PDF personnalisée avec support Unicode."""
    def header(self):
        self.add_font("DejaVu", "", str(FONT_PATH), uni=True)  # ✅ Correction du chemin de police
        self.set_font("DejaVu", size=16)
        self.cell(200, 10, "Documentation Ansible Windows", ln=True, align="C")
        self.ln(10)


def save_to_pdf(content_list, output_file=PDF_FILE):
    """Sauvegarde le contenu dans un PDF en UTF-8."""
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ✅ Ajouter la police UTF-8 (avec correction du chemin)
    pdf.add_font("DejaVu", "", str(FONT_PATH), uni=True)

    for title, text in content_list:
        pdf.add_page()
        pdf.set_font("DejaVu", size=14)
        pdf.cell(200, 10, title, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("DejaVu", size=12)
        pdf.multi_cell(0, 10, text)

    pdf.output(output_file)
    print(f"✅ PDF sauvegardé : {output_file}")


def main():
    """Lit le JSON, scrape les pages et génère le PDF."""
    print("📖 Lecture du fichier JSON contenant les articles...")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        links = json.load(f)

    if not links:
        print("❌ Aucun lien trouvé, arrêt du script.")
        return

    content_list = []

    for entry in links:
        title, url = entry["title"], entry["link"]
        print(f"📄 Scraping : {title}")
        text = scrape_page(url)
        if text:
            content_list.append((title, text))
        time.sleep(1)  # Évite le bannissement

    print(f"📄 Génération du PDF dans {PDF_FILE}...")
    save_to_pdf(content_list)


if __name__ == "__main__":
    main()
