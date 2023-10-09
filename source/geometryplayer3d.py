import matplotlib.pyplot as plt
import PySimpleGUI
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from source.sequence import Sequence
from source.sequencemanager import SequenceManager
from source.buttonevent import ButtonEvent
from matplotlib.backend_bases import MouseButton
matplotlib.use("TkAgg")
import warnings
warnings.filterwarnings("error")
from source.utils import create_colors

px=1/plt.rcParams['figure.dpi']#TODO:magic
resolution=(1980*px,1080*px)

class GeometryPlayer3D:
    """The GeometryPlayer3D Class builds the main window and delegates the processing of events. """
    def __init__(self,data_objects,data_objects_2,data_objects_3):
        
        self.switch : bool = False
        self.fig=None
        self.fig_abs=None
        self.ax=None
        self.abs_plot=None
        self.figure_canvas_agg=None
        self.figure_abs_canvas_agg=None

        self.length_plot_window=len(data_objects_2)#TODO:only temporary
        self.colors=create_colors(self.length_plot_window)

        curves=[Sequence(data_objects_2),Sequence(data_objects), Sequence(data_objects_3)]
        #later three_dimensional_player will not receive data_objects for curve this way
        self.sequence_manager=SequenceManager(curves)

        button_menu_reset,menu_buttons=self.register_button_menu_events()
        button_list,normal_buttons=self.register_button_events()
        button_list=[button_menu_reset]+button_list
        self.events=normal_buttons+menu_buttons
        #menu_def = [['File', ['Open', 'Save', 'Exit',]],
        #        ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
        #        ['Help', 'About...'],]
        
        self.root = PySimpleGUI.Window(title="3D Result Player",
                        layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],[PySimpleGUI.Canvas(key="-CANVAS-ABS")],[button_list]],
                        finalize=True,element_justification='c', resizable=True)
        self.create_figure()
        self.create_figure_abs()
        self.register_mouse_events()

    def create_figure_abs(self) -> None:
        self.fig_abs=plt.figure(figsize=(self.fig.get_figwidth(),2))#TODO:magic
        self.abs_plot=self.fig_abs.add_subplot()
        self.figure_abs_canvas_agg = FigureCanvasTkAgg(self.fig_abs, self.root["-CANVAS-ABS"].TKCanvas)
        self.figure_abs_canvas_agg.draw()
        self.figure_abs_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)

    def create_figure(self) -> None:
        res=(resolution[0]*(28/30),resolution[1]*(2/3))
        #res=(res[0],20*px)
        self.fig = plt.figure(figsize=res)#TODO:magic
        self.ax =self.fig.add_subplot(projection='3d') #ax is a subplot
        self.default_ax_setting()
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.root["-CANVAS-"].TKCanvas)
        self.figure_canvas_agg.draw()
        self.figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)

    def default_ax_setting(self) -> None:
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        #self.ax.use_sticky_edges=False # can not zoom in adequately
    
    def set_actual_plot(self) -> None:
        self.ax.cla() #clear ax
        self.abs_plot.cla() #clear ax
        self.sequence_manager.set_actual_plot_data(self.ax,self.abs_plot, self.colors)
        self.default_ax_setting()
        self.figure_canvas_agg.draw_idle()#TODO:neccessary?-> yes!
        self.figure_canvas_agg.flush_events()
        self.figure_abs_canvas_agg.draw_idle()
        self.figure_abs_canvas_agg.flush_events()

    def run_figure(self) -> None:
        if self.switch:
            self.sequence_manager.forwards()
            self.set_actual_plot()
   
    def press_switch(self) -> None:
        self.switch=not self.switch

    def register_button_menu_events(self) -> None:
        button_menu_events=[
            ButtonEvent("standard view",self.standard_view),
            ButtonEvent("front view",self.front_view),
            ButtonEvent("front view",self.front_view),
            ButtonEvent("back view",self.back_view),
            ButtonEvent("left view",self.left_view ),
            ButtonEvent("right view",self.right_view),
            ButtonEvent("top view", self.top_view),
            ButtonEvent("bottom view", self.bottom_view),
        ]
        names=[]
        for event in button_menu_events:
            names.append(event.event_name)

        return PySimpleGUI.ButtonMenu('Reset View',
                    [names,
                    names],
                    border_width=2),button_menu_events#,background_color="gray"

    def standard_view(self):
        self.ax.azim=-60
        self.ax.elev=30
    def front_view(self):
        self.ax.azim=0
        self.ax.elev=0
    def back_view(self):
        self.ax.azim=180
        self.ax.elev=0
    def left_view(self):
        self.ax.azim=-90
        self.ax.elev=0
    def right_view(self):
        self.ax.azim=90
        self.ax.elev=0
    def top_view(self):
        self.ax.azim=0
        self.ax.elev=90
    def bottom_view(self):
        self.ax.azim=0
        self.ax.elev=-90

    def trigger_button_menu_events(self,value):
        self.trigger_button_events(value)

    def register_button_events(self):
        normal_buttons=[
            #ButtonEvent("Reset x",self.reset_x),
            ButtonEvent("\u23EE",self.sequence_manager.jump_to_start),
            ButtonEvent("\u23F4",self.sequence_manager.backwards),
            ButtonEvent("\u23EF",self.dummy),
            ButtonEvent("\u23F5",self.sequence_manager.forwards),
            ButtonEvent("\u23ED", self.sequence_manager.jump_to_end),
            ButtonEvent("+",self.sequence_manager.zoom_in),
            ButtonEvent("-",self.sequence_manager.zoom_out)
            ]       
        button_list=[]
        for event in normal_buttons:
            button_list.append(event.get_button())
        return button_list, normal_buttons
    
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
        self.figure_canvas_agg.mpl_connect('scroll_event', self.on_scroll)
        self.figure_abs_canvas_agg.mpl_connect('button_press_event', self.on_press)

    def on_scroll(self,event):
        if event.button=="up":
            self.switch=False
            self.sequence_manager.zoom_in()
            self.set_actual_plot()
        elif event.button=="down":
            self.switch=False
            self.sequence_manager.zoom_out()
            self.set_actual_plot()

    def on_press(self,event):
        if event.inaxes:
            if event.button==MouseButton.LEFT:
                sequence,index=self.sequence_manager.choose_sequence(event)
                self.sequence_manager.set_chosen_object(sequence, index)
                self.set_actual_plot()
            elif event.button==MouseButton.RIGHT:
                sequence,index=self.sequence_manager.choose_sequence(event)
                self.sequence_manager.set_hover_object(sequence, index)
                self.set_actual_plot()

    def main_loop(self):
        while True:
            event, values = self.root.read(timeout=500)
            #if event!="__TIMEOUT__":
            #    print(event, values)
            if values is not None and 0 in values.keys() and event==0:#button menu was triggered 
                self.trigger_button_menu_events(values[0])

            if event == PySimpleGUI.WIN_CLOSED:
                break
            self.trigger_button_events(event)
            if self.switch:
                self.run_figure()
        self.root.close()

