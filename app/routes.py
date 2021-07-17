""" Api routes """

from app.resources.api import api
from app.resources.directors import DirectorListApi, DirectorApi
from app.resources.login import Login, Logout
from app.resources.movies import MovieListApi, MovieApi

route = api.add_resource

route(MovieListApi, "/movies", strict_slashes=False)
route(MovieApi, "/movies/<uuid>", strict_slashes=False)
route(DirectorListApi, "/directors", strict_slashes=False)
route(DirectorApi, "/directors/<uuid>", strict_slashes=False)
route(Login, "/login", strict_slashes=False)
route(Logout, "/logout", strict_slashes=False)
