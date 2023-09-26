import unittest

class Player_Logic_Tester(unittest.TestCase):

    def test_press(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_zoom_in(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_zoom_out(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_choose_point(self):
        return
    
    def test_step_forward(self):
        return
    
    def test_step_backwards(self):
        return
    
    def test_step_forward_cuboid(self):
        return
    
    def test_step_backwards_cuboid(self):
        return
    
    def test_jump_to_end(self):
        return
    
    def test_jump_to_start(self):
        return
    
    def test_reset_view_x_axis(self):
        return
    
    def test_reset_view_invert_x_axis(self):
        return
    
    def test_reset_view_y_axis(self):
        return
    
    def test_reset_view_invert_y_axis(self):
        return
    
    def test_reset_view_z_axis(self):
        return
    
    def test_reset_view_invert_z_axis(self):
        return

if __name__ == '__main__':
    unittest.main()