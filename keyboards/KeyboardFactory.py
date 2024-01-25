from keyboards.RemoveKeyboard import RemoveKeyboard
from keyboards.ShareContactKeyboard import ShareContactKeyboard


class KeyboardFactory(object):
    @staticmethod
    def build(keyboard: str):
        if keyboard == 'contact':
            return ShareContactKeyboard.get_keyboard()
        if keyboard == 'remove_keyboard':
            return RemoveKeyboard.get_keyboard()