from functools import wraps
from Moviemon.GameManager import GameManager, GameState


# def state_check(func):
#     game_state = GameManager().game_data.state
#
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         if game_state == GameState.start_screen:
#             if request.