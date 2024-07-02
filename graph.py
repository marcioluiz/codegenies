# graph.py
"""
graph.py

Este arquivo contém funções para a construção e processamento de grafos de tarefas. 
Os grafos são utilizados para organizar e gerenciar as tarefas de desenvolvimento e teste do projeto.

Principais Funções:

- build_task_graph(backlog): Constrói um grafo de tarefas a partir de um backlog.
  - backlog (str): Backlog de tarefas em formato de string.

- process_task_graph(agent, task_graph, output_dir): Processa um grafo de tarefas e gera os arquivos de código correspondentes.
  - agent (object): Agente responsável por processar as tarefas (Developer ou Tester).
  - task_graph (Graph): Grafo de tarefas a ser processado.
  - output_dir (str): Diretório de saída onde os arquivos gerados serão salvos.

English version:

This file contains functions for constructing and processing task graphs. 
Graphs are used to organize and manage project development and testing tasks.

Main Functions:

- build_task_graph(backlog): Builds a task graph from a backlog.
  - backlog (str): Task backlog in string format.

- process_task_graph(agent, task_graph, output_dir): Processes a task graph and generates corresponding code files.
  - agent (object): Agent responsible for processing tasks (Developer or Tester).
  - task_graph (Graph): Task graph to be processed.
  - output_dir (str): Output directory where generated files will be saved.
     

"""

import re
import os
import unidecode

class Node:
    def __init__(self, name):
        self.name = name
        self.subnodes = []

    def add_subnode(self, subnode):
        self.subnodes.append(subnode)

    def __repr__(self):
        return f"Node({self.name}, subnodes={len(self.subnodes)})"
    
class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)})"

def build_task_graph(backlog):
    """
    Constrói um grafo de tarefas a partir de um backlog.

    Args:
        - backlog (str): Backlog de tarefas em formato de string.
    Returns:
        - Graph: Grafo de tarefas construído a partir do backlog.

    English:
    
    Builds a task graph from a backlog.

    Args:
        - backlog (str): Task backlog in string format.
    Returns:
        - Graph: Task graph built from the backlog.
    """
    graph = Graph()
    current_group_node = None
    nodes = {}

    for line in backlog.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("**") and line.endswith("**"):
            # Identificar uma nova categoria de tarefas
            # Identify a new category of tasks
            group_name = line.strip("**").strip()
            current_group_node = nodes.setdefault(group_name, Node(group_name))
            graph.add_node(current_group_node)
        elif line.startswith("##") or line.startswith("*"):
            # Identificar uma nova tarefa e suas subtarefas
            # Identify a new task and its subtasks
            task_node = nodes.setdefault(task_name, Node(task_name))
            if current_group_node:
                current_group_node.add_subnode(task_node)
            else:
                graph.add_node(task_node)
        else:
            # Linha que não corresponde a nenhuma das categorias acima
            # Line that doesn't match any of the above categories
            task_name = line
            task_node = nodes.setdefault(task_name, Node(task_name))
            if current_group_node:
                current_group_node.add_subnode(task_node)
            else:
                graph.add_node(task_node)

    return graph

def process_task_graph(developer, task_graph, development_dir):
    """
    Processa um grafo de tarefas e gera os arquivos de código correspondentes.

    Args:
        - agent (object): Agente responsável por processar as tarefas (Developer ou Tester).
        - task_graph (Graph): Grafo de tarefas a ser processado.
        - output_dir (str): Diretório de saída onde os arquivos gerados serão salvos.

    English:
        
    Processes a task graph and generates corresponding code files.

    Args:
        - agent (object): Agent responsible for processing tasks (Developer or Tester).
        - task_graph (Graph): Task graph to be processed.
        - output_dir (str): Output directory where generated files will be saved.
    """

    # Lista de padrões de nomes de pstas a serem testados
    # List of folder name patterns to test
    patterns = [
        # 1. "##pasta/nomedoarquivo"
        #    "##folder/filename"
        (r'##(\w+)\/(\w+)', 0),
        # 2. "##pasta-nome/nomedoarquivo"
        #    "##folder-name/filename"
        (r'##(\w+)-(\w+)\/(\w+)', 1),
        # 3. "##pasta1/pasta2/nomedoarquivo"
        #    "##folder1/folder2/filename"
        (r'##(\w+)\/(\w+)\/(\w+)', 2),
        # 4. "##pasta1/pasta2-nome/nomedoarquivo"
        #    "##folder1/folder2-name/filename"
        (r'##(\w+)\/(\w+)-(\w+)\/(\w+)', 3)
    ]

    for node in task_graph.nodes[0].subnodes:
        if "##" in node.name:
            node_name = node.name.replace(' ', '_')
            found_match = False

            # Identifica qual o padrão de nome de pastas da tarefa
            # Identifies the task's folder name pattern
            for pattern, index in patterns:
                match = re.search(pattern, node_name)
                if match:
                    if index == 0:
                        node_name = match.group(1)
                    elif index == 1:
                        node_name = f"{match.group(1)}-{match.group(2)}"
                    elif index == 2:
                        node_name = f"{match.group(1)}/{match.group(2)}"
                    elif index == 3:
                        node_name = f"{match.group(1)}/{match.group(2)}-{match.group(3)}"
                    found_match = True
                    break
            
            if not found_match:
                continue

            node_name = unidecode.unidecode(node_name)
            node_development_dir = os.path.join(development_dir, node_name)
            # Processa Tarefa
            # Process Task
            developer.process_task(node, node_development_dir)
