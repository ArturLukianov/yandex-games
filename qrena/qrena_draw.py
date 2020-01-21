from qrena_constants import *
from qrena_base import *
from qrena_items import *
from qrena_characters import *

def draw_background(relative_to, screen=None):
    global background_textures, tiles_in_row, tiles_in_col, tile_width, tile_height
    xr = relative_to[0] % tile_width
    yr = relative_to[1] % tile_height
    for i in range(tiles_in_row + 1):
        for j in range(tiles_in_col + 1):
            screen.blit(background_textures[0], (xr + (j - 1) * tile_width, yr + (i - 1) * tile_height))      


def draw_stats(hero, screen=None):
    global screen_width, screen_height, tile_width, tile_height, items_textures, stats_font, special_textures
    pg.draw.rect(screen, white, (tile_width // 2, screen_height - tile_height * 3 - tile_height // 2, screen_width - tile_width, tile_height * 3))
    pg.draw.rect(screen, black, (tile_width // 2, screen_height - tile_height * 3 - tile_height // 2, screen_width - tile_width, tile_height * 3), 1)
    pg.draw.rect(screen, red, (tile_width + 4, screen_height - tile_height * 3, hero.health - 8, tile_height // 2))
    screen.blit(special_textures[1], (tile_width, screen_height - tile_height * 3))
    screen.blit(stats_font.render("HP: (" + str(hero.health) + "/100)", 0, black), (tile_width * 5, screen_height - tile_height * 3 - tile_height // 8))
    pg.draw.rect(screen, blue, (tile_width + 4, screen_height - tile_height * 2 - tile_height // 2, hero.mana - 8, tile_height // 2))
    screen.blit(special_textures[1], (tile_width, screen_height - tile_height * 2 - tile_height // 2))
    screen.blit(stats_font.render("MP: (" + str(hero.mana) + "/100)", 0, black), (tile_width * 5, screen_height - tile_height * 2 - tile_height // 8 * 5))
    screen.blit(special_textures[0], (tile_width, screen_height - tile_height * 2))
    screen.blit(pg.transform.scale(items_textures[hero.current_weapon().texture_number], (tile_width - 4, tile_height - 4)), (tile_width + 2, screen_height - tile_height * 2 + 2))
    screen.blit(stats_font.render("ATK: " + str(hero.current_weapon().attack), 0, black), (tile_width * 8, screen_height - tile_height * 3 - tile_height // 8))


def draw_inventory(hero, cursor_pos, screen=None):
    global inv_item_name_font, cursor_v, screen_width, screen_height, tile_width, tile_height, items_textures, tiles_in_row, special_textures
    pg.draw.rect(screen, white, (tile_width, tile_height, screen_width - tile_width * 2, screen_height - tile_height * 2))
    pg.draw.rect(screen, black, (tile_width, tile_height, screen_width - tile_width * 2, screen_height - tile_height * 2), 1)
    for i in range(3):
        for j in range(tiles_in_row - 4):
            pg.draw.rect(screen, black, (tile_width * 2 + j * tile_width, tile_height * 2 + i
                                         * tile_height, tile_width, tile_height), 1)
    for i in range(len(hero.inventory)):
        screen.blit(pg.transform.scale(items_textures[hero.inventory[i].texture_number], (tile_width - 4, tile_height - 4)),
                    (tile_width * 2 + (i % (tiles_in_row - 4)) * tile_width + 2, tile_height * 2 + (i // (tiles_in_row - 4) * tile_height + 2)))
    screen.blit(special_textures[0],
                (tile_width * 2 + cursor_pos[0] // cursor_v * tile_width,
                 tile_height * 2 + cursor_pos[1] // cursor_v * tile_height))
    item_ind = cursor_pos[0] // cursor_v + cursor_pos[1] // cursor_v * (tiles_in_row -4)
    if item_ind >= len(hero.inventory):
        screen.blit(inv_item_name_font.render("Empty", 0, black), (tile_width * 3, tile_height * 5))
    else:
        target_item = hero.inventory[item_ind]
        item_text = items_textures[target_item.texture_number]
        screen.blit(inv_item_name_font.render(target_item.name, 0, black), (tile_width * 3, tile_height * 5))
        pg.draw.rect(screen, black, (screen_width - tile_width * 9, tile_height * 6, tile_width * 6, tile_height * 6), 1)
        item_text = pg.transform.rotate(item_text, -45)
        item_text = pg.transform.scale(item_text, (tile_width * 6 - 4, tile_height * 6 - 4))
        screen.blit(item_text, (screen_width - tile_width * 9 + 2, tile_height * 6 + 2))
        if type(target_item) == Weapon:
            screen.blit(inv_stat_font.render("ATK: " + str(target_item.attack), 0, black), (tile_width * 3, tile_height * 8))
            if hero.weapon_index == item_ind:
                screen.blit(inv_stat_font.render("Using", 0, green), (tile_width * 3, tile_height * 9))

