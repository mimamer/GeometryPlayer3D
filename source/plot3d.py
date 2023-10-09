import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    
    def update(self, sequence_manager,colors):
        self.plot.cla()
        sequence_manager.set_actual_plot_data_3d(self.plot,colors)
        sequence_manager.set_actual_chosen_data_object_3d(self.plot)
        sequence_manager.set_actual_hover_data_object_3d(self.plot)
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