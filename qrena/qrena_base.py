from qrena_constants import *

def get_relative_position(position, relative_to):
    global screen_width, screen_height, tile_width, tile_height
    xr = relative_to[0] - position[0] + screen_width // 2 - tile_width // 2
    yr = relative_to[1] - position[1] + screen_height // 2 - tile_height // 2
    return xr, yr

def distance_le(point1, point2, than):
    xd = abs(point1[0] - point2[0])
    yd = abs(point1[1] - point2[1])
    if xd ** 2 + yd ** 2 <= than ** 2:
        return True
    return False
