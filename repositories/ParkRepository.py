from database.models.Park import Park
from database.models.YandexSession import YandexSession


class ParkRepository(object):
    def create_park_with_session(self, cookie, **attributes):
        park = Park.update_or_create(attributes)
        YandexSession.update_or_create({
            'park_id': park.id,
            'session': cookie
        })

        return park