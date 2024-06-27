"""
base_agent.py

Este arquivo define as classes para os diferentes agentes 
usados no projeto: Analyst, SquadLeader, Developer e Tester. 
Cada agente utiliza um modelo de linguagem grande (LLM) 
específico para realizar suas tarefas.

Classes:

- Analyst: Responsável por gerar relatórios iniciais e backlogs de tarefas.
  - __init__(self, model, properties_file, interactive=False): Inicializa o agente Analyst.
    - model (Ollama): Modelo de linguagem a ser utilizado pelo analista.
    - properties_file (str): Caminho para o arquivo de propriedades do projeto.
    - interactive (bool): Define se o processo será interativo.

  - generate_report(self): Gera o relatório inicial do projeto.

- SquadLeader: Coordena a equipe e gera relatórios e backlogs de tarefas para os desenvolvedores e testers.
  - __init__(self, model, interactive=False): Inicializa o agente SquadLeader.
    - model (Ollama): Modelo de linguagem a ser utilizado pelo líder de equipe.
    - interactive (bool): Define se o processo será interativo.

  - generate_general_report(self, analyst_report): Gera o relatório geral do projeto.
    - analyst_report (str): Relatório inicial gerado pelo analista.

  - generate_backend_backlog(self, analyst_report): Gera o backlog de tarefas de backend.
    - analyst_report (str): Relatório inicial gerado pelo analista.

  - generate_frontend_backlog(self, analyst_report): Gera o backlog de tarefas de frontend.
    - analyst_report (str): Relatório inicial gerado pelo analista.

  - generate_test_backlog(self, analyst_report): Gera o backlog de tarefas de testes.
    - analyst_report (str): Relatório inicial gerado pelo analista.

        •	Developer: Responsável por implementar as tarefas de desenvolvimento conforme o backlog gerado.
            •	init(self, model, name, interactive=False): Inicializa o agente Developer.
                •	model (Ollama): Modelo de linguagem a ser utilizado pelo desenvolvedor.
                •	name (str): Nome do desenvolvedor.
                •	interactive (bool): Define se o processo será interativo.
            •	Tester: Responsável por realizar os testes e validar as implementações.
                •	init(self, model, interactive=False): Inicializa o agente Tester.
                    •	model (Ollama): Modelo de linguagem a ser utilizado pelo tester.
                    •	interactive (bool): Define se o processo será interativo.
"""
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
