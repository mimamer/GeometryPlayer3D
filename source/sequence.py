from source.dataobject import square_distance_between
from source.dataobject import DataObject
import math

class Sequence:
    def __init__(self, input_objects):
        self.plot_data=None
        self.data_objects=[]
        self.gen  = self.next_value(input_objects)
        self.distance_dict={}

    def reset_to_actual_points(self,tmp_index):
        if tmp_index>=len(self.data_objects):
            self.plot_data=self.data_objects[:len(self.data_objects)]
        else:
            self.plot_data=self.data_objects[:tmp_index]

    def plot_sequence_data(self,ax,color):
        #actual point lists for faster plotting, problems if these list cannot get long due to 'LineCollection3D's between points
        actual_point_list_x=[]
        actual_point_list_y=[]
        actual_point_list_z=[]
        start_list_index=0
        index=0
        plot_first_linecollection3d=True
        plot_contains_points=False
        while index<len(self.plot_data):#TODO:color is changing, is this good? -> not when zooming (mehr als eine Zusammenhangskomponente)
            if self.plot_data[index].is_vertex:
                actual_point_list_x.append(self.plot_data[index].data[0])
                actual_point_list_y.append(self.plot_data[index].data[1])
                actual_point_list_z.append(self.plot_data[index].data[2])
                plot_contains_points=True
            else:#LineCollection3D
                if plot_first_linecollection3d and not plot_contains_points:#problem if all the points come after this stuff...
                    #TODO:have to do this after all points are plotted , create testdata first
                    # -> cuboids need to be plotted later, remember color in "cuboid list" eg.
                    print("Tighten ax lims")
                    ax.set_xlim((self.plot_data[index].min_lims[0],self.plot_data[index].max_lims[0]))
                    ax.set_ylim((self.plot_data[index].min_lims[1],self.plot_data[index].max_lims[1]))
                    ax.set_zlim((self.plot_data[index].min_lims[2],self.plot_data[index].max_lims[2]))
                plot_first_linecollection3d=False
                if len(actual_point_list_x)>0:
                    ax.scatter(xs=actual_point_list_x, ys=actual_point_list_y,  zs=actual_point_list_z, depthshade=False, c=color[start_list_index:len(actual_point_list_x)])
                    actual_point_list_x=[]
                    actual_point_list_y=[]
                    actual_point_list_z=[]
                    start_list_index=index+1
                self.plot_data[index].plot_data_object(ax,color[index])
                
            index+=1
        if len(actual_point_list_x)>0:
            ax.scatter(xs=actual_point_list_x, ys=actual_point_list_y,  zs=actual_point_list_z, depthshade=False,\
                        c=color[start_list_index:start_list_index+len(actual_point_list_x)])    

    def plot_sequence_abs_data(self,abs_plot, chosen_sequence, color):
        min_sequence_length=min([len(self.plot_data),len(chosen_sequence.plot_data)])#TODO:bit ugly
        xvals=[i for i in range(min_sequence_length)]#TODO:always the real numbers..., what are the original indices
        if chosen_sequence==self:
            yvals=[0]*len(self.plot_data)
        else:
            yvals=[math.sqrt(get_squared_distance_between_sequences(self,chosen_sequence,i)) for i in range(min_sequence_length) ]
        return abs_plot.plot(xvals,yvals,linewidth=1, marker="o", c=color)

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

    #TODO: dynamisch, lege pro sequenz distance-dir an: ref_0(chosen): { ref_1: wert_1, ref_2: wert_2 usw}
    def get_max_squared_dist_value(self,chosen_data_object):
        if self.distance_dict =={} or chosen_data_object not in self.distance_dict.keys():
            distance_dict_for_chosen={}
            for i in range(len(self.plot_data)):#erganze demnach falls ref nicht plot data war
                distance_dict_for_chosen[self.plot_data[i]]=square_distance_between(self.plot_data[i],chosen_data_object) 
                #nur die aus dem dict
            self.distance_dict[chosen_data_object]=distance_dict_for_chosen

        sq_dist_values=[]
        for data_object in self.plot_data:
            if data_object in self.distance_dict[chosen_data_object].keys():
                sq_dist_values.append(self.distance_dict[chosen_data_object][data_object])
            else:
                new_value=square_distance_between(data_object,chosen_data_object)
                self.distance_dict[chosen_data_object][data_object]=new_value
                sq_dist_values.append(new_value)

            
       # sq_dist_values=[square_distance_between(self.plot_data[i],chosen_data_object) 
       #                     for i in range(len(self.plot_data))]#nur die aus dem dict
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
    
    def compute_squared_distance_to(self,sequence):
        min_sequence_length=min([len(self.plot_data),len(sequence.plot_data)])
        for i in range(min_sequence_length):
            distance=square_distance_between(self.plot_data[i],sequence.plot_data[i]) 
            self.distance_dict[sequence.plot_data[i]]={self.plot_data[i]:distance}

    def generate_dict_entry_in_other(self,other_sequence,i):
        #runtime may be better with generatigng other sequence data with resprect to chosen sequence
        if self.plot_data[i] not in other_sequence.distance_dict.keys():
            new_value=square_distance_between(self.plot_data[i],other_sequence.plot_data[i]) 
            other_sequence.distance_dict[self.plot_data[i]]={other_sequence.plot_data[i]:new_value}
            return new_value
        elif self.plot_data[i] in other_sequence.distance_dict.keys() and \
            other_sequence.plot_data[i] not in other_sequence.distance_dict[self.plot_data[i]].keys():
            new_value=square_distance_between(self.plot_data[i],other_sequence.plot_data[i]) 
            other_sequence.distance_dict[self.plot_data[i]][other_sequence.plot_data[i]]=new_value
            return new_value
        else:
            return other_sequence.distance_dict[self.plot_data[i]][other_sequence.plot_data[i]]


def get_squared_distance_between_sequences(self_sequence:Sequence,chosen_sequence:Sequence,i:int):
    if i >=min([len(chosen_sequence.plot_data), len(self_sequence.plot_data)]) or i <0:
        raise Exception(f"{i} is not in valid range")
    if self_sequence.distance_dict=={} and chosen_sequence.distance_dict=={}:
        chosen_sequence.compute_squared_distance_to(self_sequence)
        return chosen_sequence.distance_dict[self_sequence.plot_data[i]][chosen_sequence.plot_data[i]]
        #generate data in chosen
        
    if self_sequence.distance_dict!={}:
        return chosen_sequence.generate_dict_entry_in_other(self_sequence,i)
    
    if chosen_sequence.distance_dict!={}:
        return self_sequence.generate_dict_entry_in_other(chosen_sequence,i)