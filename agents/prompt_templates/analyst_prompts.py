# prompt_templates/analyst_templates.py

from main import translate_string

class AnalystPrompts:
    def __init__(self, language):
        self.language = language

    @staticmethod
    def get_report_prompt(self):
        return translate_string("analyst_prompts", "analyst_report_prompt_instructions", self.language)
    
    @staticmethod
    def get_refinement_instructions(self):
        return translate_string("analyst_prompts", "analyst_report_refinement_instructions", self.language)