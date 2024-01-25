from orator.orm import has_many, has_one
from database import db
from orator import Model

Model.set_connection_resolver(db)


class Park(Model):
    __table__ = 'parks'
    __guarded__ = []

    @has_many
    def drivers(self):
        return Driver

    @has_one
    def session(self):
        return YandexSession


from database.models.Driver import Driver
from database.models.YandexSession import YandexSession
