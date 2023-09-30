from source.sequence import Sequence

class SequenceManager:
    def __init__(self,curves : list[Sequence] = None):
        self.tmp_index=0
        self.total_index=0
        self.plot_data=[]#all plot data of sequences
        
        if curves is None:
            self.curves=[]
        else:
            self.curves=curves
        

    def adjust_data_points_for_zoom(self,lim_x,lim_y,lim_z):
        for curve in self.curves:
            curve.adjust_data_points_for_zoom(lim_x,lim_y,lim_z)


    def is_empty_plot(self):
        for curve in self.curves:
            if not curve.is_empty():
                return False
        return True
        
    def get_sequence_data(self,index):
        return self.curves[index].get_curve_plot_data()
    
    def adjust_data_points_for_zoom_delete_max(self):
        if self.is_empty_plot():#TODO: this case should not appear
            return
        print("FORCE NEW BOUNDS")
        #TODO:Cuboid may be not that optimal regarding usability, may change something here
        #later better
        self.chosen_curve=self.curves[0]
        self.chosen_point=[self.chosen_curve.x[0],self.chosen_curve.y[0],self.chosen_curve.z[0]]
        max_abs_value_x=self.chosen_curve.get_max_abs_value_x_axis(self.chosen_point)
        max_abs_value_y=self.chosen_curve.get_max_abs_value_y_axis(self.chosen_point)
        max_abs_value_z=self.chosen_curve.get_max_abs_value_z_axis(self.chosen_point)

        max_abs_value=0
        axis=-1
        if abs(max_abs_value_x)>abs(max_abs_value_y) and abs(max_abs_value_x)>abs(max_abs_value_z):
            max_abs_value=max_abs_value_x
            axis=0
        elif abs(max_abs_value_y)>abs(max_abs_value_x) and abs(max_abs_value_y)>abs(max_abs_value_z):
            max_abs_value=max_abs_value_y
            axis=1
        elif abs(max_abs_value_z)>abs(max_abs_value_x) and abs(max_abs_value_z)>abs(max_abs_value_y):
            max_abs_value=max_abs_value_z
            axis=2

        #Try to zoom only in one dimension 
        # take the max abs value of the three axis, the others will be incrememted by one, such that they will not filter values -> not fast enough
        # sort only after the biggest axis

        for curve in self.curves:
            curve.set_plot_data_to_cuboid(max_abs_value,self.chosen_point,axis)
        print("FORCE NEW BOUNDS--END")


    def backwards(self):
        if self.tmp_index>0:
            self.tmp_index=self.tmp_index-1
            self.set_plot_data_regarding_tmp_index()

    def forwards(self):#step
        if self.curves != []:
            self.tmp_index+=1
            #!= to have the right behavior when we used backwards
            if self.tmp_index>self.total_index:
                self.add_point()
                #sache mit den Quadern fehlt noch...
            self.set_plot_data_regarding_tmp_index()
            
            
    def add_point(self):
        for curve in self.curves:
            curve.add_point()
        if self.curves!=[]:
            self.total_index+=1

    def set_plot_data_regarding_tmp_index(self):
        for curve in self.curves:
            curve.reset_to_actual_points(self.tmp_index)

    def choose_sequence(self,event):
        for index in range(len(self.plot_data)):
            print(self.plot_data[index])
            test=(self.plot_data[index].contains(event))#TODO:does not work :( only with Line2D
            if(test):
                self.chosen_curve=index
                return index
            
    def set_actual_plot_data(self,ax,colors):
        for index in range(len(self.curves)):#cuboids has to be added seperately... see cuboids.py
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
