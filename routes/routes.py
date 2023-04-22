# Routes for the application
from flask import Blueprint
from controllers.controllers import index,add_subscription

blueprint = Blueprint('blueprint', __name__, template_folder="/templates")

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/add_subscription', methods=['POST'])(add_subscription)