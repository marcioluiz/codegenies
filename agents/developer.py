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

This file defines the base class Developer and its subclasses (BackendDeveloper, FrontendDeveloper).

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

    def generate_structure(self, prompt):
        structure = self.evaluate(prompt)
        if self.interactive:
            final_structure = self.interact(structure)
        else:
            final_structure = structure
        return self._parse_structure_response(final_structure)
    
    def _parse_structure_response(self, response):
        if isinstance(response, str):
            return {"Estrutura": response}
        elif isinstance(response, dict):
            return response
        else:
            return {"Estrutura": response}
    
    def remove_pattern(self, text, pattern):
        return re.sub(pattern, '', text)

    def _sanitize_task_name(self, task):
        """
        Substituir caracteres não alfanuméricos e truncar até 30 caracteres.
        Argumentos:
            - tarefa (str): Descrição da tarefa.
        Retorna:
            - str: nome do arquivo higienizado.

        English:
        
        Sanitizes the task name to create a valid filename.
        Args:
            - task (str): Task description.
        Returns:
            - str: Sanitized filename.
        """
        # Substitua caracteres não alfanuméricos por sublinhados e trunque o nome da tarefa para 30 caracteres
        # Replace non-alphanumeric characters with underscores and truncate the task name to 30 characters
        return re.sub(r'[^a-zA-Z0-9]', '_', task[:30])

    # Função para processar criação de pastas
    # Function to process folder creation
    def process_create_folder(self, task, base_dir):
        match = re.search(r'##pastas\/(\w+)', task)
        if match:
            dir_name = match.group(1)
            dir_name = unidecode.unidecode(dir_name)
            dir_name = self._sanitize_task_name(dir_name)
            dir_name = self.remove_pattern(dir_name, '##(\w+)\/')
            dir_path = os.path.join(base_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            print(f"Pasta criada: {dir_path}")
            return dir_path
        else:
            print(f"Nome de pasta inválido: {task}. Usando nome padrão.")
            return base_dir

    # Função para processar criação de arquivos
    # Function to process file creation
    def process_create_file(self, task, base_dir):
        match = re.search(r'##(\w+)\/(\w+\.\w+)', task)
        if match:
            file_name = match.group(2)
            file_name = unidecode.unidecode(file_name)
            file_name = self.remove_pattern(file_name, '##(\w+)\/')
            file_name_sanitized = file_name.replace('_', '-')
            file_path = os.path.join(base_dir, file_name_sanitized)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            return file_path
        else:
            print(f"Nome de arquivo inválido: {task}. Usando nome padrão.")
            return None

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

    def process_task(self, node, development_dir, parent_category):
        """
        Processa uma tarefa, gerando a estrutura e código necessários.
        Lida com sub-nós aninhados se fornecido.

        English:

        Processes a task, generating the necessary structure and code.
        Handles nested subnodes if provided.
        """
        task = node.name

        # Processa tarefas dos tipos previstos (classes, funções, etc.)
        # Process tasks of the expected types (classes, functions, etc.)
        if parent_category.lower().startswith("**criar classes e funções") or \
                parent_category.lower().startswith("**criar") and \
                ("arquivos" in parent_category.lower() or \
                 "funções" in parent_category.lower() or \
                 "migrations" in parent_category.lower() or \
                 "métodos" in parent_category.lower() or \
                 "rotas" in parent_category.lower() or \
                 "testes" in parent_category.lower() or \
                 "mocks" in parent_category.lower() or \
                 "helpers" in parent_category.lower() or \
                 "utilitários" in parent_category.lower() or \
                 "outras atividades" in parent_category.lower()) or \
                "##" in task:
            
            if "##" in task:
                # Testa se encontra o padrão de nome de arquivo "nomedoarquivo.tipo.ext"
                # Tests for the filename pattern "filename.type.ext"  
                match = re.search(r'##(\w+)\/(\w+\.\w+\.\w+)', task)
                if not match:
                    # Testa se encontra o padrão de nome de arquivo "nomedoarquivo.ext"
                    # Tests for the filename pattern "filename.ext" 
                    match = re.search(r'##(\w+)\/(\w+\.\w+)', task)
                if match:
                    file_name = match.group(2)
                    file_name = unidecode.unidecode(file_name)
                    file_name = self.remove_pattern(file_name, '##(\w+)\/')
                    file_path = os.path.join(development_dir, file_name)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    self.generate_and_write_code(file_path, task)

                    for subnode in node.subnodes:
                        self.process_task(subnode, development_dir, task)

            else:
                task_description = task.replace('*', '').strip()
                structure_prompt = f"{prompt_templates.structure_prompt_instructions}\n\n{task_description}"
                print(f"Processando estrutura para a tarefa: {task_description}")
                try:
                    structure = self.generate_structure(structure_prompt)
                except Exception as e:
                    print(f"Erro ao gerar a estrutura para a tarefa '{task_description}': {e}")
                    return

                os.makedirs(development_dir, exist_ok=True)
                task_name = self._sanitize_task_name(task_description)
                task_name = unidecode.unidecode(task_name)
                task_name = self.remove_pattern(task_name, '##(\w+)\/')
                structure_file_path = os.path.join(development_dir, f"estrutura_{task_name}.txt")
                with open(structure_file_path, 'w') as f:
                    if isinstance(structure, dict):
                        for key, value in structure.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(structure)

                code_prompt = f"{prompt_templates.code_prompt_instruction}{task_description}{prompt_templates.code_structure_refinement_prompt}{structure}"
                print(f"Processando código para a tarefa: {task_description}")
                try:
                    code = self.develop_code(code_prompt)
                except Exception as e:
                    print(f"Erro ao gerar o código para a tarefa '{task_description}': {e}")
                    return

                file_name = self._sanitize_task_name(task_description)
                file_name = unidecode.unidecode(file_name)
                file_name = self.remove_pattern(file_name, '##(\w+)\/')
                code_file_path = os.path.join(development_dir, file_name)
                os.makedirs(os.path.dirname(code_file_path), exist_ok=True)

                with open(code_file_path, 'w') as f:
                    if isinstance(code, dict):
                        for key, value in code.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(code)

                print(f"Código gerado e salvo em: {code_file_path}")

                for subnode in sorted(node.subnodes, key=lambda x: x.name):
                    subnode_task_name = subnode.name
                    subnode_development_dir = os.path.join(development_dir, subnode_task_name)
                    os.makedirs(subnode_development_dir, exist_ok=True)
                    self.process_task(subnode, subnode_development_dir, task_description)
    
    def get_source_code(self):
        # Obtém o código-fonte da classe base
        # Se a resposta for uma string simples ela é retornada
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()
