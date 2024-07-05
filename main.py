"""
main.py

Este arquivo é o ponto de entrada principal para a execução do projeto. 
Ele coordena a configuração inicial, a criação de agentes, 
a geração de relatórios e a estruturação do projeto.

Funções:

- clean_pycache(root_dir): Remove pastas __pycache__ do diretório especificado.
  - root_dir (str): Caminho do diretório raiz onde a limpeza deve ser realizada.

- create_directories(project_base_path): Cria as estruturas de pastas necessárias no projeto.
  - project_base_path (str): Caminho da raiz do projeto onde as pastas serão criadas.

- start(project_name, analyst_properties): Inicializa e executa o processo de configuração e execução do projeto.
  - project_name (str): Nome do projeto.
  - analyst_properties (str): Caminho para o arquivo de propriedades do analista.

- if __name__ == "__main__": Ponto de entrada do script quando executado diretamente.

English version:

This file is the main entry point for project execution. 
It coordinates initial setup, agent creation, report generation, 
and project structuring.

Functions:

- clean_pycache(root_dir): Removes __pycache__ folders from the specified directory.
  - root_dir (str): Root directory path where cleaning should be performed.

- create_directories(project_base_path): Creates necessary folder structures in the project.

- start(project_name, analyst_properties): Initializes and executes the project setup and execution process.
  - project_name (str): Project name.
  - analyst_properties (str): Path to the analyst properties file.

- if __name__ == "__main__": Script entry point when executed directly.
"""
import os
import inspect
import shutil
import sys
from io import StringIO
from agents import Analyst, SquadLeader, Developer, Tester
from graph import Graph, build_task_graph, process_task_graph
from langchain_community.llms import Ollama

def clean_pycache(root_dir):
    """
    Remove pastas __pycache__ do diretório especificado.

    Args:
    - root_dir (str): Caminho do diretório raiz onde a limpeza deve ser realizada.

    English:
    
    Removes __pycache__ folders from the specified directory.

    Args:
    - root_dir (str): Root directory path where cleaning should be performed.
    """
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dir = os.path.join(root, dir_name)
                shutil.rmtree(pycache_dir)
                print(f"Removida pasta __pycache__ em {pycache_dir}")

        # Verifica se estamos na pasta agents ou na subpasta prompt_templates
        if 'agents' in root and 'prompt_templates' in dirs:
            prompt_templates_dir = os.path.join(root, 'prompt_templates')
            for sub_root, sub_dirs, sub_files in os.walk(prompt_templates_dir):
                for sub_dir_name in sub_dirs:
                    if sub_dir_name == "__pycache__":
                        sub_pycache_dir = os.path.join(sub_root, sub_dir_name)
                        shutil.rmtree(sub_pycache_dir)
                        print(f"Removida pasta __pycache__ em {sub_pycache_dir}")

def create_directories(project_base_path):
    """
    Cria as estruturas de pastas necessárias no projeto.

    Args:
    - project_base_path (str): Caminho da raiz do projeto onde as pastas serão criadas.

    English:
    
    Creates necessary folder structures in the project.

    Args:
    - project_base_path (str): Root path of the project where folders will be created.
    """
    base_dirs = ["agents", "reports", "dev"]
    for base_dir in base_dirs:
        os.makedirs(os.path.join(project_base_path, base_dir), exist_ok=True)

class MultiOutput:
    def __init__(self, *outputs):
        self.outputs = outputs

    def write(self, message):
        for output in self.outputs:
            output.write(message)

    def flush(self):
        for output in self.outputs:
            output.flush()

