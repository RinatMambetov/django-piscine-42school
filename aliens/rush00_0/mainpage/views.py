import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from Moviemon.GameManager import GameManager, GameState
from Moviemon.mixins import GamedataContextMixin

game_manager: GameManager = GameManager()


class IndexView(GamedataContextMixin, generic.TemplateView):
    template_name = 'mainpage/index.html'

    def get(self, request, *args, **kwargs):
        if game_manager.game_data.current_page != '/':
            return redirect(game_manager.game_data.current_page)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        key = request.POST.get("KEY")
        if key == "A":
            game_manager.load_default_settings()
            game_manager.game_data.state = GameState.worldmap
            game_manager.game_data.current_page = "/worldmap"
            return redirect('/worldmap')
        elif key == "B":
            game_manager.game_data.state = GameState.loading
            game_manager.game_data.current_page = "/options/load_game"
            return redirect('/options/load_game')
        return HttpResponseRedirect(request.path_info)