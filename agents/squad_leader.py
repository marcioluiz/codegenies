# agents/squad_leader.py
import os
from .base_agent import BaseAgent
import json

class SquadLeader(BaseAgent):
    def __init__(self, llm):
        super().__init__("Líder de Equipe", llm)

    def generate_general_report(self, analyst_report):
        instructions = "Seja um bom analista de requisitos e crie um relatório bem completo. Com base no relatório do analista acima, gere um relatório geral do projeto, abordando todos os aspectos relevantes: Backend, Frontend e Testes: classes, funções e uso geral do framework escolhido conforme relatório acima, bem como todas as tarefas associadas."
        prompt = f"{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        return self._parse_response(response)

    def generate_backend_backlog(self, analyst_report):
        instructions = "Com base no relatório do Analista acima, gere o backlog de atividades de backend abordando tudo o que há pra ser desenvolvido no módulo de Backend: listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto. Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias. Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter. Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
        prompt = f"{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        return self._parse_response(response)

    def generate_frontend_backlog(self, analyst_report):
        instructions = "Com base no relatório do Analista acima, gere o backlog de atividades de frontend abordando tudo o que há pra ser desenvolvido no módulo de Frontend: listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto. Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias. Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter. Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
        prompt = f"{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        return self._parse_response(response)

    def generate_test_backlog(self, analyst_report):
        instructions = "Com base no relatório do Analista acima, gere o backlog de atividades de testes abordando tudo o que há pra ser desenvolvido no módulo de Testes: listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto. Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias. Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter. Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
        prompt = f"{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        return self._parse_response(response)

    def _parse_response(self, response):
        # Se a resposta for uma string simples, apenas retorne-a
        if isinstance(response, str):
            return {"Relatório Geral": response}
        # Se for um dicionário JSON válido, retorne-o diretamente
        elif isinstance(response, dict):
            return response
        # Caso contrário, retorne um dicionário com a resposta como valor
        else:
            return {"Relatório Geral": response}
        
    def save_content(self, dir_path, filename, content):
        """
        Salva o conteúdo do líder de equipe em um arquivo.

        Args:
            dir_path (str): O diretório onde o arquivo será salvo.
            filename (str): O nome do arquivo.
            content (str): O conteúdo a ser salvo no arquivo.

        Returns:
            str: O conteúdo do líder de equipe.
        """
        with open(os.path.join(dir_path, filename), 'w') as file:
            file.write(content)
        
        return content
        
    def get_source_code(self):
        return super().get_source_code()  # Obtém o código-fonte da classe base
