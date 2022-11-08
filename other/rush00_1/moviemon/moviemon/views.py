from django.shortcuts import render, redirect
from django.conf import settings as django_settings
import typing
from .game import Game, game_storage, start_new_game
import os
import random


def title_screen(request):
    return render(request, "titlescreen.html", {
        'buttons': {'A': {'link': '/worldmap/new_game/', 'active': True},
                    'B': {'link': '/options/load_game/', 'active': True}},
        'title': 'Moviemon'
    })


def worldmap(request, direction: typing.Optional[str] = None):

    monster_id = False
    if request.method == "GET":
        # Start to create a new game for user
        if 'new_game' in request.path:
            start_new_game()

    current_game: Game = game_storage.get_current_game()

    action = {}
    if direction:
        action = current_game.set_new_player_position(direction)
        if not action:
            action = {}
        if action.get('action', {}).get('type') == 'monster':
            monster_id = action['action'].get('monster_id')
    map_data = current_game.get_data_for_map()
    map_data = {**map_data, **action}

    return render(request, "worldmap.html", {
        'buttons': {'A': {'link': f'/battle/{monster_id}', 'active': monster_id is not False},
                    'select': {'link': '/moviedex'}, 'start': {'link': '/options'},
                    'arrow_top': {'link': '/worldmap/up'}, 'arrow_left': {'link': '/worldmap/left'},
                    'arrow_right': {'link': '/worldmap/right'}, 'arrow_bottom': {'link': '/worldmap/bottom'},
                    },
        "title": "Catch em all",
        **map_data
    })


def battle(request, moviemon_id: str):
    current_game: Game = game_storage.get_current_game()
    moviemon = current_game._moviemons[moviemon_id]
    luck = 50 - moviemon["imdbRating"] * 10 + current_game._player_strength * 5
    check = 1
    if luck < 1:
        luck = 1
    elif luck > 90:
        luck = 90
    if 'throw' in request.path:
        if current_game._movieballs_count > 0:
            if random.randint(1, 100) > luck:
                battle_text = "Throw Failed! Try again!"
                current_game._movieballs_count -= 1
            else:
                battle_text = f"Congrats, You catched {moviemon['Title']}! Press B to return to Worldmap!"
                current_game._captured_movies.append(moviemon['imdbID'])
                current_game._player_strength += 1
                current_game.clear_cell()
                check = 0
        else:
            battle_text = "Oooops! You're out of movieballs! Press B to return to Worldmap!"
            check = 0
    else:
        battle_text = f'{moviemon["Title"]} appeared!'
    game_dict = {**moviemon, 'Luck': luck, 'Movieballs': current_game._movieballs_count, 'Battle_Text': battle_text, 'buttons': {'B': {'link': '/worldmap', 'active': True}}}
    if check:
        game_dict['buttons']['A'] = {'link': f'/battle/{moviemon_id}/throw', 'active': True}
    return render(request, 'battle.html', game_dict)


def moviedex(request):
    direction = None

    current_game = game_storage.get_current_game()
    if request.method == "GET" and request.GET:
        direction = request.GET.get("direction")
    else:
        current_game.moviedex_current = 0

    try:
        selected_pos = current_game.moviedex_current
    except AttributeError:
        current_game.moviedex_current = 0
        selected_pos = 0

    captured_movies = current_game.get_captured_movies()

    if direction == 'down' and selected_pos < len(captured_movies) - 1:
        selected_pos += 1
        current_game.moviedex_current = selected_pos
    if direction == 'up' and selected_pos > 0:
        selected_pos -= 1
        current_game.moviedex_current = selected_pos
    selected_id = current_game.get_movie_id_by_pos(selected_pos)
    movies_to_show = current_game.get_selected_previous_and_next_movie(selected_pos)

    return render(request, "moviedex.html", {
        'buttons': {'A': {'link': f'/moviedex/{selected_id}', 'active': True},
                    'select': {'link': '/worldmap'},
                    'arrow_top': {'link': '/moviedex/up'},
                    'arrow_bottom': {'link': '/moviedex/down'}
                    },
        'title': 'Moviedex',
        'captured_movies': movies_to_show,
        'selected_movie_id': selected_id
    })


def detail(request, moviemon: str):
    if moviemon in ['up', 'down']:
        return redirect(f'/moviedex?direction={moviemon}')
    current_game = game_storage.get_current_game()
    movie = current_game.get_movie(moviemon)
    return render(request, 'detail.html', {
        'buttons': {'B': {'link': '/moviedex', 'active': True}},
        'title': 'Detail',
        'movie': movie
    })


def option(request):
    return render(request, "options.html", {
        'buttons': {'A': {'link': '/options/save_game/', 'active': True, 'text': 'A - Save'},
                    'B': {'link': '/', 'active': True, 'text': 'B - Quit'},
                    'start': {'link': '/worldmap'}},
        'title': 'Options'
    })


