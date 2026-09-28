# Учебный проект логирования на Яндекс и тестирование

Автотесты формы авторизации Яндекса (`https://passport.yandex.ru/auth/`)
на Python + Selenium + pytest.

## Стек

- Python 3.10+
- Selenium
- webdriver-manager
- pytest

## Структура проекта
```
ya_log/
├── config/
│ ├── init.py
│ └── config.py # URL, TIMEOUT, селекторы, ожидаемые тексты
├── tests/
│ ├── init.py
│ └── test_ya_log_form.py # тесты формы авторизации
├── tools/
│ ├── init.py
│ └── tools.py # wait_element, phone_input и др.
├── requirements.txt
├── README.md
├── ya_log.iml
└── venv/ # виртуальное окружение

```

## Установка

```bash
git clone <url-репозитория>
cd ya_log
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

Требуется установленный Google Chrome — ChromeDriver подтянется
автоматически через webdriver-manager.

## Настройка

Все параметры тестов лежат в config/config.py:  

* URL	Адрес страницы авторизации
* TIMEOUT	Таймаут явных ожиданий, сек
* PHONE_INPUT	Селектор поля ввода телефона
* NEXT_BUTTON	Селектор кнопки «Далее»
* ERROR_MESSAGE	Селектор сообщения об ошибке
* PHONE_INPUT_INVALID	Невалидный номер для негативного теста
* PHONE_INPUT_VALID	Валидный номер для позитивного теста
* EXPECTED_ERROR	Ожидаемый текст ошибки о формате номера
* CAPTCHA_BLOCK	Селектор блока с капчей
* CAPTCHA_TEXT	Ожидаемый текст капчи

## Запуск тестов
```bash
pytest -v
```
Точечный запуск:

```bash
pytest tests/test_ya_log_form.py -v
pytest tests/test_ya_log_form.py::test_yandex_auth_invalid_phone -v
pytest tests/test_ya_log_form.py::test_yandex_auth_valid_phone -v
```
## Что тестируется
tests/test_ya_log_form.py содержит два сценария:  

1. test_yandex_auth_invalid_phone — негативный
* Вводит невалидный номер (PHONE_INPUT_INVALID) через tools.phone_input.
* Дожидается появления блока с ошибкой (ERROR_MESSAGE).
* Проверяет, что текст совпадает с EXPECTED_ERROR («Недопустимый формат номера»).

2. test_yandex_auth_valid_phone — позитивный
* Вводит валидный номер (PHONE_INPUT_VALID).
* Яндекс как ботозащиту показывает капчу — тест дожидается блока капчи (CAPTCHA_BLOCK).
* Проверяет, что текст совпадает с CAPTCHA_TEXT («Введите фразу с картинки»).
  
Позитивный тест не логинится по-настоящему: он лишь проверяет, что после валидного номера Яндекс переводит пользователя на шаг с капчей. Проходить капчу автоматически не предполагается.  

## Фикстура драйвера
```python
@pytest.fixture()
def driver():
    service = Service(ChromeDriverManager().install())
    options = ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(cfg.URL)
    yield browser
    browser.quit()
 ```
### Особенности:

--headless — браузер работает без GUI (удобно для CI).  
yield + browser.quit() — браузер гарантированно закрывается даже при падении теста.  
Фикстура поднимает свежий профиль на каждый тест, поэтому куки прошлых сессий не влияют на результат.  

### Хелперы (tools/tools.py)
* wait_element(browser, delay=TIMEOUT, by=By.CSS_SELECTOR, value=None)	Явное ожидание появления элемента в DOM (WebDriverWait + presence_of_element_located)
* phone_input(driver, phone_str)	Ввод телефона в поле и клик по кнопке «Далее»

Тесты зависят от вёрстки Яндекса: при редизайне селекторы в config/config.py придётся обновить.
