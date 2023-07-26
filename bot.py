import tkinter as tk
import openai
import asyncio
import os
from typing import List, Generator
from collections import deque


def initialize_openai_api_key():
    # Check if the key is in the environment variables
    if "OPENAI_API_KEY" in os.environ:
        openai.api_key = os.environ["OPENAI_API_KEY"]
    else:
        config = load_config('config.json')
        # Check if the key is in the configuration file
        if "openai_api_key" in config:
            openai.api_key = config["openai_api_key"]
        else:
            # Ask the user for the key
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            openai_api_key = simpledialog.askstring("OpenAI API Key", "Please enter your OpenAI API Key:")
            root.destroy()
            
            if openai_api_key is not None and openai_api_key.strip() != '':
                openai.api_key = openai_api_key
                # Save the key in the configuration file for future use
                config["openai_api_key"] = openai_api_key
                update_config('config.json', config)
            else:
                raise ValueError("No OpenAI API Key provided.")
            return False ##api key is not initialized properly
    return True

def create_conversation(prompt, max_messages=10):
    messages = deque(maxlen=max_messages)
    messages.append({'role': 'system', 'content': prompt})

    def get_messages():
        return list(messages)  # return a copy to prevent modification

    def add_user_message(content):
        messages.append({"role": "user", "content": content})

    def add_assistant_message(text):
        messages.append({"role": "assistant", "content": text})

    def update_prompt(new_prompt):
        messages.clear()
        messages.append({'role': 'user', 'content': new_prompt})
    

    return get_messages, add_user_message, add_assistant_message, update_prompt

get_messages, add_user_message, add_assistant_message, update_prompt = create_conversation(prompt="解释用户输入的段落内容，帮助用户理解其含义。")

def get_response(messages:deque, model) -> Generator:
    completion = openai.ChatCompletion.create(
    model= model,
    messages= list(messages),  # Convert deque to list
    temperature=0,
    stream=True  
    )
    return completion
    
## the method exposed to the outside
def get_explanation(text:str, model:str) -> Generator:
    add_user_message(text)
    messages = get_messages()
    response = get_response(messages, model)
    return response


if __name__ == "__main__":
    initialize_openai_api_key()
    get_response(get_messages(), "gpt-4")