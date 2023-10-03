from source.dataobject import square_distance_between
from source.dataobject import DataObject
class Sequence:
    def __init__(self, input_objects):
        self.plot_data=None
        self.data_objects=[]
        self.gen  = self.next_value(input_objects)

    def reset_to_actual_points(self,tmp_index):
        self.plot_data=self.data_objects[:tmp_index]

    def plot_sequence_data(self,ax,color):
        for index in range(len(self.plot_data)):#TODO:color is changing, is this good? -> not when zooming
            self.plot_data[index].plot_data_object(ax,color[index])
    
    def add_point(self):
        try:
            data_object = next(self.gen)
            self.data_objects.append(data_object)
        except StopIteration as stop:
            raise stop


    def next_value(self,input_objects):
        for i in range(len(input_objects)):
            try:
                yield DataObject(input_objects[i])
            except StopIteration as stop:
                raise stop

    def is_empty(self):
        if self.plot_data is None or len(self.plot_data)==0:
            return True
        
    def get_sequence_plot_data(self):
        return self.plot_data

    
    def get_max_squared_dist_value(self,chosen_data_object):
        sq_dist_values=[square_distance_between(self.plot_data[i],chosen_data_object) 
                            for i in range(len(self.plot_data))]
        max_sq_dist_value=max(sq_dist_values)
        self.delete_list=[index for index in range(len(self.plot_data)) if sq_dist_values[index]==max_sq_dist_value]
        return max_sq_dist_value
    
    def set_plot_data_to_radius(self):
        vals=[]
        for index in range(len(self.plot_data)):
            if index in self.delete_list:
                continue
            vals.append(self.plot_data[index])
        self.plot_data=vals