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
import io
import sys
import re
import unidecode
from .base_agent import BaseAgent
from .prompt_templates.developer_prompts import DeveloperPrompts
from utils.translation_utils import translate_string
from utils.pattern_matching import PatternMatching

class Developer(BaseAgent):
    """
    Initializes a developer with a language model and role.

        Args:
            - llm (Ollama): Language model to be used by the developer.
            - name (str): Name of the developer (e.g., "Backend Developer", "Frontend Developer").
            - interactive (bool): Defines if the process should run with interactions with the user.
    """
    def __init__(self, name, llm, development_style, language, interactive):
        super().__init__(name, llm, language, interactive)
        self.prompts = DeveloperPrompts(self.language)
        self.development_style = development_style
        self.patterns = PatternMatching()

    def develop_code(self, prompt):
        final_prompt = f"{prompt}\n\n{self.prompts.develop_code_instructions()}"
        code = self.evaluate(final_prompt)
        if self.interactive:
            final_code = self.interact(code)
        else:
            final_code = code
        return self._parse_code_response(final_code)
    
    def develop_code_with_tests(self, prompt):
        final_prompt = f"{prompt}\n\n{self.prompts.develop_code_with_tests_instructions()}"
        code = self.evaluate(final_prompt)
        if self.interactive:
            final_code = self.interact(code)
        else:
            final_code = code
        return self._parse_code_response(final_code)
    
    def develop_code_with_correction(self, general_report):
        print("Starting code generation with 01 cycle of testing and correction...")
        generated_code_with_tests = self.develop_code_with_tests(general_report)
        test_results = self.test_code(generated_code_with_tests)
        if test_results.startswith('fail'):
            print("Issues found during testing. Correcting...")
            corrected_code_with_tests = self.correct_code(generated_code_with_tests, test_results)
            print("Code generation cicle with corrections completed.")
            return self._parse_code_response(corrected_code_with_tests)
        else:
            print("No issues found. Code generation cicle finishing successfully.")
            return self._parse_code_response(generated_code_with_tests)

    def test_code(self, generated_code_with_tests):
        """
        Tests the generated code by evaluating its syntax and executing it.

        Args:
            - generated_code_with_tests (str): The code and tests generated to be tested.

        Returns:
            - final_test_evaluation_results (str): success or error.
        """
        print("Testing the generated code...\n\n")
        issues = []

        # Step 1: Syntax Check
        test_execution_prompt = f"{generated_code_with_tests}\n\n{self.prompts.check_syntax_of_generated_code()}"
        syntax_test_results = self.evaluate(test_execution_prompt)
        if self.interactive:
            final_syntax_test_results = self.interact(syntax_test_results)
        else:
            final_syntax_test_results = syntax_test_results
        print("\n\nSyntax check finished.\n\n")

        # Step 2: Code and Tests Execution Check
        test_code_execution_prompt = f"{generated_code_with_tests}\n\n{self.prompts.execute_tests_and_generated_code()}"
        test_code_execution_results = self.evaluate(test_code_execution_prompt)
        if self.interactive:
            final_test_code_execution_results = self.interact(test_code_execution_results)
        else:
            final_test_code_execution_results = test_code_execution_results
        print("\n\nCode execution test finished.\n\n")

        # Join results
        final_tests_results = f"{final_syntax_test_results}\n\n{final_test_code_execution_results}"

        # Step 3: Evaluate Results
        test_evaluation_prompt = f"{final_tests_results}\n\n{self.prompts.evaluate_test_results()}"
        test_evaluation_results = self.evaluate(test_evaluation_prompt)
        if self.interactive:
            final_test_evaluation_results = self.interact(test_evaluation_results)
        else:
            final_test_evaluation_results = test_evaluation_results
        print("\n\nTests Evaluation finished.\n\n")

        return final_test_evaluation_results

    def correct_code(self, generated_code_with_tests, test_results):
        """
        Corrects the issues found during testing by modifying the generated code.

        Args:
            - generated_code_with_tests (str): The code generated that had issues.

        Returns:
            - str: The corrected code.
        """
        # Generate a corrected version of the code
        code_correction_prompt = f"{generated_code_with_tests}\n\n{test_results}\n\n{self.prompts.correct_code_based_on_test_results()}"
        corrected_code_with_tests = self.develop_code_with_tests(code_correction_prompt)
        print("\n\nCorrections applied.\n\n")

        return self._parse_code_response(corrected_code_with_tests)

    def _parse_code_response(self, response):
        """
        Parses the code response into a dictionary format.

        Args:
        - response (str or dict): Response from code generation.

        Returns:
        - dict: Parsed response with translated 'Code' key.
        """
        parsed_code = {}

        if isinstance(response, str):
            # Extract filenames and code content
            lines = response.splitlines()
            current_filename = None
            current_code = []

            # Patterns list to be tested along 
            # with the right group indexes to be extracted
            patterns = self.patterns.filename_matching_patterns_no_hashtag()

            for line in lines:
                # loops through patterns 
                # only if line begins with "##" or "#"
                if (("##") or ("#")) in line:
                    # Iterate over the patterns to find a match
                    for pattern, group_index in patterns:
                        filename_match = re.search(pattern, line)
                        if current_filename == None:
                            if filename_match:
                                # Update current filename
                                current_filename = filename_match.group(group_index) 
                        # Check for an end tag to finalize the code capture
                        if (current_filename != None) and (current_code != []):
                            if ('end-' in line):
                                # Save the current filename and its code
                                parsed_code[current_filename] = "\n".join(current_code).strip()
                                current_filename = None  # Reset filename
                                current_code = []  # Reset code
                                break
                    # Add line to the current code
                elif current_filename:
                    current_code.append(line)

            # Save the last file's code if it exists
            if current_filename:
                parsed_code[current_filename] = "\n".join(current_code).strip()

            return parsed_code

        elif isinstance(response, dict):
            return response  # Assuming this is already in the desired format

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
    
    def detect_language_by_file_extension(self, text):
        """
        Detects the programming language based on the first occurrence of a file extension pattern.

        Args:
            - text (str): The text that contains the filename and extension.

        Returns:
            - str: Detected file extension or None if not found.
        """
        # List of common file extensions for different programming languages
        language_extensions = self.patterns.language_extensions_list()

        # Regex pattern to match filenames with extensions (e.g., filename.ext)
        # The extension must match one of the valid language extensions
        pattern = r'\b\w+\.(' + '|'.join(language_extensions) + r')\b'

        # Search for the first occurrence of the filename with the correct extension
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            # Return the detected file extension
            return match.group(1)

        # If no extension is found, return None
        return None
    
    def is_comment_line(self, stripped_line, comment_prefixes):
        """
        Checks whether a line is a comment based on the given prefixes.

        Args:
            - stripped_line (str): Line of code without whitespace at the ends.
            - comment_prefixes (dict): Dictionary with comment prefixes.

        Returns:
            - bool: True if the line is a comment, False otherwise.
        """
        single = comment_prefixes.get('single', '')
        multi_start = comment_prefixes.get('multi_start', '')
        multi_end = comment_prefixes.get('multi_end', '')

        if single and stripped_line.startswith(single):
            return True
        if multi_start and stripped_line.startswith(multi_start):
            return True
        if multi_end and stripped_line.endswith(multi_end):
            return True
        return False

    def get_comment_prefix(self, language_extension):
        """
        Gets the comment prefixes for the specified file extension.

        Args:
            - language_extension (str): Programming language file extension.

        Returns:
            - dict: Dictionary with 'single' and 'multi' for comment prefixes.
        """
        if not language_extension:
            return {'single': '', 'multi_start': '', 'multi_end': ''}
            
        comment_styles = self.patterns.comment_styles_list()

        return comment_styles.get(language_extension.lower(), {'single': '//', 'multi_start': '/*', 'multi_end': '*/'})

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
                if block_language != None:
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
                language_extension = self.detect_language_by_file_extension(line.strip())
                if language_extension:
                    block_language = language_extension

        # Merge the modified lines back into a single code
        cleaned_code = '\n'.join(modified_code_lines)

        return cleaned_code
    
    def fix_comments_prefix(self, code):
        """
        Fix comment prefixes in code if necessary.

        Args:
            - code (str or dict): Code generated to correct comment prefixes.

        Returns:
            - str or dict: Code with corrected comment prefixes.
        """
        if isinstance(code, dict):
            # Recursively fix comments in dictionaries of code
            modified_code = {}
            for key, value in code.items():
                modified_code[key] = self.fix_comments_prefix(value)
            return modified_code

        lines = code.split('\n')
        modified_lines = []
        block_language = None
        comment_prefixes = {'single': '', 'multi_start': '', 'multi_end': ''}  # Default initialization

        for line in lines:
            stripped_line = line.strip()

            if block_language == None:
                # Detect the language based on the file extension
                language_extension = self.detect_language_by_file_extension(stripped_line)
                if language_extension:
                    block_language = language_extension
                    comment_prefixes = self.get_comment_prefix(block_language)
                else:
                    # Keep default prefixes if language is not detected
                    comment_prefixes = {'single': '', 'multi_start': '', 'multi_end': ''}

            if not block_language:
                # Se a linguagem ainda não foi detectada, mantém a linha como está
                modified_lines.append(line)
                continue

            if self.is_comment_line(stripped_line, comment_prefixes):
                # Linha é um comentário
                if comment_prefixes['multi_start'] and stripped_line.startswith(comment_prefixes['multi_start']):
                    # Início de bloco de comentário
                    modified_line = line.replace(comment_prefixes['multi_start'], f"{comment_prefixes['multi_start']} ")
                    modified_lines.append(modified_line)
                    continue
                elif comment_prefixes['multi_end'] and stripped_line.endswith(comment_prefixes['multi_end']):
                    # Fim de bloco de comentário
                    modified_line = line.replace(comment_prefixes['multi_end'], f" {comment_prefixes['multi_end']}")
                    modified_lines.append(modified_line)
                    continue
                elif comment_prefixes['single'] and stripped_line.startswith(comment_prefixes['single']):
                    # Comentário de linha única
                    # Remove prefixos existentes e aplica o correto
                    cleaned_line = re.sub(r'^[' + re.escape(''.join(comment_prefixes.values())) + r']+', '', stripped_line).strip()
                    modified_line = f"{comment_prefixes['single']} {cleaned_line}"
                    modified_lines.append(modified_line)
                    continue

            # Linha não é um comentário, mantém como está
            modified_lines.append(line)

        modified_code = '\n'.join(modified_lines)
        return modified_code
            
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
            if self.development_style == "normal":
                code = self.develop_code(code_prompt)
            elif self.development_style == "tdd":
                code = self.develop_code_with_tests(code_prompt)
            elif self.development_style == "code-correction":
                code = self.develop_code_with_correction(code_prompt)
        except Exception as e:
            error_message = translate_string("developer", "generate_and_write_code_error", self.language)
            print(f"{error_message}: {task_description}: {e}")
            return

        # Prepare a list to hold the file 
        # paths and corresponding code
        file_paths_and_codes = []

        # Remove markup from generated code
        if isinstance(code, dict):
            for key, value in code.items():
                cleaned_code = self.remove_markup_from_code(value)
                cleaned_code = self.fix_comments_prefix(cleaned_code)
                file_path_for_key = os.path.join(os.path.dirname(file_path), f"{key}")
                
                # Check if the file exists and determine the mode (append if exists, write if not)
                file_mode = 'a' if os.path.exists(file_path_for_key) else 'w'
                
                file_paths_and_codes.append((file_path_for_key, cleaned_code, file_mode))
        else:
            cleaned_code = self.remove_markup_from_code(code)
            cleaned_code = self.fix_comments_prefix(cleaned_code)
            file_mode = 'a' if os.path.exists(file_path) else 'w'
            file_paths_and_codes = [(file_path, cleaned_code, file_mode)]

        # Write to all files
        for path, content, mode in file_paths_and_codes:
            try:
                with open(path, mode) as f:
                    f.write(content)
            except Exception as e:
                error_message = translate_string("developer", "code_written_fail", self.language)
                print(f"{error_message}: {path}: {e}")
                continue  # Continue to next file if one fails

        generate_code_message = translate_string("developer", "generate_and_write_code_success", self.language)
        print(f"{generate_code_message}: {', '.join([path for path, _, _ in file_paths_and_codes])}")
        # # Remove markup from generated code
        # if isinstance(code, dict):
        #     for key, value in code.items():
        #         # code[key] = self.remove_markup_from_code(value)
        #         cleaned_code = self.remove_markup_from_code(value)
        #         # Fix comment prefixes if necessary
        #         cleaned_code = self.fix_comments_prefix(cleaned_code)
        #         file_path_for_key = os.path.join(os.path.dirname(file_path), f"{key}")  # Determine the file path for this key
        #         file_paths_and_codes.append((file_path_for_key, cleaned_code))
        # else:
        #     # code = self.remove_markup_from_code(code)
        #     cleaned_code = self.remove_markup_from_code(code)
        #     cleaned_code = self.fix_comments_prefix(cleaned_code)
        #     file_paths_and_codes = [(file_path, cleaned_code)]  # Just one file path

        # # Write to all files
        # for path, content in file_paths_and_codes:
        #     try:
        #         with open(path, 'w') as f:
        #             f.write(content)
        #     except Exception as e:
        #         error_message = translate_string("developer", "code_written_fail", self.language)
        #         print(f"{error_message}: {path}: {e}")
        #         continue  # Continue to next file if one fails


    def extract_test_file_name(self, main_file_name):
        """
        Generates the test file name based on the main file name.

        Args:
        - main_file_name (str): The name of the main file.

        Returns:
        - str: The corresponding test file name.
        """
        base, ext = os.path.splitext(main_file_name)
        test_file_name = f"test_{base}{ext}"
        return test_file_name

    def process_task(self, node, development_dir):
        """
        Processes a task, generating the necessary structure and code.
        Handles nested subnodes if provided.
        """
        task = node.name
        file_name = None  # Initialize file_name at the start
            
        if "##" in task:
            
            # Patterns list to be tested along 
            # with the right group indexes to be extracted
            patterns = self.patterns.filename_matching_patterns()
                    
            # Iterate over the patterns to find a match
            for pattern, group_index in patterns:
                match = re.search(pattern, task)
                if match:
                    # Get the correct group that matched as file name
                    file_name = match.group(group_index)

                if file_name != None:
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
