import mpl_toolkits
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy
class DataObject:
    def __init__(self,data):
        self.is_vertex=True
        factor=0.01
        if len(data)!=1:
            self.is_vertex=False
        self.data=None
        if self.is_vertex:
            self.data=numpy.array(data[0]) #is list of three numbers
        else:
            try:
                segments=[(
                    numpy.array(data[index][0])*factor,
                    numpy.array(data[index][1])*factor)
                    for index in range(len(data))]
                self.data=Line3DCollection(segments,edgecolor="black")
            except Exception as e:
                print(e)
        print("initialized data object", self.data, self.is_vertex)
        
    def plot_data_object(self,ax,color):
        if self.is_vertex:
            ax.scatter(xs=self.data[0], ys=self.data[1],  zs=self.data[2], depthshade=False, c=color)
        else:
            ax.add_collection3d(self.data)