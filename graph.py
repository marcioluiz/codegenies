# graph.py

import re
import os

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
            group_name = line.strip("**").strip()
            current_group_node = Node(group_name)
            nodes[group_name] = current_group_node
            graph.add_node(current_group_node)
            current_task_node = None
        elif line.startswith("##"):
            # Identificar uma nova tarefa de criar pasta ou arquivo
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
            task_name = line
            task_node = Node(task_name)
            if current_group_node:
                current_group_node.add_subnode(task_node)
            else:
                graph.add_node(task_node)
            nodes[task_name] = task_node
            current_task_node = task_node

    return graph

def process_task_graph(developer, task_graph, development_dir, extension):
    def dfs(node, visited, stack):
        visited.add(node)
        for subnode in node.subnodes:
            if subnode not in visited:
                dfs(subnode, visited, stack)
        stack.append(node)

    visited = set()
    stack = []

    # Realiza a DFS para todos os nós do grafo
    for node in task_graph.nodes:
        if node not in visited:
            dfs(node, visited, stack)

    # Processa os nós em ordem topológica
    while stack:
        node = stack.pop()
        node_development_dir = os.path.join(development_dir, node.name.replace(' ', '_'))
        os.makedirs(node_development_dir, exist_ok=True)

        # Processa cada sub-nó com base na categoria do nó superior
        if node.subnodes:
            for subnode in node.subnodes:
                subnode_development_dir = os.path.join(node_development_dir, subnode.name.replace(' ', '_'))
                developer.process_task(subnode, subnode_development_dir, extension, node.name)
        else:
            developer.process_task(node, node_development_dir, extension, node.name)
