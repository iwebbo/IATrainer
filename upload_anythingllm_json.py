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

"""

import os
import json
import requests

# 🔧 CONFIGURATION
ANYTHINGLLM_API_URL = "http://localhost:3001/api/v1"
ANYTHINGLLM_API_KEY = "0M6D0DJ-QVDMFQB-KNZMBH3-16F5KXH"
DOCUMENT_FOLDER_NAME = "Crewai"  # Nom du dossier pour stocker les documents JSON
JSON_ROOT_FOLDER = "json"  # Dossier contenant les fichiers JSON à uploader

headers = {"Authorization": f"Bearer {ANYTHINGLLM_API_KEY}"}


def create_or_verify_folder():
    """
    Vérifie si le dossier existe, sinon le crée.
    """
    print(f"🔍 Vérification du dossier '{DOCUMENT_FOLDER_NAME}'...")

    # Vérification de l'existence du dossier
    check_response = requests.get(f"{ANYTHINGLLM_API_URL}/documents/folder/{DOCUMENT_FOLDER_NAME}", headers=headers)

    if check_response.status_code == 200:
        print(f"✅ Dossier '{DOCUMENT_FOLDER_NAME}' déjà existant.")
        return True

    # Création du dossier s'il n'existe pas
    print(f"🚀 Création du dossier '{DOCUMENT_FOLDER_NAME}'...")
    create_response = requests.post(
        f"{ANYTHINGLLM_API_URL}/document/create-folder",
        json={"name": DOCUMENT_FOLDER_NAME},
        headers=headers,
    )

    if create_response.status_code == 200:
        print(f"✅ Dossier '{DOCUMENT_FOLDER_NAME}' créé avec succès !")
        return True
    else:
        print(f"❌ Erreur lors de la création du dossier : {create_response.text}")
        return False


def find_all_json_files(root_folder):
    """
    Recherche récursivement tous les fichiers JSON dans le dossier et ses sous-dossiers.
    """
    json_files = []
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files


def upload_json_documents():
    """
    Upload tous les fichiers JSON du dossier 'json' vers AnythingLLM en tant que documents.
    """
    if not os.path.exists(JSON_ROOT_FOLDER):
        print(f"❌ Erreur : Le dossier '{JSON_ROOT_FOLDER}' n'existe pas.")
        return 0

    json_files = find_all_json_files(JSON_ROOT_FOLDER)
    uploaded_files = 0

    if not json_files:
        print("⚠️ Aucun fichier JSON trouvé à uploader.")
        return 0

    for filepath in json_files:
        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            json_data = json.load(file)  # Charger le JSON tel quel

        # Construire la requête d'upload vers /v1/document/upload/{folderName}
        upload_url = f"{ANYTHINGLLM_API_URL}/document/upload/{DOCUMENT_FOLDER_NAME}"
        files = {"file": (filename, json.dumps(json_data, ensure_ascii=False))}  # Envoi du JSON brut comme fichier

        response = requests.post(upload_url, files=files, headers=headers)

        if response.status_code == 200:
            print(f"✅ {filename} uploadé avec succès dans '{DOCUMENT_FOLDER_NAME}' !")
            uploaded_files += 1
        else:
            print(f"❌ Échec de l'upload de {filename} : {response.text}")

    return uploaded_files


# 🚀 Exécution du script
if __name__ == "__main__":
    if create_or_verify_folder():
        total_uploaded = upload_json_documents()
        print(f"\n🎯 {total_uploaded} fichiers JSON envoyés dans '{DOCUMENT_FOLDER_NAME}' sur AnythingLLM !")
