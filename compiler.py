from scanner import Scanner
from anytree import RenderTree
from copy import deepcopy
from parser_utils import make_diagrams, Transition_Diagram, ParserNode, is_terminal
from codegen import CodeGen

# TODO: lexical errors?
all_diagrams = make_diagrams()


def enter_diagram(diagram_name, current_token):
    diagram = all_diagrams[diagram_name]
    for transition_symbol_full in diagram.states['S0']:
        if "#" in transition_symbol_full:
            strings = transition_symbol_full.split("#")
            transition_symbol = strings[0]
        else:
            transition_symbol = transition_symbol_full
        if transition_symbol == 'EPS':
            if current_token in diagram.follow:
                return transition_symbol_full
            else:
                continue
        if is_terminal(transition_symbol):
            if transition_symbol == current_token:
                return transition_symbol_full
            else:
                continue
        else:
            transition_symbol = all_diagrams[transition_symbol]
            if current_token in transition_symbol.first or (
                    'EPS' in transition_symbol.first and current_token in transition_symbol.follow):
                return transition_symbol_full
    return None


def transition(self):
    if self.current_state == 'FINAL':
        return 'FINAL'
    if self.current_state == 'S0':
        transition_symbol_full = enter_diagram(self.name, self.current_token)
        if transition_symbol_full:
            if "#" in transition_symbol_full:
                strings = transition_symbol_full.split("#")
                transition_symbol = strings[0]
                action = strings[1]
                # print(f'code_generator.{action}()')
                eval(f'code_generator.{action}()')
            else:
                transition_symbol = transition_symbol_full
            self.current_state = self.states[self.current_state][transition_symbol_full]
            self.traversed_edge = transition_symbol
            return 'SUCCESS'
        else:
            return 'ERR_NT'
    else:
        transition_symbol_full = list(self.states[self.current_state].keys())[0]
        if "#" in transition_symbol_full:
            strings = transition_symbol_full.split("#")
            transition_symbol = strings[0]
            action = strings[1]
            # print(f'code_generator.{action}()')
            eval(f'code_generator.{action}()')
        else:
            transition_symbol = transition_symbol_full
        if is_terminal(transition_symbol) or transition_symbol == 'EPS':
            self.current_state = self.states[self.current_state][transition_symbol_full]
            self.traversed_edge = transition_symbol
            if self.current_token == transition_symbol or transition_symbol == 'EPS':
                return 'SUCCESS'
            else:
                return 'ERR_T'
        else:
            transition_symbol = all_diagrams[transition_symbol]
            if enter_diagram(transition_symbol.name, self.current_token):
                self.current_state = self.states[self.current_state][transition_symbol_full]
                self.traversed_edge = transition_symbol.name
                return 'SUCCESS'
            else:
                if self.current_token in transition_symbol.follow:
                    self.current_state = self.states[self.current_state][transition_symbol_full]
                    self.traversed_edge = transition_symbol.name
                    return 'ERR_MISS'
                else:
                    return 'ERR_IL'


Transition_Diagram.transition = transition


class Parser:
    def __init__(self, scanner_module, transition_diagrams):
        self.scanner = scanner_module
        self.transition_diagrams = transition_diagrams  # {name of diagram : object}
        self.diagram_stack = []
        self.current_diagram = None
        self.current_token_full = None
        self.current_token = None
        self.EOF = False
        self.root = None

    def tokenize(self, token):
        if token.token == 'SYMBOL' or token.token == 'KEYWORD' or token.token == 'EOF':
            return token.lexeme
        else:
            return token.token

    def run(self):
        errors = []
        self.transition_diagrams['Program'].current_state = 'S0'
        self.current_diagram = self.transition_diagrams['Program']  # the name of the start state
        self.current_token_full = self.scanner.get_next_token()
        self.current_token = self.tokenize(self.current_token_full)
        self.diagram_stack.append(self.current_diagram)
        self.root = self.current_diagram.parser_node
        while self.diagram_stack:
            # print(self.current_diagram.name)
            # print(self.current_diagram.current_state)
            # print(self.current_token)
            if self.EOF:
                break
            self.current_diagram = self.diagram_stack[-1]
            if self.current_diagram.name == 'Program' and self.current_token == '$':
                code_generator.end_program()
                ParserNode('$', parent=self.current_diagram.parser_node)
                break
            self.current_diagram.current_token = self.current_token
            transition_res = self.current_diagram.transition()
            if transition_res == 'SUCCESS':
                edge = self.current_diagram.traversed_edge
                if edge == 'EPS':
                    ParserNode('epsilon', parent=self.current_diagram.parser_node)
                    continue
                elif is_terminal(edge):
                    ParserNode(f"({self.current_token_full.token}, {self.current_token_full.lexeme})",
                               parent=self.current_diagram.parser_node)
                    self.current_token_full = self.scanner.get_next_token()
                    self.current_token = self.tokenize(self.current_token_full)
                else:
                    diagram_instance = deepcopy(self.transition_diagrams[edge])
                    diagram_instance.current_state = 'S0'
                    diagram_instance.parser_node = ParserNode(edge, parent=self.current_diagram.parser_node)
                    self.diagram_stack.append(diagram_instance)
            elif transition_res == 'FINAL':
                self.diagram_stack.pop()
            else:  # error
                if self.current_token == '$':
                    errors.append(f'#{self.scanner.line} : syntax error, Unexpected EOF')
                    self.EOF = True
                elif transition_res == 'ERR_T':
                    errors.append(f'#{self.scanner.line} : syntax error, missing {self.current_diagram.traversed_edge}')
                elif transition_res == 'ERR_NT':
                    if self.current_token in self.current_diagram.follow:
                        errors.append(f'#{self.scanner.line} : syntax error, missing {self.current_diagram.name}')
                        self.diagram_stack.pop()
                    else:
                        errors.append(f'#{self.scanner.line} : syntax error, illegal {self.current_token}')
                        self.current_token_full = self.scanner.get_next_token()
                        self.current_token = self.tokenize(self.current_token_full)
                elif transition_res == 'ERR_MISS':
                    errors.append(f'#{self.scanner.line} : syntax error, missing {self.current_diagram.traversed_edge}')
                elif transition_res == 'ERR_IL':
                    errors.append(f'#{self.scanner.line} : syntax error, illegal {self.current_token}')
                    self.current_token_full = self.scanner.get_next_token()
                    self.current_token = self.tokenize(self.current_token_full)

        return errors


file_name = 'input.txt'
scanner = Scanner(file_name)
err_file = open('syntax_errors.txt', 'w')
tree_file = open('parse_tree.txt', 'wb')
parser = Parser(scanner, all_diagrams)
code_generator = CodeGen(parser)
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

tree_file.write(format(RenderTree(parser.root)).encode("UTF-8"))
tree_file.close()
