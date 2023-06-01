from anytree import Node


class ParserNode(Node):
    def __init__(self, name, parent=None, children=None, **kwargs):
        super().__init__(name, parent, children, **kwargs)
        if children:
            self.children = children
        self.name = name
        self.parent = parent

    def __repr__(self):
        return self.name


class Transition_Diagram:
    def __init__(self, name):
        self.name = name
        self.states = {'FINAL': {}}
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
        self.parser_node = ParserNode(name=name, children=[])
        self.first = None
        self.follow = None

    def add_state(self, begin_state, edge_token, end_state):
        if begin_state not in self.states:
            self.states[begin_state] = {}
        self.states[begin_state][edge_token] = end_state


def make_diagrams():
    transition_diagrams = {}
    # Creating transition diagrams
    # line 1
    program_diagram = Transition_Diagram('Program')
    program_diagram.add_state('S0', '#start_program', 'S1_0')
    program_diagram.add_state('S1_0', 'Declaration-list', 'S1')
    program_diagram.add_state('S1', '#end_program', 'FINAL')
    # program_diagram.add_state('S0', 'Declaration-list', 'FINAL')
    transition_diagrams['Program'] = program_diagram

    # line 2
    declaration_list_diagram = Transition_Diagram('Declaration-list')
    declaration_list_diagram.add_state('S0', 'Declaration', 'S1')
    declaration_list_diagram.add_state('S1', "#semantic_refresh", 'S2')
    declaration_list_diagram.add_state('S2', 'Declaration-list', 'FINAL')
    # declaration_list_diagram.add_state('S1', 'Declaration-list', 'FINAL')
    declaration_list_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['Declaration-list'] = declaration_list_diagram

    # line 3
    declaration_diagram = Transition_Diagram('Declaration')
    declaration_diagram.add_state('S0', 'Declaration-initial', 'S1')
    declaration_diagram.add_state('S1', 'Declaration-prime', 'FINAL')
    transition_diagrams['Declaration'] = declaration_diagram

    # line 4
    declaration_initial_diagram = Transition_Diagram('Declaration-initial')
    declaration_initial_diagram.add_state('S0', '#push', 'S1')
    declaration_initial_diagram.add_state('S1', 'Type-specifier', 'S2')
    declaration_initial_diagram.add_state('S2', '#push', 'S3')
    declaration_initial_diagram.add_state('S3', 'ID', 'FINAL')
    transition_diagrams['Declaration-initial'] = declaration_initial_diagram

    # line 5
    declaration_prime_diagram = Transition_Diagram('Declaration-prime')
    declaration_prime_diagram.add_state('S0', 'Fun-declaration-prime', 'FINAL')
    declaration_prime_diagram.add_state('S0', 'Var-declaration-prime', 'FINAL')
    transition_diagrams['Declaration-prime'] = declaration_prime_diagram

    # line 6
    var_declaration_prime_diagram = Transition_Diagram('Var-declaration-prime')
    var_declaration_prime_diagram.add_state('S0', '#declare', 'S1')
    var_declaration_prime_diagram.add_state('S1', ';', 'FINAL')
    var_declaration_prime_diagram.add_state('S0', '[', 'S2')
    var_declaration_prime_diagram.add_state('S2', '#push', 'S3')
    var_declaration_prime_diagram.add_state('S3', 'NUM', 'S4')
    var_declaration_prime_diagram.add_state('S4', ']', 'S5')
    var_declaration_prime_diagram.add_state('S5', '#dec_arr', 'S6')
    var_declaration_prime_diagram.add_state('S6', ';', 'FINAL')
    transition_diagrams['Var-declaration-prime'] = var_declaration_prime_diagram

    # line 7
    fun_declaration_prime_diagram = Transition_Diagram('Fun-declaration-prime')
    fun_declaration_prime_diagram.add_state('S0', '#dec_fun', 'S1')
    fun_declaration_prime_diagram.add_state('S1', '(', 'S2')
    fun_declaration_prime_diagram.add_state('S2', 'Params', 'S3')
    fun_declaration_prime_diagram.add_state('S3', ')', 'S4')
    fun_declaration_prime_diagram.add_state('S4', 'Compound-stmt', 'S5')
    fun_declaration_prime_diagram.add_state('S5', '#end_func', 'FINAL')

    # fun_declaration_prime_diagram.add_state('S0', '(', 'S1')
    # fun_declaration_prime_diagram.add_state('S2', ')', 'S3')
    # fun_declaration_prime_diagram.add_state('S1', 'Params', 'S2')
    # fun_declaration_prime_diagram.add_state('S3', 'Compound-stmt', 'FINAL')
    transition_diagrams['Fun-declaration-prime'] = fun_declaration_prime_diagram

    # line 8
    type_specifier_diagram = Transition_Diagram('Type-specifier')
    type_specifier_diagram.add_state('S0', 'int', 'FINAL')
    type_specifier_diagram.add_state('S0', 'void', 'FINAL')
    transition_diagrams['Type-specifier'] = type_specifier_diagram

    # line 9
    params_diagram = Transition_Diagram('Params')
    params_diagram.add_state('S0', '#push', 'S1')
    params_diagram.add_state('S1', 'int', 'S2')
    params_diagram.add_state('S2', '#push', 'S3')
    params_diagram.add_state('S3', 'ID', 'S4')
    params_diagram.add_state('S4', 'Param-prime', 'S5')
    params_diagram.add_state('S5', 'Param-list', 'FINAL')
    params_diagram.add_state('S0', 'void', 'FINAL')

    # params_diagram.add_state('S0', 'int', 'S1')
    # params_diagram.add_state('S1', 'ID', 'S2')
    # params_diagram.add_state('S0', 'void', 'FINAL')
    # params_diagram.add_state('S2', 'Param-prime', 'S3')
    # params_diagram.add_state('S3', 'Param-list', 'FINAL')
    transition_diagrams['Params'] = params_diagram

    # line 10
    param_list_diagram = Transition_Diagram('Param-list')
    param_list_diagram.add_state('S0', ',', 'S1')
    param_list_diagram.add_state('S1', 'Param', 'S2')
    param_list_diagram.add_state('S2', 'Param-list', 'FINAL')
    param_list_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['Param-list'] = param_list_diagram

    # line 11
    param_diagram = Transition_Diagram('Param')
    param_diagram.add_state('S0', 'Declaration-initial', 'S1')
    param_diagram.add_state('S1', 'Param-prime', 'FINAL')
    transition_diagrams['Param'] = param_diagram

    # line 12
    param_prime_diagram = Transition_Diagram('Param-prime')
    param_prime_diagram.add_state('S0', '[', 'S1')
    param_prime_diagram.add_state('S1', ']', 'S2')
    param_prime_diagram.add_state('S2', '#dec_parr', 'FINAL')
    param_prime_diagram.add_state('S0', 'EPS', 'S3')
    param_prime_diagram.add_state('S3', '#dec_pvar', 'FINAL')
    transition_diagrams['Param-prime'] = param_prime_diagram

    # line 13
    compound_stmt_diagram = Transition_Diagram('Compound-stmt')
    compound_stmt_diagram.add_state('S0', '#start_scope', 'S1')
    compound_stmt_diagram.add_state('S1', '{', 'S2')
    compound_stmt_diagram.add_state('S2', 'Declaration-list', 'S3')
    compound_stmt_diagram.add_state('S3', 'Statement-list', 'S4')
    compound_stmt_diagram.add_state('S4', '}', 'S5')
    compound_stmt_diagram.add_state('S5', '#finish_scope', 'FINAL')


    # compound_stmt_diagram.add_state('S0', '{', 'S1')
    # compound_stmt_diagram.add_state('S3', '}', 'FINAL')
    # compound_stmt_diagram.add_state('S1', 'Declaration-list', 'S2')
    # compound_stmt_diagram.add_state('S2', 'Statement-list', 'S3')
    transition_diagrams['Compound-stmt'] = compound_stmt_diagram

    # line 14
    statement_list_diagram = Transition_Diagram('Statement-list')
    statement_list_diagram.add_state('S0', 'Statement', 'S1')
    statement_list_diagram.add_state('S1', '#semantic_refresh', 'S2')
    statement_list_diagram.add_state('S2', 'Statement-list', 'FINAL')
    statement_list_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['Statement-list'] = statement_list_diagram

    # line 15
    statement_diagram = Transition_Diagram('Statement')
    statement_diagram.add_state('S0', 'Expression-stmt', 'FINAL')
    statement_diagram.add_state('S0', 'Compound-stmt', 'FINAL')
    statement_diagram.add_state('S0', 'Selection-stmt', 'FINAL')
    statement_diagram.add_state('S0', 'Iteration-stmt', 'FINAL')
    statement_diagram.add_state('S0', 'Return-stmt', 'FINAL')
    transition_diagrams['Statement'] = statement_diagram

    # line 16
    expression_stmt_diagram = Transition_Diagram('Expression-stmt')
    expression_stmt_diagram.add_state('S0', 'break', 'S1_0')
    expression_stmt_diagram.add_state('S1_0', '#scope_break', 'S1')
    expression_stmt_diagram.add_state('S1', ';', 'FINAL')
    expression_stmt_diagram.add_state('S0', ';', 'FINAL')
    expression_stmt_diagram.add_state('S0', 'Expression', 'S1_1')
    expression_stmt_diagram.add_state('S1_1', '#pop3', 'S1')
    transition_diagrams['Expression-stmt'] = expression_stmt_diagram

    # line 17
    selection_stmt_diagram = Transition_Diagram('Selection-stmt')
    selection_stmt_diagram.add_state('S0', 'if', 'S1')
    selection_stmt_diagram.add_state('S1', '(', 'S2')
    selection_stmt_diagram.add_state('S2', 'Expression', 'S3')
    selection_stmt_diagram.add_state('S3', ')', 'S4')
    selection_stmt_diagram.add_state('S4', '#save', 'S5')
    selection_stmt_diagram.add_state('S5', 'Statement', 'S6')
    selection_stmt_diagram.add_state('S6', '#ifc_action', 'S7')
    selection_stmt_diagram.add_state('S7', 'else', 'S8')
    selection_stmt_diagram.add_state('S8', 'Statement', 'S9')
    selection_stmt_diagram.add_state('S9', '#fill_jp', 'FINAL')
    # selection_stmt_diagram.add_state('S0', 'if', 'S1')
    # selection_stmt_diagram.add_state('S1', '(', 'S2')
    # selection_stmt_diagram.add_state('S3', ')', 'S4_0')
    # selection_stmt_diagram.add_state('S4_0', '#save', 'S4')
    # selection_stmt_diagram.add_state('S5', 'else', 'S6')
    # selection_stmt_diagram.add_state('S2', 'Expression', 'S3')
    # selection_stmt_diagram.add_state('S4', 'Statement', 'S5')
    # selection_stmt_diagram.add_state('S6', 'Statement', 'FINAL')
    transition_diagrams['Selection-stmt'] = selection_stmt_diagram

    # line 18
    iteration_stmt_diagram = Transition_Diagram('Iteration-stmt')
    iteration_stmt_diagram.add_state('S0', '#loop', 'S1_0')
    iteration_stmt_diagram.add_state('S1_0', 'repeat', 'S1')
    iteration_stmt_diagram.add_state('S2', 'until', 'S3')
    iteration_stmt_diagram.add_state('S3', '(', 'S4')
    iteration_stmt_diagram.add_state('S5', ')', 'S10')
    iteration_stmt_diagram.add_state('S10', '#until', 'FINAL')
    iteration_stmt_diagram.add_state('S1', 'Statement', 'S2')
    iteration_stmt_diagram.add_state('S4', 'Expression', 'S5')
    transition_diagrams['Iteration-stmt'] = iteration_stmt_diagram

    # line 19
    return_stmt_diagram = Transition_Diagram('Return-stmt')
    return_stmt_diagram.add_state('S0', 'return', 'S1')
    return_stmt_diagram.add_state('S1', 'Return-stmt-prime', 'S2')
    return_stmt_diagram.add_state('S2', '#fun_return', 'FINAL')
    transition_diagrams['Return-stmt'] = return_stmt_diagram

    # line 20
    return_stmt_prime_diagram = Transition_Diagram('Return-stmt-prime')
    return_stmt_prime_diagram.add_state('S2', ';', 'FINAL')
    return_stmt_prime_diagram.add_state('S0', ';', 'FINAL')
    return_stmt_prime_diagram.add_state('S0', 'Expression', 'S1')
    return_stmt_prime_diagram.add_state('S1', '#function_return', 'S2')
    transition_diagrams['Return-stmt-prime'] = return_stmt_prime_diagram

    # line 21
    expression_diagram = Transition_Diagram('Expression')
    expression_diagram.add_state('S0', '#pid', 'S1_0')
    expression_diagram.add_state('S1_0', 'ID', 'S1')
    expression_diagram.add_state('S1', 'B', 'FINAL')
    expression_diagram.add_state('S0', 'Simple-expression-zegond', 'FINAL')
    transition_diagrams['Expression'] = expression_diagram

    # line 22
    b_diagram = Transition_Diagram('B')
    b_diagram.add_state('S0', '=', 'S1')
    b_diagram.add_state('S1', 'Expression', 'S2')
    b_diagram.add_state('S2', '#assign', 'FINAL')
    b_diagram.add_state('S0', '[', 'S3')
    b_diagram.add_state('S3', 'Expression', 'S4')
    b_diagram.add_state('S4', ']', 'S5')
    b_diagram.add_state('S5', '#parr', 'S6')
    b_diagram.add_state('S6', 'H', 'FINAL')
    b_diagram.add_state('S0', 'Simple-expression-prime', 'FINAL')
    # b_diagram.add_state('S0', '[', 'S1')
    # b_diagram.add_state('S1', 'Expression', 'S2')
    # b_diagram.add_state('S2', ']', 'S3')
    # b_diagram.add_state('S0', '=', 'S4')
    # b_diagram.add_state('S3', 'H', 'FINAL')
    # b_diagram.add_state('S4', 'Expression', 'FINAL')
    # b_diagram.add_state('S0', 'Simple-expression-prime', 'FINAL')
    transition_diagrams['B'] = b_diagram

    # line 23
    h_diagram = Transition_Diagram('H')
    h_diagram.add_state('S0', '=', 'S1')
    h_diagram.add_state('S1', 'Expression', 'S2')
    h_diagram.add_state('S2', '#assign', 'FINAL')
    h_diagram.add_state('S0', 'g', 'S3')
    h_diagram.add_state('S3', 'd', 'S4')
    h_diagram.add_state('S4', 'c', 'FINAL')
    # h_diagram.add_state('S0', '=', 'S3')
    # h_diagram.add_state('S0', 'G', 'S1')
    # h_diagram.add_state('S1', 'D', 'S2')
    # h_diagram.add_state('S2', 'C', 'FINAL')
    # h_diagram.add_state('S3', 'Expression', 'FINAL')
    transition_diagrams['H'] = h_diagram

    # line 24
    simple_expression_zegond_diagram = Transition_Diagram('Simple-expression-zegond')
    simple_expression_zegond_diagram.add_state('S0', 'Additive-expression-zegond', 'S1')
    simple_expression_zegond_diagram.add_state('S1', 'C', 'FINAL')
    transition_diagrams['Simple-expression-zegond'] = simple_expression_zegond_diagram

    # line 25
    simple_expression_prime_diagram = Transition_Diagram('Simple-expression-prime')
    simple_expression_prime_diagram.add_state('S0', 'Additive-expression-prime', 'S1')
    simple_expression_prime_diagram.add_state('S1', 'C', 'FINAL')
    transition_diagrams['Simple-expression-prime'] = simple_expression_prime_diagram

    # line 26
    c_diagram = Transition_Diagram('C')
    c_diagram.add_state('S0', 'Relop', 'S1')
    c_diagram.add_state('S1', 'Additive-expression', 'S2')
    c_diagram.add_state('S2', '#opera', 'FINAL')
    c_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['C'] = c_diagram

    # line 27
    relop_diagram = Transition_Diagram('Relop')
    relop_diagram.add_state('S0', '#push', 'S1')
    relop_diagram.add_state('S1', '<', 'FINAL')
    relop_diagram.add_state('S1', '==', 'FINAL')
    transition_diagrams['Relop'] = relop_diagram

    # line 28
    additive_expression_diagram = Transition_Diagram('Additive-expression')
    additive_expression_diagram.add_state('S0', 'Term', 'S1')
    additive_expression_diagram.add_state('S1', 'D', 'FINAL')
    transition_diagrams['Additive-expression'] = additive_expression_diagram

    # line 29
    additive_expression_prime_diagram = Transition_Diagram('Additive-expression-prime')
    additive_expression_prime_diagram.add_state('S0', 'Term-prime', 'S1')
    additive_expression_prime_diagram.add_state('S1', 'D', 'FINAL')
    transition_diagrams['Additive-expression-prime'] = additive_expression_prime_diagram

    # line 30
    additive_expression_zegond_diagram = Transition_Diagram('Additive-expression-zegond')
    additive_expression_zegond_diagram.add_state('S0', 'Term-zegond', 'S1')
    additive_expression_zegond_diagram.add_state('S1', 'D', 'FINAL')
    transition_diagrams['Additive-expression-zegond'] = additive_expression_zegond_diagram

    # line 31
    d_diagram = Transition_Diagram('D')
    d_diagram.add_state('S0', 'Addop', 'S1')
    d_diagram.add_state('S1', 'Term', 'S2_0')
    d_diagram.add_state('S2_0', '#opera', 'S2')
    d_diagram.add_state('S2', 'D', 'FINAL')
    d_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['D'] = d_diagram

    # line 32
    addop_diagram = Transition_Diagram('Addop')
    addop_diagram.add_state('S0', '#push', 'S1')
    addop_diagram.add_state('S1', '+', 'FINAL')
    addop_diagram.add_state('S1', '-', 'FINAL')
    transition_diagrams['Addop'] = addop_diagram

    # line 33
    term_diagram = Transition_Diagram('Term')
    term_diagram.add_state('S0', 'Factor', 'S1')
    term_diagram.add_state('S1', 'G', 'FINAL')
    transition_diagrams['Term'] = term_diagram

    # line 34
    term_diagram_prime = Transition_Diagram('Term-prime')
    term_diagram_prime.add_state('S0', 'Factor-prime', 'S1')
    term_diagram_prime.add_state('S1', 'G', 'FINAL')
    transition_diagrams['Term-prime'] = term_diagram_prime

    # line 35
    term_diagram_zegond = Transition_Diagram('Term-zegond')
    term_diagram_zegond.add_state('S0', 'Factor-zegond', 'S1')
    term_diagram_zegond.add_state('S1', 'G', 'FINAL')
    transition_diagrams['Term-zegond'] = term_diagram_zegond

    # line 36
    g_diagram = Transition_Diagram('G')
    g_diagram.add_state('S0', '#push', 'S1_0')
    g_diagram.add_state('S1_0', '*', 'S1')
    g_diagram.add_state('S1', 'Factor', 'S2_0')
    g_diagram.add_state('S2_0', '#opera', 'S2')
    g_diagram.add_state('S2', 'G', 'FINAL')
    g_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['G'] = g_diagram

    # line 37
    factor_diagram = Transition_Diagram('Factor')
    factor_diagram.add_state('S0', '(', 'S1')
    factor_diagram.add_state('S1', 'Expression', 'S2')
    factor_diagram.add_state('S2', ')', 'FINAL')
    factor_diagram.add_state('S0', '#pid', 'S3_0')
    factor_diagram.add_state('S3_0', 'ID', 'S3')
    factor_diagram.add_state('S3', 'Var-call-prime', 'FINAL')
    factor_diagram.add_state('S0', '#pnum', 'S6')
    factor_diagram.add_state('S6', 'NUM', 'FINAL')
    transition_diagrams['Factor'] = factor_diagram

    # line 38
    var_call_prime_diagram = Transition_Diagram('Var-call-prime')
    var_call_prime_diagram.add_state('S0', '(', 'S1')
    var_call_prime_diagram.add_state('S1', 'Args', 'S2')
    var_call_prime_diagram.add_state('S2', ')', 'S3')
    var_call_prime_diagram.add_state('S3', '#call', 'FINAL')
    var_call_prime_diagram.add_state('S0', 'Var-prime', 'FINAL')
    transition_diagrams['Var-call-prime'] = var_call_prime_diagram

    # line 39
    var_prime_diagram = Transition_Diagram('Var-prime')
    var_prime_diagram.add_state('S0', '[', 'S1')
    var_prime_diagram.add_state('S1', 'Expression', 'S2')
    var_prime_diagram.add_state('S2', ']', 'S3')
    var_prime_diagram.add_state('S3', '#parr', 'FINAL')
    var_prime_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['Var-prime'] = var_prime_diagram

    # line 40
    factor_prime_diagram = Transition_Diagram('Factor-prime')
    factor_prime_diagram.add_state('S0', '(', 'S1')
    factor_prime_diagram.add_state('S1', 'Args', 'S2')
    factor_prime_diagram.add_state('S2', ')', 'S3')
    factor_prime_diagram.add_state('S3', '#call', 'FINAL')
    factor_prime_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['Factor-prime'] = factor_prime_diagram

    # line 41
    factor_zegond_diagram = Transition_Diagram('Factor-zegond')
    factor_zegond_diagram.add_state('S0', '(', 'S1')
    factor_zegond_diagram.add_state('S1', 'Expression', 'S2')
    factor_zegond_diagram.add_state('S2', ')', 'FINAL')
    factor_zegond_diagram.add_state('S0', '#pnum', 'S4')
    factor_zegond_diagram.add_state('S4', 'NUM', 'FINAL')
    transition_diagrams['Factor-zegond'] = factor_zegond_diagram

    # line 42
    args_diagram = Transition_Diagram('Args')
    args_diagram.add_state('S0', 'Arg-list', 'FINAL')
    args_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['Args'] = args_diagram

    # line 43
    args_list_diagram = Transition_Diagram('Arg-list')
    args_list_diagram.add_state('S0', 'Expression', 'S1')
    args_list_diagram.add_state('S1', '#add_args', 'S2')
    args_list_diagram.add_state('S2', 'Arg-list-prime', 'FINAL')
    transition_diagrams['Arg-list'] = args_list_diagram

    # line 44
    arg_list_prime_diagram = Transition_Diagram('Arg-list-prime')
    arg_list_prime_diagram.add_state('S0', ',', 'S1')
    arg_list_prime_diagram.add_state('S1', 'Expression', 'S2_0')
    arg_list_prime_diagram.add_state('S2_0', '#add_args', 'S2')
    arg_list_prime_diagram.add_state('S2', 'Arg-list-prime', 'FINAL')
    arg_list_prime_diagram.add_state('S0', 'EPS', 'FINAL')
    transition_diagrams['Arg-list-prime'] = arg_list_prime_diagram

    for name, diagram in transition_diagrams.items():
        diagram.first = Symbols[name].first
        diagram.follow = Symbols[name].follow

    return transition_diagrams


