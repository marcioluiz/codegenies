# graph.py

import re

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

    def build_graph(self, agents):
        for agent_name, agent in agents.items():
            node = Node(agent_name)
            self.add_node(node)

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
            group_name = line.strip("**").strip()
            current_group_node = Node(group_name)
            nodes[group_name] = current_group_node
            graph.add_node(current_group_node)
        elif is_new_task_line(line):
            task_name = line
            if current_group_node:
                task_node = Node(task_name)
                current_group_node.add_subnode(task_node)
                nodes[task_name] = task_node
            else:
                task_node = Node(task_name)
                graph.add_node(task_node)
                nodes[task_name] = task_node
        elif line.startswith("##"):
            task_name = line
            if current_group_node:
                task_node = Node(task_name)
                current_group_node.add_subnode(task_node)
                nodes[task_name] = task_node
            else:
                task_node = Node(task_name)
                graph.add_node(task_node)
                nodes[task_name] = task_node
        else:
            task_name = line
            if current_group_node:
                task_node = Node(task_name)
                current_group_node.add_subnode(task_node)
                nodes[task_name] = task_node
            else:
                task_node = Node(task_name)
                graph.add_node(task_node)
                nodes[task_name] = task_node

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

    for node in task_graph.nodes:
        if node not in visited:
            dfs(node, visited, stack)

    while stack:
        node = stack.pop()
        if node.subnodes:
            for subnode in node.subnodes:
                developer.process_task(subnode.name, development_dir, extension)
        else:
            developer.process_task(subnode.name, development_dir, extension)
