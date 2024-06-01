# agents/tester.py
import os
from agents import Developer

class Tester(Developer):
    def __init__(self, llm, interactive=True):
        super().__init__(llm, "Tester")
        self.interactive = interactive

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
    
    def save_content(self, dir_path, filename, content):
        """
        Salva o conteúdo do testador em um arquivo.

        Args:
            dir_path (str): O diretório onde o arquivo será salvo.
            filename (str): O nome do arquivo.
            content (str): O conteúdo a ser salvo no arquivo.

        Returns:
            str: O conteúdo do testador.
        """
        with open(os.path.join(dir_path, filename), 'w') as file:
            file.write(content)
        
        return content
    
    def get_source_code(self):
        return super().get_source_code()  # Obtém o código-fonte da classe base