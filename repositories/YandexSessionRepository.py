from database.models.YandexSession import YandexSession


class YandexSessionRepository(object):
    @staticmethod
    def all():
        return YandexSession.with_('park').get(['park_id', 'session'])