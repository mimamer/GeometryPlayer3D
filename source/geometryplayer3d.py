
import PySimpleGUI
import matplotlib
from source.plot3d import Plot3D
from source.plotdistance import PlotDistance
from source.sequence import Sequence
from source.sequencemanager import SequenceManager
from source.eventbinder import EventBinder
from matplotlib.backend_bases import MouseButton, MouseEvent
from source.utils import open_dataobjects
matplotlib.use("TkAgg")


class GeometryPlayer3D:
    """The GeometryPlayer3D Class builds the root window and delegates the processing of events. """
    def __init__(self):
        
        self.switch : bool = False
        self.plot_3d:Plot3D=Plot3D()
        self.plot_distance: PlotDistance=PlotDistance()

        self.sequence_manager:SequenceManager=SequenceManager(None)
        self.event_binder:EventBinder=EventBinder(self.plot_3d, self.sequence_manager)

        PySimpleGUI.theme('SystemDefault')
        
        self.root = PySimpleGUI.Window(title="3D Result Player",
                        layout=[
                            [PySimpleGUI.FileBrowse("Open Sequence",enable_events=True)],
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

    def trigger_view_menu_events(self,value:str) -> None:
        self.trigger_events(value)

    def trigger_events(self, event:str) -> None:
        if event=="\u23EF":
            self.press_switch()
            return
        for self_event in self.event_binder.events:
            if self_event.event_name==event:
                self.switch=False
                self_event.trigger_command()
                self.update_plot()
                break

    def trigger_open(self, fname):
        try:
            self.sequence_manager.add_sequence(open_dataobjects(fname),fname)
        except Exception as e:
            print(e)
            pass
        self.update_plot()

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
            if values is not None and 0 in values.keys() and event==0:#button menu was triggered,TODO: could trigger playbackspeed here too? 
                self.trigger_view_menu_events(values[0])
            if event == PySimpleGUI.WIN_CLOSED or event=="Exit":
                break
            if event=="Open Sequence" and values["Open Sequence"] is not None:
                self.trigger_open(values['Open Sequence'])
            self.trigger_events(event)
            if self.switch:
                self.run_figure()
        self.root.close()

