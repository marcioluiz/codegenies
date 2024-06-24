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


    def save_content(self, dir_path, filename, content):
        """
        Salva o conteúdo do desenvolvedor em um arquivo.

        Args:
            dir_path (str): O diretório onde o arquivo será salvo.
            filename (str): O nome do arquivo.
            content (str): O conteúdo a ser salvo no arquivo.

        Returns:
            str: O conteúdo do desenvolvedor.
        """
        with open(os.path.join(dir_path, filename), 'w') as file:
            file.write(content)
        return content

    def _sanitize_task_name(self, task):
        """
        Sanitizes the task name to create a valid filename.
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', task[:30])
    
    def process_task(self, task, development_dir, extension, subnodes=None):
        """
        Processes a task, generating the required structure and code.
        Handles nested subnodes if provided.
        """
        structure_prompt = f"Gere a estrutura de pastas e arquivos necessária para a tarefa: {task}"
        print(f"Processando estrutura para a tarefa: {task}")
        try:
            structure = self.generate_structure(structure_prompt)
        except Exception as e:
            print(f"Erro ao gerar a estrutura para a tarefa '{task}': {e}")
            return

        os.makedirs(development_dir, exist_ok=True)
        task_name = self._sanitize_task_name(task)
        structure_file_path = os.path.join(development_dir, f"estrutura_{task_name}.txt")
        with open(structure_file_path, 'w') as f:
            if isinstance(structure, dict):
                for key, value in structure.items():
                    f.write(f"{key}: {value}\n")
            else:
                f.write(structure)

        code_prompt = f"Gere o código necessário para a tarefa: {task} observando também a estrutra criada para a mesma: {structure}"
        print(f"Processando código para a tarefa: {task}")
        try:
            code = self.develop_code(code_prompt)
        except Exception as e:
            print(f"Erro ao gerar o código para a tarefa '{task}': {e}")
            return

        filename = self.get_filename_from_code(code, extension)
        code_file_path = os.path.join(development_dir, filename)
        with open(code_file_path, 'w') as f:
            if isinstance(code, dict):
                for key, value in code.items():
                    f.write(f"{key}: {value}\n")
            else:
                f.write(code)
        
        # Process subnodes if provided
        if subnodes:
            for subnode in subnodes:
                subnode_task_name = subnode.name
                subnode_development_dir = os.path.join(development_dir, task_name)
                os.makedirs(subnode_development_dir, exist_ok=True)
                self.process_task(subnode_task_name, subnode_development_dir, extension, subnode.subnodes)

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

    def process_backlog(self, backlog, development_dir, extension):
        def is_new_task_line(line):
            return bool(re.match(r'^[A-Za-z0-9]+\.', line.strip()))

        tasks = backlog.splitlines()
        current_task = []
        for line in tasks:
            if is_new_task_line(line) and current_task:
                task_text = "\n".join(current_task).strip()
                self.process_task(task_text, development_dir, extension)
                current_task = [line]
            else:
                current_task.append(line)

        if current_task:
            task_text = "\n".join(current_task).strip()
            self.process_task(task_text, development_dir, extension)

    def develop_code_from_backlog(self, backlog, development_dir):
        dir_pattern = re.compile(r'create directory[:\s]*["\'**]*(.*?)["\'**]*', re.IGNORECASE)
        file_pattern = re.compile(r'create file[:\s]*["\'**]*(.*?)["\'**]*', re.IGNORECASE)

        tasks = backlog.splitlines()
        for task in tasks:
            if not isinstance(task, str):
                task = str(task)

            dir_match = dir_pattern.search(task)
            if dir_match:
                dir_path = os.path.join(development_dir, dir_match.group(1))
                os.makedirs(dir_path, exist_ok=True)
                print(f"Diretório criado: {dir_path}")
                continue

            file_match = file_pattern.search(task)
            if file_match:
                file_path = os.path.join(development_dir, file_match.group(1))
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write("")
                print(f"Arquivo criado: {file_path}")
                continue

            if 'create class' in task.lower():
                print(f"Classe identificada: {task.strip()}")
            elif 'create function' in task.lower():
                print(f"Função identificada: {task.strip()}")

    def get_source_code(self):
        return super().get_source_code()
