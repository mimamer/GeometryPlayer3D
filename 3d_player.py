import matplotlib.pyplot as plt
import numpy as np
import time
import tkinter as tk
from tkinter import TclError, ttk
import tkinter as tk
from ast import literal_eval
import numpy

switch=False
ax=None
gen=None
wframe = None

def read_data(path):
    file=open(path)
    #data=literal_eval(file.read())
    data=literal_eval(file.read())
    arr=list(data)
    print(type(arr),data[0], data[1], data[2])
    return arr

def create_figure():
    print("create figure")
    global ax
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Set the z axis limits, so they aren't recalculated each frame.
    ax.set_zlim(-1, 1)

    # Begin plotting.
    
    return ax
def gen_gen(data_objects):
    global switch
    global ax
    global gen
    # Make the X, Y meshgrid.    
    #xs = np.linspace(-1, 1, 50)
    #ys = np.linspace(-1, 1, 50)
    #X, Y = np.meshgrid(xs, ys)
    gen  = next_value(data_objects)

def run_figure():
    print("run figure", switch)
    global gen
    global wframe
    
    if switch:
        if wframe:
            wframe.remove()
        #calls the next item of generator
        wframe = next(gen)
        plt.pause(1.00)


def next_value(data_objects):
    # Generate data.
    print(data_objects)
    for data_object in data_objects:
        data_string=numpy.array(data_object)
        print(data_string)
        #try: 
        data=(data_string)
        # Plot the new wireframe and pause briefly before continuing.
        x,y,z= data[0], data[1], data[2]
        print("PLOT", x,y,z)
        yield ax.plot(x,y,z)
        #except:
            #data=numpy.array(literal_eval(data_string))
            # Plot the new wireframe and pause briefly before continuing.
            #x,y,z= data[0], data[1], data[2]
            #yield ax.voxels(data[0:8])
        #    print("NONE")
        #    yield None


            

def pause_figure():
    global switch
    switch=not switch



def create_button_frame(container):
    global ax
    frame = ttk.Frame(container)

    frame.columnconfigure(0, weight=1)

    ttk.Button(frame, text='Play', command=run_figure).grid(column=0, row=0)
    ttk.Button(frame, text='Play/Pause', command=pause_figure).grid(column=0, row=1)


    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)

    return frame


def create_main_window(data_objects):
    global ax
    root = tk.Tk()
    root.title('3D Result Player')
    root.resizable(0, 0)
    #try:
    #    # windows only (remove the minimize/maximize button)
    #    root.attributes('-toolwindow', True)
    #except TclError:
    #    print('Not supported on your platform')

    # layout on the root window
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    create_figure()
    ax.grid(column=1, row=0)
    
    button_frame = create_button_frame(root)
    button_frame.grid(column=0, row=0)
    gen_gen(data_objects)

    def nextframe():
        run_figure()
        root.after(1000, nextframe)
    root.after(1000, nextframe)
    #run_figure(ax)

    root.mainloop()


if __name__ == "__main__":
    path="/home/michelle/real/3d_player/plot_tests/1_mini.txt"
    data_objects=read_data(path)
    create_main_window(data_objects)