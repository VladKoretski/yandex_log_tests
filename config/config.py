import os
from dotenv import load_dotenv

URL = "https://passport.yandex.ru/auth/"

login = os.getenv("YA.DISK_LOGIN")
password = os.getenv("YA.DISK_PASSWORD")

TIMEOUT = 10

#CSS Selectors
PHONE_INPUT = '[data-testid="text-field-input"]'
NEXT_BUTTON = '[data-testid="split-add-user-next-phone"]'
ERROR_MESSAGE = '[data-testid="error-message"]'
BY_FACE_OR_PRINT_BUTTON = '[data-testid="webauthn-auth-button"]'
CAPTCHA_BLOCK = ".description-block"

#check elements for assertions
EXPECTED_ERROR = 'Недопустимый формат номера'
CAPTCHA_TEXT = 'Введите номер телефона\nЧтобы войти или зарегистрироваться'

PHONE_INPUT_INVALID = '(963) 063-66-48999'
PHONE_INPUT_VALID = '(963) 063-66-48'