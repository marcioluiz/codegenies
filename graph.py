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

class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return f"Edge(from={self.from_node.name}, to={self.to_node.name})"
    
class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)})"

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
    def dfs(node, visited, stack):
        visited.add(node)
        # Ordenar os sub-nós em ordem alfabética antes de realizar a DFS
        # Sort sub-nodes alphabetically before performing DFS
        for subnode in node.subnodes:
            print(node.subnodes)
        for subnode in node.subnodes:
            if subnode not in visited:
                dfs(subnode, visited, stack)
        stack.append(node)

    visited = set()
    stack = []

    # Realiza a DFS para todos os nós do grafo, ordenando em ordem alfabética
    # Perform DFS for all nodes in the graph, sorting alphabetica
    for node in task_graph.nodes:
        if node not in visited:
            dfs(node, visited, stack)

    # Processa os nós em ordem topológica
    # Process nodes in topological order
    while stack:
        node = stack.pop()
        
        node_name = node.name.replace(' ', '_')
        match = re.search(r'##pastas\/(\w+)', node_name)
        if match:
           node_name = match.group(1)
        node_name = unidecode.unidecode(node_name)
        node_development_dir = os.path.join(development_dir, node_name)

        # Processa cada sub-nó com base na categoria do nó superior, em ordem alfabética
        # Process each sub-node based on the category of the parent node, alphabetically
        if node.subnodes:
            for subnode in node.subnodes:
                print(node.subnodes)
            for subnode in node.subnodes:
                subnode_name = subnode.name.replace(' ', '_')
                match = re.search(r'##pastas\/(\w+)', subnode_name)
                if match:
                    subnode_name = match.group(1)
                subnode_name = unidecode.unidecode(subnode_name)
                subnode_development_dir = os.path.join(node_development_dir, subnode_name)
                developer.process_task(subnode, subnode_development_dir, node.name)
        else:
            developer.process_task(node, node_development_dir, node.name)
