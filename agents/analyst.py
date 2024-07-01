"""
analyst.py

Este arquivo define a classe para o agente Analista. 
A classe herda da classe base definida em `base_agent.py` e 
implementa métodos específicos para as suas tarefas.

Classes:

- Analyst: Classe do agente (Analista).
  - __init__(self, model, [name], interactive=False): Inicializa o agente.
    - model (Ollama): Modelo de linguagem a ser utilizado pelo agente.
    - name (str): Nome do agente (apenas para Developer).
    - interactive (bool): Define se o processo será interativo.

English version:

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
from .prompt_templates import AnalystPrompts as prompt_templates

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
    def __init__(self, llm, properties_file, interactive=True):
        super().__init__("Analista", llm)
        self.properties_file = properties_file
        self.project_data = self.read_properties()
        self.interactive = interactive

    def read_properties(self):
        """
        Recupera as propriedades do projeto

        Engish:

        Retrieves properties related to the project
        """
        config = configparser.ConfigParser()
        config.read(self.properties_file)
        return config

    def generate_report(self):
        """
        Gera o relatório inicial do projeto.
            Args:
            - model (Ollama): Modelo de linguagem a ser utilizado pelo líder de equipe.
            - interactive (bool): Define se o processo será interativo.

        English:

        Generates a backlog based on project analysis.
            Args:
            - model (Ollama): Language model to be used by the team leader.
            - interactive (bool): Defines whether the process will be interactive.
        """
        project_info = "\n".join([f"{section}:\n{', '.join([f'{key}: {value}' for key, value in section_data.items()])}" for section, section_data in self.project_data.items()])
        prompt = f"{prompt_templates.analyst_report_prompt_instructions}\n{project_info}\n\n{prompt_templates.analyst_report_refinement_instructions}"
        report = self.evaluate(prompt)
        if self.interactive:
            final_report = self.interact(report)
        else:
            final_report = report
        return self._parse_response(final_report)
    
    def _parse_response(self, response):
        # Se a resposta for uma string simples, apenas retorne-a
        # If the response is a simple string, just return it
        if isinstance(response, str):
            return {"Relatório de Análise": response}
        # Se for um dicionário JSON válido, retorne-o diretamente
        # If it is a valid JSON dictionary, return it directly
        elif isinstance(response, dict):
            return response
        # Caso contrário, retorne um dicionário com a resposta como valor
        # Otherwise, return a dictionary with the answer as value
        else:
            return {"Relatório de Análise": response}
    
    def get_source_code(self):
        # Obtém o código-fonte da classe base
        # Se a resposta for uma string simples ela é retornada
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()  
