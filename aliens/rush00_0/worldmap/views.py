from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from Moviemon.GameManager import GameState, GameManager
from Moviemon.mixins import GamedataContextMixin


game_manager: GameManager = GameManager()


class WorldmapView(GamedataContextMixin, TemplateView):
    template_name = "worldmap.html"

    def get(self, request, *args, **kwargs):
        if game_manager.game_data.current_page != '/worldmap':
            return redirect(game_manager.game_data.current_page)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        key = request.POST.get('KEY')
        if game_manager.game_data.state == GameState.worldmap:
            if key == 'START':
                game_manager.game_data.current_page = "/options"
                return redirect('/options')
            elif key == 'SELECT':
                game_manager.game_data.current_page = "/moviedex"
                return redirect('/moviedex')
            elif (key == "UP" or key == "DOWN" or key == "RIGHT" or key == "LEFT"):
                game_manager.move(key)
        elif game_manager.game_data.state == GameState.ready_to_battle:
            if key == 'A':
                page = f'/battle/{game_manager.get_random_movie()}'
                game_manager.game_data.current_page = page
                game_manager.game_data.state = GameState.in_battle
                game_manager.game_data.moviemons_on_the_map -= 1
                if game_manager.game_data.moviemons_on_the_map < len(game_manager.game_data.non_captured_moviemon_ids):
                    game_manager.add_random_place_moviemon()
                return redirect(page)
        elif game_manager.game_data.state == GameState.movieball_found:
            if key == 'A':
                game_manager.game_data.movieballs_on_the_map -= 1
                game_manager.game_data.player_movieballs += 1
                game_manager.game_data.state = GameState.worldmap
                game_manager.add_random_place_movieball()
        return HttpResponseRedirect(request.path_info)
