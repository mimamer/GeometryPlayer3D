import unittest
from source.sequencemanager import SequenceManager

class CurveManagerTester(unittest.TestCase):

    def test_init_with_none(self):
        curve_manager=SequenceManager(None)
        self.assertEqual(curve_manager.curves, [])


if __name__ == '__main__':
    unittest.main()