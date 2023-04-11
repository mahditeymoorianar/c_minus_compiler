import scanner

# TODO: Handle $ + Add panic mode + First and follow to detect errors early + tree

terminals = []
non_terminals = ['Program', ' Declaration-list',]   # This is line 1 and so on...

class Transition_Diagram:
    def __init__(self, name):
        self.name = name
        self.states = {}
        """" Define the states and transitions with their associated tokens
        note to first add the terminal tokens then non-terminal then epsilon
        I assume this is the order we need to check
        Indicate final state with 'FINAL'
        states = {
            "S": {
                "T1": "S",
                "T2": "S2",
                "T3": "S2"
            },
            "S2": {}
        }
        """
        self.current_state = None
        self.current_token = None
        self.traversed_edge = None

    def add_state (self, begin_state, edge_token, end_state):
        if begin_state not in self.states:
            self.states[begin_state] = {}
        self.states[begin_state][edge_token] = end_state

    def transition(self):
        for transition_token in self.states[self.current_state]:
            if transition_token in terminals:
                if transition_token == self.current_token:
                    self.current_state = self.states[self.current_state][transition_token]
                    self.traversed_edge = 'TERMINAL'
                    return
            else:
                self.current_state = self.states[self.current_state][transition_token]
                self.traversed_edge = transition_token
                return


class Parser:
    def __init__(self, scanner_module):
        self.scanner = scanner_module
        self.transition_diagrams = {}       # {name of diagram : object}
        self.diagram_stack = []
        self.current_diagram = None

    def run(self):
        self.current_diagram = self.transition_diagrams['Program']      # the name of the start state
        self.current_diagram.current_token = self.scanner.get_next_token()
        self.diagram_stack.append(self.current_diagram)
        while True:
            self.current_diagram = self.diagram_stack.pop()
            self.current_diagram.transition()
            if not self.current_diagram.current_state == 'FINAL':
                edge = self.current_diagram.traversed_edge
                if not edge == 'TERMINAL':
                    self.diagram_stack.append(self.transition_diagrams[edge])
                else:
                    self.current_diagram.current_token = self.scanner.get_next_token()
                    self.diagram_stack.append(self.current_diagram)


parser = Parser(None)

# Creating line 1 transition diagrams (sample)
d = Transition_Diagram('Program')
d.add_state('1', ' Declaration-list', 'FINAL')
parser.transition_diagrams['Program'] = d
