from orator.orm import belongs_to
from database import db
from orator import Model

Model.set_connection_resolver(db)


class YandexSession(Model):
    __table__ = 'yandex_sessions'
    __guarded__ = []

    @belongs_to
    def park(self):
        return Park

from database.models.Park import Park