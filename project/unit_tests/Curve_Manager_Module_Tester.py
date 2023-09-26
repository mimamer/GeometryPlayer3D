import unittest
from source.Curve_Manager import Curve_Manager

class Curve_Manager_module_Tester(unittest.TestCase):

    def test_init_with_none(self):
        curve_manager=Curve_Manager(None)
        self.assertEqual(curve_manager.curves, [])


if __name__ == '__main__':
    unittest.main()