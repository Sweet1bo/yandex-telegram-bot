from orator.orm import belongs_to, has_one, has_many
from database import db
from orator import Model

Model.set_connection_resolver(db)


class Driver(Model):
    __table__ = 'drivers'
    __guarded__ = []

    @belongs_to
    def park(self):
        return Park

    @has_many
    def phones(self):
        return Phone


from database.models.Park import Park
from database.models.Phone import Phone
