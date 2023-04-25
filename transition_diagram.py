from scanner import Scanner

# TODO: tree

Symbols = {}  # name : object


class Symbol:
    def __init__(self, name: str, first = None, follow = None, terminal=None):
        self.name = name
        if terminal is None:
            self.terminal = name[0].islower()
        else:
            self.terminal = terminal
        if self.terminal:
            self.first = [self.name]
        else:
            self.first = first

        self.follow = follow
        Symbols[name] = self


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
        print(self.states[self.current_state])
        for transition_symbol in self.states[self.current_state]:
            transition_symbol = Symbols[transition_symbol]
            if self.current_token in transition_symbol.first or (
                    'EPS' in transition_symbol.first and self.current_token in transition_symbol.follow):
                self.current_state = self.states[self.current_state][transition_symbol]
                self.traversed_edge = transition_symbol
                return True
        return False


class Parser:
    def __init__(self, scanner_module, transition_diagrams):
        self.scanner = scanner_module
        self.transition_diagrams = transition_diagrams # {name of diagram : object}
        self.diagram_stack = []
        self.current_diagram = None
        self.current_token = None
        self.EOF = False

    def run(self):
        errors = []
        self.transition_diagrams['Program'].current_state = 'S0'
        self.current_diagram = self.transition_diagrams['Program']  # the name of the start state
        self.current_token = self.scanner.get_next_token()[1]
        self.diagram_stack.append(self.current_diagram)
        while not self.EOF:
            print(self.current_diagram.name)
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
            else:  # error
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
        return errors


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


transition_diagrams = {}
# Creating transition diagrams
# line 1
program_diagram = Transition_Diagram('Program')
program_diagram.add_state('S0', 'Declaration_list', 'FINAL')
transition_diagrams['Program'] = program_diagram

# line 2
declaration_list_diagram = Transition_Diagram('Declaration_list')
declaration_list_diagram.add_state('S0', 'Declaration', 'S1')
declaration_list_diagram.add_state('S1', 'Declaration_list', 'FINAL')
declaration_list_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Declaration_list'] = declaration_list_diagram

# line 3
declaration_diagram = Transition_Diagram('Declaration')
declaration_diagram.add_state('S0', 'Declaration_initial', 'S1')
declaration_diagram.add_state('S1', 'Declaration_prime', 'FINAL')
transition_diagrams['Declaration'] = declaration_diagram

# line 4
declaration_initial_diagram = Transition_Diagram('Declaration_initial')
declaration_initial_diagram.add_state('S1', 'ID', 'FINAL')
declaration_initial_diagram.add_state('S0', 'Type_specifier', 'S1')
transition_diagrams['Declaration_initial'] = declaration_initial_diagram

# line 5
declaration_prime_diagram = Transition_Diagram('Declaration_prime')
declaration_prime_diagram.add_state('S0', 'Fun_declaration_prime', 'FINAL')
declaration_prime_diagram.add_state('S0', 'Var_declaration_prime', 'FINAL')
transition_diagrams['Declaration_prime'] = declaration_prime_diagram

# line 6
var_declaration_prime_diagram = Transition_Diagram('Var_declaration_prime')
var_declaration_prime_diagram.add_state('S0', '[', 'S1')
var_declaration_prime_diagram.add_state('S2', ']', 'S3')
var_declaration_prime_diagram.add_state('S3', ';', 'FINAL')
var_declaration_prime_diagram.add_state('S0', ';', 'FINAL')
var_declaration_prime_diagram.add_state('S1', 'NUM', 'S2')
transition_diagrams['Var_declaration_prime'] = var_declaration_prime_diagram

# line 7
fun_declaration_prime_diagram = Transition_Diagram('Fun_declaration_prime')
fun_declaration_prime_diagram.add_state('S0', '(', 'S1')
fun_declaration_prime_diagram.add_state('S2', ')', 'S3')
fun_declaration_prime_diagram.add_state('S1', 'Params', 'S2')
fun_declaration_prime_diagram.add_state('S3', 'Compound_stmt', 'FINAL')
transition_diagrams['Fun_declaration_prime'] = fun_declaration_prime_diagram

# line 8
type_specifier_diagram = Transition_Diagram('Type_specifier')
type_specifier_diagram.add_state('S0','int', 'FINAL')
type_specifier_diagram.add_state('S0','void', 'FINAL')
transition_diagrams['Type_specifier'] = type_specifier_diagram

