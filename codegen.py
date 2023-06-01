MACHINE_PARAMETER = 45000
MACHINE_FUN_INDEX = 41000
MACHINE_CONTAINER = 400
MACHINE_WORD_SIZE = 4

COUNTER_REGISTER0 = 40000

class Register:
    rsp_temp = MACHINE_PARAMETER
    rsp_proc = MACHINE_CONTAINER

    def __init__(self):
        self.return_address = self.get_parameter()
        self.return_value = self.get_parameter()
        self.rbp_container = self.get_parameter()

    def get_temporary(self):
        out, self.rsp_temp = self.rsp_temp, self.rsp_temp + MACHINE_WORD_SIZE
        return out

    def get_parameter(self):
        out, self.rsp_proc = self.rsp_proc, self.rsp_proc + MACHINE_WORD_SIZE
        return out

class Activation:
    class Scope:
        class IDMem:
            def __init__(self, lexeme=None, el_type=None, no_args=None, id_type=None, scope=None, address=None):
                self.extra = {'params': [], 'line': 0}
                self.lexeme = lexeme
                self.scope = scope
                self.el_type = el_type
                self.no_args = no_args
                self.id_type = id_type
                self.address = address

            def __str__(self):
                return F"({self.lexeme},{self.address})"

        def __init__(self, parent=None):
            self.parent = parent
            self.variables = {}
            self.fun_params = {}

        def add_identifier(self, lexeme):
            self.variables[lexeme] = self.IDMem(lexeme=lexeme, scope=self)
            return self.variables[lexeme]

        def get_identifier(self, lexeme):
            return self.variables.get(lexeme) or \
                   (self.parent.get_identifier(lexeme) if self.parent else None)

    def __init__(self, register, memory=None, parent=None):
        self.scope = self.Scope()
        self.pro_memory = memory
        self.register = register
        self.pro_parent = parent

        if parent:
            register.get_parameter(), register.get_parameter() \
                , register.get_parameter(), register.get_parameter()

        self.scope_stack = []

    def add_variable(self, lexeme, is_param=False):

        new = self.scope.add_identifier(lexeme)

        if is_param:
            self.pro_memory.no_args = self.pro_memory.no_args + is_param
            self.pro_memory.extra['params'].append(new)

        return new

    def get_variable(self, lexeme):
        memory = self.scope.get_identifier(lexeme)
        if memory:
            return 0, memory

        if self.pro_parent:
            num, memory = self.pro_parent.get_variable(lexeme)
            return num + 1, memory

        return 0, None

    def deep_scope(self):
        self.scope_stack.append(self.register.rsp_proc)
        self.scope = self.Scope(parent=self.scope)

    def high_scope(self):
        self.scope = self.scope.parent
        self.register.rsp_proc = self.scope_stack.pop()

class StackManager:

    def __init__(self):
        self.reg, self.run_time_stack = Register(), []
        self.activation = Activation(self.reg)
        self.rbp_proc = self.reg.rsp_proc

    def deep_activation(self, memory=None):
        self.rbp_proc, self.activation = \
            self.reg.rsp_proc, Activation(self.reg, memory, self.activation)

    def high_activation(self): self.activation = self.activation.pro_parent

    def get_temporary(self): return self.reg.get_temporary()

    def get_parameter(self): return self.reg.get_parameter() - self.rbp_proc

