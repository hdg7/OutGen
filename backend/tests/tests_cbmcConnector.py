import unittest
import CBMCConnector


class TestCBMCConnector(unittest.TestCase):

    def test_cbmcConnector(self):
        cbmcC = CBMCConnector.CBMCConnector("/Users/nalshahwan/ffep/examplesAl/file3a.pre.c","func")
        cbmcC.createContraintsFile()
        s = cbmcC.getConstraints()
        self.assertEqual(str(s.check()),"sat")

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(Tests.TestCBMCConnector('test_cbmcConnector'))
        return suite
