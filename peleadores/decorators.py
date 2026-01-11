from django.core.exceptions import PermissionDenied

def editor_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Convertimos todos los nombres de grupo a minúsculas y quitamos espacios
        grupos = [g.name.lower().strip() for g in request.user.groups.all()]
        if request.user.is_superuser or "editor" in grupos:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied  # 403 para todos los demás
    return wrapper

