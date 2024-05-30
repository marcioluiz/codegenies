# agents/developer.py
import os
from .base_agent import BaseAgent

class Developer(BaseAgent):
    def __init__(self, llm, name):
        super().__init__(name, llm)

    def develop_code(self, prompt):
        instructions = "Com base no backlog de atividades acima, gere gere todo o código dos arquivos demandados nas instruções do backlog. Coloque todo o código sequencialmente marcando início de arquivos com: ##arquivo.ext eo o fim de todo arquivo com: ##end-arquivo.ext ."
        final_prompt = f"{prompt}\n\n{instructions}"
        code = self.evaluate(final_prompt)
        final_code = self.interact(code)
        return self._parse_code_response(final_code)

    def _parse_code_response(self, response):
        # Se a resposta for uma string simples, apenas retorne-a
        if isinstance(response, str):
            return {"Código": response}
        # Se for um dicionário JSON válido, retorne-o diretamente
        elif isinstance(response, dict):
            return response
        # Caso contrário, retorne um dicionário com a resposta como valor
        else:
            return {"Código": response}
    
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
    
    def get_source_code(self):
        return super().get_source_code()  # Obtém o código-fonte da classe base
