import copy
import os
import pickle
import random
from dataclasses import dataclass
from enum import Enum
from math import floor, ceil

from singleton_decorator import singleton
from django.conf import settings
from moviedex.service import Moviemon
import numpy as np


def forDjango(cls):
    cls.do_not_call_in_templates = True
    return cls


@forDjango
class GameState(Enum):
    start_screen = 0
    worldmap = 1
    movieball_found = 9
    ready_to_battle = 2
    catch_moviemon = 10
    missed_moviemon = 11
    out_of_movieballs = 12
    in_battle = 3
    moviedex = 4
    moviedex_detail = 5
    saving = 6
    loading = 7
    options = 8


@dataclass
class GameData:
    player_strength: int
    player_position: [int]
    player_movieballs: int
    captured_moviemon_ids: [str]
    non_captured_moviemon_ids: {str}
    movie_info: {str: Moviemon}
    slot_position: int
    state: GameState
    map: [[int]]
    save_slots: [str, str]
    loaded: bool
    current_page: str
    moviemons_on_the_map: int
    movieballs_on_the_map: int

@singleton
class GameManager:

    def __init__(self):
        try:
            self.load_file("current_game.mmg")
        except:
            self.game_data: GameData
            self.load_default_settings()

    def load(self, game_data: GameData):
        self.game_data = game_data
        return self

    def dump(self) -> GameData:
        return self.game_data

    def get_random_movie(self) -> Moviemon:
        return random.choice(tuple(self.game_data.non_captured_moviemon_ids))

    def get_strength(self) -> int:
        return self.game_data.player_strength

    def load_default_settings(self) -> 'GameManager':
        self.game_data = GameData(
            player_strength=settings.DEFAULT_PLAYER_STRENGTH,
            player_position=list(settings.DEFAULT_PLAYER_POSITION),
            player_movieballs=settings.DEFAULT_PLAYER_MOVIEBALLS,
            captured_moviemon_ids=[],
            non_captured_moviemon_ids=copy.copy(settings.MOVIE_IDS),
            movie_info=Moviemon.get_movies(),
            slot_position=0,
            state=GameState.start_screen,
            map=np.zeros((settings.MAP_SIZE[0], settings.MAP_SIZE[1])),
            save_slots=[
                ['Slot A', 'Free'],
                ['Slot B', 'Free'],
                ['Slot C', 'Free']
            ],
            loaded=False,
            current_page='/',
            moviemons_on_the_map=min(len(settings.MOVIE_IDS), max(settings.FRAME_SIZE)),
            movieballs_on_the_map=min(len(settings.MOVIE_IDS), max(settings.FRAME_SIZE))
        )

        for i in range(self.game_data.moviemons_on_the_map):
            self.game_data.map[random.randint(0, settings.MAP_SIZE[0] - 1)][
                random.randint(0, settings.MAP_SIZE[0] - 1)] = 2

        for i in range(self.game_data.movieballs_on_the_map):
            self.game_data.map[random.randint(0, settings.MAP_SIZE[0] - 1)][
                random.randint(0, settings.MAP_SIZE[0] - 1)] = 1

        self.game_data.map[self.game_data.player_position[1], self.game_data.player_position[0]] = -1

        return self

    def get_movie(self, id: int):
        return self.game_data.movie_info[id]

    def save(self, slot_name):
        with open(f"slot{slot_name}_{len(self.game_data.captured_moviemon_ids)}_{len(settings.MOVIE_IDS)}.mmg",
                  "wb") as save_file:
            pickle.dump(self.dump(), save_file)

    def quick_save(self):
        with open("current_game.mmg", "wb") as current_game:
            pickle.dump(self.dump(), current_game)

    def load_file(self, save_file):
        with open(save_file, "rb") as save_file:
            self.load(pickle.load(save_file))

    def frame(self):
        leftX = 0
        rightX = settings.FRAME_SIZE[0]
        topY = 0
        bottomY = settings.FRAME_SIZE[1]
        left_padding = floor(settings.FRAME_SIZE[0] / 2)
        right_padding = ceil(settings.FRAME_SIZE[0] / 2)
        top_padding = floor(settings.FRAME_SIZE[0] / 2)
        bottom_padding = ceil(settings.FRAME_SIZE[0] / 2)
        half_height = settings.FRAME_SIZE[1] // 2
        leftX = min(settings.MAP_SIZE[0] - settings.FRAME_SIZE[0],
                    max(self.game_data.player_position[0] - left_padding, 0))
        rightX = min(settings.MAP_SIZE[0],
                     max(self.game_data.player_position[0] + right_padding, settings.FRAME_SIZE[0]))
        topY = min(settings.MAP_SIZE[1] - settings.FRAME_SIZE[1],
                   max(self.game_data.player_position[1] - top_padding, 0))
        bottomY = min(settings.MAP_SIZE[1],
                      max(self.game_data.player_position[1] + bottom_padding, settings.FRAME_SIZE[1]))

        return self.game_data.map[topY: bottomY, leftX: rightX]

    def move(self, direction):
        self.game_data.map[self.game_data.player_position[1]][self.game_data.player_position[0]] = 0
        if direction == "LEFT":
            self.game_data.move_right = False
            self.game_data.player_position[0] = max(self.game_data.player_position[0] - 1, 0)
        elif direction == "RIGHT":
            self.game_data.move_right = True
            self.game_data.player_position[0] = min(self.game_data.player_position[0] + 1, settings.MAP_SIZE[0] - 1)
        elif direction == "UP":
            self.game_data.player_position[1] = max(self.game_data.player_position[1] - 1, 0)
        elif direction == "DOWN":
            self.game_data.player_position[1] = min(self.game_data.player_position[1] + 1, settings.MAP_SIZE[1] - 1)
        if self.game_data.map[self.game_data.player_position[1]][self.game_data.player_position[0]] == 1:
            self.game_data.state = GameState.movieball_found
        elif self.game_data.map[self.game_data.player_position[1]][self.game_data.player_position[0]] == 2:
            self.game_data.state = GameState.ready_to_battle
        self.game_data.map[self.game_data.player_position[1], self.game_data.player_position[0]] = -1

    def change_moviedex_position(self, value):
        new_position = self.game_data.slot_position + value
        if 0 <= new_position < len(self.game_data.captured_moviemon_ids):
            self.game_data.slot_position = new_position

    def change_slot_position(self, value):
        new_position = self.game_data.slot_position + value
        if 0 <= new_position < 3:
            self.game_data.slot_position = new_position

    def save_game(self):
        slot_pos = self.game_data.slot_position
        self.game_data.save_slots[slot_pos][1] = (
            f'{len(self.game_data.captured_moviemon_ids)}/{len(settings.MOVIE_IDS)}'
        )
        for file in os.listdir(os.getcwd()):
            if file.startswith(f'slot{"ABC"[slot_pos]}'):
                os.remove(file)
        self.save('ABC'[slot_pos])

    def load_game(self):
        pos = self.game_data.slot_position
        slot = self.game_data.save_slots[pos][1]
        if slot == 'Free':
            return
        file_name = f'slot{"ABC"[pos]}/{slot}.mmg'.replace('/', '_')
        self.load_file(file_name)
        self.game_data.loaded = True
        self.game_data.current_page = '/options/load_game'

    def reset_slot_position(self):
        self.game_data.slot_position = 0

    def catch_chance(self, moviemon_id):
        monster_strength = float(self.game_data.movie_info[moviemon_id].rating)
        return int(max(1.0, min(90.0, 50 - monster_strength * 10 + self.game_data.player_strength * 5)))

    def dice_roll(self, catch_chance):
        return catch_chance > random.random() * 100

    def add_random_place_movieball(self):
        self.game_data.map[random.randint(0, settings.MAP_SIZE[0] - 1)][
            random.randint(0, settings.MAP_SIZE[0] - 1)] = 1
        self.game_data.movieballs_on_the_map += 1

    def add_random_place_moviemon(self):
        self.game_data.map[random.randint(0, settings.MAP_SIZE[0] - 1)][
            random.randint(0, settings.MAP_SIZE[0] - 1)] = 2
        self.game_data.moviemons_on_the_map += 1