class CodeGen:
    def __init__(self, parser=None):
        self.semantic_errors = []
        self.semantic_stack = []
        self.program_block = []
        self.function_arg = []
        self.loops_stack = []
        self.func_stack = []
        self.fun_memory = None
        self.fun_refresh = []
        self.parser = parser
        self.functions_index = {}
        self.error_detected = False
        self.stack_manager = StackManager()

    def sspop(self):
        print(f"ss = {self.semantic_stack}")
        return self.semantic_stack.pop()

    def start_program(self):
        rbp = self.stack_manager.reg.rbp_container

        self.program_block.append(F'(ASSIGN, #{rbp}, {MACHINE_CONTAINER})')
        self.program_block.append(F'(ASSIGN, #{rbp}, {COUNTER_REGISTER0})')

    def pid(self, lexeme=None):

        level, row = self.stack_manager.activation.get_variable(lexeme or self.parser.current_token)

        if row is None:

            if self.parser.current_token == 'output':
                self.semantic_stack.extend(('PRINT', 'output', 'void'))
            else:
                self.semantic_errors.append(
                    F'#{self.parser.scanner.line} : Semantic Error! \'{self.parser.current_token}\' is not defined.')

                self.error_detected = True
                self.semantic_stack.extend((None, None, None))

        elif row.el_type == 'arr':
            address = self.indirect_address(level, row.address)[1:]
            if self.fun_refresh:
                self.fun_refresh[-1].append((address, level, row.address))
            self.semantic_stack.extend((address, row.el_type, row.id_type))

        elif row.el_type == 'fun':
            self.fun_memory = row
            self.semantic_stack.extend((None, row.lexeme, row.id_type))

        elif row.el_type != 'fun':

            address = self.indirect_address(level, row.address)
            if self.fun_refresh:
                self.fun_refresh[-1].append((address, level, row.address))
            self.semantic_stack.extend((address, row.el_type, row.id_type))

    def indirect_address(self, level, address, temp_address=None):

        temp = temp_address or self.stack_manager.get_temporary()
        self.program_block.append(F'(ASSIGN, {MACHINE_CONTAINER}, {temp})')
        for _ in range(level):
            self.program_block.append(F'(ADD, {temp}, #{3 * MACHINE_WORD_SIZE}, {temp})')
            self.program_block.append(F'(ASSIGN, @{temp}, {temp})')

        self.program_block.append(F'(ADD, {temp}, #{address}, {temp})')
        return F'@{temp}'

    def opera(self):
        print(self.semantic_stack)
        print("^^^^^^^^")
        op2_id_type = self.sspop()
        op2_el_type = self.sspop()
        op2_addr = self.sspop()
        op = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '<': 'LT', '==': 'EQ'}[self.sspop()]
        op1_id_type = self.sspop()
        op1_el_type = self.sspop()
        op1_addr = self.sspop()

        if self.error_detected:
            self.semantic_stack.extend((None, None, None))

        elif op1_el_type == 'arr' or op2_el_type == 'arr':
            self.semantic_errors.append(
                F'#{self.parser.scanner.line} : Semantic Error! Type mismatch in operands, Got array instead of int.')

            self.error_detected = True
            self.semantic_stack.extend((None, None, None))

        elif op1_id_type != op2_id_type:
            self.semantic_errors.append(
                F'#{self.parser.scanner.line} : Semantic Error! Type mismatch in operands, Got different types.')

            self.error_detected = True
            self.semantic_stack.extend((None, None, None))

        else:
            address = self.stack_manager.get_temporary()
            self.program_block.append(F"({op}, {op1_addr}, {op2_addr}, {address})")
            self.semantic_stack.extend((address, op1_el_type, op1_id_type))

    def push(self):
        self.semantic_stack.append(self.parser.current_token)
        print(f'>>>>>>>>>>>> {self.semantic_stack}')

    def pop3(self):
        self.sspop(), self.sspop(), self.sspop()
        self.error_detected = False

    def semantic_refresh(self):
        self.error_detected = False

    def pnum(self):
        self.semantic_stack.extend((F'#{self.parser.current_token}', 'var', 'int'))

    def assign(self):
        rhs_id_type = self.sspop()
        rhs_el_type = self.sspop()
        rhs_addr = self.sspop()
        lhs_id_type = self.sspop()
        lhs_el_type = self.sspop()
        lhs_addr = self.sspop()

        transform = {'pvar': 'int', 'var': 'int', 'arr': 'array', 'parr': 'array'}

        if self.error_detected:
            self.semantic_stack.extend((None, None, None))

        elif not (transform.get(rhs_el_type) and transform.get(lhs_el_type)) \
                or transform.get(rhs_el_type) != transform.get(lhs_el_type):
            self.semantic_errors.append(
                F'#{self.parser.scanner.line} : Semantic Error! Type mismatch in operands, Got array instead of int.')

            self.error_detected = True
            self.semantic_stack.extend((None, None, None))

        elif 'void' in {lhs_id_type, rhs_id_type}:
            self.semantic_errors.append(
                F'#{self.parser.scanner.line} : Semantic Error! Type mismatch in operands, Got void type.')

            self.error_detected = True
            self.semantic_stack.extend((None, None, None))

        else:
            self.program_block.append(F"(ASSIGN, {rhs_addr}, {lhs_addr})")
            self.semantic_stack.extend((lhs_addr, 'var', lhs_id_type))

    def declare(self, el_type='var', is_param=False):
        lexeme = self.sspop()
        id_type = self.sspop()

        if id_type == 'void':
            self.semantic_errors.append(
                F'#{self.parser.scanner.line} : Semantic Error! Illegal type of void for \'{lexeme}\'.')
            self.error_detected = True

        else:
            mem = self.stack_manager.activation.add_variable(lexeme, is_param=is_param)
            mem.id_type = id_type
            mem.el_type = el_type
            mem.no_args = 0
            mem.address = self.stack_manager.get_parameter()

            if not is_param:
                self.pid(lexeme), self.sspop(), self.sspop()
                lhs_addr = self.sspop()
                self.program_block.append(F"(ASSIGN, #0, {lhs_addr})")

            self.program_block.append(F"(ADD, #4, {COUNTER_REGISTER0}, {COUNTER_REGISTER0})")

    def dec_parr(self):
        self.declare('parr', True)

    def dec_pvar(self):
        self.declare('pvar', True)

    def start_scope(self):
        self.stack_manager.activation.deep_scope()

    def finish_scope(self):
        self.stack_manager.activation.high_scope()

    def dec_fun(self):
        lexeme = self.sspop()
        id_type = self.sspop()

        mem = self.stack_manager.activation.add_variable(lexeme)
        mem.id_type = id_type
        mem.el_type = 'fun'
        mem.no_args = 0
        mem.address = self.stack_manager.get_parameter()
        mem.extra['line'] = len(self.program_block) + 2

        self.func_stack.append([])
        self.fun_refresh.append([])
        self.functions_index[lexeme] = len(self.functions_index)
        pro_sbp = self.stack_manager.reg.rbp_container

        func_mom = MACHINE_FUN_INDEX + MACHINE_WORD_SIZE * self.functions_index[lexeme]
        self.program_block.append(F'(ASSIGN, #{pro_sbp}, {func_mom})')

        self.save()
        self.program_block.append(
            F"(ADD, #{4 * MACHINE_WORD_SIZE}, {COUNTER_REGISTER0}, {COUNTER_REGISTER0})")
        self.stack_manager.deep_activation(mem)

    def end_func(self):

        for line in self.func_stack.pop():
            self.program_block[line] = F'(JP, {len(self.program_block)})'

        self.back()
        self.stack_manager.high_activation()
        self.fill_jp()
        self.fun_refresh.pop()

    def back(self):
        temp = self.stack_manager.get_temporary()
        self.program_block.append(F'(ASSIGN, @{MACHINE_CONTAINER}, {temp})')
        self.program_block.append(F'(JP, @{temp})')

    def dec_arr(self):
        s_num = self.sspop()
        lexeme = self.sspop()
        id_type = self.sspop()

        s_num = int(s_num)

        if id_type == 'void':
            self.semantic_errors.append(F'#{self.parser.scanner.line} : Illegal type of void for \'{lexeme}\'.')
            self.error_detected = True

        else:
            mem = self.stack_manager.activation.add_variable(lexeme)
            mem.id_type = id_type
            mem.el_type = 'arr'
            mem.no_args = s_num
            all_address = [self.stack_manager.get_parameter() for _ in range(s_num)]
            mem.address = all_address[0]

            orig, temp = self.stack_manager.get_temporary(), self.stack_manager.get_temporary()
            self.program_block.append(F"(ASSIGN, {MACHINE_CONTAINER}, {orig})")

            for addr in all_address:
                self.program_block.append(F"(ADD, {orig}, #{addr}, {temp})")
                self.program_block.append(F"(ASSIGN, #0, @{temp})")

            self.program_block.append(
                F"(ADD, #{len(all_address) * MACHINE_WORD_SIZE}, {COUNTER_REGISTER0}, {COUNTER_REGISTER0})")

    def parr(self):
        idn_id_type = self.sspop()
        _ = self.sspop()
        num_ind = self.sspop()
        arr_id_type = self.sspop()
        _ = self.sspop()
        address = self.sspop()

        if idn_id_type != 'int':
            self.semantic_errors.append(F'#{self.parser.scanner.line} : Illegal type of index for the array.')

            self.error_detected = True
            self.semantic_stack.extend((None, None, None))

        else:
            temp = self.stack_manager.get_temporary()
            self.program_block.append(F"(MULT, {num_ind}, #{MACHINE_WORD_SIZE}, {temp})")
            self.program_block.append(F"(ADD, {address}, {temp}, {temp})")
            self.semantic_stack.extend((F'@{temp}', 'var', arr_id_type))

    def label(self):
        self.semantic_stack.append(len(self.program_block))

    def save(self):
        self.label()
        self.program_block.append('saved!')

    def fill_jpf(self):
        line = self.sspop()
        _, _, check = self.sspop(), self.sspop(), self.sspop()

        self.program_block[line] = F'(JPF, {check}, {len(self.program_block)})'

    def fill_jp(self):
        ind = self.sspop()
        self.program_block[ind] = F'(JP, {len(self.program_block)})'

    def ifc_action(self):
        ind = self.sspop()
        _ = self.sspop()
        _ = self.sspop()
        self.program_block[ind] = F'(JPF, {self.sspop()}, {len(self.program_block) + 1})'
        self.save()

    def function_return(self):
        self.sspop(), self.sspop()
        addr = self.sspop()

        if self.error_detected:
            return

        temp = self.stack_manager.get_temporary()
        self.program_block.append(F'(ADD, {MACHINE_CONTAINER}, #{MACHINE_WORD_SIZE}, {temp})')
        self.program_block.append(F'(ASSIGN, {addr}, @{temp})')

    def scope_break(self):
        if len(self.loops_stack):
            self.loops_stack[-1].append(len(self.program_block))
            self.program_block.append('break')
        else:
            self.semantic_errors.append(
                F"#{self.parser.scanner.line} : Semantic Error! No 'repeat ... until' found for 'break'.")

            self.error_detected = True

    def until(self):
        _, _, address = self.sspop(), self.sspop(), self.sspop(),
        line = self.sspop()

        self.program_block.append(F'(JPF, {address}, {line})')

        for line in self.loops_stack.pop():
            self.program_block[line] = F'(JP, {len(self.program_block)})'

    def loop(self):
        self.label()
        self.loops_stack.append([])

    def call(self):
        id_type, lexeme, address = \
            self.sspop(), self.sspop(), self.sspop()

        if lexeme == 'output' and address == 'PRINT':

            if len(self.function_arg) > 1:
                self.semantic_errors.append(
                    F'#{self.parser.scanner.line} : Semantic Error! Mismatch in numbers of arguments of output.')
            else:
                self.program_block.append(F'(PRINT, {self.function_arg[0][0]})')

            self.semantic_stack.extend((None, None, None))
            self.error_detected = True

            self.function_arg.clear()
            return

        params = list(map(lambda x: (x.address, x.el_type, x.id_type), self.fun_memory.extra['params']))

        if len(params) != len(self.function_arg):
            self.semantic_errors.append(
                F'#{self.parser.scanner.line} : Semantic Error! Mismatch in numbers of arguments of \'{lexeme}\'.')

            self.semantic_stack.extend((None, None, None))
            self.error_detected = True

            self.function_arg.clear()
            return

        transform = {'pvar': 'int', 'var': 'int', 'arr': 'array', 'parr': 'array'}
        diff = [
            (i, transform[x[1]], transform[y[1]]) for i, (x, y) in enumerate(zip(params, self.function_arg), start=1)
        ]
        diff = list(filter(lambda x: x[1] != x[2], diff))

        if diff:
            self.semantic_errors.append(
                F'#{self.parser.scanner.line} : Semantic Error! Mismatch in type of argument {diff[0][0]} of \'{lexeme}\'. '
                F'Expected \'{diff[0][1]}\' but got \'{diff[0][2]}\' instead.')

            self.semantic_stack.extend((None, None, None))
            self.error_detected = True

        else:

            self.semantic_stack.extend((self.call_function(lexeme), 'var', self.fun_memory.id_type))
            for at_address, level, row_address in self.fun_refresh[-1]:
                self.indirect_address(level, row_address, at_address[1:])

        self.function_arg.clear()

    def call_function(self, lexeme):

        jump, address = self.fun_memory.extra["line"], self.stack_manager.get_temporary()
        x = len(self.program_block) + 2 * len(self.function_arg) + 11

        self.program_block.append(F'(ASSIGN, {COUNTER_REGISTER0}, {address})')

        temp = self.stack_manager.get_temporary()

        self.program_block.append(F'(ADD, {address}, #{0 * MACHINE_WORD_SIZE}, {temp})')
        self.program_block.append(F'(ASSIGN, #{x}, @{temp})')

        self.program_block.append(F'(ADD, {address}, #{1 * MACHINE_WORD_SIZE}, {temp})')
        self.program_block.append(F'(ASSIGN, #0, @{temp})')

        self.program_block.append(F'(ADD, {address}, #{2 * MACHINE_WORD_SIZE}, {temp})')
        self.program_block.append(F'(ASSIGN, {MACHINE_CONTAINER}, @{temp})')

        func_mom = MACHINE_FUN_INDEX + MACHINE_WORD_SIZE * self.functions_index[lexeme]

        self.program_block.append(F'(ADD, {address}, #{3 * MACHINE_WORD_SIZE}, {temp})')
        self.program_block.append(F'(ASSIGN, {func_mom}, @{temp})')

        for addr, el_type, id_type in self.function_arg:
            self.program_block.append(F'(ADD, {temp}, #{MACHINE_WORD_SIZE}, {temp})')
            self.program_block.append(F'(ASSIGN, {addr}, @{temp})')

        self.program_block.append(F'(ASSIGN, {address}, {MACHINE_CONTAINER})')

        self.program_block.append(F'(JP, {jump})')

        result = self.stack_manager.get_temporary()
        self.program_block.append(F'(ADD, {MACHINE_CONTAINER}, #{MACHINE_WORD_SIZE * 1}, {result})')
        self.program_block.append(F'(ASSIGN, @{result}, {result})')

        temp = self.stack_manager.get_temporary()
        self.program_block.append(F'(ADD, {MACHINE_CONTAINER}, #{2 * MACHINE_WORD_SIZE}, {temp})')
        self.program_block.append(F'(ASSIGN, @{temp}, {MACHINE_CONTAINER})')
        return result

    def add_args(self):
        x3, x2, x1 = \
            self.sspop(), self.sspop(), self.sspop()

        self.function_arg.append((x1, x2, x3))

    def fun_return(self):

        if len(self.func_stack):
            self.func_stack[-1].append(len(self.program_block))
            self.program_block.append('return')
        else:
            self.semantic_errors.append(
                F"#{self.parser.scanner.line}: Semantic Error! No 'function' found for 'return'.")

            self.error_detected = True

    def end_program(self):

        level, self.fun_memory = self.stack_manager.activation.get_variable('main')
        self.call_function('main')

        with open('output.txt', 'w') as f:
            if self.semantic_errors:
                f.write('The code has not been generated.')
            else:
                f.writelines([F'{i}\t{x}\n' for i, x in enumerate(self.program_block)])

        with open('semantic_errors.txt', 'w') as f:
            if self.semantic_errors:
                f.writelines([F'{x}\n' for x in self.semantic_errors])
            else:
                f.write('The input program is semantically correct.')