import mpl_toolkits
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy
from source.limit import Limit

class DataObject:
    def __init__(self,data):
        self.is_vertex=True
        self.width_x=0
        self.height_y=0
        self.depth_z=0
        self.limit=Limit()
        if len(data)!=1:
            self.is_vertex=False
        self.data=None
        if self.is_vertex:
            self.data=numpy.array(data[0]) #is list of three numbers
            self.limit.correct_limits_values(self.data[0], self.data[1],self.data[2])
        else:
            try:
                segments=[(
                    numpy.array(data[index][0]),
                    numpy.array(data[index][1]))
                    for index in range(len(data))]
                self.data=segments
                self.set_dimensions()
            except Exception as e:
                print(e)
    
    def set_dimensions(self):
        for segment in self.data:
            for index in range(len(segment)):
                self.limit.correct_limits_values(segment[index][0], segment[index][1],segment[index][2])
        min_lim=self.limit.get_min()
        max_lim=self.limit.get_max()
        self.width_x=max_lim[0]-min_lim[0]
        self.height_y=max_lim[1]-min_lim[1]
        self.depth_z=max_lim[2]-min_lim[2]

    def get_plot_data_object(self,color='yellow') -> dict:
        if self.is_vertex:
            return {"x":self.data[0],
                    "y": self.data[1],
                    "z": self.data[2],
                    "color":color}
        else:
            return {"line_collection":Line3DCollection(self.data,edgecolor=color),
                    "min_lim":self.limit.get_min(),
                    "max_lim":self.limit.get_max(),
                    "width_x": self.width_x,
                    "height_y": self.height_y,
                    "depth_z": self.depth_z,
                    "color":color}


def square_distance_between(object_a:DataObject,object_b:DataObject):#TODO:think about volume distances..., rename?
    if object_a.is_vertex and object_b.is_vertex:
        return square_distance_between_points(object_a.data,object_b.data)
    
    if object_a.is_vertex and not object_b.is_vertex:
        point_list=get_points(object_b)
        return min([square_distance_between_points(object_a.data, point_list[index]) \
                            for index in range(len(point_list)) ])
    
    if not object_a.is_vertex and object_b.is_vertex:
        point_list=get_points(object_a)
        sq_dist_list=[square_distance_between_points(object_b.data, point_list[index]) \
                            for index in range(len(point_list)) ]
        return min(sq_dist_list)
    
    if not object_a.is_vertex and not object_b.is_vertex:
        point_list_a=get_points(object_a)
        point_list_b=get_points(object_b)
        return min([square_distance_between_points(point_list_a[index_a], point_list_b[index_b]) \
                            for index_a in range(len(point_list_a)) for index_b in range(len(point_list_b)) ])

def square_distance_between_points(point_data_a,point_data_b):
    return (point_data_a[0]-point_data_b[0])**2+(point_data_a[1]-point_data_b[1])**2+(point_data_a[2]-point_data_b[2])**2

def get_points(object_a:DataObject):
    if object_a.is_vertex:
        return object_a.data
    else:
        return [[object_a.data[seg][index][0],object_a.data[seg][index][1],object_a.data[seg][index][2]] \
                    for seg in range(len(object_a.data)) for index in range(2)]