from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from Moviemon.mixins import GamedataContextMixin
from Moviemon.GameManager import GameManager, GameState

game_manager: GameManager = GameManager()


class BattleView(GamedataContextMixin, TemplateView):
    template_name = "battle.html"

    def get(self, request, *args, **kwargs):
        if game_manager.game_data.current_page != f'/battle/{kwargs["moviemon_id"]}':
            return redirect(game_manager.game_data.current_page)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        moviemon_id = context["moviemon_id"]
        context["movie_info"] = game_manager.game_data.movie_info[moviemon_id]
        context["catch_chance"] = game_manager.catch_chance(moviemon_id)
        return context

    def post(self, request, *args, **kwargs):
        key = request.POST.get('KEY')
        if key == "B":
            game_manager.game_data.state = GameState.worldmap
            game_manager.game_data.current_page = "/worldmap"
            return redirect('/worldmap')
        elif key == "A" and game_manager.game_data.state == GameState.in_battle or game_manager.game_data.state == GameState.missed_moviemon:
            if game_manager.game_data.player_movieballs > 0:
                game_manager.game_data.player_movieballs -= 1
                moviemon_id = kwargs["moviemon_id"]
                catch_chance = game_manager.catch_chance(moviemon_id)
                if game_manager.dice_roll(catch_chance):
                    game_manager.game_data.state = GameState.catch_moviemon
                    game_manager.game_data.non_captured_moviemon_ids.discard(moviemon_id)
                    game_manager.game_data.captured_moviemon_ids.append(moviemon_id)
                    game_manager.game_data.player_strength += 1
                else:
                    game_manager.game_data.state = GameState.missed_moviemon
            else:
                game_manager.game_data.state = GameState.out_of_movieballs
        return HttpResponseRedirect(request.path_info)
