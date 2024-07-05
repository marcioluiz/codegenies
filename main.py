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
import inspect, json, os, shutil, sys
from io import StringIO
from agents import Analyst, SquadLeader, Developer, Tester
from graph import build_task_graph, process_task_graph
from langchain_community.llms import Ollama

# Global variable for language selection
LANGUAGE = None

def load_translations(module_name, lang):
    """
    Translate the given string key based on the selected language.

    Args:
    - module_name (str): Name of the module or file to load translations for.
    - lang (str): Language code ("pt-br" or "en-us").

    Returns:
    - dict: Translations dictionary for the specified module and language.
    """
    translations_file = os.path.join(os.path.dirname(__file__), "l18n", module_name + ".json")
    with open(translations_file, "r", encoding="utf-8") as f:
        translations = json.load(f)
    # Return translations for the specified language, default to empty dictionary if not found
    return translations.get(lang, {})  

def translate_string(module_name, key, lang):
    """
    Translate the given string key based on the selected language.
    
    Args:
    - key (str): Key to translate.
    - language (str): Language code ("pt-br" or "en-us").
    
    Returns:
    - str: Translated string if available, otherwise returns the original key.
    """
    translations = load_translations(module_name, lang)
    # Return the translation if found, otherwise return the original key
    return translations.get(key, key)

def select_language(self):
    """
    Prompt the user to select a language for the project.
    
    Returns:
    - str: Language code ("pt-br" or "en-us").
    """
    while True:
        lang_input = input("Select language / Selecione o idioma (pt-br / en-us): ").strip().lower()
        if lang_input in ["pt-br", "en-us"]:
            self.LANGUAGE = lang_input
            break
        else:
            print("Invalid selection / Seleção inválida. Please select 'pt-br' or 'en-us'.")
            continue

class MultiOutput:
    def __init__(self, *outputs):
        self.outputs = outputs

    def write(self, message):
        for output in self.outputs:
            output.write(message)

    def flush(self):
        for output in self.outputs:
            output.flush()

def clean_pycache(self, root_dir):
    """
    Removes __pycache__ folders from the specified directory.

    Args:
    - root_dir (str): Root directory path where cleaning should be performed.
    """
    
    # Get pycache message key translation
    pycache_message_key = "pycache_message_key"
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dir = os.path.join(root, dir_name)
                shutil.rmtree(pycache_dir)
                print(self.translate_string("main", pycache_message_key, LANGUAGE).format(pycache_dir))

        # Verifica se estamos na pasta agents ou na subpasta prompt_templates
        if 'agents' in root and 'prompt_templates' in dirs:
            prompt_templates_dir = os.path.join(root, 'prompt_templates')
            for sub_root, sub_dirs, sub_files in os.walk(prompt_templates_dir):
                for sub_dir_name in sub_dirs:
                    if sub_dir_name == "__pycache__":
                        sub_pycache_dir = os.path.join(sub_root, sub_dir_name)
                        shutil.rmtree(sub_pycache_dir)
                        print(self.translate_string("main", pycache_message_key, LANGUAGE).format(sub_pycache_dir))

def create_directories(project_base_path):
    """   
    Creates necessary folder structures in the project.

    Args:
    - project_base_path (str): Root path of the project where folders will be created.
    """
    base_dirs = ["agents", "reports", "dev"]
    for base_dir in base_dirs:
        os.makedirs(os.path.join(project_base_path, base_dir), exist_ok=True)

