# main.py

import os
import inspect
import shutil
from agents import Analyst, SquadLeader, Developer, Tester
from graph import Graph
from langchain_community.llms import Ollama

def clean_pycache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dir = os.path.join(root, dir_name)
                shutil.rmtree(pycache_dir)
                print(f"Removida pasta __pycache__ em {pycache_dir}")

def create_directories(project_base_path):
    base_dirs = ["agents", "reports", "dev"]
    for base_dir in base_dirs:
        os.makedirs(os.path.join(project_base_path, base_dir), exist_ok=True)

def start(project_name, analyst_properties):
    # Limpar pastas __pycache__
    clean_pycache(os.path.dirname(__file__))

    # Inicializando o Ollama
    llm_anl = Ollama(model="llama3:8b-instruct-q4_K_M")  # Modelo Llama-3 para fazer o papel de Analyst
    llm_dev = Ollama(model="codegemma:7b-instruct-v1.1-q4_K_M")  # Modelo Codegemma para fazer o papel de Developer
    llm_sq = Ollama(model="mistral")  # Modelo Mistral para fazer o papel de Squadleader

    ## BEGIN 100% Working 
    # Inicializando o analista
    analyst = Analyst(llm_anl, analyst_properties)
    analyst.generate_report()
    analyst_report = analyst.output

    # Inicializando o líder de equipe
    squad_leader = SquadLeader(llm_sq)

    # Criando os agentes desenvolvedores e tester
    backend_developer = Developer(llm_dev, "Desenvolvedor Backend")
    frontend_developer = Developer(llm_dev, "Desenvolvedor Frontend")
    tester = Tester(llm_dev)

    # Criando o grafo
    agents = {
        "Analista": analyst,
        "Líder de Equipe": squad_leader,
        "Desenvolvedor Backend": backend_developer,
        "Desenvolvedor Frontend": frontend_developer,
        "Tester": tester
    }

    graph = Graph()
    graph.build_graph(agents)

    # Criando a estrutura de pastas na raiz do diretório de build
    project_base_path = os.path.join(os.path.dirname(__file__), "build", project_name)
    create_directories(project_base_path)

    # Salvando os arquivos na pasta agents
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

    squad_leader.generate_general_report(analyst_report)
    general_report = squad_leader.output
    squad_leader.generate_backend_backlog(analyst_report)
    backend_backlog = squad_leader.output
    squad_leader.generate_frontend_backlog(analyst_report)
    frontend_backlog = squad_leader.output
    squad_leader.generate_test_backlog(analyst_report)
    test_backlog = squad_leader.output

    # Salvando os relatórios na pasta de relatórios
    reports = {
        "relatório_geral_do_projeto.txt": general_report,
        "backlog_de_tarefas_de_backend.txt": backend_backlog,
        "backlog_de_tarefas_de_frontend.txt": frontend_backlog,
        "backlog_de_tarefas_de_testes.txt": test_backlog
    }
    
    for report_file, report_content in reports.items():
        if report_content is not None:
            with open(os.path.join(project_base_path, "reports", report_file), 'w') as f:
                f.write(str(report_content))
    ## END 100% Working 
    
    ## TO-DO solve problems with code
    # Desenvolvimento
    developers = [backend_developer, frontend_developer]
    for developer in developers:
        development_dir = os.path.join(project_base_path, "dev", developer.name.lower().replace(' ', '_'))
        os.makedirs(development_dir, exist_ok=True)

        # Geração da estrutura
        if developer.name.lower().replace(' ', '_') == 'desenvolvedor_backend':
            structure_prompt = f"Gere toda a estrutura de pastas e arquivos necessária para o desenvolvimento do {developer.name} conforme o Bakclog de Tarefas {backend_backlog}"
        elif developer.name.lower().replace(' ', '_') == 'desenvolvedor_frontend':
            structure_prompt = f"Gere toda a estrutura de pastas e arquivos necessária para o desenvolvimento do {developer.name} conforme o Bakclog de Tarefas {frontend_backlog}"

        developer.generate_structure(structure_prompt)
        structure = developer.output 
        if structure is not None:
            file_path = os.path.join(development_dir, "estrutura.txt")
            with open(file_path, 'w') as f:
                f.write(structure)

        # Desenvolvimento do código
        if developer.name.lower().replace(' ', '_') == 'desenvolvedor_backend':
            code_prompt = f"Gere todo o código necessário conforme o backlog de atividades de backend e preencha o conteúdo do arquivo com o código. Bakclog de Tarefas {backend_backlog}"
        elif developer.name.lower().replace(' ', '_') == 'desenvolvedor_frontend':
            code_prompt = f"Gere todo o código necessário conforme o backlog de atividades de frontend e preencha o conteúdo do arquivo com o código. Bakclog de Tarefas {frontend_backlog}"

        developer.develop_code(code_prompt)
        code = developer.output
        if code is not None:
            if developer.name.lower().replace(' ', '_') == 'desenvolvedor_backend':
                file_path = os.path.join(development_dir, "codigo.py")
            elif developer.name.lower().replace(' ', '_') == 'desenvolvedor_frontend':
                file_path = os.path.join(development_dir, "codigo.jsx")
            with open(file_path, 'w') as f:
                f.write(code)

    # Desenvolvimento dos testes
    test_dir = os.path.join(project_base_path, "dev", "tester")
    os.makedirs(test_dir, exist_ok=True)
    test_structure_prompt = f"Gere a estrutura de pastas e arquivos necessária para os testes. Bakclog de Tarefas {test_backlog}"
    tester.generate_structure(test_structure_prompt)
    test_structure = tester.output
    if test_structure is not None:
        file_path = os.path.join(test_dir, "estrutura_teste.txt")
        with open(file_path, 'w') as f:
            f.write(test_structure)

    test_code_prompt = f"Preencha o conteúdo dos arquivos de teste gerados conforme o relatório de backlog e outros relatórios necessários. Bakclog de Tarefas {test_backlog}"
    tester.develop_tests(test_code_prompt)
    tests = tester.output 
    if tests is not None:
        file_path = os.path.join(test_dir, "teste.py")
        with open(file_path, 'w') as f:
            f.write(tests)

    # Criando o README do Projeto
    readme_content = f"# {project_name}\n\n[Insira a descrição do projeto aqui]"
    with open(os.path.join(project_base_path, "README.md"), 'w') as f:
        f.write(readme_content)

    # Criando o relatório de ações completo
    actions_report = "[Insira o relatório de ações completo aqui]"
    with open(os.path.join(project_base_path, "relatorio_acoes.txt"), 'w') as f:
        f.write(actions_report)

if __name__ == "__main__":
    project_name = input("Nome do projeto: ")
    analyst_properties = os.path.join(os.path.dirname(__file__), "project.properties")
    start(project_name, analyst_properties)
