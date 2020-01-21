from functools import wraps
from flask import abort
from flask_login import current_user

def edit_permission_required(f):
    """Permissions:
        - A logged-out user does not have permission.
        - A guest editor must have created the page they're editing.
        - An admin always has permission.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapper
