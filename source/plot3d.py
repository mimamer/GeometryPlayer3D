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
        if not sequence_manager.is_empty_plot():
            plot_data_3d=sequence_manager.get_plot_data_3d()
            self.handle_plot_data(plot_data_3d,sequence_manager)
            chosen_dict=sequence_manager.get_chosen_data_object_3d()
            self.handle_single_object(chosen_dict,'fuchsia',sequence_manager)
            hover_dict=sequence_manager.get_hover_data_object_3d()
            self.handle_single_object(hover_dict,'aqua',sequence_manager)

        self.set_plot_lims(sequence_manager)
        self.set_default_plot_labels(sequence_manager.get_sequence_names(),sequence_manager.get_sequence_representative_colors())
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def handle_single_object(self,object_dictionary,color:str,sequence_manager):#lims too
            if object_dictionary is not None: 
                if "line_collection" in object_dictionary.keys():
                    self.plot.add_collection3d(object_dictionary["line_collection"])#TODO:if line collection to small other kind of plotting, TODO:_ sequence_manager stuff is evil here, correct_lims is a sequence_manager function!
                    sequence_manager.correct_lims([object_dictionary["min_lims"][0]],[object_dictionary["min_lims"][1]],[object_dictionary["min_lims"][2]])
                    sequence_manager.correct_lims([object_dictionary["max_lims"][0]],[object_dictionary["max_lims"][1]],[object_dictionary["max_lims"][2]])
                
                else:
                    self.plot.scatter(object_dictionary["xs"],object_dictionary["ys"],object_dictionary["zs"],s=25, depthshade=False,
                                    marker="o", c=color)
                    sequence_manager.correct_lims([object_dictionary["xs"]],[object_dictionary["ys"]],[object_dictionary["zs"]])
    
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

    def set_default_plot_labels(self,legend_names=None, legend_colors=None) -> None:
        self.plot.set_xlabel("x")
        self.plot.set_ylabel("y")
        self.plot.set_zlabel("z")
        if legend_names is not None and legend_colors is not None:
            self.plot.legend(labels=legend_names, labelcolor=legend_colors)
        #if legend_colors is not None:
        #    self.plot.legend(labelcolor=legend_colors)

    def handle_plot_data(self, plot_data_3d,sequence_manager):
        sequence_manager.min_lim=None
        sequence_manager.max_lim=None
        for sequence in plot_data_3d:
            for dict_elem in sequence:
                if "line_collection" in dict_elem.keys():
                    self.plot.add_collection3d(dict_elem["line_collection"])
    
                    #TODO:if not visible plot as squares
                    sequence_manager.correct_lims([dict_elem["min_lims"][0]],[dict_elem["min_lims"][1]],[dict_elem["min_lims"][2]])
                    sequence_manager.correct_lims([dict_elem["max_lims"][0]],[dict_elem["max_lims"][1]],[dict_elem["max_lims"][2]])
                else:
                    self.plot.scatter(xs=dict_elem["xs"],
                            ys=dict_elem["ys"],
                            zs=dict_elem["zs"],
                            depthshade=False,
                            s=5,
                            c=dict_elem["color"],
                            marker="o")
                    sequence_manager.correct_lims(dict_elem["xs"],dict_elem["ys"],dict_elem["zs"])
        #TODO:if line collection to small other kind of plotting
        #if self.width_x/ax_width<is_visible_factor \

    def set_plot_lims(self,sequence_manager):
        if sequence_manager.min_lim is not None and sequence_manager.max_lim is not None:
            self.plot.set_xlim(sequence_manager.min_lim[0],sequence_manager.max_lim[0])
            self.plot.set_ylim(sequence_manager.min_lim[1],sequence_manager.max_lim[1])
            self.plot.set_zlim(sequence_manager.min_lim[2],sequence_manager.max_lim[2])



