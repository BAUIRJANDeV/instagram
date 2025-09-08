import re

from rest_framework.exceptions import ValidationError

phone_regex=re.compile( r'^(?:\+998|998|0)?(9[0-9])\d{7}$')
email_regex=re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
username_regex = re.compile(r'^[A-Za-z][A-Za-z0-9_]{7,}$')

def valid_username(username: str) -> bool:
    return re.fullmatch(username_regex, username) is not None

def chech_email_or_phone(user_input):
    if re.fullmatch(phone_regex,user_input):
        data='phone'
    elif re.fullmatch(email_regex,user_input):
        data='email'
    else:
        data={
            'success':False,
            'msg':'Siz hato email yoki telefon raqam kiritingiz',
        }
        raise ValidationError(data)

    return data
