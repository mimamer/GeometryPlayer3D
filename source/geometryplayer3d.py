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

from source.utils import get_new_lims, create_colors

class GeometryPlayer3D:
    """The GeometryPlayer3D Class builds the main window and delegates the processing of events. """
    def __init__(self,data_objects, data_objects2):
        
        self.switch=False

        self.fig=None
        self.ax=None
        self.figure_canvas_agg=None
        self.zoom_factor=0
        self.zoom_step=0.01

        self.length_plot_window=len(data_objects)#TODO:only temporary
        self.colors=create_colors(self.length_plot_window)

        curves=[Sequence(data_objects),Sequence(data_objects2)]#later three_dimensional_player will not receive data_objects for curve this way
        self.sequence_manager=SequenceManager(curves)
        self.previous_lim_change=None
        button_menu_reset=self.register_button_menu_events()
        button_list=[button_menu_reset]+self.register_button_events()
        #menu_def = [['File', ['Open', 'Save', 'Exit',]],
        #        ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
        #        ['Help', 'About...'],]
        
        self.root = PySimpleGUI.Window(title="3D Result Player", layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],[button_list]], finalize=True,element_justification='c')
        self.create_figure()
        self.register_mouse_events()

    def create_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d') #ax is a subplot
        self.default_ax_setting()
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.root["-CANVAS-"].TKCanvas)
        self.figure_canvas_agg.draw()
        self.figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)

    def default_ax_setting(self):
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.use_sticky_edges=False # can not zoom in adequately
    
    def set_actual_plot(self):
        self.ax.cla() #clear ax
        self.sequence_manager.set_actual_plot_data(self.ax, self.colors)
        self.default_ax_setting()
        self.figure_canvas_agg.draw_idle()#TODO:necesary?


    def zoom(self):#zoom should keep view angle, even when adjust is necessary
        self.sequence_manager.adjust_data_points_for_zoom_delete_max()


    def zoom_out(self):
        if self.sequence_manager.is_empty_plot():
            return
        self.zoom_factor-=1
        self.sequence_manager.set_plot_data_regarding_tmp_index()
        for i in range(self.zoom_factor):
            self.zoom()

    def zoom_in(self):
        if self.sequence_manager.is_empty_plot():
            return
        self.zoom_factor+=1
        self.zoom()
    
    def run_figure(self):
        if self.switch:
            self.sequence_manager.forwards()
            self.set_actual_plot()
   
    def press_switch(self):
        self.switch=not self.switch

    def register_button_menu_events(self):
        self.values=['x to front','-x to front','y to front','-y to front','z to front','-z to front']
        return PySimpleGUI.ButtonMenu('Reset View',
                    [self.values,
                    self.values],
                    border_width=2)#,background_color="gray"
    
    def trigger_button_menu_events(self,value):#here we need self.values, or better analogoues to ButtonEvent but without Button instead Strings and again trigger_command
        print("TRIGGERED")
        if value=='x to front':
            print("FRONT X")

    def register_button_events(self):
        self.events=[
            #ButtonEvent("Reset x",self.reset_x),
            ButtonEvent("\u23EE",self.sequence_manager.jump_to_start),
            ButtonEvent("\u23F4",self.sequence_manager.backwards),
            ButtonEvent("\u23EF",self.dummy ),
            ButtonEvent("\u23F5",self.sequence_manager.forwards),
            ButtonEvent("\u23ED", self.sequence_manager.jump_to_end),
            ButtonEvent("+",self.zoom_in),#zoom is kind of difficult to move into another class. Maybe ax as own, don't know
            ButtonEvent("-",self.zoom_out)
            ]       
        button_list=[]
        for event in self.events:
            button_list.append(event.get_button())
        return button_list
    
    def dummy(self):
        return
    
    def trigger_button_events(self, event):
        if event=="\u23EF":
            self.press_switch()
            return
        for self_event in self.events:
            if self_event.event_name==event:
                self.switch=False
                self_event.trigger_command()
                self.set_actual_plot()
    
    def register_mouse_events(self):
        plt.connect('button_press_event', on_click)
        plt.connect('scroll_event', self.on_press)
        plt.connect('button_press_event', self.on_press)

    def on_press(self,event):
        if event.button=="up":
            self.switch=False
            self.zoom_in()
            self.set_actual_plot()
        elif event.button=="down":
            self.switch=False
            self.zoom_out()
            self.set_actual_plot()
        pressed = self.ax.button_pressed
        self.ax.button_pressed = -1 # some value that doesn't make sense.
        coords = self.ax.format_coord(event.xdata, event.ydata) # coordinates string in the form x=value, y=value, z= value
        print("pressed, coords",coords)
        self.ax.button_pressed = pressed
        print('you pressed', event.button, event.xdata, event.ydata, event.x, event.y,self.ax.format_coord(event.x,event.y))
        
        print("mouseevent occured on the line", self.sequence_manager.choose_sequence(event))

    def main_loop(self):
        while True:
            event, values = self.root.read(timeout=500)#returns lways the last triggered value, this is a problem.
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
