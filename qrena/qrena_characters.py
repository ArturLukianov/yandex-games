from random import randint, choice
from qrena_items import *
from qrena_constants import *
from qrena_base import *

class Character:
    def __init__(self, name, health, mana, position, inventory):
        self.name = name
        self.health = health
        self.mana = mana
        self.position = position
        self.frame = 0
        self.direction = "right"
        self.action = "stand"
        self.frames = 0
        self.inventory = inventory
        self.weapon_index = -1
        self.attacking = False
        self.attacking_frame = 0
        self.lock = False

    def get_wear(self):
        res = []
        for item in self.inventory:
            if type(item) == Wear:
                res.append(item)
        return res

    def weapons_count(self):
        weapons = 0
        for item in self.inventory:
            if type(item) is Weapon:
                weapons += 1
        return weapons

    def next_weapon_index(self):
        for i in range(self.weapon_index + 1, len(self.inventory)):
            if type(self.inventory[i]) == Weapon:
                return i
        return -1

    def next_weapon(self):
        nwi = self.next_weapon_index()
        if nwi == -1:
            return Weapon("Hand", (0,0), True, 1, 1)
        return self.inventory[nwi]

    def current_weapon(self):
        if self.weapon_index == -1:
            return Weapon("Hand", (0, 0), True, 1, 1)
        return self.inventory[self.weapon_index]

    def change_weapon_next(self):
        self.weapon_index = self.next_weapon_index()

    def reset_frames(self):
        self.frames = 0

    def next_frame(self):
        self.frames += 1
        if self.action == "go":
            if self.frames == 3:
                self.frame = (self.frame + 1) % 2
                self.reset_frames()

    def reset_attacking_frame(self):
        self.attacking_frame = 0

    def next_attacking_frame(self):
        self.attacking_frame = (self.attacking_frame + 20) % 120

    def delta_move(self, dx, dy, buildings_on_map):
        if self.lock:
            dx = 0
            dy = 0
        if dx != 0 or dy != 0:
            if self.action == "go":
                self.next_frame()
            else:
                self.action = "go"
                self.reset_frames()
            if dx > 0:
                self.direction = "left"
            elif dx < 0:
                self.direction = "right"
        else:
            self.action = "stand"
            self.reset_frames()
        self.position = (self.position[0] + dx, self.position[1])
        for building in buildings_on_map:
            if building.collides(self.position):
                self.position = (self.position[0] - dx, self.position[1])
                break
        self.position = (self.position[0], self.position[1] + dy)
        for building in buildings_on_map:
            if building.collides(self.position):
                self.position = (self.position[0], self.position[1] - dy)
                break

    def draw(character, queue, relative_to=(0,0), screen=None):
        global character_textures
        xr, yr = get_relative_position(character.position, relative_to)
        def _():
            texture_number = 0
            lefted = 0
            if character.direction == "left":
                lefted = 1
            if character.action == "stand":
                if character.direction == "right":
                    texture_number = 0
                else:
                    texture_number = 1
            if character.action == "go":
                direction_add = 0
                if character.direction == "left":
                    direction_add = 2
                texture_number = 2 + direction_add + character.frame
            screen.blit(character_textures[texture_number], (xr, yr))
            for item in character.get_wear():
                ixr = xr - item.offset[0]
                if lefted:
                    ixr = xr + tile_width + item.offset[0] - items_textures[item.texture_number].get_rect().w
                screen.blit(pg.transform.flip(items_textures[item.texture_number], lefted, 0), (ixr, yr - item.offset[1]))
            if character.attacking:
                direction_add = 1
                if character.direction == "left":
                    direction_add = -1
                offset_vector = pg.math.Vector2(0, -24)
                rotated_offset_vector = offset_vector.rotate(direction_add * character.attacking_frame)
                weapon= pg.transform.rotozoom(items_textures[character.current_weapon().texture_number], -character.attacking_frame, 1)
                if character.direction == "left":
                    weapon = pg.transform.flip(weapon, 1, 0)
                screen.blit(weapon, rotated_offset_vector + (xr - 4, yr))
        queue.append((_, (xr, yr)))

    def hint(obj, queue, relative_to=(0,0), screen=None):
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
        queue.append((_, (xr - tile_width // 2 + 3, yr - tile_height // 4 * 3 - 1)))

class Hero(Character):
    pass


class NPC(Character):

    target = None
    point = (50, 50)
    stand_time = 0

    def live(self, buildings_on_map):
        if (self.target is None or self.target == self.position) and self.stand_time == 0:
            self.target = (self.point[0] + randint(-30, 30), self.point[1] + randint(-30, 30))
            self.stand_time = randint(10, 200)
        if self.stand_time == 0 or (self.target is not None and self.target != self.position):
            dx = self.target[0] - self.position[0]
            dy = self.target[1] - self.position[1]
            dx = min(1, max(-1, dx))
            dy = min(1, max(-1, dy))
            self.delta_move(dx, dy, buildings_on_map)
        else:
            self.stand_time -= 1
            self.delta_move(0, 0, buildings_on_map)

    def speak(self, other):
        if type(other) == Hero:
            return "Hello, Hero!"
        return "???"

class Enemy(Character):
    target = None
    point = (-50, -50)
    stand_time = 0

    def __init__(self, name, health, mana, position, inventory, t):
        super().__init__(name, health, mana, position, inventory)
        self.t = t

    def live(self, buildings_on_map):
        if (self.target is None or self.target == self.position) and self.stand_time == 0:
            self.target = (self.point[0] + randint(-30, 30), self.point[1] + randint(-30, 30))
            self.stand_time = randint(10, 200)
        if self.stand_time == 0 or (self.target is not None and self.target != self.position):
            dx = self.target[0] - self.position[0]
            dy = self.target[1] - self.position[1]
            dx = min(1, max(-1, dx))
            dy = min(1, max(-1, dy))
            self.delta_move(dx, dy, buildings_on_map)
        else:
            self.stand_time -= 1
            self.delta_move(0, 0, buildings_on_map)

    def speak(self, other):
        if type(other) == Hero:
            return "Tcht!"
        return "???"

    def draw(character, queue, relative_to=(0,0), screen=None):
        global character_textures
        xr, yr = get_relative_position(character.position, relative_to)
        def _():
            texture_number = 0
            lefted = 0
            if character.direction == "left":
                lefted = 1
            if character.action == "stand":
                if character.direction == "right":
                    texture_number = character.t[1]["stand"]["right"]
                else:
                    texture_number = character.t[1]["stand"]["left"]
            if character.action == "go":
                if character.direction == "left":
                    texture_number = character.t[1]["go"]["left"][character.frame]
                else:
                    texture_number = character.t[1]["go"]["right"][character.frame]
            screen.blit(character.t[0][texture_number], (xr, yr))
            for item in character.get_wear():
                ixr = xr - item.offset[0]
                if lefted:
                    ixr = xr + tile_width + item.offset[0] - items_textures[item.texture_number].get_rect().w
                screen.blit(pg.transform.flip(items_textures[item.texture_number], lefted, 0), (ixr, yr - item.offset[1]))
            if character.attacking:
                direction_add = 1
                if character.direction == "left":
                    direction_add = -1
                offset_vector = pg.math.Vector2(0, -24)
                rotated_offset_vector = offset_vector.rotate(direction_add * character.attacking_frame)
                weapon= pg.transform.rotozoom(items_textures[character.current_weapon().texture_number], -character.attacking_frame, 1)
                if character.direction == "left":
                    weapon = pg.transform.flip(weapon, 1, 0)
                screen.blit(weapon, rotated_offset_vector + (xr - 4, yr))
        queue.append((_, (xr, yr)))

    def next_frame(self):
        self.frames += 1
        if self.action == "go":
            if self.frames == len(self.t[1]["go"]["right"]):
                self.frame = (self.frame + 1) % 2
                self.reset_frames()
