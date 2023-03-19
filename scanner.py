import dfa as dfa_lib
from token_type import TokenType
from modules.keyword import Keyword


class Scanner:
    def __init__(self, file_name):
        self.dfa: dfa_lib.DFA
        self.__create_the_dfa()
        self.current_token: (TokenType, str) = TokenType.ERROR, "not implemented"
        self.state_dict = {18: 'Unmatched comment', 19: 'SYMBOL', 14: 'SYMBOL', 16: 'Invalid number', 2: 'NUM',
                           6: 'COMMENT', 15: 'Unclosed comment', 8: 'ID/KW', 10: 'SYMBOL', -1: 'Invalid input',
                           11: 'SYMBOL', 12: 'WHITESPACE'}  # {STATE_ID: TOKEN_TYPE} and for keywords also we use ID in this dictionary
        self.keywords = ["break", "else", "if", "int","repeat", "return", "until", "void"]
        self.special_states = {11, 8, 2, 19}
        self.buffer_size = 1024  # size of each buffer in bytes
        self.buffer = []
        self.file = open(file_name, 'r')
        self.EOF = False
        self.EOL = False

    def get_next_token(self) -> (TokenType, str):
        """
        This method is called by other modules and reads from the file character by character
            till it detects a token and returns it as a tuple in the specified format.
        :return: (token_type: TokenType, token_lexeme: str)
        """
        self.dfa.reset()
        while True:
            if not self.buffer:
                buff = self.file.read(self.buffer_size)  # read buffer_size bytes from file
                if not buff:  # stop if end of file is reached
                    self.buffer += '\0'
                else:
                    chars = [char for char in buff]
                    self.buffer += chars
            current_char = self.buffer.pop(0)
            if current_char == '\0':
                self.EOF = True
            self.EOL = False
            if self.dfa.move(current_char):
                self.current_token = self.dfa.get_current_token()
                state = self.current_token[0]
                lexeme = self.current_token[1]
                if state in self.special_states:
                    self.buffer.insert(0, current_char)
                    lexeme = lexeme[:-1]
                if state == 12:     # white space
                    if current_char == '\n':
                        self.EOL = True
                    return 'WHITESPACE', None
                if state == 8:      # ID/KW
                    if lexeme in self.keywords:
                        state = 'KEYWORD'
                    else:
                        state = 'ID'
                else:
                    state = self.state_dict.get(state)
                return state, lexeme


    def __create_the_dfa(self):
        """
        This method creates the dfa object and defines the states and the transitions
            and store it in Scanner.dfa.
        It also should set the self.state_types which specifies which state belongs to which token_type
        :return:
        """
        dfa = dfa_lib.DFA()
        dfa.add_transition(dfa_lib.Charsets.digit, 0, 1)
        dfa.add_transition(dfa_lib.Charsets.digit, 1, 1)
        dfa.add_transition(dfa_lib.Charsets.letter, 1, 16)
        dfa.add_transition(dfa_lib.Charsets.other(dfa_lib.Charsets.letter), 1, 2)
        dfa.add_transition('/', 0, 3)
        dfa.add_transition('*', 3, 4)
        dfa.add_transition('*', 4, 5)
        dfa.add_transition('\0', 4, 15)
        dfa.add_transition(dfa_lib.Charsets.other('*\0'), 4, 4)
        dfa.add_transition('\0', 5, 15)
        dfa.add_transition('/', 5, 6)
        dfa.add_transition(dfa_lib.Charsets.other('/\0'), 5, 4)
        dfa.add_transition(dfa_lib.Charsets.letter, 0, 7)
        dfa.add_transition(dfa_lib.Charsets.letter.union(dfa_lib.Charsets.digit), 7, 7)
        dfa.add_transition(dfa_lib.Charsets.other(dfa_lib.Charsets.letter.union(dfa_lib.Charsets.digit)), 7, 8)
        dfa.add_transition('=', 0, 9)
        dfa.add_transition('=', 9, 10)
        dfa.add_transition(dfa_lib.Charsets.other('='), 9, 11)
        dfa.add_transition('*', 0, 17)
        dfa.add_transition('/', 17, 18)
        dfa.add_transition(dfa_lib.Charsets.other('/'), 17, 19)
        dfa.add_transition(dfa_lib.Charsets.symbol.difference('*/='), 0, 14)
        dfa.add_transition(dfa_lib.Charsets.whitespace, 0, 12)

        terminal_states = [18, 19, 14, 16, 2, 6, 15, 8, 10, 11, 12]
        for s in terminal_states:
            dfa.make_state_terminal(s)

        self.dfa = dfa
