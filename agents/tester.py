# agents/tester.py
import os
from agents import Developer

class Tester(Developer):
    def __init__(self, llm):
        super().__init__(llm, "Tester")

    def generate_structure(self, prompt):
        structure = self.evaluate(prompt)
        return self.interact(structure)

    def develop_tests(self, prompt):
        tests = self.evaluate(prompt)
        return self.interact(tests)
    
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