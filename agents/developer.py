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
"""
import os
import re
from .base_agent import BaseAgent

class Developer(BaseAgent):
    """
    Inicializa o agente Developer.
    
    Args:
        - model (Ollama): Modelo de linguagem a ser utilizado pelo desenvolvedor.
        - name (str): Nome do desenvolvedor.
        - interactive (bool): Define se o processo será interativo.
    """
    def __init__(self, llm, name, interactive=True):
        super().__init__(name, llm)
        self.interactive = interactive

    def develop_code(self, prompt):
        instructions = (
            "Com base no backlog de atividades acima, gere gere todo o código dos arquivos "
            "demandados nas instruções do backlog. Coloque todo o código sequencialmente marcando "
            "início de arquivos com: ##arquivo.ext eo o fim de todo arquivo com: ##end-arquivo.ext ."
        )
        final_prompt = f"{prompt}\n\n{instructions}"
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

    def _sanitize_task_name(self, task):
        """
        Sanitizes the task name to create a valid filename.
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', task[:30])
    
    def process_task(self, node, development_dir, extension, parent_category):
        """
        Processa uma tarefa, gerando a estrutura e código necessários.
        Lida com sub-nós aninhados se fornecido.
        """
        task = node.name

        # Verifica se a tarefa é de criação de pasta, arquivo ou código
        if parent_category.lower().startswith("criar pastas"):
            # Criar pasta para a tarefa corrente
            match = re.search(r'##pastas\/(\w+)', task)
            if match:
                dir_name = match.group(1)  # Nome da pasta
            else:
                print(f"Nome de pasta inválido: {dir_name}. Usando nome padrão.")
                dir_name = "new_folder"
            dir_name = self._sanitize_task_name(dir_name)
            dir_path = os.path.join(development_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            print(f"Pasta criada: {dir_path}")

            # Processar sub-nós e criar pastas para cada um
            for subnode in sorted(node.subnodes, key=lambda x: x.name):
                subnode_task = subnode.name
                match = re.search(r'##pastas\/(\w+)', subnode_task)
                if match:
                    subnode_dir_name = match.group(1)
                else:
                    print(f"Nome de sub-pasta inválido: {subnode_dir_name}. Usando nome padrão.")
                    subnode_dir_name = "new_subfolder"
                subnode_dir_name = self._sanitize_task_name(subnode_dir_name)
                subnode_dir_path = os.path.join(dir_path, subnode_dir_name)
                os.makedirs(subnode_dir_path, exist_ok=True)
                print(f"Sub-pasta criada: {subnode_dir_path}")

        elif parent_category.lower().startswith("criar arquivos"):
            # Criar arquivo para a tarefa corrente
            # Buscar padrão "nomedoarquivo.ext"
            match = re.search(r'##(\w+)\/(\w+\.\w+)', task)
            if match:
                file_name = match.group(1)  # Nome do arquivo completo
            else:
                print(f"Nome de arquivo inválido: {file_name}. Usando nome padrão.")
                file_name = f"new_file.{extension}"

            if file_name:
                file_name = self._sanitize_task_name(file_name)
                file_path = os.path.join(development_dir, file_name)

                # Garantir que os diretórios no caminho existam
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                open(file_path, 'w').close()
                print(f"Arquivo criado: {file_path}")

                # Processar sub-nós e criar arquivos para cada um
                for subnode in sorted(node.subnodes, key=lambda x: x.name):
                    subnode_task = subnode.name
                    subnode_file_name = None
                    match = re.search(r'##(\w+)\/(\w+\.\w+)', subnode_task)
                    
                    if match:
                        subnode_file_name = match.group(1)  # Nome do arquivo completo
                    else:
                        print(f"Nome de sub-arquivo inválido: {subnode_task}. Pulando criação do sub-arquivo.")
                    if subnode_file_name:
                        subnode_file_name = self._sanitize_task_name(subnode_file_name)
                        subnode_file_path = os.path.join(development_dir, subnode_file_name)

                        # Garantir que os diretórios no caminho existam
                        os.makedirs(os.path.dirname(subnode_file_path), exist_ok=True)

                        open(subnode_file_path, 'w').close()
                        print(f"Sub-arquivo criado: {subnode_file_path}")

        elif parent_category.lower().startswith("criar classes e funções") or \
                parent_category.lower().startswith("criar") and \
                "funções" in parent_category.lower() or \
                "migrations" in parent_category.lower() or \
                "métodos" in parent_category.lower() or \
                "rotas" in parent_category.lower() or \
                "testes" in parent_category.lower() or \
                "mocks" in parent_category.lower() or \
                "helpers" in parent_category.lower() or \
                "utilitários" in parent_category.lower() or \
                "outras atividades" in parent_category.lower() or \
                "##" in task :

            # Verifica se é um nó pai com ##
            if "##" in task:
                # Processar nó pai com ## como um arquivo
                match = re.search(r'##(\w+)\/(\w+\.\w+)', task)
                if match:
                    file_name = match.group(0)
                else:
                    print(f"Nome de arquivo inválido: {task}. Usando nome padrão.")
                    file_name = f"new_file.{extension}"
                file_name = self._sanitize_task_name(match)
                file_path = os.path.join(development_dir, match)
                open(file_path, 'w').close()
                print(f"Arquivo criado: {file_path}")

                # Processar sub-nós como funções/classes dentro do arquivo criado
                if node.subnodes:
                    for subnode in sorted(node.subnodes, key=lambda x: x.name):
                        subnode_task_name = subnode.name
                        subnode_development_dir = os.path.join(development_dir, file_name)
                        self.process_task(subnode, subnode_development_dir, extension, task)

            else:
                # Criar código dentro de um arquivo existente ou novo
                task_description = task.replace('*', '').strip()
                structure_prompt = f"Gere a estrutura de pastas e arquivos necessária para a tarefa: {task_description}"
                print(f"Processando estrutura para a tarefa: {task_description}")
                try:
                    structure = self.generate_structure(structure_prompt)
                except Exception as e:
                    print(f"Erro ao gerar a estrutura para a tarefa '{task_description}': {e}")
                    return

                os.makedirs(development_dir, exist_ok=True)
                task_name = self._sanitize_task_name(task_description)
                structure_file_path = os.path.join(development_dir, f"estrutura_{task_name}.txt")
                with open(structure_file_path, 'w') as f:
                    if isinstance(structure, dict):
                        for key, value in structure.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(structure)

                code_prompt = f"Gere o código necessário para a tarefa: {task_description} observando também a estrutura criada para a mesma: {structure}"
                print(f"Processando código para a tarefa: {task_description}")
                try:
                    code = self.develop_code(code_prompt)
                except Exception as e:
                    print(f"Erro ao gerar o código para a tarefa '{task_description}': {e}")
                    return

                # Geração de um nome de arquivo mais curto e significativo
                sanitized_task_name = re.sub(r'[^a-zA-Z0-9]', '_', task_description)
                filename = f"{sanitized_task_name}.{extension}"
                code_file_path = os.path.join(development_dir, filename)

                with open(code_file_path, 'w') as f:
                    if isinstance(code, dict):
                        for key, value in code.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(code)

                print(f"Código gerado e salvo em: {code_file_path}")

                # Processar sub-nós, se houver
                if node.subnodes:
                    for subnode in sorted(node.subnodes, key=lambda x: x.name):
                        subnode_task_name = subnode.name
                        subnode_development_dir = os.path.join(development_dir, task_name)
                        os.makedirs(subnode_development_dir, exist_ok=True)
                        self.process_task(subnode, subnode_development_dir, extension, task_description)
    
    def get_source_code(self):
        return super().get_source_code()
