import json

def load_config(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        config = json.load(file)
    return config

def update_config(file_path, config):
    with open(file_path, 'w') as file:
        json.dump(config, file)