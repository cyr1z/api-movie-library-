from app.app import api
from app.resources.countries import CountryListApi
from app.resources.directors import DirectorListApi
from app.resources.genres import GenreListApi
from app.resources.movies import MovieListApi
from app.resources.users import UserListApi
from flask_login import current_user, login_user
from app.models import User

route = api.add_resource

route(MovieListApi, "/movies", "/movies/<uuid>", strict_slashes=False)
route(UserListApi, "/users", "/users/<uuid>", strict_slashes=False)
route(GenreListApi, "/genres", "/genres/<uuid>", strict_slashes=False)
route(CountryListApi, "/countries", "/countries/<uuid>", strict_slashes=False)
route(DirectorListApi, "/directors", "/directors/<uuid>", strict_slashes=False)
