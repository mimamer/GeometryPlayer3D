from source.utils import open_dataobjects, open_dataobjects_minus
from source.geometryplayer3d import GeometryPlayer3D

if __name__ == "__main__":
    player= GeometryPlayer3D(open_dataobjects(),open_dataobjects_minus())
    
    player.create_main_window()