def save(request, save_file_name: str = None):

    current_game = game_storage.get_current_game()
    try:
        current_game.selected_pos
    except AttributeError:
        current_game.selected_pos = 0

    if save_file_name == 'up' and current_game.selected_pos > 0:
        current_game.selected_pos -= 1
    elif save_file_name == 'down' and current_game.selected_pos < 2:
        current_game.selected_pos += 1

    folder = os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves')
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    saves = [None, None, None]
    for file in files:
        file_ = file.split('/')[-1]
        if file_.startswith('slotA'):
            score1 = file_.split('_')[1]
            score2 = file_.split('_')[2].split('.')[0]
            score = f"{score1}/{score2}"
            saves[0] = {'filename': file_, 'name': f'Slot A: {score}'}
        elif file_.startswith('slotB'):
            score1 = file_.split('_')[1]
            score2 = file_.split('_')[2].split('.')[0]
            score = f"{score1}/{score2}"
            saves[1] = {'filename': file_, 'name': f'Slot B: {score}'}
        elif file_.startswith('slotC'):
            score1 = file_.split('_')[1]
            score2 = file_.split('_')[2].split('.')[0]
            score = f"{score1}/{score2}"
            saves[2] = {'filename': file_, 'name': f'Slot C: {score}'}

    load_link = f"/options/save_game/{current_game.selected_pos}"

    if request.method == 'POST' and save_file_name not in ['#', 'up', 'down']:
        if save_file_name == "0":
            to_remove: str = None
            for file_ in saves:
                if not file_:
                    continue
                if file_['filename'].startswith('slotA'):
                    to_remove = file_['filename']
                    break
            if to_remove:
                os.remove(os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves', to_remove))
            file = f"slotA_{current_game.get_current_score()}.mmg"
        elif save_file_name == "1":
            to_remove: str = None
            for file_ in saves:
                if not file_:
                    continue
                if file_['filename'].startswith('slotB'):
                    to_remove = file_['filename']
                    break
            if to_remove:
                os.remove(os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves', to_remove))
            file = f"slotB_{current_game.get_current_score()}.mmg"
        elif save_file_name == "2":
            to_remove: str = None
            for file_ in saves:
                if not file_:
                    continue
                if file_['filename'].startswith('slotC'):
                    to_remove = file_['filename']
                    break
            if to_remove:
                os.remove(os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves', to_remove))
            file = f"slotC_{current_game.get_current_score()}.mmg"
        game_storage.dump(current_game, file)

    return render(request, "load.html", {
        'buttons': {'A': {'link': load_link, 'active': True, 'httpmethod': 'post', 'text': "Save"},
                    'B': {'link': '/options', 'active': True, 'text': 'Cancel'},
                    'arrow_top': {'link': '/options/save_game/up', 'active': True},
                    'arrow_bottom': {'link': '/options/save_game/down', 'active': True}
                    },
        'title': 'Save game',
        'savefiles': saves,
        'selected_file_pos': current_game.selected_pos
    })


def load(request, save_file_name: str = None):

    current_game = game_storage.get_current_game()
    if request.method == 'GET' and save_file_name is None:
        current_game.selected_pos = 0

    try:
        current_game.selected_pos
    except AttributeError:
        current_game.selected_pos = 0

    if save_file_name == 'up' and current_game.selected_pos > 0:
        current_game.selected_pos -= 1
    elif save_file_name == 'down' and current_game.selected_pos < 2:
        current_game.selected_pos += 1

    arrow_buttons_status = True

    folder = os.path.join(django_settings.BASE_DIR, 'moviemon', 'saves')
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    saves = [None, None, None]
    for file in files:
        file_ = file.split('/')[-1]
        if file_.startswith('slotA'):
            score1 = file_.split('_')[1]
            score2 = file_.split('_')[2].split('.')[0]
            score = f"{score1}/{score2}"
            saves[0] = {'filename': file_, 'name': f'Slot A: {score}'}
        elif file_.startswith('slotB'):
            score1 = file_.split('_')[1]
            score2 = file_.split('_')[2].split('.')[0]
            score = f"{score1}/{score2}"
            saves[1] = {'filename': file_, 'name': f'Slot B: {score}'}
        elif file_.startswith('slotC'):
            score1 = file_.split('_')[1]
            score2 = file_.split('_')[2].split('.')[0]
            score = f"{score1}/{score2}"
            saves[2] = {'filename': file_, 'name': f'Slot C: {score}'}

    load_target = saves[current_game.selected_pos]['filename'] if saves[current_game.selected_pos] else "#"
    load_link = f"/options/load_game/{load_target}"

    a_text = " Load"
    method = 'post'
    if request.method == 'POST' and save_file_name not in ['#', 'up', 'down']:
        game = game_storage.load(save_file_name)
        game_storage.set_current_game(game)
        load_link = '/worldmap'
        arrow_buttons_status = False
        a_text = "Start Game"
        method = 'get'

    return render(request, "load.html", {
        'buttons': {'A': {'link': load_link, 'active': True, 'httpmethod': method, 'text': a_text},
                    'B': {'link': '/', 'active': arrow_buttons_status},
                    'arrow_top': {'link': '/options/load_game/up', 'active': arrow_buttons_status},
                    'arrow_bottom': {'link': '/options/load_game/down', 'active': arrow_buttons_status}
                    },
        'title': 'Load game',
        'savefiles': saves,
        'selected_file_pos': current_game.selected_pos
    })
