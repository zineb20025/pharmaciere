from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(*roles):
    """
    Décorateur pour restreindre l'accès selon le rôle de l'employé.
    Exemples d'utilisation :
        @role_required('pharmacien')
        @role_required('admin', 'pharmacien')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if hasattr(user, 'role') and user.role in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("Vous n'avez pas les droits nécessaires pour accéder à cette page.")
        return _wrapped_view
    return decorator

# Raccourcis pratiques
admin_required = role_required('admin')
pharmacien_required = role_required('pharmacien')
caissier_required = role_required('caissier')
admin_or_pharmacien_required = role_required('admin', 'pharmacien')
admin_or_caissier_required = role_required('admin', 'caissier')
pharmacien_or_caissier_required = role_required('pharmacien', 'caissier')
