# graph.py

class Node:
    def __init__(self, agent):
        self.agent = agent
        self.children = []

    def add_child(self, agent):
        self.children.append(agent)

    def remove_child(self, agent):
        self.children.remove(agent)

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, agent):
        node = Node(agent)
        self.nodes[agent.name] = node

    def add_edge(self, parent_name, child_name):
        parent_node = self.nodes[parent_name]
        child_node = self.nodes[child_name]
        parent_node.add_child(child_node)

    def remove_edge(self, parent_name, child_name):
        parent_node = self.nodes[parent_name]
        child_node = self.nodes[child_name]
        parent_node.remove_child(child_node)

    def get_children(self, agent_name):
        return self.nodes[agent_name].children

    def build_graph(self, agents):
        for agent in agents.values():
            self.add_node(agent)

        for parent_name in agents:
            if parent_name == "Líder de Equipe":  # Corrigindo para o nome correto
                continue
            for child_name in agents:
                if parent_name != child_name:
                    self.add_edge("Líder de Equipe", child_name)  # Corrigindo para o nome correto
