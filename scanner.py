import dfa as dfa_lib
from token_type import TokenType
from modules.keyword import Keyword


class Scanner:
    def __init__(self, file_name):
        self.dfa: dfa_lib.DFA
        self.__create_the_dfa()
        self.current_token: (TokenType, str) = TokenType.ERROR, "not implemented"
        self.state_dict = {18: 'Unmatched comment', 19: 'SYMBOL', 14: 'SYMBOL', 16: 'Invalid number', 2: 'NUM',
                           6: 'COMMENT', 15: 'Unclosed comment', 8: 'ID/KW', 10: 'SYMBOL',
                           11: 'SYMBOL'}  # {STATE_ID: TOKEN_TYPE} and for keywords also we use ID in this dictionary
        self.keywords = {"if": Keyword.IF, "else": Keyword.ELSE, "void": Keyword.VOID, "int": Keyword.INT,
                         "repeat": Keyword.REPEAT, "until": Keyword.UNTIL, "return": Keyword.RETURN}
        self.special_states = {11, 8, 2, 19}
        self.buffer_size = 1024  # size of each buffer in bytes
        self.buffer = []
        self.file = open(file_name, 'r')
        self.EOF = False
        self.EOL = False
        self.NewLine = False

    def get_next_token(self) -> (TokenType, str):
        """
        This method is called by other modules and reads from the file character by character
            till it detects a token and returns it as a tuple in the specified format.
        :return: (token_type: TokenType, token_lexeme: str)
        """
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
                if current_char == '\n':
                    self.NewLine = True
                elif self.NewLine:      # transition point
                    self.NewLine = False
                    self.EOL = True
                else:
                    self.EOL = False
                if self.dfa.move(current_char):
                    self.current_token = self.dfa.get_current_token()
                    state = self.current_token[0]
                    lexeme = self.current_token[1]
                    if state in self.special_states:
                        self.buffer.insert(0, current_char)
                    if state == 8:  # ID/KW
                        if lexeme in self.keywords:
                            state = 'KEYWORD'
                        else:
                            state = 'ID'
                    else:
                        state = self.state_dict.get(state)
                    return state, lexeme

    # def __detect_token_type(self, state_id: int, lexeme: str) -> TokenType:
    #     """
    #     This method inputs a number as the state_id and detects what token_type does that state
    #         specify based on the dfa. It also inputs a string as lexeme which is used to differentiate
    #         the types KEYWORD and ID from each other.
    #     :param state_id:
    #     :param lexeme: It is used to differentiate the types KEYWORD and ID from each other.
    #     :return: token_type: TokenType
    #     """
    #     state_type = self.state_types[state_id]
    #     if state_type == TokenType.ID and lexeme in self.keywords.keys():
    #         return TokenType.KEYWORD
    #     return state_type

    def __create_the_dfa(self):
        """
        This method creates the dfa object and defines the states and the transitions
            and store it in Scanner.dfa.
        It also should set the self.state_types which specifies which state belongs to which token_type
        :return:
        """
        dfa = dfa_lib.DFA()
        # TODO: to create the dfa object and define the states and transitions
        self.dfa = dfa
