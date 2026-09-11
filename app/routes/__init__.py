from flask import Blueprint

main = Blueprint('main', __name__)

from app.routes import guests  # noqa: E402  (register routes on main)
from app.routes import rooms   # noqa: E402  (register routes on main)
