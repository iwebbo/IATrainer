from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import sys
import subprocess
import locale
import importlib.util

app = Flask(__name__, static_folder='static')
CORS(app)  # Permet les requêtes cross-origin

BASE_DIR = "output"  # Répertoire de sortie
MAX_REQUESTS_BEFORE_PAUSE = 4  # Nombre max avant pause
PAUSE_DURATION = 10  # Pause en secondes (ajuste selon besoin)

# Détection de l'encodage du système
SYSTEM_ENCODING = locale.getpreferredencoding()

# Dictionnaire des scripts disponibles
SCRIPTS = {
    "1": "lib/search_duck.py",
    "2": "lib/search_ansible.py",
    "3": "lib/stackflow.py",
    "4": "lib/llm_duck.py",
    "5": "lib/llm_duck_image.py",
    "6": "lib/llm_duck_videos.py",
    "7": "lib/llm_duck_wikipedia.py",
    "8": "lib/llm_duck_articles.py",
    "9": "lib/llm_duck_company.py",
    "10": "lib/generate_input.py",
}

# Importer dynamiquement le module generate_input.py pour pouvoir l'utiliser directement
try:
    spec = importlib.util.spec_from_file_location("generate_input", "lib/generate_input.py")
    generate_input_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generate_input_module)
    has_generate_input = True
    print("✅ Module generate_input.py chargé avec succès")
except Exception as e:
    has_generate_input = False
    print(f"❌ Erreur lors du chargement de generate_input.py: {e}")
    print("Les fonctionnalités de génération de requêtes via CrewAI ne seront pas disponibles")

def lire_fichier_input(fichier):
    """Lit les requêtes depuis un fichier texte"""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            return [ligne.strip() for ligne in f.readlines() if ligne.strip()]
    except FileNotFoundError:
        return []

def ecrire_fichier_input(fichier, queries):
    """Écrit les requêtes dans un fichier texte"""
    try:
        with open(fichier, "w", encoding="utf-8") as f:
            for query in queries:
                file.write(f"{query}\n")
        return True
    except Exception as e:
        return False

def decode_output_safely(byte_output):
    """Tente de décoder la sortie de manière sécurisée en essayant plusieurs encodages"""
    encodings = ['utf-8', 'latin-1', 'cp1252', SYSTEM_ENCODING]
    
    for encoding in encodings:
        try:
            return byte_output.decode(encoding)
        except UnicodeDecodeError:
            continue
    
    # Si tous les décodages échouent, on utilise latin-1 qui ne génère jamais d'erreur
    # (mais peut produire des caractères incorrects)
    return byte_output.decode('latin-1')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    """Renvoie la liste des scripts disponibles"""
    script_list = []
    for key, path in SCRIPTS.items():
        name = path.split('/')[-1].replace('.py', '').replace('_', ' ').title()
        script_list.append({"id": key, "name": name, "path": path})
    return jsonify(script_list)

@app.route('/api/queries', methods=['GET'])
def get_queries():
    """Récupère les requêtes du fichier inputs.txt"""
    queries = lire_fichier_input("inputs.txt")
    return jsonify(queries)

@app.route('/api/queries', methods=['POST'])
def save_queries():
    """Sauvegarde les requêtes dans le fichier inputs.txt"""
    data = request.json
    if 'queries' in data:
        try:
            with open("inputs.txt", "w", encoding="utf-8") as f:
                for query in data['queries']:
                    f.write(f"{query}\n")
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    return jsonify({"success": False, "error": "Données manquantes"})

@app.route('/api/generate-queries', methods=['POST'])
def generate_queries():
    """Génère des requêtes à partir de mots-clés via CrewAI"""
    if not has_generate_input:
        return jsonify({"success": False, "error": "Le module generate_input.py n'est pas disponible"})
    
    data = request.json
    
    if not data or 'keyword1' not in data:
        return jsonify({"success": False, "error": "Le premier mot-clé est obligatoire"})
    
    keyword1 = data['keyword1'].strip()
    keyword2 = data.get('keyword2', '').strip() or None
    count = int(data.get('count', 20))
    
    try:
        phrases = generate_input_module.generate_search_phrases(keyword1, keyword2, nombre=count)
        
        # Sauvegarde dans inputs.txt si demandé
        if data.get('save', False):
            generate_input_module.save_phrases_to_file(phrases)
        
        return jsonify({
            "success": True,
            "phrases": phrases,
            "count": len(phrases)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/execute', methods=['POST'])
def execute_script():
    """Exécute un script selon le choix"""
    data = request.json
    
    if 'script_id' not in data:
        return jsonify({"success": False, "error": "ID de script manquant"})
    
    script_id = data['script_id']
    
    # Vérifie si le script existe
    if script_id not in SCRIPTS:
        return jsonify({"success": False, "error": "Script invalide"})
    
    # Obtient les requêtes
    if 'use_file' in data and data['use_file']:
        queries = lire_fichier_input("inputs.txt")
    elif 'queries' in data:
        queries = data['queries']
    else:
        return jsonify({"success": False, "error": "Aucune requête fournie"})
    
    # Si aucune requête, retourne une erreur
    if not queries:
        return jsonify({"success": False, "error": "Aucune requête trouvée"})
    
    results = []
    script_path = SCRIPTS[script_id]
    
    for i, query in enumerate(queries):
        # Configuration de l'environnement pour le subprocess avec UTF-8
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        # Exécute le script avec subprocess pour capturer la sortie
        cmd = f'python {script_path} "{query}" "{BASE_DIR}"'
        
        try:
            # Exécute la commande et capture la sortie
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                env=env
            )
            stdout, stderr = process.communicate()
            
            # Décodage sécurisé des sorties
            output = decode_output_safely(stdout)
            error = decode_output_safely(stderr)
            
            result = {
                "query": query,
                "output": output,
                "error": error,
                "success": process.returncode == 0
            }
            
            results.append(result)
            
            # Ajoute une pause après un certain nombre de requêtes
            if (i+1) % MAX_REQUESTS_BEFORE_PAUSE == 0 and i < len(queries) - 1:
                time.sleep(PAUSE_DURATION)
                
        except Exception as e:
            results.append({
                "query": query,
                "output": "",
                "error": str(e),
                "success": False
            })
    
    return jsonify({
        "success": True,
        "results": results
    })

@app.route('/api/output', methods=['GET'])
def get_output_files():
    """Récupère la liste des fichiers de sortie"""
    if not os.path.exists(BASE_DIR):
        return jsonify([])
    
    files = []
    for filename in os.listdir(BASE_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(BASE_DIR, filename)
            file_stat = os.stat(file_path)
            
            files.append({
                "name": filename,
                "size": file_stat.st_size,
                "modified": file_stat.st_mtime
            })
    
    return jsonify(sorted(files, key=lambda x: x["modified"], reverse=True))

@app.route('/api/output/<filename>', methods=['GET'])
def get_output_file(filename):
    """Récupère le contenu d'un fichier de sortie"""
    file_path = os.path.join(BASE_DIR, filename)
    
    if not os.path.exists(file_path) or not filename.endswith('.json'):
        return jsonify({"error": "Fichier non trouvé"}), 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Assurez-vous que le répertoire de sortie existe
    os.makedirs(BASE_DIR, exist_ok=True)
    
    # Crée un fichier inputs.txt vide s'il n'existe pas
    if not os.path.exists("inputs.txt"):
        with open("inputs.txt", "w", encoding="utf-8") as f:
            pass
    
    print(f"📋 Encodage système détecté: {SYSTEM_ENCODING}")
    print(f"🚀 Serveur démarré sur http://0.0.0.0:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)