# prompt_templates/developer_templates.py

from utils.translation_utils import translate_string

class DeveloperPrompts:
    """
    Class containing prompts for the Developer agent.
    """
    def __init__(self, language):
        self.language = language

    def develop_code_instructions(self):
        return translate_string("developer_prompts", "develop_code_instructions", self.language)

    def structure_prompt_instructions(self):
        return translate_string("developer_prompts", "structure_prompt_instructions", self.language)

    def code_prompt_instruction(self):
        return translate_string("developer_prompts", "code_prompt_instruction", self.language)

    def code_structure_refinement_prompt(self):
        return translate_string("developer_prompts", "code_structure_refinement_prompt", self.language)