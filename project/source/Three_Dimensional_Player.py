import matplotlib.pyplot as plt
import PySimpleGUI
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from source.Three_Dimensional_Curve import Three_Dimensional_Curve
from source.Curve_Manager import Curve_Manager
from source.Button_Event import Button_Event

from matplotlib.backend_bases import MouseButton

matplotlib.use("TkAgg")
import warnings
warnings.filterwarnings("error")

from source.player_utils import get_new_lims


#dynamisch mit rein tun, falls wert schon da nimm diesen....
class Three_Dimensional_Player:
    def __init__(self,data_objects):
        
        self.switch=False
        self.fig=None
        self.ax=None
        self.figure_canvas_agg=None
        self.margins=None

        curves=[Three_Dimensional_Curve(data_objects)]#later three_dimensional_player will not receive data_objects for curve this way

        self.curve_manager=Curve_Manager(curves)
        self.previous_lim_change=None

        button_list=self.register_button_events()
        
        self.root = PySimpleGUI.Window(title="3D Result Player", layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],button_list], finalize=True)
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
        self.curve_manager.adjust_data_points_for_zoom(lim_x,lim_y,lim_z)
        self.plot_curves_actual_plot_data()

    def plot_curves_actual_plot_data(self):
        self.ax.cla() #clear ax
        for index in range(len(self.curve_manager.curves)):
            curve_plot_data=self.curve_manager.get_curve_data(index)
            self.ax.plot(curve_plot_data[0], curve_plot_data[1],  curve_plot_data[2],marker="o", markersize=5)
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
                self.curve_manager.adjust_data_points_for_zoom_delete_max()
                self.plot_curves_actual_plot_data()
            else:
                print("USERWARNING",e)
                lim_x=get_new_lims(lim_tuple=previous_x_lim)
                lim_y=get_new_lims(lim_tuple=previous_y_lim)
                lim_z=get_new_lims(lim_tuple=previous_z_lim)
                self.adjust_data_points_for_zoom(lim_x,lim_y,lim_z)
                pass

    def zoom(self, zoom_value):
        #TODO: catch None Case (no points at the beginning)
        try:
            print(self.margins)
            self.margins=(self.margins[0]+zoom_value,self.margins[1]+zoom_value,self.margins[2]+zoom_value)
            self.plot_curves_actual_plot_data()
        except ValueError: #only for zoom_in ValueError
            self.margins=(-0.49,-0.49,-0.49)
            self.plot_curves_actual_plot_data()

    def zoom_out(self):
        self.zoom(0.01)

    def zoom_in(self):
        self.zoom(-0.01)
        self.set_new_lims()
    
    def run_figure(self):
        if self.switch:
            self.curve_manager.step()
            self.plot_curves_actual_plot_data()


    def backwards(self):
        self.switch=False
        self.curve_manager.backwards()
        self.plot_curves_actual_plot_data()
    
    def forwards(self):
        self.switch=False
        self.curve_manager.forwards()
        self.plot_curves_actual_plot_data()

                
    def press_switch(self):
        self.switch=not self.switch

    def register_button_events(self):
        self.events=[Button_Event("<",self.backwards),
                Button_Event("Play/Pause",self.press_switch),
                Button_Event(">",self.forwards),
                Button_Event("+",self.zoom_in),
                Button_Event("-",self.zoom_out)]
        button_list=[]
        for event in self.events:
            button_list.append(event.get_button())
        return button_list

    def trigger_button_events(self, event):
        for self_event in self.events:
            if self_event.event_name==event:
                self_event.trigger_command()

    def create_main_window(self):

        #binding_id = plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event', on_click)
        def on_press(event):
            if event.button=="up":
                #self.figure_canvas_agg.toolbar.zoom() does not work rectangle zoom since toolbar is none
                self.zoom_in()
            elif event.button=="down":
                self.zoom_out()
            print('you pressed', event.button, event.xdata, event.ydata, event.x, event.y,self.ax.format_coord(None,None))
            
        plt.connect('scroll_event', on_press)
        plt.connect('button_press_event', on_press)

        while True:
            event, values = self.root.read(timeout=1000)

            if event == PySimpleGUI.WIN_CLOSED:
                break
            self.trigger_button_events(event)
            if self.switch:
                self.run_figure()

        self.root.close()

def on_move(event):
    if event.inaxes:
        print(f'data coords {event.xdata} {event.ydata} {event.zdata},',
              f'pixel coords {event.x} {event.y}')
def on_click(event):
    if event.button is MouseButton.MIDDLE:
        print('hi')


