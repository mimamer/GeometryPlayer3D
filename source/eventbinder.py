from source.buttonevent import ButtonEvent
from source.plot3d import Plot3D
from source.sequencemanager import SequenceManager
import PySimpleGUI

class EventBinder:
    def __init__(self,plot_3d,sequence_manager):#TODO:separate, init without register, register extra
        view_menu,view_menu_events=self.register_view_menu_events(plot_3d)
        button_list,button_events=self.register_button_events(sequence_manager)
        playback_menu,playback_events=self.register_playback_speed_events()
        self.button_list_bottom=[view_menu]+button_list+[playback_menu]
        self.events=button_events+view_menu_events+playback_events

    def get_button_list_bottom(self):
        return self.button_list_bottom
    
    
    def register_view_menu_events(self,plot_3d:Plot3D) -> tuple[PySimpleGUI.ButtonMenu,list[ButtonEvent]]:
        button_menu_events=[
            ButtonEvent("standard view",plot_3d.standard_view),
            ButtonEvent("front view",plot_3d.front_view),
            ButtonEvent("back view",plot_3d.back_view),
            ButtonEvent("left view",plot_3d.left_view ),
            ButtonEvent("right view",plot_3d.right_view),
            ButtonEvent("top view", plot_3d.top_view),
            ButtonEvent("bottom view", plot_3d.bottom_view),
        ]
        names=[]
        for event in button_menu_events:
            names.append(event.event_name)

        return PySimpleGUI.ButtonMenu('Reset View',
                    [names,
                    names],
                    border_width=2, key='Reset View'),button_menu_events
    
    def register_playback_speed_events(self) -> tuple[PySimpleGUI.ButtonMenu,list[ButtonEvent]]: #TODO:check synatx
        button_menu_events=[
            ButtonEvent(str(step/100),self.dummy) for step in range(25,201,25)
        ]
        names=[]
        for event in button_menu_events:
            names.append(event.event_name)

        return PySimpleGUI.ButtonMenu('Playback Speed',
                    [names,
                    names],
                    border_width=2, key="Playback Speed"),button_menu_events
    
    def register_button_events(self,sequence_manager:SequenceManager):
        events=[
            #ButtonEvent("Reset x",self.reset_x),
            ButtonEvent("\u23EE",sequence_manager.jump_to_start),
            ButtonEvent("\u23F4",sequence_manager.backwards),
            ButtonEvent("\u23EF",self.dummy),#TODO:more static...
            ButtonEvent("\u23F5",sequence_manager.forwards),
            ButtonEvent("\u23ED", sequence_manager.jump_to_end),
            ButtonEvent("+",sequence_manager.zoom_in),
            ButtonEvent("0",sequence_manager.zoom_reset),
            ButtonEvent("-",sequence_manager.zoom_out)
            ]       
        button_list=[]
        for event in events:
            button_list.append(event.get_button())
        return button_list, events

    def dummy(): #TODO:looks very static but is not?
        return