import os

# 🔹 Étape 3 : Entraînement sur LocalAI
print("🚀 Lancement de l'entraînement sur LocalAI...")
os.system("""
curl -X GET "http://localhost:8080/v1/models"
}'
""")

print("✅ Entraînement terminé !")