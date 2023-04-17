import scanner

# TODO: Handle errors from scanner + tree

Symbols = {} # name : object

class Symbol:
    def __init__(self, name: str, first, follow, terminal = None):
        self.name = name
        if terminal is None:
            self.terminal = name[0].islower()
        else:
            self.terminal = terminal
        self.first = first
        self.follow = follow
# eps is also a symbol name

class Transition_Diagram:
    def __init__(self, name):
        self.name = name
        self.states = {}
        """" Define the states and transitions with their associated tokens
        note to first add the terminal tokens then non-terminal then epsilon
        Indicate final state with 'FINAL'
        Ti is a Symbol object
        states = {
            "S": {
                T1: "S",
                T2: "S2",
                T3: "S2"
            },
            "S2": {}
        }
        """
        self.current_state = None
        self.current_token = None
        self.traversed_edge = None

    def add_state(self, begin_state, edge_token, end_state):
        if begin_state not in self.states:
            self.states[begin_state] = {}
        self.states[begin_state][edge_token] = end_state

    def transition(self):
        for transition_symbol in self.states[self.current_state]:
            if self.current_token in transition_symbol.first or ('EPS' in transition_symbol.first and self.current_token in transition_symbol.follow):
                self.current_state = self.states[self.current_state][transition_symbol]
                self.traversed_edge = transition_symbol
                return True
        return False


class Parser:
    def __init__(self, scanner_module):
        self.scanner = scanner_module
        self.transition_diagrams = {}  # {name of diagram : object}
        self.diagram_stack = []
        self.current_diagram = None
        self.current_token = None
        self.EOF = False

    def run(self):
        errors = []
        self.current_diagram = self.transition_diagrams['Program']  # the name of the start state
        self.current_token = self.scanner.get_next_token()[0]
        self.diagram_stack.append(self.current_diagram)
        while not self.EOF:
            if self.current_diagram.name == 'Program' and self.current_token == '$':
                break
            self.current_diagram = self.diagram_stack.pop()
            self.current_diagram.current_token = self.current_token
            if self.current_diagram.transition():
                if not self.current_diagram.current_state == 'FINAL':
                    edge = self.current_diagram.traversed_edge
                    if not edge.terminal:
                        self.diagram_stack.append(self.transition_diagrams[edge])
                    else:
                        self.current_token = self.scanner.get_next_token()[0]
                        self.diagram_stack.append(self.current_diagram)
            else: #error
                if self.current_token in Symbols[self.current_diagram.name].follow:
                    errors.append(f'{self.scanner.line} : syntax error, missing {self.current_diagram.name}')
                else:
                    errors.append(f'{self.scanner.line} : syntax error, illegal {self.current_token}')
                self.current_token = self.scanner.get_next_token()[0]
                while self.current_token not in Symbols[self.current_diagram.name].follow:
                    if self.current_token == '$':
                        errors.append(f'{self.scanner.line} : syntax error, Unexpected EOF')
                        self.EOF = True
                    errors.append(f'{self.scanner.line} : syntax error, illegal {self.current_token}')
                    self.current_token = self.scanner.get_next_token()[0]





parser = Parser(None)

# Creating line 1 transition diagrams (sample)
d = Transition_Diagram('Program')
# initializing the states (Symbols) and their first and follow sets
Symbol('Program', {'int', 'EPS'}, {'$'})
Symbol('Declaration_list', {'int', 'EPS'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Declaration', {'int'},
       {'ID', ';', 'NUM', '(', 'int', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Declaration_initial', {'int'},
       {';', '[', '(', ')', ','})
Symbol('Declaration_prime', {'(', ';'},
       {'ID', ';', 'NUM', '(', 'int', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Var_declaration_prime', {';'}, {'ID', ';', 'NUM', '(', 'int', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Fun_declaration_prime', {'('},
       {'ID', ';', 'NUM', '(', 'int', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Type_specifier', {'int'}, {'ID'})
Symbol('Params', {'int', 'void'}, {')'})
Symbol('Param_list', {',', 'EPS'}, {')'})
Symbol('Param', {'int'}, {')', ','})
Symbol('Param_prime', {'[', 'EPS'}, {')', ','})
Symbol('Compound_stmt', {'{'},
       {'ID', ';', 'NUM', '(', 'int', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return', '$'})
Symbol('Statement_list', {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'EPS'}, {'}'})
Symbol('Statement', {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'untill', 'return'})
Symbol('Expression_stmt', {'ID', ';', 'NUM', '(', 'break'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'untill', 'return'})
Symbol('Selection_stmt', {'if'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'untill', 'return'})
Symbol('Iteration_stmt', {'repeat'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'untill', 'return'})
Symbol('Return_stmt', {'return'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'untill', 'return'})
Symbol('Return_stmt_prime', {'ID', ';', 'NUM', '('},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'untill', 'return'})
Symbol('Expression', {'ID', 'NUM', '('}, {';', ']', ')', ','})
Symbol('B', {'[', '(', '=', '<', '==', '+', '-', '*', 'EPS'}, {';', ']', ')', ','})
Symbol('H', {'=', '<', '==', '+', '-', '*', 'EPS'}, {';', ']', ')', ','})
Symbol('Simple_expression_zegond', {'NUM', '('}, {';', ']', ')', ','})
Symbol('Simple_expression_prime', {'(', '<', '==', '+', '-', '*', '$'}, {';', ']', ')', ','})
Symbol('C', {'<', '==', 'EPS'}, {';', ']', ')', ','})
Symbol('Relop', {'<', '=='}, {'ID', 'NUM', '('})
Symbol('Additive_expression', {'ID', 'NUM', '('}, {';', ']', ')', ','})
Symbol('Additive_expression_prime', {'(', '+', '-', '*', 'EPS'}, {';', ']', ')', ',', '<', '=='})
Symbol('Additive_expression_zegond', {'NUM', '('}, {';', ']', ')', ',', '<', '=='})
Symbol('D', {'+', '-', 'EPS'}, {';', ']', ')', ',', '<', '=='})
Symbol('Addop', {'+', '-'}, {'ID', 'NUM', '('})
Symbol('Term', {'ID', 'NUM', '('}, {';', ',', ']', ')'})
Symbol('Term_prime', {'(', '*', 'EPS'}, {';', ',', ']', ')'})
Symbol('Term_zegond', {'NUM', '('}, {';', ',', ']', ')'})
Symbol('G', {'*', 'EPS'}, {';', ',', ']', ')'})
Symbol('Factor', {'ID', 'NUM', '('}, {';', ',', ']', ')', '*'})
Symbol('Var_call_prime', {'[', '(', 'EPS'}, {';', ',', ']', ')', '*'})
Symbol('Var_prime', {'[', 'EPS'}, {';', ',', ']', ')', '*'})
Symbol('Factor_prime', {'(', 'EPS'}, {';', ',', ']', ')', '*'})
Symbol('Factor_zegond', {'(', 'NUM'}, {';', ',', ']', ')', '*'})
Symbol('Args', {'ID', 'NUM', '(', 'EPS'}, {')'})
Symbol('Arg_list', {'ID', 'NUM', '('}, {')'})
Symbol('Arg_list_prime', {',', 'EPS'}, {')'})
