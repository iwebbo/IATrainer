import os

# 🔹 Étape 3 : Entraînement sur LocalAI
print("🚀 Lancement de l'entraînement sur LocalAI...")
os.system("""
curl -X POST "http://localhost:8080/v1/models" -H "Content-Type: application/json" -d '{
  "model": "qwen2.5-coder-3b-instruct",
  "dataset": "file://formatted_training_data.jsonl",
  "epochs": 5,
  "batch_size": 4
}'
""")

print("✅ Entraînement terminé !")