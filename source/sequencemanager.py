from source.sequence import Sequence
from matplotlib.lines import Line2D
import math
from source.limit import Limit
from source.dataobject import square_distance_between
from source.utils import create_color
from matplotlib.backend_bases import MouseButton
import os.path

class SequenceManager:
    def __init__(self,input_sequences : list[Sequence] = None):
        self.tmp_index=0
        self.total_index=0
        self.zoom_factor=0
        self.limit=Limit()
        
        if input_sequences is None:
            self.sequences=[]
        else:
            self.sequences=input_sequences

        self.max_range=1
        self.length_plot_window=self.max_range
        self.finished_sequences=[]
        self.addable_points=len(self.sequences)
        #TODO:refactor this stuff, can I do better?
        self.chosen_sequence=None
        self.chosen_data_object=None
        self.hover_sequence=None
        self.hover_data_object=None

    def add_sequence(self,data_objects,fname):
        sequence_name=os.path.basename(fname)
        new_sequence=Sequence(data_objects,sequence_name,create_color(len(data_objects)))#TODO:here instead color generator next call
        if len(self.sequences)==0:
            self.chosen_sequence=new_sequence
            self.hover_sequence=new_sequence
        self.sequences.append(new_sequence)
        self.addable_points+=1
        self.max_range=max(self.max_range,len(data_objects))
        self.catch_up(new_sequence, len(self.sequences)-1)
        self.set_plot_data_regarding_tmp_index()
        if len(self.sequences)==1:
            self.forwards()
        return
    
    def get_sequence_names(self):
        names=[sequence.name for sequence in self.sequences if not sequence.is_empty()]
        return names
        
    def get_sequence_representative_colors(self):
        colors=[sequence.representative_color for sequence in self.sequences if not sequence.is_empty()]
        return colors

    def catch_up(self,sequence, seq_index):
        for index in range(self.total_index):
            try:
                sequence.add_point()
            except StopIteration:
                self.finished_sequences.append(seq_index)
                self.addable_points-=1
                break

    def is_empty_plot(self) -> bool:
        for sequence in self.sequences:
            if not sequence.is_empty():
                return False
        return True
        
    def get_sequence_data(self,index:int):
        return self.sequences[index].get_curve_plot_data()
    
    def zoom_out(self):
        if self.zoom_factor==0 or self.is_empty_plot() or self.chosen_data_object is None:
            return
        tmp_zoom_factor=self.zoom_factor-1
        self.set_plot_data_regarding_tmp_index()
        for i in range(tmp_zoom_factor):
            self.zoom_in()
        self.zoom_factor=tmp_zoom_factor

    def zoom_reset(self):
        if self.zoom_factor==0 or self.is_empty_plot() or self.chosen_data_object is None:
            return
        self.zoom_factor=0
        self.set_plot_data_regarding_tmp_index()

    
    def zoom_in(self):#TODO:shorter
        if self.is_empty_plot() or self.chosen_data_object is None:
            return
        # radial zoom (because it's instinctive),
        # although it is possible to not show a border data point even if it would be in the cubic view
        empty=0
        for sequence in self.sequences:
            if sequence.is_empty():
                empty+=1
        if (empty==len(self.sequences)-1 and len(self.chosen_sequence.plot_data)==1) \
            or (self.limit.get_min()==self.chosen_data_object.limit.get_min() and self.limit.get_max()==self.chosen_data_object.limit.get_max()):#TODO:not enough if second sequence object in chosen_object
            return

        sq_dist_values=[]
        for index in range(len(self.sequences)):
            sequence=self.sequences[index]
            if not sequence.is_empty():
                value=sequence.get_max_squared_dist_value(self.chosen_data_object)
                sq_dist_values.append(value)
            else:
                sq_dist_values.append(-1)#default, since -1 is an impossible value
        max_value=max(sq_dist_values)
        if self.hover_data_object is not None and self.hover_index not in self.hover_sequence.scope:
            self.hover_data_object=None
            self.hover_index=None
            self.hover_sequence=None

        for index in range(len(self.sequences)):
            if not self.sequences[index].is_empty() and sq_dist_values[index]!=-1 and max_value==sq_dist_values[index]:
                self.sequences[index].apply_sequence_delete_list()
        self.zoom_factor+=1


    def backwards(self):
        if self.tmp_index>0:
            self.tmp_index=self.tmp_index-1
            self.set_plot_data_regarding_tmp_index()

    def forwards(self):#step
        if self.sequences == []:
            return
        if self.addable_points>0 or self.tmp_index<self.total_index:
            self.tmp_index+=1
            #!= to have the right behavior when we used backwards
            if self.tmp_index>self.total_index:
                self.addable_points-=self.add_point()
            self.set_plot_data_regarding_tmp_index()

    def add_point(self):  
        if self.addable_points>0:   
            stop_iteration_counter=0
            for index in range(len(self.sequences)):
                if index not in self.finished_sequences:
                    try:
                        self.sequences[index].add_point()
                    except StopIteration:
                        self.finished_sequences.append(index)
                        stop_iteration_counter+=1
            if self.sequences!=[] and len(self.finished_sequences)!=len(self.sequences):
                self.total_index+=1
            return stop_iteration_counter
        return 0

    def set_plot_data_regarding_tmp_index(self):
        self.limit.reset()
        for sequence in self.sequences:
            sequence.reset_to_actual_points(self.tmp_index, self.length_plot_window)

    def choose_sequence(self,event):#TODO:testing, shorter?
        index_chosen=int(round(event.xdata,0))
        if max(event.xdata,index_chosen)-min(event.xdata,index_chosen)>=0.5:
            return None,None
        min_dist=None
        chosen_sequence=None

        self.compute_dist_lines()#update before usage

        for line in self.dist_lines:
            xvals,yvals=self.dist_lines[line]["xs"],self.dist_lines[line]["ys"]
            if len(yvals)==0:
                print("yvals are not right (xvals,yvals)", xvals,yvals)
                continue
            else:
                y_index=None
                for i in range(len(xvals)):
                    if index_chosen==xvals[i]:
                        y_index=i
                        break
                if y_index==None:
                    continue
                yval=yvals[y_index]
                print("Yval and index",yval,y_index)
            current_abs=yval-event.ydata
            if yval < event.ydata:
                current_abs=event.ydata-yval
            
            if min_dist is None or min_dist>current_abs:
                min_dist=current_abs
                chosen_sequence=line
                y_index_star=y_index

        if min_dist is None or min_dist>=1:
            return None,None

        if event.button==MouseButton.LEFT:
            self.zoom_reset()
            self.set_chosen_object(chosen_sequence, y_index_star)
        else:
            self.set_hover_object(chosen_sequence,y_index_star)
    
    def set_chosen_object(self,chosen_sequence, index_chosen):
        if chosen_sequence is not None and index_chosen is not None:
            self.chosen_sequence=chosen_sequence
            self.chosen_data_object=self.chosen_sequence.data_objects[index_chosen]
            self.chosen_index=index_chosen

    def set_hover_object(self,hover_seq,index):

        if hover_seq is not None and index in hover_seq.scope:
            self.hover_sequence=hover_seq
            self.hover_data_object=self.hover_sequence.data_objects[index]
            self.hover_index=index
     
    def get_plot_data_3d(self):
        if self.is_empty_plot():
            return
        result=[]
        self.limit.reset()
        for index in range(len(self.sequences)):
            sequence=self.sequences[index]
            if sequence==self.chosen_sequence:
                if sequence==self.hover_sequence:
                    result.append(sequence.plot_sequence_data( [self.hover_data_object,self.chosen_data_object]))
                else:
                    result.append(sequence.plot_sequence_data( self.chosen_data_object))
            elif sequence==self.hover_sequence:
                result.append(sequence.plot_sequence_data( self.hover_data_object))
            else:
                result.append(sequence.plot_sequence_data())
            self.limit.correct_limits_limit(sequence.limit)#TODO:plot_sequence_data refresh the limits, this is too hidden, rename function
        return result

    def compute_dist_lines(self):
        if self.is_empty_plot():
            return
        self.dist_lines =dict()
        for index in range(len(self.sequences)):
            sequence=self.sequences[index]
            xvals,yvals=sequence.get_plot_sequence_distance_data(self.chosen_sequence)
            if xvals is not None and yvals is not None:
                self.dist_lines[sequence]={
                    "xs":xvals,
                    "ys":yvals,
                    "color":sequence.representative_color
                    }
   
    def get_scope_data(self):
        if self.dist_lines is None or len(self.dist_lines)==0:
            return None
        result={}
        for sequence in self.sequences:
            try:
                xvals=[self.dist_lines[sequence]["xs"][scope_index] for scope_index in sequence.scope]
                yvals=[self.dist_lines[sequence]["ys"][scope_index] for scope_index in sequence.scope]
                sequence_result={"xs":xvals,
                             "ys":yvals,
                             }
                result[sequence]=sequence_result
            except IndexError as e:
                #chosen sequence has ended
                print(e)

        return result


    def get_plot_distance_data(self):
        return self.dist_lines

    def get_chosen_data_object_3d(self):
        if self.chosen_data_object is not None:
            return self.chosen_data_object.get_plot_data_object('fuchsia')

    def get_chosen_data_object_distance(self):
        if self.chosen_data_object is not None:
            return self.chosen_index

    def get_hover_data_object_3d(self):
          if self.hover_data_object is not None:
            return self.hover_data_object.get_plot_data_object('aqua')

    def get_hover_data_object_distance(self):
        if self.hover_data_object is not None:
            if self.hover_index in self.hover_sequence.scope:
                if self.hover_index >=self.chosen_sequence.total_length:
                    return self.hover_index,-1.0
                return self.hover_index, \
                    math.sqrt(square_distance_between(self.chosen_sequence.data_objects[self.hover_index],self.hover_data_object))
            else:
                return None, None
        return None,None

    def jump_to_start(self):
        self.tmp_index=0
        self.set_plot_data_regarding_tmp_index()
        return

    def jump_to_end(self):
        if self.sequences == []:
            return
        while self.addable_points>0 or self.tmp_index<self.total_index:
                self.tmp_index+=1
                if self.tmp_index>self.total_index:
                    self.addable_points-=self.add_point()
        self.set_plot_data_regarding_tmp_index()
