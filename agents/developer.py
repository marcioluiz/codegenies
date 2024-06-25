# agents/developer.py
import os
import re
from .base_agent import BaseAgent

class Developer(BaseAgent):
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
            # Criar pasta
            dir_name = task.replace('##', '').strip()
            # Buscar padrão "##pastas/nome_da_pasta"
            match = re.search(r'##pastas/([^\\/*?:"<>|]+)', dir_name)
            if match:
                dir_name = match.group(1)  # Nome da pasta
            else:
                print(f"Nome de pasta inválido: {dir_name}. Usando nome padrão.")
                dir_name = "new_folder"
            dir_name = self._sanitize_task_name(dir_name)
            dir_path = os.path.join(development_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            print(f"Pasta criada: {dir_path}")

        elif parent_category.lower().startswith("criar arquivos"):
            # Criar arquivo
            file_name = task.replace('##', '').strip()
            # Buscar padrão "nomedoarquivo.ext"
            match = re.search(r'([^\\/*?:"<>|]+)\.([a-zA-Z]+)$', file_name)
            if match:
                file_name = match.group(0)  # Nome do arquivo completo
            else:
                print(f"Nome de arquivo inválido: {file_name}. Usando nome padrão.")
                file_name = f"new_file.{extension}"
            file_name = self._sanitize_task_name(file_name)
            file_path = os.path.join(development_dir, file_name)
            open(file_path, 'w').close()
            print(f"Arquivo criado: {file_path}")

        elif parent_category.lower().startswith("criar classes e funções"):
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
                for subnode in node.subnodes:
                    subnode_task_name = subnode.name
                    subnode_development_dir = os.path.join(development_dir, task_name)
                    os.makedirs(subnode_development_dir, exist_ok=True)
                    self.process_task(subnode, subnode_development_dir, extension, task_description)

    def get_filename_from_code(self, code, extension=None):
        if not isinstance(code, str):
            code = str(code)

        # Expressão regular para encontrar o padrão "arquivo.ext"
        pattern_filename_ext = re.compile(r'["\'##]*(.*)\.(\w+)', re.IGNORECASE)
        match_filename_ext = pattern_filename_ext.search(code)

        if match_filename_ext:
            filename = match_filename_ext.group(1)
            filename_with_extension = f"{filename}.{extension}"
            return filename_with_extension

        # Expressão regular para encontrar o padrão "criar arquivo" ou "create file"
        pattern_instruction = re.compile(r'(?:criar arquivo|create file)[\s:]*["\'##]*', re.IGNORECASE)
        match_instruction = pattern_instruction.search(code)
        
        if not match_instruction:
            print("Nenhum padrão 'criar arquivo' ou 'create file' encontrado no código.")
            return None
        else:
            # Extrai a parte do código após o padrão "criar arquivo" ou "create file"
            code_after_instruction = code[match_instruction.end():]

            # Expressão regular para extrair o nome do arquivo após o padrão "criar arquivo" ou "create file"
            pattern_filename = re.compile(r'["\'##]*([^"\':*]+)\.(\w+)', re.IGNORECASE)
            match_filename = pattern_filename.search(code_after_instruction)

            if not match_filename:
                print("Nenhum nome de arquivo encontrado após o padrão 'criar arquivo' ou 'create file'. Usando nome padrão.")
                return f"new_file.{extension}"

            filename = match_filename.group(1)
            file_extension = match_filename.group(2)

            # Usar a extensão fornecida no argumento da função, se não for None, caso contrário, usar a encontrada no código
            final_extension = extension if extension else file_extension
            filename_with_extension = f"{filename}.{final_extension}"
            return filename_with_extension

    def get_source_code(self):
        return super().get_source_code()
