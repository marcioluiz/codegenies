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
    tasks = backlog.splitlines()
    nodes = {}
    current_group_node = None

    def is_new_task_line(line):
        return bool(re.match(r'^[A-Za-z0-9]+\.', line.strip()))

    for line in tasks:
        line = line.strip()
        if not line:
            continue
        if line.startswith("**") and line.endswith("**"):
            # Identificar uma nova categoria de tarefas
            # Identify a new category of tasks
            group_name = line.strip("**").strip()
            current_group_node = Node(group_name)
            nodes[group_name] = current_group_node
            graph.add_node(current_group_node)
            current_task_node = None
        elif line.startswith("##"):
            # Identificar uma nova tarefa de criar pasta ou arquivo
            # Identify a new task to create folder or file
            task_name = line.strip("##").strip()
            task_node = Node(task_name)
            if current_group_node:
                current_group_node.add_subnode(task_node)
            else:
                graph.add_node(task_node)
            nodes[task_name] = task_node
            current_task_node = task_node
        elif line.startswith("*"):
            # Identificar uma nova função a ser criada dentro de um arquivo
            # Identify a new function to be created within a file
            function_name = line.strip("*").strip()
            function_node = Node(function_name)
            if current_task_node:
                current_task_node.add_subnode(function_node)
            elif current_group_node:
                current_group_node.add_subnode(function_node)
            else:
                graph.add_node(function_node)
            nodes[function_name] = function_node
        else:
            # Linha que não corresponde a nenhuma das categorias acima
            # Line that doesn't match any of the above categories
            task_name = line
            task_node = Node(task_name)
            if current_group_node:
                current_group_node.add_subnode(task_node)
            else:
                graph.add_node(task_node)
            nodes[task_name] = task_node
            current_task_node = task_node

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
    for node in task_graph.nodes[0].subnodes:
        if "##" in node.name:
            node_name = node.name.replace(' ', '_')
            # Testa se encontra o padrão "##pasta/nomedoarquivo e demais instruções"
            # Tests if the pattern "##folder/filename and other instructions" is found
            match = re.search(r'##(\w+)\/(\w+)', node_name)
            if match:
                node_name = match.group(1)
            elif not match:
                # Testa se encontra o padrão "##pasta-nome/nomedoarquivo e demais instruções"
                # Tests if the pattern "##folder-name/filename and other instructions" is found
                match = re.search(r'##(\w+)-(\w+)\/(\w+)', node_name)
            if match:
                node_name = f"{match.group(1)}-{match.group(2)}"
            node_name = unidecode.unidecode(node_name)
            node_development_dir = os.path.join(development_dir, node_name)

            developer.process_task(node, node_development_dir, task_graph.nodes[0].name)
