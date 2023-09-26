from source.utils import read_data
from source.graphanimator3d import GraphAnimator3D

if __name__ == "__main__":
    path="/home/michelle/real/3d_player/project/test_data/modified.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    player= GraphAnimator3D(data_objects)
    

    player.create_main_window()