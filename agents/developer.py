"""
developer.py

Este arquivo define a classe para agentes Desenvolvedores. 
A classe herda da classe base definida em `base_agent.py` e 
implementa métodos específicos para as suas tarefas.

Classes:

- Developer: Classe do agente (Desenvolvedor).
  - __init__(self, model, [name], interactive=False): Inicializa o agente.
    - model (Ollama): Modelo de linguagem a ser utilizado pelo agente.
    - name (str): Nome do agente (apenas para Developer).
    - interactive (bool): Define se o processo será interativo.

English:

This file defines the base class Developer and its subclasses:
 (BackendDeveloper, FrontendDeveloper).

Classes:

- Developer: Base class for developers.
  - __init__(self, llm, role): Initializes a developer with a language model and role.
    - llm (Ollama): Language model to be used by the developer.
    - role (str): Role of the developer (e.g., "Backend Developer", "Frontend Developer").

- BackendDeveloper: Subclass of Developer for backend development tasks.
- FrontendDeveloper: Subclass of Developer for frontend development tasks.
"""
import os
import re
import unidecode
from .base_agent import BaseAgent
from .prompt_templates import DeveloperPrompts as prompt_templates

class Developer(BaseAgent):
    """
    Inicializa o agente Developer.
    
    Args:
        - model (Ollama): Modelo de linguagem a ser utilizado pelo desenvolvedor.
        - name (str): Nome do desenvolvedor.
        - interactive (bool): Define se o processo será interativo.

    English:

    Initializes a developer with a language model and role.

        Args:
            - llm (Ollama): Language model to be used by the developer.
            - name (str): Name of the developer (e.g., "Backend Developer", "Frontend Developer").
            - interactive (bool): Defines if the process should run with interactions with the user.
    """
    def __init__(self, llm, name, interactive=True):
        super().__init__(name, llm)
        self.interactive = interactive

    def develop_code(self, prompt):
        final_prompt = f"{prompt}\n\n{prompt_templates.develop_code_instructions}"
        code = self.evaluate(final_prompt)
        if self.interactive:
            final_code = self.interact(code)
        else:
            final_code = code
        return self._parse_code_response(final_code)

    def _parse_code_response(self, response):
        if isinstance(response, str):
            return {"Código": response}
        elif isinstance(response, dict):
            return response
        else:
            return {"Código": response}
    
    def sanitize_file_name(self, file_name):
        """
        Sanitza um nome de arquivo usando a biblioteca unicode e
        remove o padrão '##(\w+)\/' usando a função re.sub().

        English:
        
        Sanitizes a filename using unicode library and
        removes the pattern '##(\w+)\/' using the re.sub() function.
        """
        file_name = unidecode.unidecode(file_name)
        file_name = re.sub('##(\w+)\/', '', file_name)
        return file_name.lower()

    # Função para gerar e escrever código em arquivos
    # Function to generate and write code to files
    def generate_and_write_code(self, file_path, task_description):
        code_prompt = f"{prompt_templates.code_prompt_instruction}{task_description}"
        print(f"Processando código para a tarefa: {task_description}")
        try:
            code = self.develop_code(code_prompt)
        except Exception as e:
            print(f"Erro ao gerar o código para a tarefa '{task_description}': {e}")
            return

        with open(file_path, 'w') as f:
            if isinstance(code, dict):
                for key, value in code.items():
                    f.write(f"{key}: {value}\n")
            else:
                f.write(code)

        print(f"Código gerado e salvo em: {file_path}")

    def process_task(self, node, development_dir):
        """
        Processa uma tarefa, gerando a estrutura e código necessários.
        Lida com sub-nós aninhados se fornecido.

        English:

        Processes a task, generating the necessary structure and code.
        Handles nested subnodes if provided.
        """
        task = node.name
            
        if "##" in task:
            file_name = ''
            
            # Lista de padrões a serem testados juntamente com o índice do grupo a ser extraído
            # Patterns list to be tested along with the right group indexes to be extracted
            patterns = [
                # 1. "##nomedoarquivo.ext"
                #    "##filename.ext"
                (r'##(((\w+)|(\w+\-\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 1),
                # 2. "##nomedapasta/nomearquivo.ext ou ##nomeda-pasta/nomearquivo.ext" 
                #    "##foldername/filename.ext" or "##folder-name/filename.ext" 
                (r'##((\w+\D\w+))\/((\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 3),
                # 3. "##pasta/arquivo.ext" ou "##nome-pasta/arquivo.ext" e final "nome-arquivo.ext" ou "nome.arquivo.ext"
                #    "##folder/file.ext" or "##folder-name/file.ext" and ending "file-name.ext" or "file-name.ext"
                (r'##((\w+\D\w+))\/(((\w+\D\w+)|(\w+\D\w+\D\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 3),
                # 4. "##pasta1/pasta2/nomedoarquivo.ext" ou "##pasta1/pasta2-nome/nomedoarquivo.ext" e final "nomedo-arquivo.ext" ou "nomedo.arquivo.ext"
                #    "##folder1/folder2/filename.ext" or "##folder1/folder2-name/filename.ext" and ending "filename.ext" or "filename.ext"
                (r'##(((\w+)\/(\w+\D\w+))|((\w+)\/(\w+\D\w+)\/(\w+\D\w+)))\/((\w+\D\w+\D\w+|\w+\D\w+\D\w+\D\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 9)
            ]

            # Itera sobre os padrões para encontrar um match
            # Iterate over the patterns to find a match
            for pattern, group_index in patterns:
                match = re.search(pattern, task)
                if match:
                    # Pega o grupo correto que deu match
                    # Get the correct group that matched
                    file_name = match.group(group_index)  
                    break

            if file_name != '':
                file_name = self.sanitize_file_name(file_name)
                file_path = os.path.join(development_dir, file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                if file_path:
                    all_subtasks = [subnode.name for subnode in node.subnodes]
                    all_subtasks_str = "\n".join(all_subtasks)
                    complete_task_description = f"{task}\n{all_subtasks_str}"
                    self.generate_and_write_code(file_path, complete_task_description)
           
    def get_source_code(self):
        # Obtém o código-fonte da classe base
        # Se a resposta for uma string simples ela é retornada
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()
