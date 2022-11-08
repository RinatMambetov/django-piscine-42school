import os
from django.conf import settings
from Moviemon.GameManager import GameManager


def search_saved_slots():
    """
    Function check saved files and fix saved_slots if needed
    """
    saved_files = {}
    for file in os.listdir(settings.BASE_DIR):
        if file.startswith('slot'):
            key = file[:4].capitalize() + f' {file[4]}'
            value = file.split('_', maxsplit=1)[1].replace('_', '/').split('.')[0]
            saved_files[key] = value
    for slot in GameManager().game_data.save_slots:
        if slot[0] in saved_files:
            slot[1] = saved_files[slot[0]]
        else:
            slot[1] = 'Free'
