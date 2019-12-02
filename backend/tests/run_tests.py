import unittest
from tests.tests_mutator import TestMutator


suite1 = TestMutator.suite()
all_tests = unittest.TestSuite([suite1])
unittest.TextTestRunner().run(all_tests)


