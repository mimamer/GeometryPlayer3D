from data_input import read_data
from Three_Dimensional_Player import Three_Dimensional_Player

if __name__ == "__main__":
    path="/home/michelle/real/3d_player/plot_tests/modified.txt"
    data_objects=read_data(path)
    data_objects=data_objects['data']
    player= Three_Dimensional_Player()
    player.gen  = player.next_value(data_objects)

    player.create_main_window()