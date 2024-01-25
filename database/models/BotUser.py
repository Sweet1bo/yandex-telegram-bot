from orator.orm import belongs_to, has_many
from database import db
from orator import Model

Model.set_connection_resolver(db)


class BotUser(Model):
    __table__ = 'bot_users'
    __guarded__ = []

    @belongs_to
    def driver(self):
        return Driver


from database.models.Driver import Driver
