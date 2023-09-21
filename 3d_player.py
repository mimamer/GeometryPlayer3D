import matplotlib.pyplot as plt
import PySimpleGUI
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_input import read_data
from mpl_toolkits.mplot3d.art3d import Line3D
from matplotlib.backend_bases import MouseButton

matplotlib.use("TkAgg")
import warnings
warnings.filterwarnings("error")


#dynamisch mit rein tun, falls wert schon da nimm diesen....
class Three_Dimensional_Player:
    def __init__(self):
        self.switch=False
        self.fig=None
        self.ax=None
        self.gen=None
        self.figure_canvas_agg=None
        
        self.x=[]
        self.y=[]
        self.z=[]

        self.line=None
        self.index=0
        self.tmp_index=0
        play_button = PySimpleGUI.Button('Play/Pause')
        back_button = PySimpleGUI.Button('<')
        forward_button = PySimpleGUI.Button('>')
        zoom_in_button = PySimpleGUI.Button('+')
        zoom_out_button = PySimpleGUI.Button('-')
        self.margins=None
        self.root = PySimpleGUI.Window(title="3D Result Player", layout=[[PySimpleGUI.Canvas(key="-CANVAS-")],[back_button, play_button, forward_button, zoom_in_button,zoom_out_button]], finalize=True)
        self.create_figure()
        self.draw_figure()


    def draw_figure(self):
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.root["-CANVAS-"].TKCanvas)
        self.figure_canvas_agg.draw()
        self.figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)


    def create_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d') #ax is a subplot
        #self.ax.set_zlim(-1, 1)
        self.ax.use_sticky_edges=False
        self.margins=self.ax.margins()

    def get_new_lims(self,lim_tuple):#problems when diff is very small
        lim_tuple=self.ax.get_xlim()
        diff=lim_tuple[1]-lim_tuple[0]
        diff=diff/2
        left_lim=lim_tuple[0]+diff
        right_lim=lim_tuple[1]-diff
        if left_lim>=lim_tuple[0] and right_lim<=lim_tuple[1]:
            return left_lim,right_lim
        else:
            return lim_tuple[0], lim_tuple[1]
    
    def set_new_lims(self):
        #again not fixed zoom in, UserWarning automatically expanding does occur instantly,
        # maybe choose a point in the chain and zoom to it, due to cut away data points
        try:
            left_lim, right_lim=self.get_new_lims(self.ax.get_xlim)
            self.ax.set_xlim(left_lim,right_lim)
        except UserWarning as e:
            print(e)
            pass
        try:
            left_lim, right_lim=self.get_new_lims(self.ax.get_ylim)
            self.ax.set_ylim(left_lim,right_lim)
        except UserWarning as e:
            print(e)
            pass
        try:
            left_lim, right_lim=self.get_new_lims(self.ax.get_zlim)
            self.ax.set_zlim(left_lim,right_lim)
        except UserWarning as e:
            print(e)
            pass

    def zoom(self, zoom_value):
        try:
            print(self.margins)
            self.margins=(self.margins[0]+zoom_value,self.margins[1]+zoom_value,self.margins[2]+zoom_value)
            self.plot_actual_data()
        except ValueError: #only for zoom_out ValueError
            self.margins=(-0.49,-0.49,-0.49)
            self.plot_actual_data()

    def zoom_out(self):
        self.zoom(0.01)

    def zoom_in(self):
        self.zoom(-0.01)
        self.set_new_lims()
        
        
    def plot_actual_data(self):
        self.ax.cla() #clear ax
        self.line=Line3D(self.x[:self.tmp_index],self.y[:self.tmp_index],self.z[:self.tmp_index])
        plot_data=self.line.get_data_3d()
        self.ax.plot(plot_data[0], plot_data[1],  plot_data[2],marker="o", markersize=5)
        self.ax.use_sticky_edges=False # can not zoom in adequately
        self.ax.margins(self.margins[0],self.margins[1],self.margins[2])
        self.figure_canvas_agg.draw_idle()


    def run_figure(self):
        if self.switch:
            if self.tmp_index>self.index:
                data_object = next(self.gen)
                self.x.append(data_object[0][0])
                self.y.append(data_object[0][1])
                self.z.append(data_object[0][2])
                self.index+=1
                #sache mit den Quadern fehlt noch...
            
            self.plot_actual_data()
            self.tmp_index+=1



    def backwards(self):
        if self.tmp_index>0:
            self.tmp_index=self.tmp_index-1
            self.plot_actual_data()
    
    def forwards(self):
        if self.tmp_index<self.index:
            self.tmp_index=self.tmp_index+1
            self.plot_actual_data()
        else:
            tmp=self.switch
            self.switch=True
            self.run_figure()
            self.switch=tmp


    def next_value(self,data_objects):
        for i in range(len(data_objects)):
            try:
                yield data_objects[i]

            except StopIteration:
                break

                
    def pause_figure(self):
        self.switch=not self.switch

    def create_main_window(self):

        
        #binding_id = plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event', on_click)
        def on_press(event):
            if event.button=="up":
                #self.figure_canvas_agg.toolbar.zoom() does not work rectangle zoom since toolbar is none
                self.zoom_in()
            elif event.button=="down":
                self.zoom_out()
            print('you pressed', event.button, event.xdata, event.ydata)
            
        plt.connect('scroll_event', on_press)
        plt.connect('button_press_event', on_press)

        while True:
            event, values = self.root.read(timeout=1000)

            if event == PySimpleGUI.WIN_CLOSED:
                break
            if event == "Play/Pause":
                self.pause_figure()
            if event == "<":
                self.switch=False
                self.backwards()

            if event == ">":
                self.switch=False
                self.forwards()

            if event =="+":
                self.switch=False
                self.zoom_in()
            if event =="-":
                self.switch=False
                self.zoom_out()

            if self.switch:
                self.run_figure()

            #print(self.figure_canvas_agg.events)

        self.root.close()

def on_move(event):
    if event.inaxes:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')
def on_click(event):
    if event.button is MouseButton.MIDDLE:
        print('hi')


if __name__ == "__main__":
    path="/home/michelle/real/3d_player/plot_tests/modified.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    player= Three_Dimensional_Player()
    player.gen  = player.next_value(data_objects)

    player.create_main_window()