from PySimpleGUI import Button
class ButtonEvent:
    def __init__(self,event_name,command):
        self.event_name=event_name
        self.command=command
        
    def trigger_command(self):
        self.command()

    def get_button(self):
        return Button(self.event_name)
