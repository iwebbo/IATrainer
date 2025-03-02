import json

INPUT_FILE = "scraped_data.jsonl"
OUTPUT_FILE = "formatted_training_data.jsonl"

def format_for_finetuning(input_file, output_file):
    formatted_data = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            prompt = f"Explique cette question d'Ansible : {data['title']}"
            completion = data["summary"] if data["summary"] else "Pas de réponse disponible."

            formatted_data.append({"prompt": prompt, "completion": completion})

    with open(output_file, "w", encoding="utf-8") as f:
        for entry in formatted_data:
            json.dump(entry, f)
            f.write("\n")

    print(f"Données transformées en JSONL et enregistrées dans {output_file}")

if __name__ == "__main__":
    format_for_finetuning(INPUT_FILE, OUTPUT_FILE)
