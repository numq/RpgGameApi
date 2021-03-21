from flask import Blueprint

# from main import auto

bp_dev = Blueprint('dev', __name__)


@bp_dev.route('/', methods=['GET'])
def index():
    return 'index'


# @dev.route('/documentation', methods=['GET'])
# def documentation():
#     return auto.html(title='Documentation')
