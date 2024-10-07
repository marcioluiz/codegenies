"""
main.py

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
import inspect, os, shutil, sys
import inquirer
from io import StringIO
from agents import Analyst, SquadLeader, Developer, Tester
from graph import build_task_graph, process_task_graph
from langchain_community.llms import Ollama
from utils.translation_utils import translate_string

# Global variable for language selection
LANGUAGE = None

# Global variable for development style selection
DEVSTYLE = None

def select_language():
    """
    Prompt the user to select a language for the project.
    
    Returns:
    - str: Language code ("pt-br" or "en-us").
    """
    questions = [
        inquirer.List(
            'language',
            message="Select language \n Selecione o idioma",
            choices=["en-us", "pt-br"],
        ),
    ]
    
    answers = inquirer.prompt(questions)
    return answers['language']

def select_development_style(language):
    """
    Prompt the user to select the development style for the project.
    
    Returns:
    - str: Language code ("normal", "tdd" or "code-correction").
    """
    if language == "en-us": 
        questions = [
            inquirer.List(
                'dev_style',
                message="Select Development Style",
                choices=['normal', 'tdd', 'code-correction'],
            )
        ]
    elif language == "pt-br": 
        questions = [
            inquirer.List(
                'dev_style',
                message="Selecione o estilo de desenvolvimento",
                choices=['normal', 'tdd', 'code-correction'],
            )
        ]
    
    answer = inquirer.prompt(questions)
    return answer['dev_style']

class MultiOutput:
    def __init__(self, *outputs):
        self.outputs = outputs

    def write(self, message):
        for output in self.outputs:
            output.write(message)

    def flush(self):
        for output in self.outputs:
            output.flush()

def clean_pycache(root_dir, language):
    """
    Removes __pycache__ folders from the specified directory.

    Args:
    - root_dir (str): Root directory path where cleaning should be performed.
    """
    # Get pycache message key translation
    pycache_removed = "pycache_removed"
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dir = os.path.join(root, dir_name)
                shutil.rmtree(pycache_dir)
                print(translate_string('main', pycache_removed, language),{pycache_dir})

        # Verifica se estamos na pasta agents ou na subpasta prompt_templates
        if 'agents' in root and 'prompt_templates' in dirs:
            prompt_templates_dir = os.path.join(root, 'prompt_templates')
            for sub_root, sub_dirs, sub_files in os.walk(prompt_templates_dir):
                for sub_dir_name in sub_dirs:
                    if sub_dir_name == "__pycache__":
                        sub_pycache_dir = os.path.join(sub_root, sub_dir_name)
                        shutil.rmtree(sub_pycache_dir)
                        print(translate_string('main', pycache_removed, language),{sub_pycache_dir})

def create_directories(project_base_path):
    """   
    Creates necessary folder structures in the project.

    Args:
    - project_base_path (str): Root path of the project where folders will be created.
    """
    base_dirs = ["agents", "reports", "dev"]
    for base_dir in base_dirs:
        os.makedirs(os.path.join(project_base_path, base_dir), exist_ok=True)

def start(project_name, analyst_properties, development_style, language):
    """
    Initializes and executes the project setup and execution process.
    Args:
    - project_name (str): Project name.
    - analyst_properties (str): Path to the analyst properties file.
    """

    # Define an interactive process
    interactive = input(translate_string('main', 'execute_interactive_message', language)).strip().lower() in ['s', 'y']
    
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

    # Define which agents should execute their routines
    generate_all_routines_message = "generate_all_message"
    generate_all = input(translate_string('main', generate_all_routines_message, language)).strip().lower() in ['s', 'y']
    if (generate_all and development_style == "normal" ):
        generate_backend = True
        generate_frontend = True
        generate_tests = True
    elif (generate_all and ( development_style == "tdd" or development_style == "code-correction")): 
        generate_backend = True
        generate_frontend = True
        generate_tests = False
    else:
        generate_backend_message = "generate_backend_message"
        generate_backend = generate_all or input(translate_string('main', generate_backend_message, language)).strip().lower() in ['s', 'y']
        
        generate_frontend_message = "generate_frontend_message"
        generate_frontend = generate_all or input(translate_string('main', generate_frontend_message, language)).strip().lower() in ['s', 'y']

        generate_tests_message = "generate_tests_message"
        generate_tests = generate_all or input(translate_string('main', generate_tests_message, language)).strip().lower() in ['s', 'y']

    # Clean __pycache__ folders
    clean_pycache(os.path.dirname(__file__), language)

    # Phi-3 model to play the role of Analyst
    llm_anl = Ollama(model="phi3:14b-medium-128k-instruct-q4_K_M")
    # DeepSeek Coder model to play the role of Developer | Old model -> codegemma:7b-instruct-q4_K_M
    llm_dev = Ollama(model="deepseek-coder-v2:16b-lite-instruct-q4_K_M")
    # Lama-3 model to play the role of Squadleader
    llm_sq = Ollama(model="llama3.1:8b-instruct-q4_K_M")

    # Initializing Analyst
    analyst = Analyst(translate_string('main', 'analyst_name', language), llm_anl, analyst_properties, language, interactive=interactive)
    analyst.generate_report()
    analyst_report = analyst.output

    # Initializing Squad Leader
    squad_leader = SquadLeader(translate_string('main', 'squad_leader_name', language), llm_sq, analyst_properties, language, interactive=interactive)

    # Agents array
    agents = {
        translate_string('main', 'analyst_name', language): analyst,
        translate_string('main', 'squad_leader_name', language): squad_leader
    }

    # Creating developer agents and tester
    if generate_backend:
        backend_developer = Developer(translate_string('main', 'backend_developer_name', language), llm_dev, development_style, language, interactive=interactive)
        agents[translate_string('main', 'backend_developer_name', language)] = backend_developer

    if generate_frontend:
        frontend_developer = Developer(translate_string('main', 'frontend_developer_name', language), llm_dev, development_style, language, interactive=interactive)
        agents[translate_string('main', 'frontend_developer_name', language)] = frontend_developer

    if generate_tests:
        tester = Tester(translate_string('main', 'frontend_developer_name', language), llm_dev, language, interactive=interactive)
        agents[translate_string('main', 'tester_name', language)] = tester

    # Creating folder structure in the build
    project_base_path = os.path.join(os.path.dirname(__file__), "build", project_name)
    create_directories(project_base_path)

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

    # Generate the project general report
    squad_leader.generate_general_report(analyst_report)
    general_report = squad_leader.output

    # Generate developer and tester reports
    if generate_backend:
        squad_leader.generate_backend_backlog(general_report)
        backend_backlog = squad_leader.output

    if generate_frontend:
        squad_leader.generate_frontend_backlog(general_report)
        frontend_backlog = squad_leader.output
        
    if generate_tests:
        squad_leader.generate_test_backlog(general_report)
        test_backlog = squad_leader.output

    # Saving reports in the reports folder
    reports = {
        translate_string('main', 'project_report_file', language): general_report
    }

    if generate_backend:
        reports[translate_string('main', 'backend_report_file', language)] = backend_backlog
    if generate_frontend:
        reports[translate_string('main', 'frontend_report_file', language)] = frontend_backlog
    if generate_tests:
        reports[translate_string('main', 'test_report_file', language)] = test_backlog
    
    for report_file, report_content in reports.items():
        if report_content is not None:
            with open(os.path.join(project_base_path, "reports", report_file), 'w') as f:
                f.write(str(report_content))
    
    # Creating task graphs
    if generate_backend:
        backend_task_graph = build_task_graph(backend_backlog)
    if generate_frontend:
        frontend_task_graph = build_task_graph(frontend_backlog)
    if generate_tests:
        test_task_graph = build_task_graph(test_backlog)
        
    ## Processing Task Graphs
    if generate_backend:
        development_dir = os.path.join(project_base_path, "dev", backend_developer.name.lower().replace(' ', '_'))
        os.makedirs(development_dir, exist_ok=True)
        processing_task_graph_message = translate_string('main', 'processing_task_graph', language)
        print(f"{processing_task_graph_message} {backend_developer.name}")
        process_task_graph(backend_developer, backend_task_graph, development_dir)
    
    if generate_frontend:
        development_dir = os.path.join(project_base_path, "dev", frontend_developer.name.lower().replace(' ', '_'))
        os.makedirs(development_dir, exist_ok=True)
        processing_task_graph_message = translate_string('main', 'processing_task_graph', language)
        print(f"{processing_task_graph_message} {frontend_developer.name}")
        process_task_graph(frontend_developer, frontend_task_graph, development_dir)

    if generate_tests:
        test_dir = os.path.join(project_base_path, "dev", "tester")
        os.makedirs(test_dir, exist_ok=True)
        processing_task_graph_message = translate_string('main', 'processing_task_graph', language)
        print(f"{processing_task_graph_message} {tester.name}")
        process_task_graph(tester, test_task_graph, test_dir)

    # TO-DO - improve README prompt engeneering
    # Creating Project README
    readme_content = analyst.generate_readme(project_name, general_report, backend_backlog, frontend_backlog, test_backlog)
    with open(os.path.join(project_base_path, "README.md"), 'w') as f:
        f.write(readme_content)

def main():
    # Ask the user which language to use
    LANGUAGE = select_language()

    # Ask the user development style to use
    DEVSTYLE = select_development_style(LANGUAGE)

    project_name_key = "project_folder_name_message"
    project_name = input(translate_string('main', project_name_key, LANGUAGE) + ": ")
    
    analyst_properties = os.path.join(os.path.dirname(__file__), "project.properties")

    # Redirecting standard output to capture log
    original_stdout = sys.stdout
    captured_stdout = StringIO()
    sys.stdout = MultiOutput(original_stdout, captured_stdout)
    project_base_path = os.path.join(os.path.dirname(__file__), "build", project_name)

    try:
        start(project_name, analyst_properties, DEVSTYLE, LANGUAGE)
    finally:
        # Restore the original stdout
        sys.stdout = original_stdout
        # Get the captured output
        actions_report = captured_stdout.getvalue()
        actions_report_file = translate_string('main', 'execution_report_file', LANGUAGE)
        with open(os.path.join(project_base_path, actions_report_file), 'w') as f:
            f.write(actions_report)

if __name__ == "__main__":
    main()
