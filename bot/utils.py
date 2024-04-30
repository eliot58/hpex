import random
import string
from datetime import datetime
import re

def validate_phone_number(phone_number):
    pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')
    
    if re.match(pattern, phone_number):
        return True
    else:
        return False


def generate_code():
    letters = string.ascii_uppercase
    digits = string.digits
    code = ''.join(random.choices(letters, k=2)) + ''.join(random.choices(digits, k=4))
    return code


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%d.%m.%Y')
        return True
    except ValueError:
        return False
    

def validate_code(code):
    pattern = re.compile(r'^[A-Za-z]{2}\d{4}$')
    
    if re.match(pattern, code):
        return True
    else:
        return False