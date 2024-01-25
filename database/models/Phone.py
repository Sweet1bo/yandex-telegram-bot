from orator.orm import belongs_to
from database import db
from orator import Model

Model.set_connection_resolver(db)


class Phone(Model):
    __table__ = 'phones'
    __guarded__ = []

    @belongs_to
    def driver(self):
        return Driver

from database.models.Driver import Driver