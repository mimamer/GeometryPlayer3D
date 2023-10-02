import json
import matplotlib
import matplotlib.pyplot as plt

def read_data(path):
    with open(path) as file:
        data=json.load(file)
        return data

def get_new_lims(lim_tuple):#problems when diff is very small
    diff=lim_tuple[1]-lim_tuple[0]
    diff=diff/10
    print("DIFFERENZ",diff)
    left_lim=lim_tuple[0]+diff
    right_lim=lim_tuple[1]-diff
    if left_lim>=lim_tuple[0] and right_lim<=lim_tuple[1] and left_lim!=right_lim and left_lim!=lim_tuple[0] and right_lim!=lim_tuple[1]:
        print("LIMS CHANGED", lim_tuple, "to", left_lim, right_lim)
        return left_lim,right_lim
    else:
        print("LIMS COULD NOT BE CHANGED", lim_tuple)
        return (lim_tuple[0], lim_tuple[1])
    
def greater_compare(a,bound):
    return a>bound

def smaller_compare(a,bound):
    return a<bound

def both_bound_compare(a,bound):
    bound=abs(bound)
    return a>-bound and a<bound

def set_compare_function(meaning):
    if meaning=="both":
        return both_bound_compare
    elif meaning=="+":
        return smaller_compare
    elif meaning=="-":
        return greater_compare
    else:
        raise Exception("unknown meaning string", meaning)
    
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
def open_dataobjects_minus():
    path="/home/michelle/real/3d_player/test_data/modified_meth0.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    data=[]
    for index in range(len(data_objects)):
        data_object=data_objects[index]
        data_object=[-1*data_object[0],-1*data_object[1],-1*data_object[2]]
        data.append(data_object)
    return data


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

def square_distance_between(point_a,point_b):
    return (point_a[0]-point_b[0])**2+(point_a[1]-point_b[1])**2+(point_a[2]-point_b[2])**2