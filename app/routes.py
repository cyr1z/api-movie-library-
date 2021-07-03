from app.app import api
from app.resources.countries import CountryListApi
from app.resources.directors import DirectorListApi
from app.resources.genres import GenreListApi
from app.resources.movies import MovieListApi
from app.resources.users import UserListApi

api.add_resource(
    MovieListApi,
    '/movies',
    '/movies/<uuid>',
    strict_slashes=False
)
api.add_resource(
    DirectorListApi,
    '/directors',
    '/directors/<uuid>',
    strict_slashes=False
)
api.add_resource(
    UserListApi,
    '/users',
    '/users/<uuid>',
    strict_slashes=False
)
api.add_resource(
    GenreListApi,
    '/genres',
    '/genres/<uuid>',
    strict_slashes=False
)
api.add_resource(
    CountryListApi,
    '/countries',
    '/countries/<uuid>',
    strict_slashes=False
)
