import unittest
from source.curvemanager import CurveManager

class Curve_Manager_module_Tester(unittest.TestCase):

    def test_init_with_none(self):
        curve_manager=CurveManager(None)
        self.assertEqual(curve_manager.curves, [])


if __name__ == '__main__':
    unittest.main()