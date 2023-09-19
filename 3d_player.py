import matplotlib.pyplot as plt
import numpy as np
import time
import PySimpleGUI
from ast import literal_eval
import numpy
import json
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")
back=False
switch=False
fig=None
ax=None
gen=None
line=None
wframe = None
index=0
x=[]
y=[]
z=[]

def read_data(path):
    with open(path) as file:
        data=json.load(file)
        return data

def create_figure():
    print("create figure")
    global fig
    global ax
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_zlim(-1, 1)


def run_figure():
    print("run figure", switch)
    global gen
    global ax
    global index
    global line
    
    if switch:
        #if wframe:
        #    wframe.remove()
        #calls the next item of generator
        data_object = next(gen)
        x.append(data_object[0][0])
        y.append(data_object[0][1])
        z.append(data_object[0][2])
        #sache mit den Quadern fehlt noch...
        line,=ax.plot(x,y,z, marker="o", linestyle="dashed", markersize=2)
        index+=1
        plt.pause(1.00)


def back():# auch generator drauß machen...?
    global index
    global fig
    global line
    print("try")
    try:
        xvals = x[:index-2]
        yvals = y[:index-2]
        zvals = z[:index-2]
        line.set_data_3d(xvals,yvals,zvals)
        fig.canvas.draw_idle()
    except Exception as e:
        print(e)
        pass



def next_value(data_objects):
    global back
    for i in range(len(data_objects)):
        try:
            yield data_objects[i]

        except StopIteration:
            break

            
def pause_figure():
    global switch
    switch=not switch


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def create_main_window(data_objects):
    global fig
    global switch
    create_figure()
    play_button = PySimpleGUI.Button('Play/Pause')
    back_button = PySimpleGUI.Button('<')
    root = PySimpleGUI.Window(title="3D Result Player", layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],[back_button, play_button]], finalize=True)
    draw_figure(root["-CANVAS-"].TKCanvas, fig)

    while True:
        event, values = root.read(timeout=1000)
        # End program if user closes window or
        # presses the OK button
        if event == PySimpleGUI.WIN_CLOSED:
            break
        if event == "Play/Pause":
            pause_figure()
        if event == "<":
            switch=False
            back()

        if switch:
            run_figure()

    root.close()

    #root.mainloop()


if __name__ == "__main__":
    path="/home/michelle/real/3d_player/plot_tests/modified.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    gen  = next_value(data_objects)
    print(next(gen))
    print(next(gen))

    create_main_window(data_objects)