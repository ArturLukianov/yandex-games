from random import randint, choice
from qrena_base import *

class Item:
    def __init__(self, name, position, in_inventory, texture_number):
        self.name = name
        self.position = position
        self.in_inventory = in_inventory
        self.texture_number = texture_number

    def draw(item, drawing_queue, relative_to=(0,0), screen=None):
        global items_textures
        xr, yr = get_relative_position(item.position, relative_to)
        def _():
            screen.blit(items_textures[item.texture_number], (xr, yr))
        drawing_queue.append((_, (xr,yr)))

    def hint(obj, drawing_queue, relative_to=(0,0), screen=None):
        global tile_width, tile_height, hint_font
        xr, yr = get_relative_position(obj.position, relative_to)
        def _():
            pg.draw.rect(screen, white, (xr - tile_width // 2, yr - tile_height // 4 * 3, tile_width * 2, tile_height // 2))
            pg.draw.rect(screen, black, (xr - tile_width // 2, yr - tile_height // 4 * 3, tile_width * 2, tile_height // 2), 1)
            pg.draw.polygon(screen, white, ((xr - tile_width // 8 + tile_width // 2, yr - tile_height // 4 - 1),
                                            (xr + tile_width // 8 + tile_width // 2, yr - tile_height // 4 - 1),
                                            (xr + tile_width // 2, yr)))
            pg.draw.lines(screen, black, 0,((xr - tile_width // 8 + tile_width // 2, yr - tile_height // 4 - 1),
                                            (xr + tile_width // 2, yr + 3),
                                            (xr + tile_width // 8 + tile_width // 2, yr - tile_height // 4 - 1)
                                            ), 1)
            item_name = hint_font.render(obj.name, 0, black)
            screen.blit(item_name, (xr - tile_width // 2 + 3, yr - tile_height // 4 * 3 - 1))
        drawing_queue.append((_, (xr - tile_width // 2 + 3, yr - tile_height // 4 * 3 - 1)))
        
class Weapon(Item):
    def __init__(self, name, position, in_inventory, texture_number, attack):
        self.attack = attack
        self.range = 32
        super().__init__(name, position, in_inventory, texture_number)

class Wear(Item):
    def __init__(self, name, position, in_inventory, texture_number, weared, offset):
        super().__init__(name, position, in_inventory, texture_number)
        self.offset = offset
        self.weared = False
