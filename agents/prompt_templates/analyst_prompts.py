# prompt_templates/analyst_templates.py

from utils.translation_utils import translate_string

class AnalystPrompts:
    def __init__(self, language):
        self.language = language

    def get_report_prompt(self):
        return translate_string("analyst_prompts", "analyst_report_prompt_instructions", self.language)
    
    def get_refinement_instructions(self):
        return translate_string("analyst_prompts", "analyst_report_refinement_instructions", self.language)