import pygame as pg

cursor_v = 3
tile_width = 28
tile_height = 28
tiles_in_row = 25
tiles_in_col = 25
screen_width = tile_width * tiles_in_row
screen_height = tile_height * tiles_in_col
fps = 30
cursor_pos = (0, 0)

game_running = True

K_DOWN_PRESSED = False
K_UP_PRESSED = False
K_LEFT_PRESSED = False
K_RIGHT_PRESSED = False
game_clock = pg.time.Clock()

inventory_open = False
items_can_interact = []
characters_can_interact = []

xv = 0
yv = 0
v = 2

black = (0, 0, 0)
white = (255, 255, 255)
red = (250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)

pg.init()
hint_font = pg.font.Font("uni0553.ttf", tile_height // 2 - 4)
stats_font = hint_font
inv_item_name_font = pg.font.Font("uni0553.ttf", tile_height * 2)
inv_stat_font = pg.font.Font("uni0553.ttf", tile_height)
special_textures = [pg.image.load("inv_choice.png"),
                    pg.image.load("bar.png")]
background_textures = [pg.image.load("floor.png"),
                       pg.image.load("wooden_floor.png")]
background_textures = [pg.transform.scale(i, (tile_width, tile_height)) for i in background_textures]
wall_textures = [pg.image.load("wall.png"),
                 pg.image.load("wall_side.png"),
                 pg.transform.flip(pg.image.load("wall_side.png"), 1, 0),
                 pg.image.load("wall_corner.png"),
                 pg.transform.flip(pg.image.load("wall_corner.png"), 1, 0)
                 ]
door_textures = [pg.image.load("door.png")]
character_textures = [pg.image.load("dude_right.png"),
                      pg.image.load("dude_left.png"),
                      pg.image.load("dude_go_right1.png"),
                      pg.image.load("dude_go_right2.png"),
                      pg.image.load("dude_go_left1.png"),
                      pg.image.load("dude_go_left2.png")]
character_textures = [pg.transform.scale(i, (tile_width, tile_height)) for i in character_textures]
items_textures = [pg.image.load("saber.png"),
                  pg.image.load("hand.png"),
                  pg.image.load("wizard_hat.png"),
                  pg.image.load("stick.png")]
#items_textures = [pg.transform.scale(i, (tile_width, tile_height)) for i in items_textures]
