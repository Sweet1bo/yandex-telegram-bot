from database.models.Phone import Phone


class PhoneRepository(object):
    @staticmethod
    def get_phones(phone):
        return Phone.where('phone', phone).get()