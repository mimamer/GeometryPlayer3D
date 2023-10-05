import json
import matplotlib
import matplotlib.pyplot as plt

def read_data(path):
    with open(path) as file:
        data=json.load(file)
        return data
    
#example set
def open_dataobjects():
    path="/home/michelle/real/3d_player/test_data/modified_meth0.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    return data_objects

def open_dataobjects_2():
    path="/home/michelle/real/3d_player/test_data/modified_meth1.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    return data_objects

def open_dataobjects_testformat():
    path="/home/michelle/real/3d_player/test_data/formattest.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    return data_objects
#def open_dataobjects_minus():
#    path="/home/michelle/real/3d_player/test_data/modified_meth0.txt"
#    data_objects=read_data(path)
#    data_objects=data_objects['data']
#    data=[]
#    for index in range(len(data_objects)):
#        data_object=data_objects[index]
#        data_object=[-1*data_object[0],-1*data_object[1],-1*data_object[2]]
#        data.append(data_object)
#    return data


def create_colors(length_plot_window):
    colors=[]
    for cmap in ['Greys','Greens','Purples','Oranges', 'Blues']:#TODO:limits number of curves that can be visualized, cycle, use mod operator
        cmap=plt.get_cmap(cmap)
        colo=[]
        cmap_usable=int(cmap.N/3)
        col_abs=(cmap.N-cmap_usable)/length_plot_window # hier noch volles Fenster, dieses wird aber irgendwann verkleinert, schieberegler
        i=0
        while i*col_abs<=cmap.N-cmap_usable:
            rgba=cmap(cmap_usable+int(i*col_abs))
            colo.append(matplotlib.colors.rgb2hex(rgba))
            i+=1
        colors.append(colo)
    return colors

