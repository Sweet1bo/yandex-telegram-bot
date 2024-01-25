from database.models.BotUser import BotUser


class BotUserRepository(object):
    @staticmethod
    def create_user(**attributes):
        """

        Метод создает пользователя

        :param attributes:
        :return: BotUser
        """
        user = BotUser.update_or_create({
            'telegram_user_id': attributes['telegram_user_id'],
            'driver_id': attributes['driver_id'],
            'phone': attributes['phone']
        })

        return user

    @staticmethod
    def update_user(id, data):
        return BotUser.where('id', id).update(data)


    @staticmethod
    def get_user_by_telegram_id(id):
        return BotUser.where('telegram_user_id', id).first()

    @staticmethod
    def get_user_by_telegram_id_with_relations(id):
        return BotUser.with_('driver', 'driver.park', 'driver.park.session').where('telegram_user_id', id).first()

    @staticmethod
    def get_user_by_phone(phone):
        return BotUser.with_('driver', 'driver.park', 'driver.park.session').where('phone', 'like', f'%{phone}%').first()