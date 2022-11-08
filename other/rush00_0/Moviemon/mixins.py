from typing import Dict, Any

from django.views.generic.base import ContextMixin
from Moviemon.GameManager import GameManager


class GamedataContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['game_data'] = GameManager().game_data
        context['frame'] = GameManager().frame
        return context
