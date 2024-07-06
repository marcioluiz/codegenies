"""
developer.py

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
from .prompt_templates.developer_prompts import DeveloperPrompts
from utils.translation_utils import translate_string

class Developer(BaseAgent):
    """
    Initializes a developer with a language model and role.

        Args:
            - llm (Ollama): Language model to be used by the developer.
            - name (str): Name of the developer (e.g., "Backend Developer", "Frontend Developer").
            - interactive (bool): Defines if the process should run with interactions with the user.
    """
    def __init__(self, name, llm, language, interactive):
        super().__init__(name, llm, language, interactive)
        self.prompts = DeveloperPrompts(self.language)

    def develop_code(self, prompt):
        final_prompt = f"{prompt}\n\n{self.prompts.develop_code_instructions()}"
        code = self.evaluate(final_prompt)
        if self.interactive:
            final_code = self.interact(code)
        else:
            final_code = code
        return self._parse_code_response(final_code)

    def _parse_code_response(self, response):
        """
        Parses the code response into a dictionary format.

        Args:
        - response (str or dict): Response from code generation.

        Returns:
        - dict: Parsed response with translated 'Code' key.
        """
        if isinstance(response, str):
            translated_code_key = translate_string("developer", "translated_code_key", self.language) 
            return {translated_code_key: response}
        elif isinstance(response, dict):
            return response
        else:
            translated_code_key = translate_string("developer", "translated_code_key", self.language)
            return {translated_code_key: response}
    
    def sanitize_file_name(self, file_name):
        """
        Sanitizes a filename using unicode library and
        removes the pattern '##(\w+)\/' using the re.sub() function.
        """
        file_name = unidecode.unidecode(file_name)
        file_name = re.sub('##(\w+)\/', '', file_name)
        return file_name.lower()
    
    def detect_language_by_first_line(self, line):
        """
        Detects the programming language based on the first line of code.

        Arguments:
        - line (str): The first line of code.
        - language_extensions (dict): Dictionary of supported language extensions.

        Returns:
        - str: The name of the language corresponding to the first line of code, or None if not found.
        """
        language_extensions = [
            'apl', 'asm', 'awk', 'bas', 'bat', 'c', 'clj', 'coffee', 'cpp', 'cr', 'd', 'dart',
            'ex', 'f77', 'f95', 'forth', 'fsharp', 'go', 'groovy', 'hs', 'html', 'java', 'jl',
            'js', 'kt', 'lisp', 'lua', 'm', 'ml', 'php', 'pl', 'pro', 'ps1', 'py', 'rb', 'r',
            'scala', 'scm', 'sh', 'sql', 'st', 'swift', 'ts', 'vb', 'v', 'vbs', 'vim', 'vhd',
            'xml'
        ]
        for extension in language_extensions:
            pattern = r'^.*?(?<!\\)\.' + re.escape(extension) + r'\b'
            if re.search(pattern, line.strip(), re.IGNORECASE):
                return extension
        return None

    def get_comment_prefix(self, language_extension):
        """
        Gets the comment prefix for the specified file extension.
        
        Arguments:
        - language_extension (str): The file extension of the programming language.
        
        Returns:
        -str: The appropriate comment prefix for the file extension.
        """
        comment_prefixes = {
            '/*': ['css', 'html', 'xml'],
            '//': ['c', 'cpp', 'cr', 'dart', 'd', 'fsharp', 'go', 
                   'groovy', 'java', 'js', 'kt', 'nim', 'php', 'scala', 
                   'swift', 'ts', 'v'],
            '"': ['st', 'vim'],
            '#': ['awk', 'coffee', 'ex', 'jl', 'pl', 'ps1', 'py', 
                  'rb', 'r', 'sh', 'vbs'],
            '%': ['m', 'pro'],
            '(': ['ml'],
            ';': ['asm'],
            ';;': ['clj', 'lisp', 'scm'],
            '\\': ['forth'],
            '!': ['f77', 'f95'],
            'REM': ['bat'],
            '⍝': ['apl'],
            '--': ['hs', 'lua', 'sql', 'vhd'],
            '\'': ['bas', 'vb']
            # Add more prefixes as needed
        }

        for prefix, extensions in comment_prefixes.items():
            if language_extension.lower() in extensions:
                return prefix

        return ''

    def remove_markup_from_code(self, code):
        """
        Remove markup from the generated code.
        Args:
        - code (str): The generated code with markup.
        Returns:
        - str: The clean code without markup.
        """
        # Remove patterns "```language" and "```"
        code = re.sub(r'\`\`\`.*?\n', '', code)
        code = re.sub('\`\`\`', '', code)
        
        modified_code_lines = []
        block_language = None

        code_lines = code.split('\n')
        for line in code_lines:
            if line.strip().startswith('**'):
                # Remove asterisks only if the line starts with '**'
                modified_line = re.sub(r'^\*\*|\*\*$', '', line.strip()).strip()
                if block_language:
                    comment_prefix = self.get_comment_prefix(block_language)
                    if block_language.lower() in ['css', 'html', 'xml']:
                        modified_code_lines.append(f'{comment_prefix} {modified_line} */')
                    else:
                        modified_code_lines.append(f'{comment_prefix} {modified_line}')
                else:
                    modified_code_lines.append(modified_line)
            elif line.strip().startswith('*'):
                # Remove asterisks only if the line starts with '*'
                modified_line = re.sub(r'^\*', '', line.strip()).strip()
                if block_language:
                    comment_prefix = self.get_comment_prefix(block_language)
                    if block_language.lower() in ['css', 'html', 'xml']:
                        modified_code_lines.append(f'{comment_prefix} {modified_line} */')
                    else:
                        modified_code_lines.append(f'{comment_prefix} {modified_line}')
                else:
                    modified_code_lines.append(modified_line)
            else:
                modified_code_lines.append(line)

            # Identify the first line to determine the language
            if not block_language:
                language_extension = self.detect_language_by_first_line(line.strip())
                if language_extension:
                    block_language = language_extension

        # Merge the modified lines back into a single code
        cleaned_code = '\n'.join(modified_code_lines)

        return cleaned_code
    
    def fix_comments_prefix(self, code):
        """
        Fix comment prefixes in the code if necessary.

        Args:
        - code (str): Generated code to fix comment prefixes.

        Returns:
        - str: Code with corrected comment prefixes.
        """
        if isinstance(code, str):
            lines = code.split('\n')
            modified_lines = []
            block_language = None

            for line in lines:
                if not block_language:
                    language_extension = self.detect_language_by_first_line(line.strip())
                    if language_extension:
                        block_language = language_extension

                if line.strip().startswith(self.get_comment_prefix(block_language)):
                    comment_prefix = self.get_comment_prefix(block_language)
                    current_prefix = line.split()[0] if line.strip() else ''
                    if current_prefix != comment_prefix:
                        line = line.replace(current_prefix, comment_prefix, 1)

                modified_lines.append(line)

            code = '\n'.join(modified_lines)

        return code
            
    # Function to generate and write code to files
    def generate_and_write_code(self, file_path, task_description):
        """
        Generates and writes code to a file.

        Args:
        - file_path (str): Path to write the generated code.
        - task_description (str): Description of the task.

        Notes:
        - Uses the `develop_code()` method to generate code based on the provided task description.
        - Removes markup from the generated code using the `remove_markup_from_code()` method.
        - Writes the cleaned code to the specified file path.
        - Corrects comment prefixes using `fix_comments_prefix()` if necessary.
        """
        code_prompt = f"{self.prompts.code_prompt_instruction()}{task_description}"
        code_processing_message = translate_string("developer", "code_processing_message", self.language)
        print(f"{code_processing_message}: {task_description}")
        try:
            code = self.develop_code(code_prompt)
        except Exception as e:
            error_message = translate_string("developer", "generate_and_write_code_error", self.language)
            print(f"{error_message}: {task_description}: {e}")
            return

        # Remove markup from generated code
        if isinstance(code, dict):
            for key, value in code.items():
                code[key] = self.remove_markup_from_code(value)
        else:
            code = self.remove_markup_from_code(code)

        # Fix comment prefixes if necessary
        code = self.fix_comments_prefix(code)

        with open(file_path, 'w') as f:
            if isinstance(code, dict):
                for key, value in code.items():
                    f.write(f"{value}\n")
            else:
                f.write(code)

        generate_code_message = translate_string("developer", "generate_and_write_code_success", self.language)
        print(f"{generate_code_message}: {file_path}")

    def process_task(self, node, development_dir):
        """
        Processes a task, generating the necessary structure and code.
        Handles nested subnodes if provided.
        """
        task = node.name
            
        if "##" in task:
            file_name = ''
            
            # Patterns list to be tested along with the right group indexes to be extracted
            patterns = [
                # 1. "##filename.ext"
                (r'##(((\w+)|(\w+\-\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 1),
                # 2. "##foldername/filename.ext" or "##folder-name/filename.ext" 
                (r'##((\w+\D\w+))\/((\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 3),
                # 3. "##folder/file.ext" or "##folder-name/file.ext" and ending "file-name.ext" or "file-name.ext"
                (r'##((\w+\D\w+))\/(((\w+\D\w+)|(\w+\D\w+\D\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 3),
                # 4. "##folder1/folder2/filename.ext" or "##folder1/folder2-name/filename.ext" and ending "filename.ext" or "filename.ext"
                (r'##(((\w+)\/(\w+\D\w+))|((\w+)\/(\w+\D\w+)\/(\w+\D\w+)))\/((\w+\D\w+\D\w+|\w+\D\w+\D\w+\D\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 9)
            ]

            # Iterate over the patterns to find a match
            for pattern, group_index in patterns:
                match = re.search(pattern, task)
                if match:
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
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()
