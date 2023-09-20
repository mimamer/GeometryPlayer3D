import matplotlib.pyplot as plt
import numpy as np
import time
import PySimpleGUI
from ast import literal_eval
import numpy
import json
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_input import read_data
import mpl_toolkits
from mpl_toolkits.mplot3d.art3d import Line3D

matplotlib.use("TkAgg")


#dynamisch mit rein tun, falls wert schon da nimm diesen....
class Three_Dimensional_Player:
    def __init__(self):
        self.switch=False
        self.fig=None
        self.ax=None
        self.gen=None
        
        self.x=[]
        self.y=[]
        self.z=[]

        self.line=None
        self.index=0
        self.tmp_index=0
        play_button = PySimpleGUI.Button('Play/Pause')
        back_button = PySimpleGUI.Button('<')
        self.root = PySimpleGUI.Window(title="3D Result Player", layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],[back_button, play_button]], finalize=True)
        self.create_figure()
        self.figure_canvas_agg=self.draw_figure(self.root["-CANVAS-"].TKCanvas, self.fig)

    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg

    def create_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.set_zlim(-1, 1)


    def plot_actual_data(self):
        #forget? self.fig.get_tk_widget
        self.ax.cla()
        self.line=Line3D(self.x[:self.tmp_index],self.y[:self.tmp_index],self.z[:self.tmp_index])
        plot_data=self.line.get_data_3d()
        self.ax.plot(plot_data[0], plot_data[1],  plot_data[2],marker="o", markersize=5)
        self.fig.canvas.draw_idle()


    def run_figure(self):
        if self.switch:
            if self.tmp_index>self.index:
                data_object = next(self.gen)
                self.x.append(data_object[0][0])
                self.y.append(data_object[0][1])
                self.z.append(data_object[0][2])
                self.index+=1
                #sache mit den Quadern fehlt noch...
            
            self.plot_actual_data()
            self.tmp_index+=1
            
            plt.pause(1.00)


    def backwarts(self):# auch generator drauß machen...?
        print("try")
        if self.tmp_index>0:
            try:
                self.tmp_index=self.tmp_index-1
 
                self.plot_actual_data()
                
            except Exception as e:
                print(e)
                pass



    def next_value(self,data_objects):
        for i in range(len(data_objects)):
            try:
                yield data_objects[i]

            except StopIteration:
                break

                
    def pause_figure(self):
        self.switch=not self.switch

    def create_main_window(self):

        
        while True:
            event, values = self.root.read(timeout=1000)
            # End program if user closes window or
            # presses the OK button
            if event == PySimpleGUI.WIN_CLOSED:
                break
            if event == "Play/Pause":
                self.pause_figure()
            if event == "<":
                self.switch=False
                self.backwarts()

            if self.switch:
                self.run_figure()

        self.root.close()

        #root.mainloop()


if __name__ == "__main__":
    path="/home/michelle/real/3d_player/plot_tests/modified.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    player= Three_Dimensional_Player()
    player.gen  = player.next_value(data_objects)

    player.create_main_window()