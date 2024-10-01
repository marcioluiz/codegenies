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
    
    def develop_code_with_tests_instructions(self):
        return translate_string("developer_prompts", "develop_code_with_tests_instructions", self.language)
    
    def check_syntax_of_generated_code(self):
        return translate_string("developer_prompts", "check_syntax_of_generated_code", self.language)
    
    def execute_tests_and_generated_code(self):
        return translate_string("developer_prompts", "execute_tests_and_generated_code", self.language)
    
    def evaluate_test_results(self):
        return translate_string("developer_prompts", "evaluate_test_results", self.language)
    
    def correct_code_based_on_test_results(self):
        return translate_string("developer_prompts", "correct_code_based_on_test_results", self.language)

    def structure_prompt_instructions(self):
        return translate_string("developer_prompts", "structure_prompt_instructions", self.language)

    def code_prompt_instruction(self):
        return translate_string("developer_prompts", "code_prompt_instruction", self.language)

    def code_structure_refinement_prompt(self):
        return translate_string("developer_prompts", "code_structure_refinement_prompt", self.language)