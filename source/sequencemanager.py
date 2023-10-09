from source.sequence import Sequence
from matplotlib.lines import Line2D
import math
from source.dataobject import square_distance_between
class SequenceManager:
    def __init__(self,curves : list[Sequence] = None):
        self.tmp_index=0
        self.total_index=0
        self.zoom_factor=0
        
        if curves is None:
            self.sequences=[]
        else:
            self.sequences=curves
        self.finished_sequences=[]
        self.addable_points=len(self.sequences)
        #TODO:refactor this stuff
        self.chosen_sequence=self.sequences[0]
        self.chosen_data_object=None#self.chosen_sequence.data_objects[2]
        self.hover_sequence_index=self.sequences[0]
        self.hover_data_object=None#self.chosen_sequence.data_objects[2]

    def is_empty_plot(self) -> bool:
        for curve in self.sequences:
            if not curve.is_empty():
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

    
    def zoom_in(self):
        if self.is_empty_plot() or self.chosen_data_object is None:
            return

        # radial zoom (because it's instinctive),
        # although it is possible to not show a border data point even if it would be in the cubic view
        empty=0
        for sequence in self.sequences:
            if sequence.is_empty():
                empty+=1

        if empty==len(self.sequences)-1 and len(self.chosen_sequence.plot_data)==1:
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
        if self.hover_data_object is not None:#TODO:hover data object is reset to none, may not pretty
            self.hover_data_object=None
            self.hover_index=None
            self.hover_sequence_index=None

        for index in range(len(self.sequences)):
            if not self.sequences[index].is_empty() and sq_dist_values[index]!=-1 and max_value==sq_dist_values[index]:
                self.sequences[index].set_plot_data_to_radius()#TODO:rename?
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
        for curve in self.sequences:
            curve.reset_to_actual_points(self.tmp_index)

    def choose_sequence(self,event):
        index_chosen=int(round(event.xdata,0))
        if max(event.xdata,index_chosen)-min(event.xdata,index_chosen)>=0.5:
            return None,None
        min_dist=None
        chosen_sequence=None

        for index in range(len(self.abs_line)):#TODO: yvals are a real problem here, often out of range  (cuboid chosen, etc.)
            xvals,yvals=self.abs_line[index].get_data()[0],self.abs_line[index].get_data()[1]
            print(xvals,yvals)
            if yvals.size==0:#TODO:could be a probem if only one is left
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
                chosen_sequence=index
                y_index_star=y_index

        if min_dist is None or min_dist>=0.5:
            return None,None, None
        return chosen_sequence, y_index_star
    
    def set_chosen_object(self,chosen_sequence, index_chosen):
        if chosen_sequence is not None and index_chosen is not None:
            self.chosen_sequence=self.sequences[chosen_sequence]
            self.chosen_data_object=self.chosen_sequence.data_objects[index_chosen]#one can choose a not visible object...
            self.chosen_index=index_chosen

    def set_hover_object(self,hover_seq,index):
        if hover_seq is not None:
            self.hover_sequence_index=hover_seq
            self.hover_data_object=self.sequences[hover_seq].data_objects[index]#one can choose a not visible object...
            self.hover_index=index

            
    def set_actual_plot_data_3d(self,ax,colors):
        if self.is_empty_plot():
            return
        for index in range(len(self.sequences)):
                sequence=self.sequences[index]
                sequence.plot_sequence_data(ax,colors[index])

    def set_actual_plot_distance_data(self,abs_plot,colors):
        if self.is_empty_plot():
            return
        self.abs_line : list[Line2D]=list()
        for index in range(len(self.sequences)):
                sequence=self.sequences[index]
                #TODO:next function is ugly
                line2d:Line2D=sequence.plot_sequence_abs_data(abs_plot,self.chosen_sequence,colors[index][int(len(colors[index])/2)])[0]
                self.abs_line.append(line2d)

    def set_actual_chosen_data_object_3d(self,ax):
        if self.chosen_data_object is not None:
            self.chosen_data_object.plot_data_object(ax,'fuchsia', markersize=10)

    def set_actual_chosen_data_object_distance(self,abs_plot):
        if self.chosen_data_object is not None:
            abs_plot.plot(self.chosen_index,0, marker="o", c='fuchsia')

    def set_actual_hover_data_object_3d(self,ax):
          if self.hover_data_object is not None:
            self.hover_data_object.plot_data_object(ax,'aqua', markersize=10)#TODO return make it a getter?

    def set_actual_hover_data_object_distance(self,abs_plot):
        if self.hover_data_object is not None:
            abs_plot.plot(self.hover_index,
                        math.sqrt(square_distance_between(self.chosen_sequence.plot_data[self.hover_index],self.hover_data_object)),
                        marker="o", c='aqua')

    def jump_to_start(self):
        return

    def jump_to_end(self):
        if self.sequences == []:
            return
        while self.addable_points>0 or self.tmp_index<self.total_index:
                self.tmp_index+=1
                if self.tmp_index>self.total_index:
                    self.addable_points-=self.add_point()
        self.set_plot_data_regarding_tmp_index()
