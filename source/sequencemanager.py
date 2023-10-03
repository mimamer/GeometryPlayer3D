from source.sequence import Sequence

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
        


    def is_empty_plot(self):
        for curve in self.sequences:
            if not curve.is_empty():
                return False
        return True
        
    def get_sequence_data(self,index):
        return self.sequences[index].get_curve_plot_data()
    
    def zoom_out(self):
        if self.is_empty_plot():
            return
        self.zoom_factor-=1
        self.set_plot_data_regarding_tmp_index()
        for i in range(self.zoom_factor):
            self.zoom()

    def zoom_in(self):
        if self.is_empty_plot():
            return
        self.zoom_factor+=1
        self.zoom()
    
    def zoom(self):
        if self.is_empty_plot():#TODO: this case should not appear
            return
        # radial zoom (because it's instinctive),
        # although it is possible to not show a border data point even if it would be in the cubic view
        self.chosen_sequence=self.sequences[0]
        self.chosen_data_object=self.chosen_sequence.data_objects[0]
        sq_dist_values=[]
        for index in range(len(self.sequences)):
            sequence=self.sequences[index]
            if not sequence.is_empty():
                value=sequence.get_max_squared_dist_value(self.chosen_data_object)
                sq_dist_values.append(value)
        max_value=max(sq_dist_values)
        for index in range(len(self.sequences)):
            if not self.sequences[index].is_empty() and max_value==sq_dist_values[index]:
                self.sequences[index].set_plot_data_to_radius()#TODO:rename?


    def backwards(self):#TODO:what if sequences have different lenght
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
                #sache mit den Quadern fehlt noch...
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
        return
        #for index in range(len(self.plot_data)):
        #    print(self.plot_data[index])
        #    test=(self.plot_data[index].contains(event))#TODO:does not work :( only with Line2D
        #    if(test):
        #        self.chosen_sequence=index
        #        return index
            
    def set_actual_plot_data(self,ax,colors):
        if self.is_empty_plot():
            return
        for index in range(len(self.sequences)):
                sequence=self.sequences[index]
                sequence.plot_sequence_data(ax,colors[index])


    def jump_to_start(self):
        return

    def jump_to_end(self):
        if self.sequences == []:
            return
        while self.addable_points>0 or self.tmp_index<self.total_index:
                self.tmp_index+=1
                #!= to have the right behavior when we used backwards
                if self.tmp_index>self.total_index:
                    self.addable_points-=self.add_point()
        self.set_plot_data_regarding_tmp_index()
