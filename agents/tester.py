"""
tester.py

Este arquivo define a classe para agentes Testers. 
A classe herda da classe base definida em `base_agent.py` e 
implementa métodos específicos para as suas tarefas.

Classes:

- Tester: Classe do agente (Tester).
  - __init__(self, model, [name], interactive=False): Inicializa o agente.
    - model (Ollama): Modelo de linguagem a ser utilizado pelo agente.
    - name (str): Nome do agente (apenas para Developer).
    - interactive (bool): Define se o processo será interativo.

English version:

This file defines the Tester agent class.
The class inherits from the base class defined in `base_agent.py` and
implements specific methods for its tasks.

Classes:

- Tester: Agent class (Tester).
  - __init__(self, llm, interactive=True): Initializes the agent.
    - llm (Ollama): Language model to be used by the agent.
    - interactive (bool): Defines if the process will be interactive.

"""
import os
import re
from agents import Developer

class Tester(Developer):
    def __init__(self, llm, interactive=True):
        """
        Inicializa o agente Tester.

        Args:
            - model (Ollama): Modelo de linguagem a ser utilizado pelo tester.
            - interactive (bool): Define se o processo será interativo.
        
        English:
            
        Initializes the Tester agent.

        Args:
            - llm (Ollama): Language model to be used by the tester.
            - interactive (bool): Defines if the process will be interactive.
            
        """
        super().__init__(llm, "Tester")
        self.interactive = interactive

    def develop_tests(self, prompt):
        tests = self.evaluate(prompt)
        if self.interactive:
            final_tests = self.interact(tests)
        else:
            final_tests = tests
        return self._parse_tests_response(final_tests)
    
    def _parse_tests_response(self, response):
        if isinstance(response, str):
            return {"Teste": response}
        elif isinstance(response, dict):
            return response
        else:
            return {"Teste": response}
        
    def _sanitize_task_name(self, task):
        """
        Limpa o nome da tarefa para criar um nome de arquivo válido.
        
        English:

        Sanitizes the task name to create a valid filename.
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', task[:30])
    
    def get_source_code(self):
        # Obtém o código-fonte da classe base
        # Se a resposta for uma string simples ela é retornada
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()