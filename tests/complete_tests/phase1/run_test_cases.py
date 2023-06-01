import os
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here
        # os.system("copy /tests/complete_tests_phase1/T01/input.txt input.txt")
        os.system("copy \"t02/input.txt\" \"../../../myinput.txt\"")
        os.system("notepad ../../../myinput.txt")
        print("salam")

if __name__ == '__main__':
    print("salaaam")
    # os.system("copy T01/input.txt ../../../input.txt")
    # os.system("notepad ../../../input.txt")
    # os.system("mkdir \"D:/fff/ffff/fffff\"")
    # print("salam")
    # unittest.main()

