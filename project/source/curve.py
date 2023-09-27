class Curve:
    def __init__(self, data_objects):
        self.plot_data=None
        self.x=[]
        self.y=[]
        self.z=[]
        self.gen  = self.next_value(data_objects)

    def reset_to_actual_points(self,tmp_index):
        self.plot_data=[self.x[:tmp_index],self.y[:tmp_index],self.z[:tmp_index] ]

    def adjust_data_points_for_zoom(self, lim_x,lim_y,lim_z):
        xvals=[]
        yvals=[]
        zvals=[]

        for i in range(len(self.z)):
            if self.x[i]>=lim_x[0] and self.x[i]<=lim_x[1] \
                and self.y[i]>=lim_y[0] and self.y[i]<=lim_y[1] \
                and self.z[i]>=lim_z[0] and self.z[i]<=lim_z[1]:
                        xvals.append(self.x[i])
                        yvals.append(self.y[i])
                        zvals.append(self.z[i])
        self.plot_data=[xvals,yvals,zvals]
    
    def add_point(self):
        data_object = next(self.gen)
        self.x.append(data_object[0])
        self.y.append(data_object[1])
        self.z.append(data_object[2])

    def next_value(self,data_objects):
        for i in range(len(data_objects)):
            try:
                if len(data_objects[i])==1:
                    yield data_objects[i][0]
                elif len(data_objects[i])==8:
                    print("CUBOID")
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
    
    def get_max_abs_value(self,axis,chosen_point):
        plot_axis_values=[self.plot_data[axis][i]-chosen_point[axis] for i in range(len(self.plot_data[axis]))]
        max_value=max(plot_axis_values)#TODO:minus chosen data point -> this one transforms to zero then, chosen point is the first here
        min_value=min(plot_axis_values)
        value=max(abs(max_value),abs(min_value))
        return value
        #if value==abs(max_value) and value==abs(min_value):
        #    return max_value, "both"
        #if value==abs(max_value):
        #    return max_value,"+"
        #return min_value, "-"

    def get_max_abs_value_x_axis(self,chosen_point):
        return self.get_max_abs_value(0,chosen_point)
    
    def get_max_abs_value_y_axis(self,chosen_point):
        return self.get_max_abs_value(1,chosen_point)
    
    def get_max_abs_value_z_axis(self,chosen_point):
        return self.get_max_abs_value(2,chosen_point)
    

    def set_plot_data_to_cuboid(self,max_abs_value,chosen_point,axis):
        print("KURVE HAT DATEN ERHALTEN:",max_abs_value,chosen_point,axis)
        xvals=[]
        yvals=[]
        zvals=[]
        for i in range(len(self.plot_data[0])):
            if self.plot_data[axis][i]>=chosen_point[axis]:
                start=chosen_point[axis]
                end=self.plot_data[axis][i]
            else:
                end=chosen_point[axis]
                start=self.plot_data[axis][i]
            if end-start>=max_abs_value:##TODO: killt natürlich richtiges rauszoomen...
                continue
            xvals.append(self.plot_data[0][i])
            yvals.append(self.plot_data[1][i])
            zvals.append(self.plot_data[2][i])
        self.plot_data=[xvals,yvals,zvals]
            #nur das zusammenverbinden, was auch schon in x,y,z zusammen stand
            #bei rauszoomen statt abschneiden wieder dazunehmen bis alle drin sind. also immer das nächstgelegene finden...
            # if current_max<aktuelles elem and aktuelles elem < nächstgelegenes:
            #    nächstgelegen=aktuelles elem -> was bedeutet das im 3D-Raum? SUche für jede Richtung im Raum den nächstgelegenen? -> nicht-lineare zoomen...
            #macht wahrscheinlich in dieser anwendung am meisten sinn, da wir hier Datenpunkte haben, die Linien sind nur SIchthilfen und nicht 'richtig' errechnet.