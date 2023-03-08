import unittest
from DFA import DFA as Dfa

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
        self.assertEqual(dfa.get_current_token(),   (4, 'aababbaaaabbaa'))

if __name__ == '__main__':
    unittest.main()
