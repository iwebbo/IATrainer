import json
import requests
from bs4 import BeautifulSoup
import re

INPUT_FILE = "scraped_data_duck.jsonl"
OUTPUT_FILE = "formatted_training_data_duck.jsonl"

def clean_text(text):
    """ Nettoie le texte en supprimant le code CSS, HTML et les espaces inutiles. """
    text = re.sub(r"\s+", " ", text)  # Supprime les espaces multiples
    text = re.sub(r"{.*?}", "", text)  # Supprime les blocs CSS
    text = re.sub(r"<.*?>", "", text)  # Supprime les balises HTML
    return text.strip()

def get_page_description(url):
    """Essaie d'extraire une meta description ou du texte depuis la page cible."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # ✅ Essayer la meta description en premier
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                return clean_text(meta_desc["content"])

            # ✅ Si pas de meta description, essayer le premier paragraphe
            first_paragraph = soup.find("p")
            if first_paragraph:
                return clean_text(first_paragraph.text)

        return "Pas de réponse disponible."
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération de {url} : {e}")
        return "Pas de réponse disponible."

def format_for_finetuning(input_file, output_file):
    formatted_data = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            prompt = f"Explique cette question d'Ansible : {data['title']}"

            # ✅ Vérifier si `summary` est exploitable, sinon chercher une autre source
            completion = data["summary"].strip() if data["summary"] else get_page_description(data["link"])

            formatted_data.append({"prompt": prompt, "completion": completion})

    with open(output_file, "w", encoding="utf-8") as f:
        for entry in formatted_data:
            json.dump(entry, f)
            f.write("\n")

    print(f"✅ Données transformées et sauvegardées dans {output_file}")

if __name__ == "__main__":
    format_for_finetuning(INPUT_FILE, OUTPUT_FILE)