Symbols = {}  # name : object


class Symbol:
    def __init__(self, name: str, first=None, follow=None):
        self.name = name
        self.first = first

        self.follow = follow
        Symbols[name] = self


# initializing the states (Symbols) and their first and follow sets
Symbol('Program', {'int', 'void', 'EPS'}, {'$'})
Symbol('Declaration-list', {'int', 'void', 'EPS'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Declaration', {'int', 'void'},
       {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Declaration-initial', {'int', 'void'},
       {';', '[', '(', ')', ','})
Symbol('Declaration-prime', {';', '[', '('},
       {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Var-declaration-prime', {';', '['},
       {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Fun-declaration-prime', {'('},
       {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'})
Symbol('Type-specifier', {'int', 'void'}, {'ID'})
Symbol('Params', {'int', 'void'}, {')'})
Symbol('Param-list', {',', 'EPS'}, {')'})
Symbol('Param', {'int', 'void'}, {')', ','})
Symbol('Param-prime', {'[', 'EPS'}, {')', ','})
Symbol('Compound-stmt', {'{'},
       {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return', '$'})
Symbol('Statement-list', {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'EPS'}, {'}'})
Symbol('Statement', {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return'})
Symbol('Expression-stmt', {'ID', ';', 'NUM', '(', 'break'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return'})
Symbol('Selection-stmt', {'if'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return'})
Symbol('Iteration-stmt', {'repeat'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return'})
Symbol('Return-stmt', {'return'},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return'})
Symbol('Return-stmt-prime', {'ID', ';', 'NUM', '('},
       {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'repeat', 'until', 'return'})
Symbol('Expression', {'ID', 'NUM', '('}, {';', ']', ')', ','})
Symbol('B', {'[', '(', '=', '<', '==', '+', '-', '*', 'EPS'}, {';', ']', ')', ','})
Symbol('H', {'=', '<', '==', '+', '-', '*', 'EPS'}, {';', ']', ')', ','})
Symbol('Simple-expression-zegond', {'NUM', '('}, {';', ']', ')', ','})
Symbol('Simple-expression-prime', {'(', '<', '==', '+', '-', '*', 'EPS'}, {';', ']', ')', ','})
Symbol('C', {'<', '==', 'EPS'}, {';', ']', ')', ','})
Symbol('Relop', {'<', '=='}, {'ID', 'NUM', '('})
Symbol('Additive-expression', {'ID', 'NUM', '('}, {';', ']', ')', ','})
Symbol('Additive-expression-prime', {'(', '+', '-', '*', 'EPS'}, {';', ']', ')', ',', '<', '=='})
Symbol('Additive-expression-zegond', {'NUM', '('}, {';', ']', ')', ',', '<', '=='})
Symbol('D', {'+', '-', 'EPS'}, {';', ']', ')', ',', '<', '=='})
Symbol('Addop', {'+', '-'}, {'ID', 'NUM', '('})
Symbol('Term', {'ID', 'NUM', '('}, {';', ',', ']', ')', '<', '==', '+', '-'})
Symbol('Term-prime', {'(', '*', 'EPS'}, {';', ',', ']', ')', '<', '==', '+', '-'})
Symbol('Term-zegond', {'NUM', '('}, {';', ',', ']', ')', '<', '==', '+', '-'})
Symbol('G', {'*', 'EPS'}, {';', ',', ']', ')', '<', '==', '+', '-'})
Symbol('Factor', {'ID', 'NUM', '('}, {';', ',', ']', ')', '<', '==', '+', '-', '*'})
Symbol('Var-call-prime', {'[', '(', 'EPS'}, {';', ',', ']', ')', '<', '==', '+', '-', '*'})
Symbol('Var-prime', {'[', 'EPS'}, {';', ',', ']', ')', '<', '==', '+', '-', '*'})
Symbol('Factor-prime', {'(', 'EPS'}, {';', ',', ']', ')', '<', '==', '+', '-', '*'})
Symbol('Factor-zegond', {'(', 'NUM'}, {';', ',', ']', ')', '<', '==', '+', '-', '*'})
Symbol('Args', {'ID', 'NUM', '(', 'EPS'}, {')'})
Symbol('Arg-list', {'ID', 'NUM', '('}, {')'})
Symbol('Arg-list-prime', {',', 'EPS'}, {')'})

terminals = ['ID', 'NUM', ';', ':', ',', '+', '-', '*', '=', '<', '==', '(', ')', '[', ']', '{', '}', 'int', 'void',
             'break', 'else', 'repeat', 'return', 'until', 'if']


def is_terminal(token):
    if token in terminals:
        return True
    else:
        return False
