import heapq

class ShortestPath:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start, end):
        
        if start not in self.graph.get_nodes() or end not in self.graph.get_nodes():
            return float('inf'), []

        queue = [(0, start, [start])]
        visited = set()

        while queue:
            dist, current, path = heapq.heappop(queue)
            if current == end:
                return dist, path
            if current in visited:
                continue
            visited.add(current)
            neighbors = self.graph.graph.get(current, {})
            for neighbor, weight in neighbors.items():
                if neighbor not in visited:
                    heapq.heappush(queue, (dist + weight, neighbor, path + [neighbor]))
        return float('inf'), []
