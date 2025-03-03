import requests

api_url = "http://localhost:3001/api/upload"  # URL d'AnythingLLM
headers = {"Authorization": "Bearer YOUR_API_KEY"}
files = {"file": open("search_results_clean.json", "rb")}

response = requests.post(api_url, headers=headers, files=files)

if response.status_code == 200:
    print("✅ Fichier envoyé à AnythingLLM avec succès !")
else:
    print("❌ Erreur :", response.text)
