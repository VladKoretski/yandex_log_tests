import time

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import config.config as cfg
from tools import tools

@pytest.fixture()
def driver():
    service = Service(ChromeDriverManager().install())
    options = ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(cfg.URL)
    yield browser
    browser.quit()

def test_yandex_auth_invalid_phone(driver):
    tools.phone_input(driver, cfg.PHONE_INPUT_INVALID)
    error_message = tools.wait_element(driver, value=cfg.ERROR_MESSAGE)
    message = error_message.text.strip()

    assert message == cfg.EXPECTED_ERROR, (
        f'Ожидалось "{cfg.EXPECTED_ERROR}", получено "{message}"'
    )


def test_yandex_auth_valid_phone(driver):
    tools.phone_input(driver, cfg.PHONE_INPUT_VALID)
    captcha = tools.wait_element(driver, value=cfg.CAPTCHA_BLOCK)
    assert cfg.CAPTCHA_TEXT in captcha.text

