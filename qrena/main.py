import pygame as pg
from random import randint, choice

from qrena_constants import *
from qrena_items import *
from qrena_characters import *
from qrena_draw import *
from qrena_base import *
from qrena_buildings import *

main_hero = Hero("You", 100, 100, (-30, -30), [])

characters_on_map = [NPC("Wizard", 100, 100, (50, 50), [Wear("Wizard's hat", (0, 0), True, 2, True, (1, 15))]),
                     Enemy("Slime", 1, 1, (-50, -50), [], [[pg.image.load("slime.png"),
                                                            pg.transform.flip(pg.image.load("slime.png"), 1, 0),
                                                            pg.image.load("slime_go.png"),
                                                            pg.transform.flip(pg.image.load("slime_go.png"), 1, 0)],
                                                                                         {"stand":{"right":1, "left":0},
                                                                                          "go":{"right":[1,3], "left":[0,2]},
                                                                                          }])]
items_on_map = [Weapon("Saber", (-100, -100), False, 0, 10), Weapon("Stick", (-200, -200), False, 3, 3)]
buildings_on_map = [Building(0,0,
                             [Tile(background_textures[1], ((0, 0, 28, 28),))],
                             [Tile(wall_textures[0], ((0, 0, 28, 7),)),
                              Tile(wall_textures[1], ((28 - 7, 0, 7, 28),)),
                              Tile(wall_textures[2], ((0, 0, 7, 28),)),
                              Tile(wall_textures[0], ((0, 0, 28, 7),(28-7, 0, 7, 28))),
                              Tile(wall_textures[0], ((0, 0, 28, 7),(0, 0, 7, 28))),
                              Tile(wall_textures[3], ((0, 0, 28, 7),)),
                              Tile(wall_textures[4], ((0, 0, 28, 7),)),
                              Tile(door_textures[0], ((0, 0, 28, 28),)),
                              ],
                             [[0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0],],
                             [[4,7,0,0,0,3],
                              [2,-1,-1,-1,-1,1],
                              [2,-1,-1,-1,-1,1],
                              [2,-1,-1,-1,-1,1],
                              [2,-1,-1,-1,-1,1],
                              [6,0,0,0,0,5]
                              ],
                             [])]

pg.init()

screen = pg.display.set_mode((screen_width, screen_height))#, pg.FULLSCREEN)
drawing_queue = []
roof_queue = []
special_queue = []
background_queue = []

while game_running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game_running = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_DOWN:
                yv = 1
                K_DOWN_PRESSED = True
            if e.key == pg.K_UP:
                yv = -1
                K_UP_PRESSED = True
            if e.key == pg.K_RIGHT:
                xv = 1
                K_RIGHT_PRESSED = True
            if e.key == pg.K_LEFT:
                xv = -1
                K_LEFT_PRESSED = True
            if e.key == pg.K_SPACE:
                if not inventory_open:
                    if not main_hero.attacking:
                        main_hero.reset_attacking_frame()
                    main_hero.attacking = True
            if e.key == pg.K_p:
                if not inventory_open:
                    for item in items_can_interact:
                        main_hero.inventory.append(item)
                    for item in items_can_interact:
                        del items_on_map[items_on_map.index(item)]
            if e.key == pg.K_i:
                inventory_open = not inventory_open
                cursor_pos = (0, 0)
            if e.key == pg.K_x:
                if not inventory_open:
                    main_hero.change_weapon_next()
            if e.key == pg.K_ESCAPE:
                game_running = False
            if e.key == pg.K_c:
                if not inventory_open:
                    for character in characters_can_interact:
                        print(character.speak(main_hero))
        if e.type == pg.KEYUP:
            if e.key == pg.K_DOWN:
                if yv == 1:
                    yv = 0
                    if K_UP_PRESSED:
                        yv = -1
                K_DOWN_PRESSED = False
            if e.key == pg.K_UP:
                if yv == -1:
                    yv = 0
                    if K_DOWN_PRESSED:
                        yv = 1
                K_UP_PRESSED = False
            if e.key == pg.K_RIGHT:
                if xv == 1:
                    xv = 0
                    if K_LEFT_PRESSED:
                        xv = -1
                K_RIGHT_PRESSED = False
            if e.key == pg.K_LEFT:
                if xv == -1:
                    xv = 0
                    if K_RIGHT_PRESSED:
                        xv = 1
                K_LEFT_PRESSED = False
    if not inventory_open:    
        main_hero.delta_move(-xv * v, -yv * v, buildings_on_map)
        if main_hero.attacking:
            main_hero.next_attacking_frame()
            if main_hero.attacking_frame == 0:
                main_hero.attacking = False
    else:
        previous_position = cursor_pos
        next_position = list(previous_position)
        next_position[0] += xv
        next_position[1] += yv
        next_position[0] = max(0, min(next_position[0], (tiles_in_row - 4) * cursor_v - 1))
        next_position[1] = max(0, min(next_position[1], 3 * cursor_v - 1))
        cursor_pos = tuple(next_position)
    drawing_queue = []
    special_queue = []
    background_queue = []
    items_can_interact = []
    characters_can_interact = []
    for building in buildings_on_map:
        building.draw(screen, drawing_queue, background_queue, relative_to=main_hero.position)
    for item in items_on_map:
        item.draw(drawing_queue, relative_to=main_hero.position, screen=screen)
        if distance_le(item.position, main_hero.position, 32):
            item.hint(special_queue, relative_to=main_hero.position, screen=screen)
            items_can_interact.append(item)
    for character in characters_on_map:
        character.draw(drawing_queue, relative_to=main_hero.position, screen=screen)
        if distance_le(character.position, main_hero.position, 32):
            character.hint(special_queue, relative_to=main_hero.position, screen=screen)
            characters_can_interact.append(character)
        character.live(buildings_on_map)
    main_hero.draw(drawing_queue, relative_to=main_hero.position, screen=screen)
    drawing_queue.sort(key=lambda x:x[1][1])
    special_queue.sort(key=lambda x:x[1][1])
    screen.fill(black)
    draw_background(relative_to=main_hero.position, screen=screen)
    for el in background_queue:
        el[0]()
    for el in drawing_queue:
        el[0]()
    for el in special_queue:
        el[0]()
    draw_stats(main_hero, screen=screen)
    if inventory_open:
        draw_inventory(main_hero, cursor_pos, screen=screen)
    pg.display.flip()
    game_clock.tick(fps)

pg.quit()
