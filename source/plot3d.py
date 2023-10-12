import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from source.sequencemanager import SequenceManager
import mpl_toolkits
from mpl_toolkits.mplot3d.art3d import Line3DCollection

px=1/plt.rcParams['figure.dpi']#TODO:magic
resolution=(1980*px,1080*px)
class Plot3D:
    def __init__(self):
        res=(resolution[0]*(28/30),resolution[1]*(2/3))
        #res=(res[0],20*px)
        self.figure = plt.figure(figsize=res)#TODO:magic
        self.plot =self.figure.add_subplot(projection='3d') #ax is a subplot
        self.set_default_plot_labels()
    
    def set_root(self,root):
        self.canvas = FigureCanvasTkAgg(self.figure, root["-CANVAS-3D"].TKCanvas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    
    def update(self, sequence_manager:SequenceManager):
        self.plot.cla()
        plot_data_3d=sequence_manager.get_plot_data_3d()
        self.handle_plot_data(plot_data_3d)
        chosen_dict=sequence_manager.get_chosen_data_object_3d()
        if chosen_dict is not None: 
            if "line_collection" in chosen_dict.keys():
                self.plot.add_collection3d(chosen_dict["line_collection"])#TODO:if line collection to small other kind of plotting
            else:
                self.plot.scatter(chosen_dict["xs"],chosen_dict["ys"],chosen_dict["zs"],s=25, depthshade=False,
                                   marker="o", c='fuchsia')
        
        hover_dict=sequence_manager.get_hover_data_object_3d()
        if hover_dict is not None:#TODO:function with color argument line 27-33 and 34-40 are almost the same
            if "line_collection" in hover_dict.keys():
                self.plot.add_collection3d(hover_dict["line_collection"])#TODO:if line collection to small other kind of plotting
            else:
                self.plot.scatter(hover_dict["xs"],hover_dict["ys"],hover_dict["zs"],
                            depthshade=False,s=25,marker="o", c='aqua')
        self.set_default_plot_labels()
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def standard_view(self):
        self.plot.azim=-60
        self.plot.elev=30
    def front_view(self):
        self.plot.azim=0
        self.plot.elev=0
    def back_view(self):
        self.plot.azim=180
        self.plot.elev=0
    def left_view(self):
        self.plot.azim=-90
        self.plot.elev=0
    def right_view(self):
        self.plot.azim=90
        self.plot.elev=0
    def top_view(self):
        self.plot.azim=0
        self.plot.elev=90
    def bottom_view(self):
        self.plot.azim=0
        self.plot.elev=-90

    def set_default_plot_labels(self) -> None:
        self.plot.set_xlabel("x")
        self.plot.set_ylabel("y")
        self.plot.set_zlabel("z")

    def handle_plot_data(self, plot_data_3d):
        for sequence in plot_data_3d:
            for dict_elem in sequence:
                if "line_collection" in dict_elem.keys():
                    self.plot.add_collection3d(dict_elem["line_collection"])
                    #if not visible plot as squares
                else:
                    self.plot.scatter(xs=dict_elem["xs"],
                            ys=dict_elem["ys"],
                            zs=dict_elem["zs"],
                            depthshade=False,
                            s=5,
                            c=dict_elem["color"],
                            marker="o")
        #TODO:if line collection to small other kind of plotting
        #if self.width_x/ax_width<is_visible_factor \
        #self.plot.set_xlim()