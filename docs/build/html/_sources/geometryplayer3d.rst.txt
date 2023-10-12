GeometryPlayer3D
----------------
.. py:class:: GeometryPlayer3D

The `GeometryPlayer3D` class builds the root window and delegates the processing of events.

.. py:function:: GeometryPlayer3d.__init__(self)

   Builds the GUI with binded mouseevents, buttons and
   empty plots. Return value is None.

.. py:function:: update_plot(self) -> None

   Updates the 3d Plot and the distance plot.


.. py:function:: run_figure(self) -> None 

   Goes one step forward in the animation of the sequences if the switch is on.


.. py:function:: press_switch(self) -> None

   Switch between *play* and *pause*. 

.. py:function:: trigger_button_menu_events(self,value:str) -> None

   Triggers the command that matches the parameter **value**. 
   The command has to be bounded to a button under "Reset View". 

.. py:function:: trigger_button_events(self,event:str) -> None

    Triggers the command that matches the parameter **event**. 
    The command has to be bounded to the ⏮ , ⏴ , ⏯ , ⏵ , ⏭ , + or - button. 

.. py:function:: trigger_scroll_events(self,event:matplotlib.backend_bases.MouseEvent) -> None

   | Triggers the command that matches the field *button* of parameter **event**.
   | The command has to be bounded to the mouse scroll event 'up' or 'down' . 

.. py:function:: trigger_press_events(self,event:matplotlib.backend_bases.MouseEvent) -> None

   Triggers the command that matches the field *button* of the parameter **event**. 
   The command has to be bounded to the mouse press event 'LEFT' or 'RIGHT' . 

.. py:function:: main_loop(self) -> None