# line 9
params_diagram = Transition_Diagram('Params')
params_diagram.add_state('S0', 'int', 'S1')
params_diagram.add_state('S1', 'ID', 'S2')
params_diagram.add_state('S0', 'void', 'FINAL')
params_diagram.add_state('S2', 'Param_prime', 'S3')
params_diagram.add_state('S3', 'Param_list', 'FINAL')
transition_diagrams['Params'] = params_diagram

# line 10
param_list_diagram = Transition_Diagram('Param_list')
param_list_diagram.add_state('S0', ',', 'S1')
param_list_diagram.add_state('S1', 'Param', 'S2')
param_list_diagram.add_state('S2', 'Param_list', 'FINAL')
param_list_diagram.add_state('s0', 'EPS', 'FINAL')
transition_diagrams['Param_list'] = param_list_diagram

# line 11
param_diagram = Transition_Diagram('Param')
param_diagram.add_state('S0', 'Declaration_initial', 'S1')
param_diagram.add_state('S1', 'Param_prime', 'FINAL')
transition_diagrams['Param'] = param_diagram

# line 12
param_prime_diagram = Transition_Diagram('Param_prime')
param_prime_diagram.add_state('S0', '[', 'S1')
param_prime_diagram.add_state('S1', ']', 'FINAL')
params_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Param_prime'] = param_prime_diagram

# line 13
compound_stmt_diagram = Transition_Diagram('Compound_stmt')
compound_stmt_diagram.add_state('S0', '{', 'S1')
compound_stmt_diagram.add_state('S4', '}', 'FINAL')
compound_stmt_diagram.add_state('S1', 'Declaration_list', 'S2')
compound_stmt_diagram.add_state('S3', 'Statement_list', 'S4')
transition_diagrams['Compound_stmt'] = compound_stmt_diagram

# line 14
statement_list_diagram = Transition_Diagram('Statement_list')
statement_list_diagram.add_state('S0', 'Statement', 'S1')
statement_list_diagram.add_state('S1', 'Statement_list', 'S2')
statement_list_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Statement_list'] = statement_list_diagram

# line 15
statement_diagram = Transition_Diagram('Statement')
statement_diagram.add_state('S0', 'Expression_stmt', 'FINAL')
statement_diagram.add_state('S0', 'Compound_stmt', 'FINAL')
statement_diagram.add_state('S0', 'Selection_stmt', 'FINAL')
statement_diagram.add_state('S0', 'Iteration_stmt', 'FINAL')
statement_diagram.add_state('S0', 'Return_stmt', 'FINAL')
transition_diagrams['Statement'] = statement_diagram

# line 16
expression_stmt_diagram = Transition_Diagram('Expression_stmt')
expression_stmt_diagram.add_state('S0', 'break', 'S1')
expression_stmt_diagram.add_state('S1', ';', 'FINAL')
expression_stmt_diagram.add_state('S0', ';', 'FINAL')
expression_stmt_diagram.add_state('S0', 'Expression', 'S1')
transition_diagrams['Expression_stmt'] = expression_stmt_diagram

# line 17
selection_stmt_diagram = Transition_Diagram('Selection')
selection_stmt_diagram.add_state('S0', 'if', 'S1')
selection_stmt_diagram.add_state('S1', '(', 'S2')
selection_stmt_diagram.add_state('S3', ')', 'S4')
selection_stmt_diagram.add_state('S5', 'else', 'S6')
selection_stmt_diagram.add_state('S2', 'Expression', 'S3')
selection_stmt_diagram.add_state('S4', 'Statement', 'S5')
selection_stmt_diagram.add_state('S6', 'Statement', 'S7')
transition_diagrams['Selection'] = selection_stmt_diagram

# line 18
iteration_stmt_diagram = Transition_Diagram('Iteration')
iteration_stmt_diagram.add_state('S0', 'repeat', 'S1')
iteration_stmt_diagram.add_state('S2', 'until', 'S3')
iteration_stmt_diagram.add_state('S4', ')', 'FINAL')
iteration_stmt_diagram.add_state('S1', 'Statement', 'S2')
iteration_stmt_diagram.add_state('S3', 'Expression', 'S4')
transition_diagrams['Iteration'] = iteration_stmt_diagram

