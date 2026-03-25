from functools import wraps
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS, USE_SESSION_FOR_NEXT
from flask_login.utils import expand_login_view, make_next_param, login_url as make_login_url
from flask import current_app, session, request, redirect


def admin_required(func):
    """
    Like login_required, but the user must have role 'admin'.
    Unauthenticated users get LoginManager.unauthorized();
    authenticated users without the role get redirect_for_insufficient_role.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif current_user.role != 'admin':
            return current_app.login_manager.redirect_for_insufficient_role()
        return func(*args, **kwargs)
    return decorated_view


def base_required(func):
    """
    Like login_required, but the user must have role 'base'.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif current_user.role != 'base':
            return current_app.login_manager.redirect_for_insufficient_role()
        return func(*args, **kwargs)
    return decorated_view


def redirect_for_insufficient_role(self):
    """
    LoginManager hook: set login_manager.insufficient_role_view (same idea as login_view)
    to the endpoint users without the required role should be sent to.
    """
    role_redirect_view = self.insufficient_role_view
    config = current_app.config
    if config.get('USE_SESSION_FOR_NEXT', USE_SESSION_FOR_NEXT):
        role_redirect_expanded_url = expand_login_view(role_redirect_view)
        session['_id'] = self._session_identifier_generator()
        session['next'] = make_next_param(role_redirect_expanded_url, request.url)
        redirect_url = make_login_url(role_redirect_view)
    else:
        redirect_url = make_login_url(role_redirect_view, next_url=request.url)
    return redirect(redirect_url)
