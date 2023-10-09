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
        sequence_manager.compute_dist_lines()
        plot_data_dist=sequence_manager.get_plot_distance_data()
        self.handle_plot_data(plot_data_dist)
        chosen_index=sequence_manager.get_chosen_data_object_distance()
        if chosen_index is not None:       
            self.plot.plot(chosen_index,0, marker="o", c='fuchsia')
        
        hover_index, hover_y=sequence_manager.get_hover_data_object_distance()
        if hover_index is not None:
            self.plot.plot(hover_index,
                        hover_y,
                        marker="o", c='aqua')
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def handle_plot_data(self,plot_data_dist):
        if plot_data_dist is None:
            return
        for line in plot_data_dist:
            self.plot.plot(line[0],line[1],linewidth=1, marker="o", c=line[2])