# line 19
return_stmt_diagram = Transition_Diagram('Return_stmt')
return_stmt_diagram.add_state('S0', 'return', 'S1')
return_stmt_diagram.add_state('S1', 'Return_stmt_prime', 'FINAL')
transition_diagrams['Return_stmt'] = return_stmt_diagram

# line 20
return_stmt_prime_diagram = Transition_Diagram('Return_stmt_prime')
return_stmt_prime_diagram.add_state('S1', ';', 'FINAL')
return_stmt_prime_diagram.add_state('S0', ';', 'FINAL')
return_stmt_prime_diagram.add_state('S0', 'Expression', 'S1')
transition_diagrams['Return_stmt_prime'] = return_stmt_prime_diagram

# line 21
expression_diagram = Transition_Diagram('Expression')
expression_diagram.add_state('S0', 'ID', 'S1')
expression_diagram.add_state('S1', 'B', 'FINAL')
expression_diagram.add_state('S0', 'Simple_expression_zegond', 'FINAL')
transition_diagrams['Expression'] = expression_diagram

# line 22
b_diagram = Transition_Diagram('B')
b_diagram.add_state('S0', '[', 'S1')
b_diagram.add_state('S2', ']', 'S3')
b_diagram.add_state('S0', '=', 'S4')
b_diagram.add_state('S3', 'H', 'FINAL')
b_diagram.add_state('S1', 'Expression', 'S2')
b_diagram.add_state('S4', 'Expression', 'FINAL')
transition_diagrams['B'] = b_diagram

# line 23
h_diagram = Transition_Diagram('H')
h_diagram.add_state('S0', '=', 'S3')
h_diagram.add_state('S0', 'G', 'S1')
h_diagram.add_state('S1', 'D', 'S2')
h_diagram.add_state('S2', 'C', 'FINAL')
h_diagram.add_state('S3', 'Expression', 'FINAL')
transition_diagrams['H'] = h_diagram

# line 24
simple_expression_zegond_diagram = Transition_Diagram('Simple_expression_zegond')
simple_expression_zegond_diagram.add_state('S0', 'Additive_expression_zegond', 'S1')
simple_expression_zegond_diagram.add_state('S1', 'C', 'FINAL')
transition_diagrams['Simple_expression_zegond'] = simple_expression_zegond_diagram

# line 25
simple_expression_prime_diagram = Transition_Diagram('Simple_expression_prime')
simple_expression_prime_diagram.add_state('S0', 'Additive_expression_prime', 'S1')
simple_expression_prime_diagram.add_state('S1', 'C', 'FINAL')
transition_diagrams['Simple_expression_prime'] = simple_expression_prime_diagram

# line 26
c_diagram = Transition_Diagram('C')
c_diagram.add_state('S0', 'Relop', 'S1')
c_diagram.add_state('S1', 'Additive_expression', 'FINAL')
c_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['C'] = c_diagram

# line 27
relop_diagram = Transition_Diagram('Relop')
relop_diagram.add_state('S0', '<', 'FINAL')
relop_diagram.add_state('S0', '==', 'FINAL')
transition_diagrams['Relop'] = relop_diagram

# line 28
additive_expression_diagram = Transition_Diagram('Additive_expression')
additive_expression_diagram.add_state('S0', 'Term', 'S1')
additive_expression_diagram.add_state('S1', 'D', 'FINAL')
transition_diagrams['Additive_expression'] = additive_expression_diagram

# line 29
additive_expression_prime_diagram = Transition_Diagram('Additive_expression_prime')
additive_expression_prime_diagram.add_state('S0', 'Term_prime', 'S1')
additive_expression_prime_diagram.add_state('S1', 'D', 'FINAL')
transition_diagrams['Additive_expression_prime'] = additive_expression_prime_diagram

# line 30
additive_expression_zegond_diagram = Transition_Diagram('Additive_expression_zegond')
additive_expression_zegond_diagram.add_state('S0', 'Term_zegond', 'S1')
additive_expression_zegond_diagram.add_state('S1', 'D', 'FINAL')
transition_diagrams['Additive_expression_zegond'] = additive_expression_zegond_diagram

# line 31
d_diagram = Transition_Diagram('D')
d_diagram.add_state('S0', 'Addop', 'S1')
d_diagram.add_state('S1', 'Term', 'S2')
d_diagram.add_state('S2', 'D', 'FINAL')
d_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['D'] = d_diagram

