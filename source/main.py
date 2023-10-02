from source.utils import open_dataobjects,open_dataobjects_testformat, open_dataobjects_minus, open_dataobjects_2
from source.geometryplayer3d import GeometryPlayer3D

if __name__ == "__main__":
    player= GeometryPlayer3D(open_dataobjects_testformat())
    
    player.main_loop()