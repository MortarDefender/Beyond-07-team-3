from .models import Profile


class ProfileMiddleware():
    def __init__(self, get_response) -> None:
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            request.profile = Profile.objects.filter(user=request.user).first()
        else:
            request.profile = None
