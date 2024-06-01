# graph.py

import re

class Node:
    def __init__(self, data):
        self.data = data
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def build_graph(self, agents):
        for agent_name, agent in agents.items():
            node = Node(agent_name)
            self.add_node(node)

def build_task_graph(backlog):
    graph = Graph()
    tasks = backlog.splitlines()
    nodes = {}
    edges = []

    def is_new_task_line(line):
        return bool(re.match(r'^[A-Za-z0-9]+\.', line.strip()))

    current_task = None
    for line in tasks:
        if is_new_task_line(line):
            task_name = line.strip()
            node = Node(task_name)
            nodes[task_name] = node
            graph.add_node(node)
            if current_task:
                edge = Edge(nodes.get(current_task), node)
                graph.add_edge(edge)
            current_task = task_name
        else:
            current_task = line.strip()

    return graph

def process_task_graph(developer, task_graph, development_dir, extension):
    def dfs(node, visited, stack):
        visited.add(node)
        for neighbor in node.neighbors:
            if neighbor not in visited:
                dfs(neighbor, visited, stack)
        stack.append(node)

    visited = set()
    stack = []

    for node in task_graph.nodes:
        if node not in visited:
            dfs(node, visited, stack)

    while stack:
        node = stack.pop()
        developer.process_task(node.data, development_dir, extension)
