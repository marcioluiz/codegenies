# agents/base_agent.py
import inspect
import os

class BaseAgent:
    def __init__(self, name, llm):
        self.name = name
        self.llm = llm
        self.output = ""

    def evaluate(self, prompt):
        try:
            print(f"\n O agente {self.name} está avaliando o prompt: {prompt}")
            output = self.llm.invoke(prompt)
            print(f"Resposta do modelo: {output}")
            self.output = output
            return output
        except Exception as e:
            print(f"Erro ao avaliar o prompt: {e}")
            return None

    def save_content(self, dir_path, filename, content):
        """
        Salva o conteúdo do agente em um arquivo.

        Args:
            dir_path (str): O diretório onde o arquivo será salvo.
            filename (str): O nome do arquivo.
            content (str): O conteúdo a ser salvo no arquivo.

        Returns:
            str: O conteúdo do agente.
        """
        with open(os.path.join(dir_path, filename), 'w') as file:
            file.write(content)
        
        return content

    def generate_structure(self, prompt):
        return self.evaluate(prompt)

    def develop_code(self, prompt):
        return self.evaluate(prompt)

    def validate_content(self, content, prompt):
        validation_prompt = f"\nValidar o seguinte conteúdo: {content}. {prompt}"
        return self.evaluate(validation_prompt)

    def validate_structure(self, prompt):
        return self.evaluate(prompt)

    def interact(self, prompt):
        response = prompt
        print(f"\nInteração com o agente: {self.name} para alterar a resposta do modelo de linguagem acima.")
        integrate = input("\nDeseja alerar a resposta do modelo? (s/n): ")
        if integrate.lower() == 's':
            response = ''
            user_input = input("\nAção humana Possivelmente necessária. \nPor favor, insira mais um prompt para refinar o resultado anterior: ")
            refined_prompt = user_input + "\n"  + prompt
            response = self.evaluate(refined_prompt)
        else:
            print("\nInteração encerrada. Prossiga com a execução.")
            user_input = None
            response = prompt
            
        return response

    def get_source_code(self):
        return inspect.getsource(self.__class__)
