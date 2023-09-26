from source.curve import Curve

class CurveManager:
    def __init__(self,curves : list[Curve] = None):
        
        self.chosen_curve=0
        self.chosen_point=0
        self.tmp_index=0
        self.total_index=0
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
        
    def get_curve_data(self,index):
        return self.curves[index].get_curve_plot_data()
    
    def adjust_data_points_for_zoom_delete_max(self):
        if self.is_empty_plot():#TODO: this case should not appear
            return
        print("FORCE NEW BOUNDS")
        #TODO:Cuboid may be not that optimal regarding usability, may change something here
        max_abs_x,meaning_x=self.curves[self.chosen_curve].get_max_abs_value_x_axis()
        max_abs_y,meaning_y=self.curves[self.chosen_curve].get_max_abs_value_y_axis()
        max_abs_z,meaning_z=self.curves[self.chosen_curve].get_max_abs_value_z_axis()

        for curve in self.curves:
            curve.set_plot_data_to_cuboid(max_abs_x,meaning_x,max_abs_y,meaning_y,max_abs_z,meaning_z)
        print("FORCE NEW BOUNDS--END")

    def forwards(self):
        self.step()

    def backwards(self):
        if self.tmp_index>0:
            self.tmp_index=self.tmp_index-1
            self.set_plot_data_regarding_tmp_index()

    def step(self):
        if self.tmp_index>self.total_index:
            self.add_point()
            #sache mit den Quadern fehlt noch...
        self.set_plot_data_regarding_tmp_index()
        
        self.tmp_index+=1

    def add_point(self):
        for curve in self.curves:
            curve.add_point()
        self.total_index+=1

    def set_plot_data_regarding_tmp_index(self):
        for curve in self.curves:
            curve.reset_to_actual_points(self.tmp_index)