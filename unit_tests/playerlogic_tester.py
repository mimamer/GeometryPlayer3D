import unittest
from source.utils import open_dataobjects
from source.geometryplayer3d import GeometryPlayer3D

class AnimatorLogicTester(unittest.TestCase):
    #single curve

    def test_press(self):
        player= GeometryPlayer3D(open_dataobjects())
        self.assertEqual('foo'.upper(), 'FOO')

    def test_zoom_in(self):
        player= GeometryPlayer3D(open_dataobjects())
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_zoom_out(self):
        player= GeometryPlayer3D(open_dataobjects())
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_choose_point(self):
        return
    
    def test_step_forward(self):
        data_objects=open_dataobjects()
        player= GeometryPlayer3D(data_objects)
        player.forwards()
        curve=player.sequence_manager.sequences[0]
        test_value=[curve.x,curve.y,curve.z]
        test_plot_value=curve.get_sequence_plot_data()
        self.assertEqual(test_value,test_plot_value)
        self.assertEqual(curve.x,[data_objects[0][0][0]])
        self.assertEqual(curve.y,[data_objects[0][0][1]])
        self.assertEqual(curve.z,[data_objects[0][0][2]])
        return
    
    def test_step_forward_ten_times(self):
        data_objects=open_dataobjects()
        player= GeometryPlayer3D(data_objects)
        reference_value_x=[]
        reference_value_y=[]
        reference_value_z=[]
        
        for i in range(10):
            player.forwards()
            reference_value_x.append(data_objects[i][0][0])
            reference_value_y.append(data_objects[i][0][1])
            reference_value_z.append(data_objects[i][0][2])
        curve=player.sequence_manager.sequences[0]
        test_value=[curve.x,curve.y,curve.z]
        test_plot_value=curve.get_sequence_plot_data()
        self.assertEqual(test_value,test_plot_value)
        self.assertEqual(test_value,
                         [reference_value_x,reference_value_y,reference_value_z])
        return


    def test_step_backwards(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_step_forward_cuboid(self):
        data_objects=open_dataobjects()
        player= GeometryPlayer3D(data_objects)
        reference_value_x=[]
        reference_value_y=[]
        reference_value_z=[]
        i=0
        while len(data_objects[i])==1:
            player.forwards()
            reference_value_x.append(data_objects[i][0][0])
            reference_value_y.append(data_objects[i][0][1])
            reference_value_z.append(data_objects[i][0][2])
            i+=1

        curve=player.sequence_manager.sequences[0]
        test_value=[curve.x,curve.y,curve.z]
        test_plot_value=curve.get_sequence_plot_data()
        self.assertEqual(test_value,test_plot_value)
        self.assertEqual(test_value,
                         [reference_value_x,reference_value_y,reference_value_z])
        return
    
    def test_step_backwards_cuboid(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_jump_to_end(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_jump_to_start(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_reset_view_x_axis(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_reset_view_invert_x_axis(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_reset_view_y_axis(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_reset_view_invert_y_axis(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_reset_view_z_axis(self):
        player= GeometryPlayer3D(open_dataobjects())
        return
    
    def test_reset_view_invert_z_axis(self):
        player= GeometryPlayer3D(open_dataobjects())
        return

    # more than one curve
    def test_load_curves(self):
        return

if __name__ == '__main__':
    unittest.main()