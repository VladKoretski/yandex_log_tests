from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config.config as cfg

def wait_element(browser, delay=cfg.TIMEOUT, by=By.CSS_SELECTOR, value=None):
    """
Ожидает появления элемента на веб-странице в течение заданного времени.

Функция использует механизм явного ожидания (Explicit Wait) Selenium,
который ожидает, пока элемент не станет присутствовать в DOM-дереве
страницы. Это более надежный способ поиска элементов по сравнению
с непосредственным find_element, так как учитывает время загрузки
динамического контента.

Args:
    browser (webdriver.Chrome): Экземпляр веб-драйвера Selenium,
        который управляет браузером.
    delay (int, optional): Максимальное время ожидания в секундах.
        По умолчанию используется значение TIMEOUT из конфигурационного файла.
        Если элемент не появляется за это время, будет выброшено исключение.
    by (str, optional): Метод поиска элемента. По умолчанию By.CSS_SELECTOR.
        Доступные методы:
        - By.ID - поиск по id
        - By.CLASS_NAME - поиск по классу
        - By.CSS_SELECTOR - поиск по CSS-селектору
        - By.XPATH - поиск по XPath
        - By.TAG_NAME - поиск по тегу
        - By.NAME - поиск по атрибуту name
        - By.LINK_TEXT - поиск по тексту ссылки
        - By.PARTIAL_LINK_TEXT - поиск по частичному тексту ссылки
    value (str): Значение селектора для поиска элемента.
        Обязательный параметр. Примеры:
        - Для CSS: "#id", ".class", "div.container"
        - Для XPath: "//div[@class='example']"
        - Для ID: "username"

Returns:
    WebElement: Найденный веб-элемент (объект WebElement), если он
        появляется в течение заданного времени.

Raises:
    TimeoutException: Если элемент не появляется в течение указанного
        времени delay.
    InvalidSelectorException: Если передан некорректный селектор.
    WebDriverException: При других ошибках взаимодействия с драйвером.

Notes:
    - Функция ожидает именно presence (присутствие в DOM), а не visibility
      (видимость). Это означает, что элемент может быть скрыт CSS, но уже
      существовать в DOM.
    - Для ожидания видимости элемента используйте
      EC.visibility_of_element_located вместо presence_of_element_located.
    - Рекомендуется использовать эту функцию вместо прямого вызова
      find_element для динамических страниц.
    - При использовании в цикле с большим количеством элементов
      рекомендуется увеличить delay для медленных страниц.

See Also:
    - Selenium WebDriverWait: https://selenium-python.readthedocs.io/waits.html
    - Expected Conditions: https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions
"""
    return WebDriverWait(browser, delay).until(EC.presence_of_element_located((by, value)))

def phone_input(driver, phone_str):
    """Вводит телефон и нажимает 'Далее'."""

    phone_field = wait_element(driver, value=cfg.PHONE_INPUT)
    phone_field.send_keys(phone_str)
    next_button = wait_element(driver, value=cfg.NEXT_BUTTON)
    next_button.click()

def log_by_face_or_fingerprint(driver):
    """Нажимает на кнопку 'Войти по лицу или отпечатку п"""
    button = wait_element(driver, value=cfg.BY_FACE_OR_PRINT_BUTTON)
    button.click()