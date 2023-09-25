import matplotlib.pyplot as plt
import PySimpleGUI
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from mpl_toolkits.mplot3d.art3d import Line3D
from matplotlib.backend_bases import MouseButton

matplotlib.use("TkAgg")
import warnings
warnings.filterwarnings("error")

from player_utils import get_new_lims


#dynamisch mit rein tun, falls wert schon da nimm diesen....
class Three_Dimensional_Player:
    def __init__(self):
        self.switch=False
        self.fig=None
        self.ax=None
        self.gen=None
        self.figure_canvas_agg=None
        
        self.x=[]
        self.y=[]
        self.z=[]

        self.previous_lim_change=None
        self.plot_data=None

        self.line=None
        self.index=0
        self.tmp_index=0
        play_button = PySimpleGUI.Button('Play/Pause')
        back_button = PySimpleGUI.Button('<')
        forward_button = PySimpleGUI.Button('>')
        zoom_in_button = PySimpleGUI.Button('+')
        zoom_out_button = PySimpleGUI.Button('-')
        self.margins=None
        self.root = PySimpleGUI.Window(title="3D Result Player", layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],[back_button, play_button, forward_button, zoom_in_button,zoom_out_button]], finalize=True)
        self.create_figure()
        self.draw_figure()


    def draw_figure(self):
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.root["-CANVAS-"].TKCanvas)
        self.figure_canvas_agg.draw()
        self.figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)


    def create_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d') #ax is a subplot
        #self.ax.set_zlim(-1, 1)
        self.ax.use_sticky_edges=False
        self.margins=self.ax.margins()


    
    def set_lims(self, lim_x,lim_y,lim_z):#if here not a lim arrives we need to adjust throw USERWARNING
        print("SET NEW LIMS", lim_x,lim_y,lim_z)
        if self.previous_lim_change==[lim_x,lim_y,lim_z]:
            raise UserWarning("CHANGE DID NOT SUCCEED")
        self.ax.set_xlim(lim_x[0],lim_x[1])
        self.ax.set_ylim(lim_y[0],lim_y[1])
        self.ax.set_zlim(lim_z[0],lim_z[1])
        self.previous_lim_change=[lim_x,lim_y,lim_z]

    def adjust_data_points_for_zoom(self,lim_x,lim_y,lim_z): #TODO : zoom to point, center this point first then zoom in
        #corrupt
        print("ADJUST")
        xvals=[]
        yvals=[]
        zvals=[]
        print("BOUNDARIES", lim_x,lim_y,lim_z)
        for i in range(len(self.z)):
            if self.x[i]>=lim_x[0] and self.x[i]<=lim_x[1]:
                if self.y[i]>=lim_y[0] and self.y[i]<=lim_y[1]:
                    if self.z[i]>=lim_z[0] and self.z[i]<=lim_z[1]:
                        xvals.append(self.x[i])
                        yvals.append(self.y[i])
                        zvals.append(self.z[i])
        
        self.ax.cla() #clear ax
        self.Line=None
        self.line=Line3D(xvals,yvals,zvals)
        self.plot_data=self.line.get_data_3d()
        self.ax.plot(self.plot_data[0], self.plot_data[1],  self.plot_data[2],marker="o", markersize=5)
        self.ax.use_sticky_edges=False # can not zoom in adequately
        self.ax.margins(self.margins[0],self.margins[1],self.margins[2])
        self.figure_canvas_agg.draw_idle()

    def adjust_data_points_for_zoom_delete_max(self):
        #corrupt
        print("ADJUST2", self.plot_data)

        if len(self.plot_data[0])==0:#dazu sollte es wenn möglich nicht kommen, for-Schleife weiter unten anders
            return

        max_x=max(self.plot_data[0])#nicht abs..., d.h. bevorzugt wird auf untere elems gezoomt
        max_y=max(self.plot_data[1])
        max_z=max(self.plot_data[2])

        print("MAX",max_x,max_y,max_z)

        xvals=[]
        yvals=[]
        zvals=[]
        for i in range(len(self.plot_data[0])):
            if self.plot_data[0][i]==max_x or self.plot_data[1][i]==max_y or self.plot_data[2][i]==max_z:##TODO: killt natürlich richtiges rauszoomen...
                continue
            xvals.append(self.plot_data[0][i])
            yvals.append(self.plot_data[1][i])
            zvals.append(self.plot_data[2][i])
            #nur das zusammenverbinden, was auch schon in x,y,z zusammen stand
            #bei rauszoomen statt abschneiden wieder dazunehmen bis alle drin sind. also immer das nächstgelegene finden...
            # if current_max<aktuelles elem and aktuelles elem < nächstgelegenes:
            #    nächstgelegen=aktuelles elem -> was bedeutet das im 3D-Raum? SUche für jede Richtung im Raum den nächstgelegenen? -> nicht-lineare zoomen...
            #macht wahrscheinlich in dieser anwendung am meisten sinn, da wir hier Datenpunkte haben, die Linien sind nur SIchthilfen und nicht 'richtig' errechnet.
        print("REST:",xvals,yvals,zvals, len(xvals))
        self.ax.cla() #clear ax
        self.line=None
        self.line=Line3D(xvals,yvals,zvals)
        self.plot_data=(xvals,yvals,zvals)
        print("PLOT_DATA",self.plot_data)
        self.ax.plot(self.plot_data[0], self.plot_data[1],  self.plot_data[2],marker="o", markersize=5)
        self.ax.use_sticky_edges=False # can not zoom in adequately
        self.ax.margins(self.margins[0],self.margins[1],self.margins[2])
        self.figure_canvas_agg.draw_idle()


    def set_new_lims(self):
        #again not fixed zoom in, UserWarning automatically expanding does occur instantly,
        # maybe choose a point in the chain and zoom to it, due to cut away data points
        #corrupt
        previous_x_lim=self.ax.get_xlim()
        previous_y_lim=self.ax.get_ylim()
        previous_z_lim=self.ax.get_zlim()
        lim_x=(0,0) 
        lim_y=(0,0) 
        lim_z=(0,0)
        lim_x=get_new_lims(lim_tuple=previous_x_lim)
        lim_y=get_new_lims(lim_tuple=previous_y_lim)
        lim_z=get_new_lims(lim_tuple=previous_z_lim)

        try:
            if lim_x==previous_x_lim and lim_y==previous_y_lim and lim_z==previous_z_lim:
                self.adjust_data_points_for_zoom(lim_x,lim_y,lim_z)
            else:
                self.set_lims(lim_x,lim_y,lim_z)

        except UserWarning as e:
            if str(e)=="CHANGE DID NOT SUCCEED":
                print("CASE ADJUST 2")
                self.adjust_data_points_for_zoom_delete_max()
            else:
                print("USERWARNING",e)
                lim_x=get_new_lims(lim_tuple=previous_x_lim)
                lim_y=get_new_lims(lim_tuple=previous_y_lim)
                lim_z=get_new_lims(lim_tuple=previous_z_lim)
                self.adjust_data_points_for_zoom(lim_x,lim_y,lim_z)
                pass

    def zoom(self, zoom_value):
        try:
            print(self.margins)
            self.margins=(self.margins[0]+zoom_value,self.margins[1]+zoom_value,self.margins[2]+zoom_value)
            self.plot_actual_data()
        except ValueError: #only for zoom_in ValueError
            self.margins=(-0.49,-0.49,-0.49)
            self.plot_actual_data()

    def zoom_out(self):
        self.zoom(0.01)

    def zoom_in(self):
        self.zoom(-0.01)
        self.set_new_lims()
        
        
    def plot_actual_data(self):
        self.ax.cla() #clear ax
        self.ax.plot(self.plot_data[0], self.plot_data[1],  self.plot_data[2],marker="o", markersize=5)
        self.ax.use_sticky_edges=False # can not zoom in adequately
        self.ax.margins(self.margins[0],self.margins[1],self.margins[2])
        self.figure_canvas_agg.draw_idle()


    def run_figure(self):
        if self.switch:
            if self.tmp_index>self.index:
                data_object = next(self.gen)
                self.x.append(data_object[0][0])
                self.y.append(data_object[0][1])
                self.z.append(data_object[0][2])
                self.index+=1
                #sache mit den Quadern fehlt noch...
            self.line=Line3D(self.x[:self.tmp_index],self.y[:self.tmp_index],self.z[:self.tmp_index])
            self.plot_data=self.line.get_data_3d()
            self.plot_actual_data()
            self.tmp_index+=1


    def backwards(self):
        if self.tmp_index>0:
            self.tmp_index=self.tmp_index-1
            self.plot_actual_data()
    
    def forwards(self):
        if self.tmp_index<self.index:
            self.tmp_index=self.tmp_index+1
            self.plot_actual_data()
        else:
            tmp=self.switch
            self.switch=True
            self.run_figure()
            self.switch=tmp


    def next_value(self,data_objects):
        for i in range(len(data_objects)):
            try:
                yield data_objects[i]

            except StopIteration:
                break

                
    def pause_figure(self):
        self.switch=not self.switch

    def trigger_events(self, event):
        if event == "Play/Pause":
                self.pause_figure()
        if event == "<":
            self.switch=False
            self.backwards()

        if event == ">":
            self.switch=False
            self.forwards()

        if event =="+":
            self.switch=False
            self.zoom_in()
        if event =="-":
            self.switch=False
            self.zoom_out()

        if self.switch:
            self.run_figure()

    def create_main_window(self):

        #binding_id = plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event', on_click)
        def on_press(event):
            if event.button=="up":
                #self.figure_canvas_agg.toolbar.zoom() does not work rectangle zoom since toolbar is none
                self.zoom_in()
            elif event.button=="down":
                self.zoom_out()
            print('you pressed', event.button, event.xdata, event.ydata)
            
        plt.connect('scroll_event', on_press)
        plt.connect('button_press_event', on_press)

        while True:
            event, values = self.root.read(timeout=1000)

            if event == PySimpleGUI.WIN_CLOSED:
                break
            self.trigger_events(event)

        self.root.close()

def on_move(event):
    if event.inaxes:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')
def on_click(event):
    if event.button is MouseButton.MIDDLE:
        print('hi')


