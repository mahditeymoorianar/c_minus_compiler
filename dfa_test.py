import unittest

import dfa as dfa_lib
from dfa import DFA as Dfa
from dfa import NonCharString


class MyTestCase(unittest.TestCase):
    def test1(self):
        dfa = Dfa()
        print(">>>")
        # print(State.states)
        dfa.add_transition(set('a'), 0, 1)
        dfa.add_transition(set('a'), 1, 3)
        dfa.add_transition(set('b'), 1, 2)
        dfa.add_transition(set('b'), 0, 4)
        dfa.add_transition(set('ab'), 4, 3)
        dfa.add_transition(set('c'), 4, 5)
        dfa.make_state_terminal(2)
        dfa.make_state_terminal(3)
        dfa.make_state_terminal(5)

        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('b'), True)
        self.assertEqual(dfa.get_current_token(), (2, "ab"))

        dfa.reset()

        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('a'), True)
        self.assertEqual(dfa.get_current_token(), (3, "ba"))
        dfa.clear()
        del dfa

    def test2(self):
        dfa = Dfa()
        dfa.add_transition(set('a'), 0, 1)
        dfa.add_transition(set('b'), 0, 0)
        dfa.add_transition(set('a'), 1, 2)
        dfa.add_transition(set('b'), 1, 3)
        dfa.add_transition(set('a'), 2, 4)
        dfa.add_transition(set('b'), 2, 1)
        dfa.add_transition(set('a'), 3, 3)
        dfa.add_transition(set('b'), 3, 2)
        dfa.make_state_terminal(4)

        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('a'), True)
        self.assertEqual(dfa.get_current_token(), (4, 'aababbaaaabbaa'))

        dfa.clear()
        del dfa

    def test3(self):
        dfa = Dfa()

        dfa.add_transition('a', 0, 2)
        dfa.add_transition('b', 3, 1)
        dfa.add_transition('\0', 3, 4)
        dfa.add_transition('b', 2, 2)
        dfa.add_transition('a', 2, 3)
        dfa.add_transition('c', 2, 0)
        dfa.add_transition('b', 0, 3)
        dfa.add_transition('a', 3, 2)
        dfa.make_state_terminal(1)
        dfa.make_state_terminal(4)

        dfa.reset()
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('b'), False)
        self.assertEqual(dfa.move('a'), False)
        self.assertEqual(dfa.move('\0'), True)
        self.assertEqual(dfa.get_current_token(), (4, 'abbbaaba\0'))

        dfa.move('c')
        # self.assertEqual(dfa.get_current_token(), (-1, 'Invalid input'))
        self.assertEqual(dfa.get_current_token(), (-1, 'abbbaaba\0c'))

        dfa.reset()
        try:
            dfa.move("ab")
            self.assertEqual(False, True)
        except NonCharString as error:
            self.assertEqual(True, True)
        dfa.clear()
        del dfa

    def test4(self):
        dfa = Dfa()
        dfa.add_transition(dfa_lib.Charsets.letter, 0, 3)
        dfa.add_transition(dfa_lib.Charsets.digit, 0, 0)
        dfa.add_transition("/", 0, 1)
        dfa.add_transition("/", 1, 2)
        dfa.add_transition(dfa_lib.Charsets.other("/"), 1, 0)
        dfa.add_transition("\0", 2, 4)
        dfa.add_transition('', 2, 2)
        dfa.make_state_terminal(3)
        dfa.make_state_terminal(4)

        dfa.reset()
        self.assertEqual(dfa.move('1'), False)
        self.assertEqual(dfa.move('2'), False)
        self.assertEqual(dfa.move('l'), True)
        self.assertEqual(dfa.get_current_token(), (3, '12l'))
        dfa.reset()
        self.assertEqual(dfa.move('1'), False)
        self.assertEqual(dfa.move('/'), False)
        self.assertEqual(dfa.move('l'), False)
        self.assertEqual(dfa.move('0'), False)
        self.assertEqual(dfa.move('/'), False)
        self.assertEqual(dfa.move('/'), False)
        self.assertEqual(dfa.move('/'), False)
        self.assertEqual(dfa.move('s'), False)
        self.assertEqual(dfa.move('4'), False)
        self.assertEqual(dfa.move('\0'), True)
        self.assertEqual(dfa.get_current_token(), (4, '1/l0///s4\0'))



if __name__ == '__main__':
    unittest.main()
