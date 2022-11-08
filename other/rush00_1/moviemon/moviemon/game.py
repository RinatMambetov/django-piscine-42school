import pickle
import os
import random
import typing

from django.conf import settings as django_settings
from .imdb_api import collect_imdb_data


class Game:

    PLAYER = 1
    MONSTER = 2
    POKEBALL = 3

    _max_pokeballs_count = 25

    def __init__(self,
                 current_point: tuple[int, int],
                 movieballs_count: int,
                 moviemons: dict[str, dict[str, any]]):
        self._field_size = 15
        self._current_position = current_point
        self._movieballs_count = movieballs_count
        self._moviemons: dict[str, dict] = moviemons
        self._enemies_count: int = 15
        self._captured_movies = []
        self._game_map: typing.Optional[list[list[int]]] = None
        self._player_strength = 1

    def dump(self, game_name="current"):
        GameManager.dump(self, game_name)

    def init_game_map(self) -> None:
        game_map = []
        for i in range(self._field_size):
            game_map.append([0 for _ in range(self._field_size)])
        y_pos, x_pos = self._current_position
        max_poke_count = self._max_pokeballs_count
        max_enemy_count = self._enemies_count
        for i, row in enumerate(game_map):
            for j, col in enumerate(row):
                if (i, j) == (y_pos, x_pos):
                    continue
                value = random.choices([0, 2, 3], [0.76, 0.1, 0.14])[0]
                if value == self.POKEBALL:
                    if max_poke_count <= 0:
                        value = self.MONSTER
                    max_poke_count -= 1
                if value == self.MONSTER:
                    if max_enemy_count <= 0:
                        continue
                    max_enemy_count -= 1

                game_map[i][j] = value
        enemy_count = 0
        poke_count = 0
        for row in game_map:
            for cell in row:
                if cell == self.MONSTER:
                    enemy_count += 1
                if cell == self.POKEBALL:
                    poke_count += 1
        self._game_map = game_map
        return

    def set_new_player_position(self, direction: str) -> typing.Optional[dict]:
        y_pos, x_pos = self._current_position
        if direction == 'up':
            y_pos -= 1
        elif direction == 'left':
            x_pos -= 1
        elif direction == 'right':
            x_pos += 1
        elif direction == 'bottom':
            y_pos += 1
        else:
            return
        if not 0 <= x_pos < self._field_size:
            return
        if not 0 <= y_pos < self._field_size:
            return
        self._current_position = (y_pos, x_pos)

        action = self.determine_action()
        self.dump()
        return action

    def determine_action(self) -> dict:
        y_pos, x_pos = self._current_position
        if self._game_map[y_pos][x_pos] == self.MONSTER:
            movie = self.get_random_movie()
            return {"action": {
                "type": "monster", "monster_id": movie['imdbID'],
                'message':
                    f'Monviemonster "{movie["Title"]}" found! '
                    f'{"Fight him!" if self._player_strength + 3 > float(movie["imdbRating"]) else "Run! Fly you fool! It is too strong!"}'}}
        if self._game_map[y_pos][x_pos] == self.POKEBALL:
            poke_count = random.randint(10, 20)
            self._game_map[y_pos][x_pos] = 0
            self._movieballs_count += poke_count
            return {"action": {"type": "ball", 'message': f'Found {poke_count} movieballs!'}}
        return {}

    def get_random_movie(self) -> dict[str, any]:
        free_movies = list(set(self._moviemons.keys()) - set(self._captured_movies))
        movie_key = random.choice(free_movies)
        random_movie = self._moviemons[movie_key]
        return random_movie

    def clear_cell(self):
        y_pos, x_pos = self._current_position
        self._game_map[y_pos][x_pos] = 0

    def get_strength(self) -> int:
        return self._player_strength

    def get_movie(self, movie_id: str) -> dict[str, any]:
        return self._moviemons[movie_id]

    def get_movie_id_by_pos(self, position_id: int) -> typing.Optional[str]:
        if position_id > len(self._captured_movies):
            return
        return self._captured_movies[position_id]

    def get_selected_previous_and_next_movie(self, position_id):
        captured_size = len(self._captured_movies)
        res = []
        if captured_size > 3:
            movie_ids = []
            movie_ids.extend(self._captured_movies[position_id - 1:position_id + 2])
            if len(res) != 3:
                if position_id == captured_size - 1:
                    movie_ids.insert(0, self._captured_movies[position_id - 2])
                elif position_id == 0:
                    movie_ids.append(self._captured_movies[position_id])
                    movie_ids.append(self._captured_movies[position_id + 1])
                    movie_ids.append(self._captured_movies[position_id + 2])
            for movie_id in movie_ids:
                res.append(self._moviemons[movie_id])
        else:
            for val in self._captured_movies:
                res.append(self._moviemons[val])
        return res

    def get_captured_movies(self) -> list:
        captured = []
        for movie_id in self._captured_movies:
            captured.append(self._moviemons[movie_id])
        return captured

    def save_game(self, savefile_id: int) -> None:

        if savefile_id == 1:
            filename = "slotA_{captured}_{total}"
        elif savefile_id == 2:
            filename = "slotB_{captured}_{total}"
        elif savefile_id == 3:
            filename = "slotC_{captured}_{total}"
        else:
            return

        GameManager.dump(self, filename)

    def get_current_score(self):
        return f"{len(self._captured_movies)}_{self._enemies_count}"

    def get_data_for_map(self) -> dict[str, any]:
        map_template = []
        for i, row in enumerate(self._game_map):
            new_row = []
            for j, cell in enumerate(row):
                if (i, j) == self._current_position:
                    new_row.append(1)
                else:
                    new_row.append(0)
            map_template.append(new_row)

        return {
            'map_data': {
                'player_strength': self._player_strength,
                'pokeballs': self._movieballs_count,
                'captured': f"{len(self._captured_movies)} / {self._enemies_count}",
                'field': map_template
            }
        }


class GameManager:

    def __init__(self, game=None):
        self._current_game = game

    def get_current_game(self) -> Game:
        if self._current_game is None:
            self._current_game = self.load()
        return self._current_game

    def set_current_game(self, game=None) -> None:
        if self._current_game is None and game is None:
            game = self.load()
        self._current_game = game

    @classmethod
    def load(cls, filename: str = "current"):
        filepath = os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'wb'):
                pass
        with open(filepath, 'rb') as f:
            game_instance = pickle.load(f)
        return game_instance

    @classmethod
    def dump(cls, game: Game, filename="current") -> None:
        filepath = os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves', filename)
        with open(filepath, 'wb') as f:
            pickle.dump(game, f, protocol=pickle.HIGHEST_PROTOCOL)


game_storage = GameManager()


def start_new_game():
    imdb_data = collect_imdb_data()
    game = Game((random.randint(0, 15), random.randint(0, 15)), 15, imdb_data)
    game.init_game_map()
    game_storage.set_current_game(game)
    game.dump()
    return game


if __name__ == '__main__':
    start_new_game()