# line 32
addop_diagram = Transition_Diagram('Addop')
addop_diagram.add_state('S0', '+', 'FINAL')
addop_diagram.add_state('S0', '-', 'FINAL')
transition_diagrams['Addop'] = addop_diagram

# line 33
term_diagram = Transition_Diagram('Term')
term_diagram.add_state('S0', 'Factor', 'S1')
term_diagram.add_state('S1', 'G', 'FINAL')
transition_diagrams['Term'] = term_diagram

# line 34
term_diagram_prime = Transition_Diagram('Term_prime')
term_diagram_prime.add_state('S0', 'Factor_prime', 'S1')
term_diagram_prime.add_state('S1', 'G', 'FINAL')
transition_diagrams['Term_prime'] = term_diagram_prime

# line 35
term_diagram_zegond = Transition_Diagram('Term_zegond')
term_diagram_zegond.add_state('S0', 'Factor_zegond', 'S1')
term_diagram_zegond.add_state('S1', 'G', 'FINAL')
transition_diagrams['Term_zegond'] = term_diagram_zegond

# line 36
g_diagram = Transition_Diagram('G')
g_diagram.add_state('S0', '*', 'S1')
g_diagram.add_state('S1', 'Factor', 'S2')
g_diagram.add_state('S2', 'G', 'FINAL')
g_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['G'] = g_diagram

# line 37
factor_diagram = Transition_Diagram('Factor')
factor_diagram.add_state('S0', '(', 'S1')
factor_diagram.add_state('S2', ')', 'FINAL')
factor_diagram.add_state('S0', 'ID', 'S3')
factor_diagram.add_state('S0', 'NUM', 'FINAL')
factor_diagram.add_state('S1', 'Expression', 'S2')
factor_diagram.add_state('S3', 'Var_call_prime', 'FINAL')
transition_diagrams['Factor'] = factor_diagram

# line 38
var_call_prime_diagram = Transition_Diagram('Var_call_prime')
var_call_prime_diagram.add_state('S0', '(', 'S1')
var_call_prime_diagram.add_state('S2', ')', 'FINAL')
var_call_prime_diagram.add_state('S1', 'Args', 'S2')
var_call_prime_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Var_call_prime'] = var_call_prime_diagram

# line 39
var_prime_diagram = Transition_Diagram('Var_prime')
var_prime_diagram.add_state('S0', '[', 'S1')
var_prime_diagram.add_state('S2', ']', 'FINAL')
var_prime_diagram.add_state('S1', 'Expression', 'S2')
var_prime_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Var_prime'] = var_prime_diagram

# line 40
factor_prime_diagram = Transition_Diagram('Factor_prime')
factor_prime_diagram.add_state('S0', '(', 'S1')
factor_prime_diagram.add_state('S2', ')', 'FINAL')
factor_prime_diagram.add_state('S1', 'Args', 'S2')
factor_prime_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Factor_prime'] = factor_prime_diagram

# line 41
factor_zegond_diagram = Transition_Diagram('Factor_zegond')
factor_zegond_diagram.add_state('S0', '(', 'S1')
factor_zegond_diagram.add_state('S2', ')', 'FINAL')
factor_zegond_diagram.add_state('S0', 'NUM', 'FINAL')
factor_zegond_diagram.add_state('S1', 'Expression', 'S2')
transition_diagrams['Factor_zegond'] = factor_zegond_diagram

# line 42
args_diagram = Transition_Diagram('Args')
args_diagram.add_state('S0', 'Arg_list', 'FINAL')
args_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Args'] = args_diagram

# line 43
args_list_diagram = Transition_Diagram('Args_list')
args_list_diagram.add_state('S0', 'Expression', 'S1')
args_list_diagram.add_state('S1', 'Arg_list_prime', 'FINAL')
transition_diagrams['Args_list'] = args_list_diagram

# line 44
arg_list_prime_diagram = Transition_Diagram('Arg_list_prime')
arg_list_prime_diagram.add_state('S0', ',', 'S1')
arg_list_prime_diagram.add_state('S1', 'Expression', 'S2')
arg_list_prime_diagram.add_state('S2', 'Arg_list_prime', 'FINAL')
arg_list_prime_diagram.add_state('S0', 'EPS', 'FINAL')
transition_diagrams['Arg_list_prime'] = arg_list_prime_diagram






file_name = 'input.txt'
scanner = Scanner(file_name)
err_file = open('syntax_errors.txt', 'w')
parser = Parser(scanner, transition_diagrams)
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
