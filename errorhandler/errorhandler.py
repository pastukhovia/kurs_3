from flask import Blueprint

error_handler = Blueprint('error_handler', __name__)


@error_handler.app_errorhandler(404)
def page_not_found(error):
    return f'{error}', 404


@error_handler.app_errorhandler(500)
def internal_server_error(error):
    return f'{error}', 500
