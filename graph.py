# graph.py
"""
graph.py

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
    Builds a task graph from a backlog.

    Args:
        - backlog (str): Task backlog in string format.
    Returns:
        - Graph: Task graph built from the backlog.
    """
    graph = Graph()
    current_group_node = None
    current_task_node = None
    nodes = {}

    for line in backlog.splitlines():
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("**") and line.endswith("**"):
            # New task category
            group_name = line.strip("**").strip()
            current_group_node = nodes.setdefault(group_name, Node(group_name))
            graph.add_node(current_group_node)
            current_task_node = None
            
        elif "##" in line:
            # New task to create folder or file
            task_name = line
            task_node = nodes.setdefault(task_name, Node(task_name))
            if current_group_node:
                current_group_node.add_subnode(task_node)
            else:
                graph.add_node(task_node)
            current_task_node = task_node
    
        elif line.startswith("*") or line.startswith("+"):
            # New function to be created inside a file
            if current_task_node:
                function_name = line
                function_node = nodes.setdefault(function_name, Node(function_name))
                current_task_node.add_subnode(function_node)
            else:
                # Treat as task if there is no current task node
                task_name = line
                task_node = nodes.setdefault(task_name, Node(task_name))
                if current_group_node:
                    current_group_node.add_subnode(task_node)
                else:
                    graph.add_node(task_node)
        
        else:
            # Line that does not match any of the categories above
            task_name = line
            task_node = nodes.setdefault(task_name, Node(task_name))
            if current_group_node:
                current_group_node.add_subnode(task_node)
            else:
                graph.add_node(task_node)
            current_task_node = task_node

    return graph
    

def process_task_graph(developer, task_graph, development_dir):
    """
    Processes a task graph and generates corresponding code files.

    Args:
        - agent (object): Agent responsible for processing tasks (Developer or Tester).
        - task_graph (Graph): Task graph to be processed.
        - output_dir (str): Output directory where generated files will be saved.
    """

    # List of folder name patterns to test
    patterns = [
        # 1. "##folder/filename"
        (r'##(\w+)\/(\w+)', 0),
        # 2. "##folder-name/filename"
        (r'##(\w+)-(\w+)\/(\w+)', 1),
        # 3. "##folder1/folder2/filename"
        (r'##(\w+)\/(\w+)\/(\w+)', 2),
        # 4. "##folder1/folder2-name/filename"
        (r'##(\w+)\/(\w+)-(\w+)\/(\w+)', 3)
    ]

    # Find the index of the root node starting and ending with "**"
    root_index = None
    for idx, node in enumerate(task_graph.nodes):
        if node.name.startswith("**") and node.name.endswith("**"):
            root_index = idx
            break

    if root_index is None:
        # Handle case where no root node with "**" markers is found
        raise ValueError("No root node found starting and ending with '**'.")

    for node in task_graph.nodes[root_index].subnodes:
        if "##" in node.name:
            node_name = node.name.replace(' ', '_')
            found_match = False

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
            # Process Task
            developer.process_task(node, node_development_dir)
