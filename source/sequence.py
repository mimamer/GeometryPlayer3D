from source.dataobject import square_distance_between
from source.dataobject import DataObject
import math

class Sequence:
    def __init__(self, input_objects, name, color):
        self.plot_data=None
        self.data_objects=[]
        self.input_objects=input_objects
        self.gen  = self.next_value()
        self.total_length=len(self.input_objects)
        self.distance_dict={}
        self.scope=[]
        self.name=name
        self.color=color
        self.representative_color=self.color[int(len(self.color)/2)]

    def reset_to_actual_points(self,tmp_index):
        if tmp_index>=len(self.data_objects):
            self.plot_data=self.data_objects[:len(self.data_objects)]
            self.scope= [i for i in range(len(self.data_objects))]
        else:
            self.plot_data=self.data_objects[:tmp_index]
            self.scope=[i for i in range(tmp_index)]

    def plot_sequence_data(self,color, jump_over_object=None):
        #actual point lists for faster plotting, problems if these list cannot get long due to 'LineCollection3D's between points
        actual_point_list_x=[]
        actual_point_list_y=[]
        actual_point_list_z=[]
        start_list_index=0
        index=0
        result_list=[]
        if type(jump_over_object)!=list:
            jump_over_object=[jump_over_object]
        while index<len(self.plot_data):#TODO:color is changing, is this good? -> not when zooming (mehr als eine Zusammenhangskomponente)
            if self.plot_data[index] in jump_over_object:
                index+=1
                continue
            if self.plot_data[index].is_vertex:
                actual_point_list_x.append(self.plot_data[index].data[0])
                actual_point_list_y.append(self.plot_data[index].data[1])
                actual_point_list_z.append(self.plot_data[index].data[2])
            else:#LineCollection3D
                if len(actual_point_list_x)>0:
                    zws_dict={"xs":actual_point_list_x,
                            "ys": actual_point_list_y,
                            "zs": actual_point_list_z,
                            "color": color[start_list_index:start_list_index+len(actual_point_list_x)]}
                    result_list.append(zws_dict)
                    actual_point_list_x=[]
                    actual_point_list_y=[]
                    actual_point_list_z=[]
                start_list_index=index+1
                result_list.append(self.plot_data[index].get_plot_data_object(color[index]))
            index+=1
        if len(actual_point_list_x)>0:
            zws_dict={"xs":actual_point_list_x,
                    "ys": actual_point_list_y,
                    "zs": actual_point_list_z,
                    "color": color[start_list_index:start_list_index+len(actual_point_list_x)]}
            result_list.append(zws_dict)
        return result_list

    def get_plot_sequence_distance_data(self, chosen_sequence):#TODO:generate values before, more getting 
        xvals=[i for i in range(len(self.data_objects))]
        if chosen_sequence is None:
            return None, None
        if chosen_sequence==self:
            yvals=[0]*len(xvals)
        else:
            yvals=[math.sqrt(get_squared_distance_between_sequences(self,chosen_sequence,i)) 
                   if get_squared_distance_between_sequences(self,chosen_sequence,i)!=-1.0 
                   else -1 
                   for i in xvals]
        return xvals,yvals #TODO: last line ok but computation should not be here

    def add_point(self):
        try:
            data_object = next(self.gen)
            self.data_objects.append(data_object)
        except StopIteration as stop:
            raise stop

    def next_value(self):
        for i in range(len(self.input_objects)):
            try:
                yield DataObject(self.input_objects[i])
            except StopIteration as stop:
                raise stop

    def is_empty(self):
        if self.plot_data is None or len(self.plot_data)==0:
            return True
        
    def get_sequence_plot_data(self):
        return self.plot_data

    def get_max_squared_dist_value(self,chosen_data_object):
        if self.distance_dict =={} or chosen_data_object not in self.distance_dict.keys():
            distance_dict_for_chosen={}
            for i in self.scope:#erganze demnach falls ref nicht plot data war
                distance_dict_for_chosen[self.data_objects[i]]=square_distance_between(self.data_objects[i],chosen_data_object) 
                #nur die aus dem dict
            self.distance_dict[chosen_data_object]=distance_dict_for_chosen

        sq_dist_values={}
        for index in self.scope:
            data_object=self.data_objects[index]
            if data_object in self.distance_dict[chosen_data_object].keys():
                sq_dist_values[index]=self.distance_dict[chosen_data_object][data_object]
            else:
                new_value=square_distance_between(data_object,chosen_data_object)
                self.distance_dict[chosen_data_object][data_object]=new_value
                sq_dist_values[index]=new_value

        max_sq_dist_value=max(sq_dist_values.values())

        self.delete_list=[index for index in self.scope if sq_dist_values[index]==max_sq_dist_value]#if more than one 
        return max_sq_dist_value
    
    def apply_sequence_delete_list(self):
        vals=[]
        scope_vals=[]
        for index in self.scope:
            try:
                if index in self.delete_list:
                    continue
                scope_vals.append(index)
                vals.append(self.data_objects[index])
            except IndexError as e:
                print("Index error: index", index, len(self.data_objects), len(self.scope))

        self.scope=scope_vals
        self.plot_data=vals

    def compute_squared_distance_to(self,sequence):
        min_sequence_length=min([len(self.data_objects),len(sequence.data_objects)])
        for i in range(min_sequence_length):
            distance=square_distance_between(self.data_objects[i],sequence.data_objects[i]) 
            self.distance_dict[sequence.data_objects[i]]={self.data_objects[i]:distance}

    def generate_dict_entry_in_other(self,other_sequence,i):
        #runtime may be better with generating other sequence data with respect to chosen sequence
        if self.data_objects[i] not in other_sequence.distance_dict.keys():
            new_value=square_distance_between(self.data_objects[i],other_sequence.data_objects[i]) 
            other_sequence.distance_dict[self.data_objects[i]]={other_sequence.data_objects[i]:new_value}
            return new_value
        elif self.data_objects[i] in other_sequence.distance_dict.keys() and \
            other_sequence.data_objects[i] not in other_sequence.distance_dict[self.data_objects[i]].keys():
            new_value=square_distance_between(self.data_objects[i],other_sequence.data_objects[i]) 
            other_sequence.distance_dict[self.data_objects[i]][other_sequence.data_objects[i]]=new_value
            return new_value
        else:
            return other_sequence.distance_dict[self.data_objects[i]][other_sequence.data_objects[i]]


def get_squared_distance_between_sequences(self_sequence:Sequence,chosen_sequence:Sequence,i:int):
    if self_sequence is None or chosen_sequence is None:
        raise Exception("At least one of the sequences is empty")
    if i >=max([len(chosen_sequence.data_objects), len(self_sequence.data_objects)]) or i <0:
        raise Exception(f"{i} is not in valid range")
    if i>=min(len(chosen_sequence.data_objects), len(self_sequence.data_objects)):
        return -1.0
    if self_sequence.distance_dict=={} and chosen_sequence.distance_dict=={}:
        chosen_sequence.compute_squared_distance_to(self_sequence)
        return chosen_sequence.distance_dict[self_sequence.data_objects[i]][chosen_sequence.data_objects[i]]
        #generate data in chosen
        
    if self_sequence.distance_dict!={}:
        return chosen_sequence.generate_dict_entry_in_other(self_sequence,i)
    
    if chosen_sequence.distance_dict!={}:
        return self_sequence.generate_dict_entry_in_other(chosen_sequence,i)