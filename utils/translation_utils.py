# utils/translation_utils.py

import os
import json

def load_translations(module_name, language):
    """
    Translate the given string key based on the selected language.

    Args:
    - module_name (str): Name of the module or file to load translations for.
    - language (str): Language code ("pt-br" or "en-us").

    Returns:
    - dict: Translations dictionary for the specified module and language.
    """
    base_dir = os.path.dirname(__file__)
    if "main" in module_name:
        translations_file = os.path.join(base_dir, f"../l18n/{module_name}.json")
    elif "prompts" in module_name:
        translations_file = os.path.join(base_dir, f"../l18n/agents/prompt-templates/{module_name}.json")
    else:
        translations_file = os.path.join(base_dir, f"../l18n/agents/{module_name}.json")
    with open(translations_file, "r", encoding="utf-8") as f:
        translations = json.load(f)
    # Return translations for the specified language, default to empty dictionary if not found
    return translations.get(language, {})  

def translate_string(module_name, key, language):
    """
    Translate the given string key based on the selected language.
    
    Args:
    - key (str): Key to translate.
    - language (str): Language code ("pt-br" or "en-us").
    
    Returns:
    - str: Translated string if available, otherwise returns the original key.
    """
    translations = load_translations(module_name, language)
    # Return the translation if found, otherwise return the original key
    return translations.get(key, key)