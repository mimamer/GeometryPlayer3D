        # lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
        #                      linewidth=linewidth, alpha=alpha)
#import mpl_toolkits
#from mpl_toolkits.mplot3d.art3d import Line3DCollection
from source.utils import square_distance_between
class Sequence:
    def __init__(self, data_objects):
        self.plot_data=None
        self.x=[]
        self.y=[]
        self.z=[]
        self.gen  = self.next_value(data_objects)

    def reset_to_actual_points(self,tmp_index):
        self.plot_data=[self.x[:tmp_index],self.y[:tmp_index],self.z[:tmp_index] ]
    
    def add_point(self):
        data_object = next(self.gen)
        self.x.append(data_object[0])
        self.y.append(data_object[1])
        self.z.append(data_object[2])

    def next_value(self,data_objects):
        for i in range(len(data_objects)):
            try:
                if len(data_objects[i])==3 and (type(data_objects[i][0]) is float or type(data_objects[i][0]) is int):
                    yield data_objects[i]
                elif len(data_objects[i])>=2 and type(data_objects[i][0]) is tuple:#only test 0.elem is a bit dirty
                    print("Line3DCollection")
                    yield None
                else:
                    raise Exception("Unknown geometric construct")

            except StopIteration:
                break

    def is_empty(self):
        if self.plot_data is None or len(self.plot_data)==0 or len(self.plot_data[0])==0:
            return True
        
    def get_curve_plot_data(self):
        return self.plot_data
    
    def get_max_squared_dist_value(self,chosen_point):
        sq_dist_values=[square_distance_between(\
            [self.plot_data[0][i],self.plot_data[1][i],self.plot_data[2][i]],chosen_point)\
                  for i in range(len(self.plot_data[0]))]
        max_sq_dist_value=max(sq_dist_values)
        self.delete_list=[index for index in range(len(self.plot_data[0])) if sq_dist_values[index]==max_sq_dist_value]
        return max_sq_dist_value

    def set_plot_data_to_radius(self):
        xvals=[]
        yvals=[]
        zvals=[]
        for index in range(len(self.plot_data[0])):
            if index in self.delete_list:
                continue
            xvals.append(self.plot_data[0][index])
            yvals.append(self.plot_data[1][index])
            zvals.append(self.plot_data[2][index])
        self.plot_data=[xvals,yvals,zvals]