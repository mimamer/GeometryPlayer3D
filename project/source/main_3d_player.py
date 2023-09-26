from source.data_input import read_data
from source.Three_Dimensional_Player import Three_Dimensional_Player

if __name__ == "__main__":
    path="/home/michelle/real/3d_player/project/test_data/modified.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    player= Three_Dimensional_Player(data_objects)
    

    player.create_main_window()