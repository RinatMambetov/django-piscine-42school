from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from Moviemon.mixins import GamedataContextMixin
from Moviemon.GameManager import GameManager
from options.service import search_saved_slots


class LoadView(GamedataContextMixin, View):
    def get(self, request):
        if GameManager().game_data.current_page != '/options/load_game':
            return redirect(GameManager().game_data.current_page)
        context = self.get_context_data()
        search_saved_slots()
        game_data = GameManager().game_data
        context['slots'] = game_data.save_slots
        context['a_button'] = 'Load'
        return render(request, 'saveload.html', context)

    def post(self, request):
        key = request.POST.get('KEY')
        if not GameManager().game_data.loaded:

            if key == 'A':
                GameManager().load_game()
            elif key == 'B':
                GameManager().reset_slot_position()
                GameManager().game_data.current_page = "/"
                return redirect('mainpage')
            elif key == 'UP':
                GameManager().change_slot_position(-1)
            elif key == 'DOWN':
                GameManager().change_slot_position(1)
            return HttpResponseRedirect(request.path_info)
        else:
            GameManager().game_data.loaded = False
            GameManager().reset_slot_position()
            GameManager().game_data.current_page = "/worldmap"
            return redirect('worldmap')


class SaveView(GamedataContextMixin, View):
    def get(self, request):
        if GameManager().game_data.current_page != '/options/save_game':
            return redirect(GameManager().game_data.current_page)
        context = self.get_context_data()
        search_saved_slots()
        game_data = GameManager().game_data
        context['slots'] = game_data.save_slots
        context['a_button'] = 'Save'
        return render(request, 'saveload.html', context)

    def post(self, request, *args, **kwargs):
        key = request.POST.get('KEY')
        if key == 'A':
            GameManager().save_game()
            return HttpResponseRedirect(request.path_info)
        elif key == 'B':
            GameManager().reset_slot_position()
            GameManager().game_data.current_page = "/options"
            return redirect('options')
        elif key == 'UP':
            GameManager().change_slot_position(-1)
        elif key == 'DOWN':
            GameManager().change_slot_position(1)
        return HttpResponseRedirect(request.path_info)


class OptionsView(TemplateView):
    template_name = "options.html"
    def get(self, request, *args, **kwargs):
        if GameManager().game_data.current_page != '/options':
            return redirect(GameManager().game_data.current_page)
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        key = request.POST.get('KEY')
        if key == 'A':
            GameManager().game_data.current_page = "/options/save_game"
            return redirect('save_game')
        elif key == 'START':
            GameManager().game_data.current_page = "/worldmap"
            return redirect('worldmap')
        elif key == 'B':
            GameManager().game_data.current_page = "/"
            return redirect('mainpage')
        else:
            return HttpResponseRedirect(request.path_info)
