
import PySimpleGUI
import matplotlib
from source.plot3d import Plot3D
from source.plotdistance import PlotDistance
from source.sequence import Sequence
from source.sequencemanager import SequenceManager
from source.eventbinder import EventBinder
from matplotlib.backend_bases import MouseButton, MouseEvent
matplotlib.use("TkAgg")


class GeometryPlayer3D:
    """The GeometryPlayer3D Class builds the root window and delegates the processing of events. """
    def __init__(self,data_objects,data_objects_2,data_objects_3):
        
        self.switch : bool = False
        self.plot_3d:Plot3D=Plot3D()
        self.plot_distance: PlotDistance=PlotDistance()

        curves=[Sequence(data_objects), Sequence(data_objects_2)]
        #later three_dimensional_player will not receive data_objects for curve this way
        self.sequence_manager:SequenceManager=SequenceManager(curves)
        self.event_binder:EventBinder=EventBinder(self.plot_3d, self.sequence_manager)

        #menu_def = [['File', ['Open', 'Save', 'Exit',]],
        #        ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
        #        ['Help', 'About...'],]
        
        self.root = PySimpleGUI.Window(title="3D Result Player",
                        layout=[
                            [PySimpleGUI.Canvas(key="-CANVAS-3D")],
                            [PySimpleGUI.Canvas(key="-CANVAS-DISTANCE")],
                            [self.event_binder.get_button_list_bottom()]
                        ],
                        finalize=True,element_justification='c', resizable=True)
        self.plot_3d.set_root(self.root)
        self.plot_distance.set_root(self.root)

        self.register_mouse_events()#TODO: a bit inconsequent
    
    def update_plot(self) -> None:
        self.plot_3d.update(self.sequence_manager)
        self.plot_distance.update(self.sequence_manager)

    def run_figure(self) -> None:
        if self.switch:
            self.sequence_manager.forwards()
            self.update_plot()
   
    def press_switch(self) -> None:
        self.switch=not self.switch

    def trigger_button_menu_events(self,value:str) -> None:
        self.trigger_button_events(value)

    def trigger_button_events(self, event:str) -> None:
        if event=="\u23EF":
            self.press_switch()
            return
        for self_event in self.event_binder.events:
            if self_event.event_name==event:
                self.switch=False
                self_event.trigger_command()
                self.update_plot()
                break

    def register_mouse_events(self) -> None:
        self.plot_3d.canvas.mpl_connect('scroll_event', self.trigger_scroll_events)
        self.plot_distance.canvas.mpl_connect('button_press_event', self.trigger_press_events)

    def trigger_scroll_events(self,event:MouseEvent) -> None:
        if event.button=="up":
            self.switch=False
            self.sequence_manager.zoom_in()
            self.update_plot()
        elif event.button=="down":
            self.switch=False
            self.sequence_manager.zoom_out()
            self.update_plot()

    def trigger_press_events(self,event:MouseEvent) -> None:
        if event.inaxes:
            if event.button==MouseButton.LEFT or event.button==MouseButton.RIGHT:
                self.sequence_manager.choose_sequence(event)
                self.update_plot()

    def main_loop(self) -> None:
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

