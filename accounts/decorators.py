from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def allowed_users(allowed_roles=None):
    roles = allowed_roles or []
    
    def check_role(user):
        if not user.is_authenticated:
            return False  # Redirects to login page
        
        if user.role in roles:
            return True
            
        raise PermissionDenied  # Shows 403 Forbidden for logged-in users with wrong role
        
    return user_passes_test(check_role)
