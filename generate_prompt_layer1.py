import json
from jinja2 import Template
import tkinter as tk
from tkinter.filedialog import askopenfilename
from datetime import datetime

root = tk.Tk()
root.withdraw()

# File selection from user
json_path = askopenfilename(
    title="Select an answers_layer1_*.json file",
    filetypes=[("JSON files", "*.json")]
)

if not json_path:
    print("No file selected.")
    exit()

# Load JSON 
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Define schema
template_str = """
The system is categorized as: {{ q1[0] }}.
It is primarily used by: {{ q2 | join(', ') }}.
It is accessible via: {{ q3[0] }}.
It relies on the following third-party services: {{ q4 | join(', ') }}.
The data it processes includes: {{ q5 | join(', ') }}.
The system is developed and maintained by: {{ q6[0] }}.
Compliance requirements include: {{ q7 | join(', ') }}.
It interacts externally with: {{ q8 | join(', ') }}.
""".strip()

# Create Prompt
template = Template(template_str)
prompt = template.render(**data)

# Display and save prompt
print("\nGenerated Prompt:\n")
print(prompt)

# Write to file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"prompt_layer1_{timestamp}.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(prompt)

print(f"\nPrompt saved to {output_file}")
