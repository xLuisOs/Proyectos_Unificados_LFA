import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, directed=False):
        self.graph = {}
        self.directed = directed

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, node1, node2, weight=1):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1][node2] = weight
            if not self.directed:
                self.graph[node2][node1] = weight

    def get_nodes(self):
        return list(self.graph.keys())

    def get_edges(self):
        edges = []
        for node, connections in self.graph.items():
            for neighbor, weight in connections.items():
                edges.append((node, neighbor, weight))
        return edges

    def show_graph(self):
        print("\n--- Grafo ---")
        for node, connections in self.graph.items():
            for neighbor, weight in connections.items():
                print(f"{node} --({weight})--> {neighbor}")

    def visualize(self):
        G = nx.DiGraph() if self.directed else nx.Graph()

        for node in self.graph:
            G.add_node(node)
        for node, connections in self.graph.items():
            for neighbor, weight in connections.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = nx.spring_layout(G)
        weights = nx.get_edge_attributes(G, 'weight')

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1800,
                font_size=12, font_weight='bold', arrows=self.directed, arrowstyle='-|>')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
        plt.title("Visualización del Grafo")
        plt.show()
