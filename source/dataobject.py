import mpl_toolkits
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy

is_visible_factor=0.01
data_object_counter=0

class DataObject:
    def __init__(self,data):
        global data_object_counter#TODO:only for testing
        data_object_counter+=1
        self.is_vertex=True
        self.width_x=0
        self.height_y=0
        self.depth_z=0
        self.min_lim=None
        self.max_lim=None
        factor=0.01 #TODO: only for testing, is ok #0.001 is nearly ok #0.0001too small already #0.00001 not visible
        if len(data)!=1:
            self.is_vertex=False
        self.data=None
        if self.is_vertex:
            self.data=numpy.array(data[0]) #is list of three numbers
            self.min_lim=[self.data[0], self.data[1],self.data[2]]
            self.max_lim=self.min_lim
        else:
            try:
                segments=[(
                    numpy.array(data[index][0])*factor,
                    numpy.array(data[index][1])*factor)
                    for index in range(len(data))]
                self.data=segments
                self.width_x,self.height_y,self.depth_z=self.get_dimensions()
            except Exception as e:
                print(e)
    
    def get_dimensions(self):#TODO:naming?etc, refactor with Limit class
        self.min_lim=[self.data[0][0][0],self.data[0][0][1],self.data[0][0][2]]
        self.max_lim=[self.data[0][0][0],self.data[0][0][1],self.data[0][0][2]]
        for segment in self.data:
            for index in range(len(segment)):
                for axis in range(len(self.min_lim)):
                    if self.min_lim[axis] > segment[index][axis]:
                        self.min_lim[axis]=segment[index][axis]
                    if self.max_lim[axis] < segment[index][axis]:
                       self.max_lim[axis]=segment[index][axis]
        return self.max_lim[0]-self.min_lim[0],self.max_lim[1]-self.min_lim[1],self.max_lim[2]-self.min_lim[2]


    def get_plot_data_object(self,color='yellow') -> dict:
        if self.is_vertex:
            return {"x":self.data[0],
                    "y": self.data[1],
                    "z": self.data[2],
                    "color":color}
        else:
            return {"line_collection":Line3DCollection(self.data,edgecolor=color),
                    "min_lim":self.min_lim,
                    "max_lim":self.max_lim,
                    "width_x": self.width_x,
                    "height_y": self.height_y,
                    "depth_z": self.depth_z}


def square_distance_between(object_a:DataObject,object_b:DataObject):
    if object_a.is_vertex and object_b.is_vertex:
        return square_distance_between_points(object_a.data,object_b.data)
    
    if object_a.is_vertex and not object_b.is_vertex:
        point_list=get_points(object_b)
        return max([square_distance_between_points(object_a.data, point_list[index]) \
                            for index in range(len(point_list)) ])
    
    if not object_a.is_vertex and object_b.is_vertex:
        point_list=get_points(object_a)
        sq_dist_list=[square_distance_between_points(object_b.data, point_list[index]) \
                            for index in range(len(point_list)) ]
        return max(sq_dist_list)
    
    if not object_a.is_vertex and not object_b.is_vertex:
        point_list_a=get_points(object_a)
        point_list_b=get_points(object_b)
        return max([square_distance_between_points(point_list_a[index_a], point_list_b[index_b]) \
                            for index_a in range(len(point_list_a)) for index_b in range(len(point_list_b)) ])

def square_distance_between_points(point_data_a,point_data_b):
    return (point_data_a[0]-point_data_b[0])**2+(point_data_a[1]-point_data_b[1])**2+(point_data_a[2]-point_data_b[2])**2

def get_points(object_a:DataObject):
    if object_a.is_vertex:
        return object_a.data
    else:
        return [[object_a.data[seg][index][0],object_a.data[seg][index][1],object_a.data[seg][index][2]] \
                    for seg in range(len(object_a.data)) for index in range(2)]