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
"""
import os
from .base_agent import BaseAgent
import configparser

class Analyst(BaseAgent):
    """
    Inicializa o agente Analyst.
        Args:
        - model (Ollama): Modelo de linguagem a ser utilizado pelo analista.
        - properties_file (str): Caminho para o arquivo de propriedades do projeto.
        - interactive (bool): Define se o processo será interativo.
    """
    def __init__(self, llm, properties_file, interactive=True):
        super().__init__("Analista", llm)
        self.properties_file = properties_file
        self.project_data = self.read_properties()
        self.interactive = interactive

    def read_properties(self):
        config = configparser.ConfigParser()
        config.read(self.properties_file)
        return config

    def generate_report(self):
        """
        Gera o relatório inicial do projeto.
            Args:
            - model (Ollama): Modelo de linguagem a ser utilizado pelo líder de equipe.
            - interactive (bool): Define se o processo será interativo.
        """
        project_info = "\n".join([f"{section}:\n{', '.join([f'{key}: {value}' for key, value in section_data.items()])}" for section, section_data in self.project_data.items()])
        prompt = f"Gere um relatório de análise do projeto completo com base nas propriedades a seguir e leve cada uma delas em consideração no seu relatório:\n{project_info}\n\n Acresente após uma análise rápida de total de pastas de módulos e classes de código de no máximo 04 paragráfos ao final do relatório:\n[Insira aqui a análise rápida do projeto]"
        report = self.evaluate(prompt)
        if self.interactive:
            final_report = self.interact(report)
        else:
            final_report = report
        return self._parse_response(final_report)
    
    def _parse_response(self, response):
        # Se a resposta for uma string simples, apenas retorne-a
        if isinstance(response, str):
            return {"Relatório de Análise": response}
        # Se for um dicionário JSON válido, retorne-o diretamente
        elif isinstance(response, dict):
            return response
        # Caso contrário, retorne um dicionário com a resposta como valor
        else:
            return {"Relatório de Análise": response}
    
    def generate_structure(self, prompt):
        instructions = "Com base no backlog de atividades acima, gere gere toda a estrutura de pastas e arquivos demandados nas instruções do backlog. Coloque todo as instruções sequencialmente marcando início e fim de cada estrutura com: ##begin-structure-1 e ao fim de todo arquivo com: ##end-structure-1 ."
        final_prompt = f"{prompt}\n\n{instructions}"
        structure = self.evaluate(final_prompt)
        final_structure = self.interact(structure)
        return self._parse_structure_response(final_structure)
    
    def _parse_structure_response(self, response):
        # Se a resposta for uma string simples, apenas retorne-a
        if isinstance(response, str):
            return {"Estrutura": response}
        # Se for um dicionário JSON válido, retorne-o diretamente
        elif isinstance(response, dict):
            return response
        # Caso contrário, retorne um dicionário com a resposta como valor
        else:
            return {"Estrutura": response}
    
    def get_source_code(self):
        return super().get_source_code()  # Obtém o código-fonte da classe base
