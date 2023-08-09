import pymorphy2
import bcrypt


morph = pymorphy2.MorphAnalyzer()
def get_normal_form(text: str):
    if text:
        text = text.replace('(', '').replace(')', '').replace('\'', '')

        prelogs = [' без ', ' безо ', ' близ ', ' в ',  ' во ', ' вместо ', ' вне ', ' для ', ' до ', ' за ', ' из ', ' изо ', ' и ', ' к ',  ' ко ', ' кроме ', ' между ', ' меж ', ' на ', ' над ', ' надо ', ' о ',  ' об ', ' обо ', ' от ', ' ото ', ' перед ', ' передо ', ' предо ', ' пo ', ' под ', ' при ', ' про ', ' ради ', ' с ',  ' со ', ' сквозь ', ' среди ', ' через ', ' чрез ']
        for sumb in prelogs:
            text = text.replace(sumb, ' ')

        normal_form = [morph.parse(i)[0].normal_form for i in text.split()]

        return ' '.join(normal_form)
    else:
        return text


class BcryptPasswordManager:
    """
    example:
        salt, hashed_password = BcryptPasswordManager('password').hash_password()

        password_true = BcryptPasswordManager('password', salt, hashed_password).password_check()
    """

    def __init__(self, password:str, salt=None, hashed_password=None):
        self.password = password
        self.salt = salt
        self.hashed_password = hashed_password

    def hash_password(self) -> tuple[str, str]:
        self.salt = bcrypt.gensalt().decode('utf-8')
        self.hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), self.salt.encode('utf-8')).decode('utf-8')

        return self.salt, self.hashed_password

    def password_check(self) -> bool:
        if not self.salt or not self.password:
            return False

        hashed_password_check = bcrypt.hashpw(self.password.encode('utf-8'), self.salt.encode('utf-8')).decode('utf-8')
        return self.hashed_password == hashed_password_check
