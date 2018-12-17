from apps.front.forms import BaseForm
from wtforms import StringField
from wtforms.validators import InputRequired, Regexp, EqualTo, ValidationError
import hashlib


class SMSCaptchaForm(BaseForm):
    salt = 'q3423805gdflvbdfvhsdoa`#$%'
    telephone = StringField(validators=[Regexp(r'1[345879]\d{9}')])
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5
        sign2 = hashlib.md5((timestamp+telephone+self.salt).encode('utf-8')).hexdigest()

        if sign == sign2:
            return True
        else:
            return False




