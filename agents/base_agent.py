# agents/base_agent.py
import inspect

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

    def interact(self, prompt):
        """
        Interage com o usuário para refinar a resposta.

        Args:
            initial_response (str): A resposta inicial do modelo de linguagem.

        Returns:
            str: A resposta refinada.
        """
        response = prompt
        print(f"\nInteração com o agente: {self.name} para alterar a resposta do modelo de linguagem acima.")
        interact = input("\nDeseja alerar a resposta do modelo? (s/n): ")
        if interact.lower() == 's':
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
