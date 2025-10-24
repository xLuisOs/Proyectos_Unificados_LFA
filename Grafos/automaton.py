class Automaton:
    def __init__(self, graph, initial_state, accepting_states, alphabet):
        
        self.graph = graph
        self.states = graph.get_nodes()
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.accepting_states = accepting_states

        self.transitions = {}
        for node, neighbors in graph.graph.items():
            self.transitions[node] = neighbors.copy()  

    def is_valid_path(self, path):
        
        if not path or path[0] != self.initial_state:
            return False
        if path[-1] not in self.accepting_states:
            return False
        for i in range(len(path) - 1):
            if path[i+1] not in self.transitions.get(path[i], {}):
                return False
        return True
