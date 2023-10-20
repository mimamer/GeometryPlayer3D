import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from source.sequencemanager import SequenceManager


px=1/plt.rcParams['figure.dpi']#TODO:magic
resolution=(1980*px,1080*px)
class PlotDistance():
    def __init__(self):
        self.figure=plt.figure(figsize=(resolution[0]*(28/30),2))#TODO:magic
        self.plot=self.figure.add_subplot()

    def set_root(self,root):
        self.canvas = FigureCanvasTkAgg(self.figure, root["-CANVAS-DISTANCE"].TKCanvas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)


    def update(self, sequence_manager:SequenceManager):
        self.plot.cla() #clear ax
        if not sequence_manager.is_empty_plot():
            sequence_manager.compute_dist_lines()
            scope_data=sequence_manager.get_scope_data()
            self.handle_scope_data(scope_data)

            plot_data_dist=sequence_manager.get_plot_distance_data()
            self.handle_plot_data(plot_data_dist)

            hover_index, hover_y=sequence_manager.get_hover_data_object_distance()#TODO:could be optimized
            if hover_index is not None:
                self.plot.plot(hover_index,
                            hover_y,
                            marker="o", c='aqua')

            chosen_index=sequence_manager.get_chosen_data_object_distance()
            if chosen_index is not None:       
                self.plot.plot(chosen_index,0, marker="o", c='fuchsia')
            
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def handle_plot_data(self,plot_data_dist):
        if plot_data_dist is None:
            return
        for sequence in plot_data_dist:
            self.plot.plot(plot_data_dist[sequence]["xs"],
                           plot_data_dist[sequence]["ys"],
                           marker="x",markersize=5,
                           c=plot_data_dist[sequence]["color"])

    def handle_scope_data(self,scope_data):
        if scope_data is None:
            return
        for sequence in scope_data:
            self.plot.scatter(scope_data[sequence]["xs"], scope_data[sequence]["ys"], marker="o",s=100, c="lightgray")




