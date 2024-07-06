# prompt_templates/analyst_templates.py

from utils.translation_utils import translate_string

class AnalystPrompts:
    def __init__(self, language):
        self.language = language

    def get_report_prompt(self):
        return translate_string("analyst_prompts", "analyst_report_prompt_instructions", self.language)
    
    def get_refinement_instructions(self):
        return translate_string("analyst_prompts", "analyst_report_refinement_instructions", self.language)
    
    def get_readme_instructions(self):
        return translate_string("analyst_prompts", "analyst_readme_instructions", self.language)
    
    def get_readme_prompt(self, project_name, general_report, backend_report, frontend_report, test_report):
        return (
            f"{self.get_readme_instructions()}\n\n"
            f"Project Name: {project_name}\n\n"
            f"General Report:\n{general_report}\n\n"
            f"Backend Report:\n{backend_report}\n\n"
            f"Frontend Report:\n{frontend_report}\n\n"
            f"Test Report:\n{test_report}\n"
        )