import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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


    def update(self, sequence_manager, colors):
        self.plot.cla() #clear ax
        sequence_manager.set_actual_plot_distance_data(self.plot,colors)
        sequence_manager.set_actual_chosen_data_object_distance(self.plot)
        sequence_manager.set_actual_hover_data_object_distance(self.plot)
        self.canvas.draw_idle()
        self.canvas.flush_events()

