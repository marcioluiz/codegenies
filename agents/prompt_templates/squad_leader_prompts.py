# prompt_templates/squad_leader_templates.py

from utils.translation_utils import translate_string

class SquadLeaderPrompts:

    # Instructions for creating the project general report
    def get_general_report_instructions(self, language):
        return translate_string("squad_leader_prompts", "squad_leader_general_report_instructions", language)

    # Backend backlog template
    def get_backend_backlog_model(self, language):
        return translate_string("squad_leader_prompts", "backend_backlog_model", language)

    # Instructions for creating the backend activity backlog
    def get_backend_instructions(self, language):
        return translate_string("squad_leader_prompts", "backend_instructions", language)

    # Frontend backlog template
    def get_frontend_backlog_model(self, language):
        return translate_string("squad_leader_prompts", "frontend_backlog_model", language)

    # Instructions for creating the frontend activity backlog
    def get_frontend_instructions(self, language):
        return translate_string("squad_leader_prompts", "frontend_instructions", language)

    # Tests backlog template
    def get_tests_backlog_model(self, language):
        return translate_string("squad_leader_prompts", "tests_backlog_model", language)

    # Instructions for creating the tests activity backlog
    def get_tests_instructions(self, language):
        return translate_string("squad_leader_prompts", "tests_instructions", language)