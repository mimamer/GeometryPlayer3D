from source.utils import open_dataobjects, open_dataobjects_minus
from source.graphanimator3d import GraphAnimator3D

if __name__ == "__main__":
    player= GraphAnimator3D(open_dataobjects(),open_dataobjects_minus())
    
    player.create_main_window()