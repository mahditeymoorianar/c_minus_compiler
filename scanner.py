import dfa as dfa_lib
from token_type import TokenType
from keyword import Keyword


class Scanner:
    def __init__(self):
        self.dfa: dfa_lib.DFA
        self.__create_the_dfa()
        self.current_token: (TokenType, str) = TokenType.ERROR, "not implemented"
        self.state_types: dict = {}  # {STATE_ID: TOKEN_TYPE} and for keywords also we use ID in this dictionary
        self.keywords = {"if": Keyword.IF, "else": Keyword.ELSE, "void": Keyword.VOID, "int": Keyword.INT,
                         "repeat": Keyword.REPEAT, "until": Keyword.UNTIL, "return": Keyword.RETURN}

    def get_next_token(self) -> (TokenType, str):
        '''
        This method is called by other modules and reads from the file character by character
            till it detects a token and returns it as a tuple in the specified format.
        :return: (token_type: TokenType, token_lexeme: str)
        '''
        # TODO: to implement
        self.current_token = TokenType.ERROR, "not implemented"
        return self.current_token

    def __detect_token_type(self, state_id: int, lexeme: str) -> TokenType:
        '''
        This method inputs a number as the state_id and detects what token_type does that state
            specify based on the dfa. It also inputs a string as lexeme which is used to differentiate
            the types KEYWORD and ID from each other.
        :param state_id:
        :param lexeme: It is used to differentiate the types KEYWORD and ID from each other.
        :return: token_type: TokenType
        '''
        # TODO: to implement
        return TokenType.ERROR

    def __create_the_dfa(self):
        '''
        This method creates the dfa object and defines the states and the transitions
            and store it in Scanner.dfa.
        It also should set the self.state_types which specifies which state belongs to which token_type
        :return:
        '''
        dfa = dfa_lib.DFA()
        # TODO: to create the dfa object and define the states and transitions
        self.dfa = dfa
