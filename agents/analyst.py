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
from main import translate_string

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
        prompts = AnalystPrompts(self.language)
        project_info = "\n".join([f"{section}:\n{', '.join([f'{key}: {value}' for key, value in section_data.items()])}" for section, section_data in self.project_data.items()])
        prompt = f"{prompts.get_report_prompt()}\n{project_info}\n\n{prompts.get_refinement_instructions()}"
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
    
    def get_source_code(self):
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()  
