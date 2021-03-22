from app.blueprints import bp_dev


@bp_dev.route('/', methods=['GET'])
def index():
    return 'index'

# @dev.route('/documentation', methods=['GET'])
# def documentation():
#     return auto.html(title='Documentation')
