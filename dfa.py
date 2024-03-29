class Charsets:
    digit = set("1234567890")
    letter = set("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_")
    whitespace = set("\f\n\v\t\r \0")
    symbol = set("-+=:;,[]{}()<*/")
    all = digit.union(letter).union(whitespace).union(symbol)

    @staticmethod
    def other(invalids: set) -> set:
        return Charsets.all.difference(invalids)


class NonCharString(TypeError):
    def __str__(self):
        return repr("NonCharString: the string should be in the length of 1")

    @staticmethod
    def check(string_to_check: str):
        if len(string_to_check) != 1:
            raise NonCharString()
        else:
            return True


class InvalidCharacter(ValueError):
    def __init__(self, state_id: int, char: str):
        self.state_id = state_id
        self.char = char

    def __str__(self):
        return repr(f"Invalid Character, no defined movement for character {self.char} from the state {self.state_id}")


class ExistingStateIdError(ValueError):
    def __init__(self, the_id: int):
        self.the_id = the_id

    def __str__(self):
        return repr(f"There is already a state with id {self.the_id}")


class State:
    states = {}

    def __init__(self, state_id: int = 0, is_terminal: bool = False, look_ahead: bool = False):
        '''
        It creates a new State and adds it into the State.states: dict

        :param state_id:
        :raises ExistingStateIdError if the given id already exists.
        '''
        self.otherwise = None
        self.look_ahead = look_ahead
        self.is_terminal = is_terminal
        if state_id in State.states.keys():
            raise ExistingStateIdError(state_id)
        self.state_id = state_id
        self.transitions = []
        State.states[state_id] = self

    def get_next_state(self, char: str):
        """

        :param char: the transition key
        :return: next_state: State
        :raises InvalidCharacter: if no transition defined on the given character
        """
        NonCharString.check(char)
        for transition in self.transitions:
            if char in transition.movements:
                return transition.next_state
        if self.otherwise is not None:
            return State.states[self.otherwise]
        raise InvalidCharacter(self.state_id, char)

    def add_transition(self, keys: set, next_state_id: int):
        if len(keys) == 0:
            self.otherwise = next_state_id
        self.transitions.append(Transition(State.states[next_state_id], keys))


class Transition:
    def __init__(self, next_state: State, movements: set):
        self.movements = movements
        self.next_state = next_state


class DFA:
    def __init__(self):
        self.initial_state = State(0)
        self.error_state = State(-1)

        self.current_state = self.initial_state
        self.current_token_lexeme = ""
        self.last_tokens_final_state = -1
        self.last_token_lexeme = ""

    def reset(self):
        """
        This method should reset the current state of the diagram to the START state
        :return: noting:)
        """
        self.current_token_lexeme = ""
        self.current_state = self.initial_state

    def clear(self):
        State.states.clear()
        self.initial_state = None
        self.error_state = None

    def get_current_token(self) -> (int, str):
        """
        :return: current token (the last detected token) in the form of (final_state: int, lexeme: str)
            NOTE that the current token might be an Error token
        """
        return self.last_tokens_final_state.state_id, self.last_token_lexeme

    def move(self, character: str) -> bool:
        """
        It inputs a character from the scanner and finds the appropriate transition based on the input character
            and goes to the next state.
        If it detects a token, it will store the token in some attributes of the dfa and return Ture, else it returns False
        :param character: inputted character which is a str in length of 1 ("len(character) = 1")
        :return: True if detects a token, False otherwise
        """
        NonCharString.check(character)
        self.current_token_lexeme += character
        try:
            next_state: State = self.current_state.get_next_state(character)
            self.current_state = next_state
            if next_state.is_terminal:
                self.__store()
            return next_state.is_terminal
        except InvalidCharacter:
            self.current_state = self.error_state
            # self.current_token_lexeme = "Invalid input"
            self.current_state = self.error_state
            self.__store()
            return True

    @staticmethod
    def add_transition(keys: set, beginning_state_id: int, intended_state_id: int):
        if beginning_state_id not in State.states.keys():
            State(beginning_state_id)
        if intended_state_id not in State.states.keys():
            State(intended_state_id)
        beginning_state: State = State.states[beginning_state_id]
        beginning_state.add_transition(keys, intended_state_id)

    @staticmethod
    def make_state_terminal(state_id: int):
        the_state: State = State.states[state_id]
        the_state.is_terminal = True

    @staticmethod
    def make_state_non_terminal(state_id: int):
        the_state: State = State.states[state_id]
        the_state.is_terminal = False

    @staticmethod
    def add_state(state_id: int, is_terminal: bool = False):
        State(state_id, is_terminal)

    @staticmethod
    def make_state_look_ahead(state_id: int):
        the_state: State = State.states[state_id]
        the_state.look_ahead = True

    @staticmethod
    def make_state_non_look_ahead(state_id: int):
        the_state: State = State.states[state_id]
        the_state.look_ahead = False

    def is_special_state(state_id: int) -> bool:
        return State.states[state_id].look_ahead

    def __store(self):
        '''
        This method stores the current token and must be called from the move method when it detects a token
        :return:
        '''
        self.last_token_lexeme = self.current_token_lexeme
        self.last_tokens_final_state = self.current_state
