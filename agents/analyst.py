"""
analyst.py

This file defines the Analyst class responsible for managing project 
analysis and backlog generation.

Classes:

- Analyst: Handles project analysis and backlog generation.
  - __init__(self, properties_file): Initializes the Analyst with properties file path.
    - properties_file (str): Path to the properties file containing project details.

- generate_backlog(self): Generates a backlog based on project analysis.
- get_properties(self): Retrieves properties related to the project analysis.
"""
from .base_agent import BaseAgent
import configparser
from .prompt_templates.analyst_prompts import AnalystPrompts
from utils.translation_utils import translate_string

class Analyst(BaseAgent):
    """
    Inicializa o agente Analyst.
        Args:
        - model (Ollama): Modelo de linguagem a ser utilizado pelo analista.
        - properties_file (str): Caminho para o arquivo de propriedades do projeto.
        - interactive (bool): Define se o processo será interativo.

    English
    Initializes the Analyst with properties file path.
        Args:
            - properties_file (str): Path to the properties file containing project details.
    """
    def __init__(self, name, llm, properties_file, language, interactive):
        super().__init__(name, llm, language, interactive)
        self.properties_file = properties_file
        self.project_data = self.read_properties()
        self.prompts = AnalystPrompts(self.language)

    def read_properties(self):
        """
        Retrieves properties related to the project
        """
        config = configparser.ConfigParser()
        config.read(self.properties_file)
        return config

    def generate_report(self):
        """
        Generates a backlog based on project analysis.
            Args:
            - model (Ollama): Language model to be used by the team leader.
            - interactive (bool): Defines whether the process will be interactive.
        """
        project_info = "\n".join([f"{section}:\n{', '.join([f'{key}: {value}' for key, value in section_data.items()])}" for section, section_data in self.project_data.items()])
        prompt = f"{self.prompts.get_report_prompt()}\n{project_info}\n\n{self.prompts.get_refinement_instructions()}"
        report = self.evaluate(prompt)
        if self.interactive:
            final_report = self.interact(report)
        else:
            final_report = report
        return self._parse_response(final_report)
    
    def _parse_response(self, response):
        # If the response is a simple string, just return it
        if isinstance(response, str):
            return {translate_string("analyst", "project_analysis_report", self.language): response}
        # If it is a valid JSON dictionary, return it directly
        elif isinstance(response, dict):
            return response
        # Otherwise, return a dictionary with the answer as value
        else:
            return {translate_string("analyst", "project_analysis_report", self.language): response}
    
    def generate_readme(self, general_report, backend_report=None, frontend_report=None, test_report=None, language="en-us"):
        """
        Generates README content based on project reports.

        Args:
        - general_report (str): General project report.
        - backend_report (str): Backend project report.
        - frontend_report (str): Frontend project report.
        - test_report (str): Test project report.
        - language (str): Language code for translation (default is "en-us").

        Returns:
        - str: Generated README content.
        """
        readme_content = f"# {self.project_name}\n\n"
        readme_content += f"## General Report\n\n{general_report}\n\n"

        if backend_report:
            readme_content += f"## Backend Report\n\n{backend_report}\n\n"
        if frontend_report:
            readme_content += f"## Frontend Report\n\n{frontend_report}\n\n"
        if test_report:
            readme_content += f"## Test Report\n\n{test_report}\n\n"

        readme_content += self.prompts.get_readme_instructions(language)
        return readme_content
    
    def get_source_code(self):
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()  
