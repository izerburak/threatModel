import json
import re
from datetime import datetime
import tkinter as tk
from tkinter.filedialog import askopenfilename

root = tk.Tk()
root.withdraw()

# 1. Ask for Answer file
json_path = askopenfilename(
    title="Select an answers_layerX_*.json file",
    filetypes=[("JSON files", "*.json")]
)

if not json_path:
    print("No file selected.")
    exit()

# 2. Extract Layer from the selected answer file
match = re.search(r"answers_layer(\d+)_", json_path)
if not match:
    print("Could not determine layer number from file name.")
    exit()

layer_number = match.group(1)
question_file = f"layer{layer_number}_questions.json"

# 3. Load Necessary files
try:
    with open(json_path, "r", encoding="utf-8") as f:
        answers = json.load(f)
    with open(question_file, "r", encoding="utf-8") as f:
        questions = json.load(f)
except FileNotFoundError as e:
    print(f" Required file not found: {e}")
    exit()

# 4. Generate Prompt
prompt_lines = []
for i, q in enumerate(questions, start=1):
    qid = q["id"]
    qtext = q["text"]
    user_answers = answers.get(qid, [])
    if not user_answers:
        continue
    formatted_answers = ", ".join(user_answers)
    prompt_lines.append(f"{i}. {qtext}\n→ {formatted_answers}\n")

full_prompt = "\n".join(prompt_lines)

# 5. Display and save prompt
print("\nGenerated Prompt:\n")
print(full_prompt)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"prompt_layer{layer_number}_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(full_prompt)

print(f"\nPrompt saved to {output_file}")
