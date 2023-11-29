from controllers.movies_controller import movies
from controllers.auth_controller import auth
from controllers.actors_controller import actors

registerable_controllers = [
    auth,
    movies,
    actors
]