def start(project_name, analyst_properties):
    """
    Initializes and executes the project setup and execution process.
    Args:
    - project_name (str): Project name.
    - analyst_properties (str): Path to the analyst properties file.
    """

    # Define an interactive process
    interactive_key = "execute_interactive_prompt"
    interactive = input(translate_string("main", interactive_key, LANGUAGE)).strip().lower() == 's'
    
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
    generate_backend_key = "generate_all_prompt"
    generate_all = input(translate_string("main", generate_backend_key, LANGUAGE)).strip().lower() == 's'
    if generate_all:
        generate_backend = True
        generate_frontend = True
        generate_tests = True
    else:
        generate_backend_key = "generate_backend_prompt"
        generate_backend = generate_all or input(translate_string("main", generate_backend_key, LANGUAGE)).strip().lower() == 's'
        
        generate_frontend_key = "generate_frontend_prompt"
        generate_frontend = generate_all or input(translate_string("main", generate_frontend_key, LANGUAGE)).strip().lower() == 's'

        generate_tests_key = "generate_tests_prompt"
        generate_tests = generate_all or input(translate_string("main", generate_tests_key, LANGUAGE)).strip().lower() == 's'

    # Clean __pycache__ folders
    clean_pycache(os.path.dirname(__file__))

    # Phi-3 model to play the role of Analyst
    llm_anl = Ollama(model="phi3:14b-medium-128k-instruct-q4_K_M")
    # Codegemma model to play the role of Developer
    llm_dev = Ollama(model="codegemma:7b-instruct-v1.1-q4_K_M")
    # Lama-3 model to play the role of Squadleader
    llm_sq = Ollama(model="llama3:8b-instruct-q4_K_M")

    # Initializing Analyst
    analyst = Analyst(llm_anl, translate_string("main", "analyst_name", LANGUAGE), analyst_properties, LANGUAGE, interactive=interactive)
    analyst.generate_report()
    analyst_report = analyst.output

    # Initializing Squad Leader
    squad_leader = SquadLeader(llm_sq, interactive=interactive)

    # Agents array
    agents = {
        translate_string("main", "analyst_name", LANGUAGE): analyst,
        translate_string("main", "squad_leader_name", LANGUAGE): squad_leader
    }

    # Creating developer agents and tester
    if generate_backend:
        backend_developer = Developer(llm_dev, translate_string("main", "backend_developer_name", LANGUAGE), interactive=interactive)
        agents[translate_string("main", "backend_developer_name", LANGUAGE)] = backend_developer

    if generate_frontend:
        frontend_developer = Developer(llm_dev, translate_string("main", "frontend_developer_name", LANGUAGE), interactive=interactive)
        agents[translate_string("main", "frontend_developer_name", LANGUAGE)] = frontend_developer

    if generate_tests:
        tester = Tester(llm_dev, interactive=interactive)
        agents[translate_string("main", "tester_name", LANGUAGE)] = tester

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
        squad_leader.generate_backend_backlog(analyst_report)
        backend_backlog = squad_leader.output
    if generate_frontend:
        squad_leader.generate_frontend_backlog(analyst_report)
        frontend_backlog = squad_leader.output
    if generate_tests:
        squad_leader.generate_test_backlog(analyst_report)
        test_backlog = squad_leader.output

    # Saving reports in the reports folder
    reports = {
        translate_string("main", "project_report_file", LANGUAGE): general_report
    }

    if generate_backend:
        reports[translate_string("main", "backend_report_file", LANGUAGE)] = backend_backlog
    if generate_frontend:
        reports[translate_string("main", "frontend_report_file", LANGUAGE)] = frontend_backlog
    if generate_tests:
        reports[translate_string("main", "test_report_file", LANGUAGE)] = test_backlog
    
    for report_file, report_content in reports.items():
        if report_content is not None:
            with open(os.path.join(project_base_path, "reports", report_file), 'w') as f:
                f.write(str(report_content))
    
    # Creating task graphs
    backend_task_graph = build_task_graph(backend_backlog) if generate_backend else None
    frontend_task_graph = build_task_graph(frontend_backlog) if generate_frontend else None
    test_task_graph = build_task_graph(test_backlog) if generate_tests else None

    ## Processing Task Graphs
    if generate_backend:
        development_dir = os.path.join(project_base_path, "dev", backend_developer.name.lower().replace(' ', '_'))
        os.makedirs(development_dir, exist_ok=True)
        print(translate_string("main", "processing_task_graph", LANGUAGE).format(backend_developer.name))
        process_task_graph(backend_developer, backend_task_graph, development_dir)
    
    if generate_frontend:
        development_dir = os.path.join(project_base_path, "dev", frontend_developer.name.lower().replace(' ', '_'))
        os.makedirs(development_dir, exist_ok=True)
        print(translate_string("main", "processing_task_graph", LANGUAGE).format(frontend_developer.name))
        process_task_graph(frontend_developer, frontend_task_graph, development_dir)

    if generate_tests:
        test_dir = os.path.join(project_base_path, "dev", "tester")
        os.makedirs(test_dir, exist_ok=True)
        process_task_graph(tester, test_task_graph, test_dir)

    # TO-DO - create prompt logic to create project README
    # Creating Project README
    readme_content = f"# {project_name}\n\n[Insert project description here]"
    with open(os.path.join(project_base_path, "README.md"), 'w') as f:
        f.write(readme_content)

def main():
    # Ask the user which language they want to use
    select_language()

    project_name_key = "project_name_prompt"
    project_name = input(translate_string("main", project_name_key, LANGUAGE) + ": ")
    
    analyst_properties = os.path.join(os.path.dirname(__file__), "project.properties")

    # Redirecting standard output to capture log
    original_stdout = sys.stdout
    captured_stdout = StringIO()
    sys.stdout = MultiOutput(original_stdout, captured_stdout)
    project_base_path = os.path.join(os.path.dirname(__file__), "build", project_name)

    try:
        start(project_name, analyst_properties)
    finally:
        # Restore the original stdout
        sys.stdout = original_stdout
        # Get the captured output
        actions_report = captured_stdout.getvalue()
        actions_report_file = translate_string("main", "execution_report_file", LANGUAGE)
        with open(os.path.join(project_base_path, actions_report_file), 'w') as f:
            f.write(actions_report)

if __name__ == "__main__":
    main()
