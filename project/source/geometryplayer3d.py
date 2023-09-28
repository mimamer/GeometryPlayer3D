import matplotlib.pyplot as plt
import PySimpleGUI
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from source.sequence import Sequence
from source.sequencemanager import SequenceManager
from source.buttonevent import ButtonEvent

from matplotlib.backend_bases import MouseButton

matplotlib.use("TkAgg")#TODO:tkinter is needed
import warnings
warnings.filterwarnings("error")

from source.utils import get_new_lims

#import mpl_toolkits
#from mpl_toolkits.mplot3d.art3d import Line3DCollection

from PySimpleGUI import Button
#dynamisch mit rein tun, falls wert schon da nimm diesen....
class GeometryPlayer3D:
    """The GeometryPlayer3D Class builds the main window and delegates the processing of events. """
    def __init__(self,data_objects, data_objects2):
        
        self.switch=False
        self.fig=None
        self.ax=None

        self.figure_canvas_agg=None
        self.margins=None

        curves=[Sequence(data_objects),Sequence(data_objects2)]#later three_dimensional_player will not receive data_objects for curve this way
        length_data_objects=len(data_objects)
        self.length_plot_window=length_data_objects
        self.create_colors()

        self.curve_manager=SequenceManager(curves)
        self.previous_lim_change=None
        button_menu_reset=self.register_button_menu_events()
        button_list=[button_menu_reset]+self.register_button_events()
        #menu_def = [['File', ['Open', 'Save', 'Exit',]],
        #        ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
        #        ['Help', 'About...'],]
        
        self.root = PySimpleGUI.Window(title="3D Result Player", layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],[button_list]], finalize=True,element_justification='c')
        self.create_figure()
        self.draw_figure()
        self.register_mouse_events()


    def draw_figure(self):
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.root["-CANVAS-"].TKCanvas)
        self.figure_canvas_agg.draw()
        self.figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)


    def create_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d') #ax is a subplot
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
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

    def create_colors(self):
            self.colors=[]
            for cmap in ['Greys','Greens','Purples','Oranges', 'Blues']:#TODO:limits number of curves that can be visualized, cycle, use mod operator
                cmap=plt.get_cmap(cmap)
                colo=[]
                cmap_usable=int(cmap.N/3)
                col_abs=(cmap.N-cmap_usable)/self.length_plot_window # hier noch volles Fenster, dieses wird aber irgendwann verkleinert, schieberegler
                i=0
                while i*col_abs<=cmap.N-cmap_usable:
                    rgba=cmap(cmap_usable+int(i*col_abs))
                    colo.append(matplotlib.colors.rgb2hex(rgba))
                    i+=1
                self.colors.append(colo)
    def plot_curves_actual_plot_data(self):
        self.ax.cla() #clear ax
        
        # lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
        #                      linewidth=linewidth, alpha=alpha)

        for index in range(len(self.curve_manager.curves)):#cuboids has to be added seperately... see cuboids.py
            #this is kind of ugly
            curve_plot_data=self.curve_manager.get_curve_data(index)


            #TODO:only for testing, this is not pretty
            # here we can divide between scatter and add_collection3d
            if index<len(self.curve_manager.curve_plot):
                #also changes ax.plot
                self.curve_manager.curve_plot[index]=self.ax.scatter(xs=curve_plot_data[0], ys=curve_plot_data[1],  zs=curve_plot_data[2], depthshade=False, c=self.colors[index][:len(curve_plot_data[0])])#could use 3dline?
            else:#curve is not registered in plot data
                self.curve_manager.curve_plot.append(self.ax.scatter(xs=curve_plot_data[0], ys=curve_plot_data[1],  zs=curve_plot_data[2], depthshade=False,c=self.colors[index][:len(curve_plot_data[0])]))
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
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

    def jump_to_start(self):
        return
    def jump_to_end(self):
        return

                
    def press_switch(self):
        self.switch=not self.switch

    def register_button_menu_events(self):
        self.values=['x to front','-x to front','y to front','-y to front','z to front','-z to front']
        return PySimpleGUI.ButtonMenu('Reset View',
                    [self.values,
                    self.values],
                    border_width=2)#,background_color="gray"
    
    def trigger_button_menu_events(self,value):
        print("TRIGGERED")
        if value=='x to front':
            print("FRONT X")


    def register_button_events(self):

        self.events=[
            #ButtonEvent("Reset x",self.reset_x),
            ButtonEvent("\u23EE",self.jump_to_start),
            ButtonEvent("\u23F4",self.backwards),
            ButtonEvent("\u23EF",self.press_switch),
            ButtonEvent("\u23F5",self.forwards),
            ButtonEvent("\u23ED", self.jump_to_end),
            ButtonEvent("+",self.zoom_in),
            ButtonEvent("-",self.zoom_out)
            ]       
        button_list=[]
        for event in self.events:
            button_list.append(event.get_button())
        return button_list

    def trigger_button_events(self, event):
        for self_event in self.events:
            if self_event.event_name==event:
                self_event.trigger_command()
    
    

    def register_mouse_events(self):
        #binding_id = plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event', on_click)
        def on_press(event):
            if event.button=="up":
                #self.figure_canvas_agg.toolbar.zoom() does not work rectangle zoom since toolbar is none
                self.zoom_in()
            elif event.button=="down":
                self.zoom_out()
            pressed = self.ax.button_pressed
            self.ax.button_pressed = -1 # some value that doesn't make sense.
            coords = self.ax.format_coord(event.xdata, event.ydata) # coordinates string in the form x=value, y=value, z= value
            print("pressed, coords",coords)
            self.ax.button_pressed = pressed
            print('you pressed', event.button, event.xdata, event.ydata, event.x, event.y,self.ax.format_coord(event.x,event.y))
            
            print("mouseevent occured on the line", self.curve_manager.choose_curve(event))
        plt.connect('scroll_event', on_press)
        plt.connect('button_press_event', on_press)

    def create_main_window(self):

        while True:
            event, values = self.root.read(timeout=500)#returns lways the last triggered value, this is a problem.
            print(event)
            if hasattr(event,"button"):
                print("EVENT BUTTON", event.button)
            if values is not None and 0 in values.keys() and event==0:#leftclick on button menu, not use event.button this would be wrong...
                self.trigger_button_menu_events(values[0])
                print("EVENT",event,values[0])

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