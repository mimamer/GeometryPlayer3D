from source.sequence import Sequence

class SequenceManager:
    def __init__(self,curves : list[Sequence] = None):
        self.tmp_index=0
        self.total_index=0
        self.plot_data=[]#all plot data of sequences
        
        if curves is None:
            self.sequences=[]
        else:
            self.sequences=curves
        


    def is_empty_plot(self):
        for curve in self.sequences:
            if not curve.is_empty():
                return False
        return True
        
    def get_sequence_data(self,index):
        return self.sequences[index].get_curve_plot_data()
    
    def adjust_data_points_for_zoom_delete_max(self):
        if self.is_empty_plot():#TODO: this case should not appear
            return
        #TODO:Cuboid may be not that optimal regarding usability, may change something here
        #later better
        self.chosen_curve=self.sequences[0]
        self.chosen_point=[self.chosen_curve.x[0],self.chosen_curve.y[0],self.chosen_curve.z[0]]
        sq_dist_values=[]
        for index in range(len(self.sequences)):
            sequence=self.sequences[index]
            if not sequence.is_empty():
                value=sequence.get_max_squared_dist_value(self.chosen_point)
                sq_dist_values.append(value)
        max_value=max(sq_dist_values)
        for index in range(len(self.sequences)):
            if not self.sequences[index].is_empty() and max_value==sq_dist_values[index]:
                self.sequences[index].set_plot_data_to_radius()#TODO:rename?


    def backwards(self):
        if self.tmp_index>0:
            self.tmp_index=self.tmp_index-1
            self.set_plot_data_regarding_tmp_index()

    def forwards(self):#step
        if self.sequences != []:
            self.tmp_index+=1
            #!= to have the right behavior when we used backwards
            if self.tmp_index>self.total_index:
                self.add_point()
                #sache mit den Quadern fehlt noch...
            self.set_plot_data_regarding_tmp_index()
            
            
    def add_point(self):
        for curve in self.sequences:
            curve.add_point()
        if self.sequences!=[]:
            self.total_index+=1

    def set_plot_data_regarding_tmp_index(self):
        for curve in self.sequences:
            curve.reset_to_actual_points(self.tmp_index)

    def choose_sequence(self,event):
        for index in range(len(self.plot_data)):
            print(self.plot_data[index])
            test=(self.plot_data[index].contains(event))#TODO:does not work :( only with Line2D
            if(test):
                self.chosen_curve=index
                return index
            
    def set_actual_plot_data(self,ax,colors):
        if self.is_empty_plot():
            return
        for index in range(len(self.sequences)):#cuboids has to be added seperately... see cuboids.py
                #this is kind of ugly
                curve_plot_data=self.get_sequence_data(index)
                #TODO:only for testing, this is not pretty
                # here we can divide between scatter and add_collection3d
                if index<len(self.plot_data):
                    #also changes ax.plot
                    self.plot_data[index]=ax.scatter(xs=curve_plot_data[0], ys=curve_plot_data[1],  zs=curve_plot_data[2], depthshade=False, c=colors[index][:len(curve_plot_data[0])])#could use 3dline?
                else:#curve is not registered in plot data
                    self.plot_data.append(ax.scatter(xs=curve_plot_data[0], ys=curve_plot_data[1],  zs=curve_plot_data[2], depthshade=False,c=colors[index][:len(curve_plot_data[0])]))


    def jump_to_start(self):
        return
    def jump_to_end(self):
        return
