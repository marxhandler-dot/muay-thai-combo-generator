# File: combo_manager.py
import json
from datetime import datetime
from colorama import init, Fore, Style
import os
from pathlib import Path
init()

def save_combo(combinations_data, user_name, file_name):
    try:
        if not file_name.endswith('.json'):
            file_name = file_name + '.json'

        data_to_save = {
            "name": user_name,
            "created": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "combinations": combinations_data,
            "total_combos": len(combinations_data),
            "total_techniques": sum(len(inner_list) for inner_list in combinations_data),
        }

        with open(file_name, "w") as json_file:
            json.dump(data_to_save, json_file, indent=2)

        return True, "File saved successfully"
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

def get_save_preferences():
    save_choice = input(Fore.MAGENTA +"Do you want to save these combinations?"+ Style.BRIGHT + "(y/n)"  + Style.RESET_ALL + Fore.MAGENTA + ": " + Style.RESET_ALL).lower()

    if save_choice != 'y':
        return {"should_save": False}

    combo_name = input(Fore.BLUE + Style.BRIGHT + "Enter a name for this combo set: "+ Style.RESET_ALL)
    filename = input(Fore.BLUE + Style.BRIGHT + "Enter filename (without .json): "+ Style.RESET_ALL)

    return {
        'should_save': True,
        'combo_name': combo_name,
        'filename': filename
    }

def get_available_savefiles():
    try:
        json_files = list(Path('.').glob('*.json'))
        if not json_files:
            return []

        return [file.name for file in json_files]
    except Exception as e:
        return []

def load_combo_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)

        #
        if 'name' not in data or 'combinations' not in data:
            return None, "Invalid save file format"


        return {
            'name': data['name'],
            'combinations': data['combinations']
        }, "File loaded successfully"

    except FileNotFoundError:
        return None, "File not found"
    except json.JSONDecodeError:
        return None, "File is corrupted or invalid JSON"
    except Exception as e:
        return None, f"Error loading file: {str(e)}"