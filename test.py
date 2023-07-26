import tkinter as tk
import json
import bot  # Import your bot module

def load_prompts(filename):
    with open(filename, 'r',encoding='utf-8') as file:
        data = json.load(file)
        return {prompt['tag']: prompt['text'] for prompt in data['prompts']}

def switch_prompt(listbox, prompts):
    selected_prompt = listbox.get(tk.ACTIVE)
    bot.update_prompt(prompts[selected_prompt])

def create_listbox(root, prompts):
    listbox = tk.Listbox(root)
    for prompt in prompts:
        listbox.insert(tk.END, prompt)
    listbox.pack()
    return listbox

def create_switch_button(root, listbox, prompts):
    button = tk.Button(root, text="Switch Prompt", 
                command=lambda: switch_prompt(listbox, prompts))
    button.pack()
    return button

def main():
    root = tk.Tk()
    prompts = load_prompts('prompts.json')
    listbox = create_listbox(root, prompts)
    button = create_switch_button(root, listbox, prompts)
    root.mainloop()

if __name__ == "__main__":
    main()
