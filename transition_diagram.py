from scanner import Scanner
from anytree import RenderTree
from copy import deepcopy
from DATA import make_diagrams, Transition_Diagram, Symbols, ParserNode


# TODO: tree, lexical errors?


def transition(self):
    print('**********')
    print(self.name)
    print(self.current_state)
    print(self.current_token)
    # print(self.states[self.current_state])
    # print('**********')
    if self.current_state == 'FINAL':
        return 'FINAL'
    for transition_symbol in self.states[self.current_state]:
        if transition_symbol == 'EPS':
            if self.current_token in Symbols[self.name].follow:
                self.current_state = self.states[self.current_state]['EPS']
                self.traversed_edge = 'EPS'
                return 'SUCCESS'
            else:
                continue
        transition_symbol = Symbols[transition_symbol]
        if self.current_token in transition_symbol.first or (
                'EPS' in transition_symbol.first and self.current_token in transition_symbol.follow):
            self.current_state = self.states[self.current_state][transition_symbol.name]
            self.traversed_edge = transition_symbol
            return 'SUCCESS'
    return 'ERR'


Transition_Diagram.transition = transition


class Parser:
    def __init__(self, scanner_module, transition_diagrams):
        self.scanner = scanner_module
        self.transition_diagrams = transition_diagrams  # {name of diagram : object}
        self.diagram_stack = []
        self.current_diagram = None
        self.current_token = None
        self.EOF = False
        self.root = None

    def run(self):
        errors = []
        self.transition_diagrams['Program'].current_state = 'S0'
        self.current_diagram = self.transition_diagrams['Program']  # the name of the start state
        self.current_token = self.scanner.get_next_token()
        self.diagram_stack.append(self.current_diagram)
        self.root = self.current_diagram.parser_node
        while self.diagram_stack:
            if self.EOF:
                break
            self.current_diagram = self.diagram_stack[-1]
            if self.current_diagram.name == 'Program' and self.current_token == '$':
                break
            # print(self.current_diagram.name, '***')
            self.current_diagram.current_token = self.current_token
            transition_res = self.current_diagram.transition()
            if transition_res == 'SUCCESS':
                edge = self.current_diagram.traversed_edge
                if edge == 'EPS':
                    # ParserNode('epsilon', parent=self.current_diagram.parser_node)
                    continue
                elif edge.terminal:
                    # ParserNode(edge.name, parent=self.current_diagram.parser_node)
                    self.current_token = self.scanner.get_next_token()
                else:
                    # ParserNode(edge.name, parent=self.current_diagram.parser_node)
                    diagram_instance = deepcopy(self.transition_diagrams[edge.name])
                    diagram_instance.current_state = 'S0'
                    self.diagram_stack.append(diagram_instance)
            elif transition_res == 'FINAL':
                self.diagram_stack.pop()
            else:  # error
                # print('%%%%%%%%%%%%%')
                # print(self.current_diagram.name)
                # print(self.current_diagram.current_state)
                # print(self.current_token)
                # print(self.current_diagram.traversed_edge.name)
                # print('%%%%%%%%%%%%%')
                if self.current_token in Symbols[self.current_diagram.name].follow:
                    errors.append(f'{self.scanner.line} : syntax error, missing {self.current_diagram.name}')
                else:
                    errors.append(f'{self.scanner.line} : syntax error, illegal {self.current_token}')
                self.current_token = self.scanner.get_next_token()
                while self.current_token not in Symbols[self.current_diagram.name].follow:
                    if self.current_token == '$':
                        errors.append(f'{self.scanner.line} : syntax error, Unexpected EOF')
                        self.EOF = True
                    errors.append(f'{self.scanner.line} : syntax error, illegal {self.current_token}')
                    self.current_token = self.scanner.get_next_token()
        return errors


file_name = 'input.txt'
scanner = Scanner(file_name)
err_file = open('syntax_errors.txt', 'w')
parser = Parser(scanner, make_diagrams())
err = parser.run()
if not err:
    err_file.write('There is no syntax error.')
else:
    line = 0
    for e in err:
        err_file.write(e)
        line += 1
        if not line == len(err):
            err_file.write('\n')

# print(RenderTree(parser.root))