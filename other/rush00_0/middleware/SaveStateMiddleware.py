from Moviemon.GameManager import GameManager


class SaveStateMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # Code that is executed in each request before the view is called

        response = self.get_response(request)
        # Code that is executed in each request after the view is called
        GameManager().quick_save()
        return response
