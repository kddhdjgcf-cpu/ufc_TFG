from django.core.exceptions import PermissionDenied

def editor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated and
            request.user.groups.filter(name="Editor").exists()
        ):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper
