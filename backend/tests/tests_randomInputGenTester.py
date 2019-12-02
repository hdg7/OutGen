import unittest
from ..generator import RandomInputGenerator
from ..tester import Tester


class TestRandomInputGenTester(unittest.TestCase):

    def test_randomInputGenTester(self):
        inputGen = RandomInputGenerator.RandomInputGenerator("/Users/nalshahwan/ffep/examplesAl/file3a.pre.c","func")
        inputs=inputGen.generateRandomInputs(10)
        tester = Tester.Tester("/Users/nalshahwan/ffep/examplesAl/file3a.pre.c","func",inputs)
        self.assertEqual(len(tester.testFunction()),10)

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(TestModelController('test_randomInputGenTester'))
        return suite
