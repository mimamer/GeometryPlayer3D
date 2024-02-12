import json
import matplotlib
import matplotlib.pyplot as plt

def read_data(path):
    with open(path) as file:
        data=json.load(file)
        return data
    
#example set
def open_dataobjects(path):
    data_objects=read_data(path)
    data_objects=data_objects['data']
    return data_objects

color_mod=0
def create_color(length_plot_window):
    global color_mod
    cmaps=['Greys','Greens','Purples','Oranges', 'Blues']
    cmap =cmaps[color_mod%len(cmaps)]
    color_mod+=1
    cmap=plt.get_cmap(cmap)
    colo=[]
    cmap_usable=int(cmap.N/3)
    col_abs=(cmap.N-cmap_usable)/length_plot_window 
    i=0
    while i*col_abs<=cmap.N-cmap_usable:
        rgba=cmap(cmap_usable+int(i*col_abs))
        colo.append(matplotlib.colors.rgb2hex(rgba))
        i+=1
    return colo

