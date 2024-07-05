# prompt_templates/developer_templates.py

from main import translate_string

class DeveloperPrompts:
    """
    Class containing prompts for the Developer agent.
    """
    def __init__(self, language):
        self.language = language

    @staticmethod
    def develop_code_instructions():
        return translate_string("developer_prompts", "develop_code_instructions", self.language)

    @staticmethod
    def structure_prompt_instructions():
        return translate_string("developer_prompts", "structure_prompt_instructions", self.language)

    @staticmethod
    def code_prompt_instruction():
        return translate_string("developer_prompts", "code_prompt_instruction", self.language)

    @staticmethod
    def code_structure_refinement_prompt():
        return translate_string("developer_prompts", "code_structure_refinement_prompt", self.language)