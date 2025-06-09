import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# Load Questions From Json file
with open("layer1_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Start GUI 
root = tk.Tk()
root.title("Threat Modeling - Layer 1")
root.geometry("600x300")

current_index = 0
answers = {}
checkbox_vars = []
other_entry = None

def render_question(index):
    global checkbox_vars, other_entry

    for widget in root.winfo_children():
        widget.destroy()

    q = questions[index]

    question_label = tk.Label(
        root,
        text=f"{index + 1}. {q['text']}",
        font=("Helvetica", 12, "bold"),
        wraplength=550,
        justify="left"
    )
    question_label.pack(pady=10)

    checkbox_vars = []
    for opt in q["options"]:
        var = tk.BooleanVar()
        tk.Checkbutton(
            root,
            text=opt,
            variable=var,
            anchor="w",
            wraplength=500
        ).pack(fill="x", padx=20, anchor="w")
        checkbox_vars.append((opt, var))

    # "Other" Part
    tk.Label(root, text="Other (please specify):").pack(pady=(10, 0))
    other_entry = tk.Entry(root, width=70)
    other_entry.pack(pady=5)

    # "Next" button
    tk.Button(root, text="Next", command=on_next).pack(pady=20)

def on_next():
    global current_index, answers

    selected = [opt for opt, var in checkbox_vars if var.get()]
    other_text = other_entry.get().strip()

    if other_text:
        selected.append(f"{other_text}")

    if not selected:
        messagebox.showwarning("Input Needed", "Please select at least one option.")
        return

    question_id = questions[current_index]["id"]
    answers[question_id] = selected

    print(f"\nQuestion {current_index + 1}: {questions[current_index]['text']}")
    for ans in selected:
        print("-", ans)

    current_index += 1
    if current_index < len(questions):
        render_question(current_index)
    else:
        save_answers()
        messagebox.showinfo("Finished", "Layer 1 questions completed!")
        root.quit()

def save_answers():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"answers_layer1_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2, ensure_ascii=False)
    print(f"\n Answers saved to {filename}")

# Start
render_question(current_index)
root.mainloop()