def start(project_name, analyst_properties):
    """
    Inicializa e executa o processo de configuração e execução do projeto.

    Args:
    - project_name (str): Nome do projeto.
    - analyst_properties (str): Caminho para o arquivo de propriedades do analista.

    English:
    
    Initializes and executes the project setup and execution process.
    Args:
    - project_name (str): Project name.
    - analyst_properties (str): Path to the analyst properties file.
    """
    
    # Define um processo interativo
    # Define an interactive process
    interactive = input("Executar o processo interativo? (s/n): ").strip().lower() == 's'
    
    # variávies que controlam a execução dos blocos dos agentes desenvolvedores
    # variables that control the execution of developer agent blocks
    generate_backend = False
    generate_frontend = False
    generate_tests = False
    
    backend_developer = None
    frontend_developer = None
    tester = None
    
    backend_backlog = None
    frontend_backlog = None
    test_backlog = None

    # Define quais agentes devem executar suas rotinas
    generate_all = input("Deseja gerar backend, frontend e testes? (s/n): ").strip().lower() == 's'
    if generate_all:
        generate_backend = True
        generate_frontend = True
        generate_tests = True
    else:
        generate_backend = input("Gerar backend? (s/n): ").strip().lower() == 's'
        generate_frontend = input("Gerar frontend? (s/n): ").strip().lower() == 's'
        generate_tests = input("Gerar testes? (s/n): ").strip().lower() == 's'

    # Limpar pastas __pycache__
    # Clean __pycache__ folders
    clean_pycache(os.path.dirname(__file__))

    # Inicializando o Ollama
    # Initializing Ollama
    # Modelo Phi-3 para fazer o papel de Analista
    # Phi-3 model to play the role of Analyst
    llm_anl = Ollama(model="phi3:14b-medium-128k-instruct-q4_K_M")
    # Modelo Codegemma para fazer o papel de Desenvolvedor
    # Codegemma model to play the role of Developer
    llm_dev = Ollama(model="codegemma:7b-instruct-v1.1-q4_K_M")
    # Modelo Lama-3 para fazer o papel de Líder de Equipe
    # Lama-3 model to play the role of Squadleader
    llm_sq = Ollama(model="llama3:8b-instruct-q4_K_M")

    # Inicializando o analista
    # Initializing Analyst
    analyst = Analyst(llm_anl, analyst_properties, interactive=interactive)
    analyst.generate_report()
    analyst_report = analyst.output

    # Inicializando o líder de equipe
    # Initializing Squad Leader
    squad_leader = SquadLeader(llm_sq, interactive=interactive)

    # Array de agentes
    # Agents array
    agents = {
        "Analista": analyst,
        "Líder de Equipe": squad_leader
    }

    # Criando os agentes desenvolvedores e tester
    # Creating developer agents and tester
    if generate_backend:
        backend_developer = Developer(llm_dev, "Desenvolvedor Backend", interactive=interactive)
        agents["Desenvolvedor Backend"] = backend_developer

    if generate_frontend:
        frontend_developer = Developer(llm_dev, "Desenvolvedor Frontend", interactive=interactive)
        agents["Desenvolvedor Frontend"] = frontend_developer

    if generate_tests:
        tester = Tester(llm_dev, interactive=interactive)
        agents["Tester"] = tester

    # Criando a estrutura de pastas na raiz do diretório de build
    # Creating folder structure in the build
    project_base_path = os.path.join(os.path.dirname(__file__), "build", project_name)
    create_directories(project_base_path)

    # Salvando os arquivos na pasta agents
    # Saving files in the agents folder
    for agent_name, agent in agents.items():
        agent_file = agent_name.lower().replace(' ', '_') + ".py"
        agent_content = f"# {agent_name}\n\n{agent.__doc__}\n\n"
        if inspect.isfunction(agent) or inspect.isclass(agent):
            agent_content += inspect.getsource(agent)
        else:
            agent_content += str(agent)
        agent_path = os.path.join(project_base_path, "agents", agent_file)
        with open(agent_path, 'w') as f:
            f.write(agent_content)

    # Gera o relatório geral do projeto
    # Generate the project general report
    squad_leader.generate_general_report(analyst_report)
    general_report = squad_leader.output

    # Gera os relatórios dos desenvolvedores e tester
    # Generate developer and tester reports
    if generate_backend:
        squad_leader.generate_backend_backlog(analyst_report)
        backend_backlog = squad_leader.output
    if generate_frontend:
        squad_leader.generate_frontend_backlog(analyst_report)
        frontend_backlog = squad_leader.output
    if generate_tests:
        squad_leader.generate_test_backlog(analyst_report)
        test_backlog = squad_leader.output

    # Salvando os relatórios na pasta de relatórios
    # Saving reports in the reports folder
    reports = {
        "relatório_geral_do_projeto.txt": general_report
    }

    if generate_backend:
        reports["backlog_de_tarefas_de_backend.txt"] = backend_backlog
    if generate_frontend:
        reports["backlog_de_tarefas_de_frontend.txt"] = frontend_backlog
    if generate_tests:
        reports["backlog_de_tarefas_de_testes.txt"] = test_backlog
    
    for report_file, report_content in reports.items():
        if report_content is not None:
            with open(os.path.join(project_base_path, "reports", report_file), 'w') as f:
                f.write(str(report_content))
    
    # Criando os grafos das tarefas
    # Creating task graphs
    backend_task_graph = build_task_graph(backend_backlog) if generate_backend else None
    frontend_task_graph = build_task_graph(frontend_backlog) if generate_frontend else None
    test_task_graph = build_task_graph(test_backlog) if generate_tests else None

    ## Processamento dos Grafos de Tarefas
    ## Processing Task Graphs
    if generate_backend:
        development_dir = os.path.join(project_base_path, "dev", backend_developer.name.lower().replace(' ', '_'))
        os.makedirs(development_dir, exist_ok=True)
        print("Processando Grafos de Tarefas para {}".format(backend_developer.name))
        process_task_graph(backend_developer, backend_task_graph, development_dir)
    
    if generate_frontend:
        development_dir = os.path.join(project_base_path, "dev", frontend_developer.name.lower().replace(' ', '_'))
        os.makedirs(development_dir, exist_ok=True)
        print("Processando Grafos de Tarefas para {}".format(frontend_developer.name))
        process_task_graph(frontend_developer, frontend_task_graph, development_dir)

    if generate_tests:
        test_dir = os.path.join(project_base_path, "dev", "tester")
        os.makedirs(test_dir, exist_ok=True)
        process_task_graph(tester, test_task_graph, test_dir)

    # TO-DO - create prompt logic to create project README
    # Criando o README do Projeto
    # Creating Project README
    readme_content = f"# {project_name}\n\n[Insira a descrição do projeto aqui]"
    with open(os.path.join(project_base_path, "README.md"), 'w') as f:
        f.write(readme_content)

def main():# Define which agents should execute their routines
    project_name = input("Nome do projeto: ")
    analyst_properties = os.path.join(os.path.dirname(__file__), "project.properties")
    
    # Redirecionando a saída padrão para capturar o log
    # Redirecting standard output to capture log
    original_stdout = sys.stdout
    captured_stdout = StringIO()
    sys.stdout = MultiOutput(original_stdout, captured_stdout)
    project_base_path = os.path.join(os.path.dirname(__file__), "build", project_name)

    try:
        start(project_name, analyst_properties)
    finally:
        # Restaura o stdout original
        # Restore the original stdout
        sys.stdout = original_stdout
        # Obtém a saída capturada
        # Get the captured output
        actions_report = captured_stdout.getvalue()
        with open(os.path.join(project_base_path, "relatorio_geral_execucao.txt"), 'w') as f:
            f.write(actions_report)

if __name__ == "__main__":
    main()
