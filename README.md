Скрапер для сайта https://www.olx.co.id/


Начало работы:

1 - Клонировать себе библиотеку ax
`git clone https://git.faqhld.com/restate/ax.git`

2 - Клонировать себе сам скрапер
`git clone https://github.com/enderViggin/scraper_olx_co.git`

3 - Установить зависимости скрапера

 3.1 - Открыть файл `setup.py` (находится в корне проекта) и указать значение для переменной `PATH_TO_AX_LIBRARY`. Значением должен быть путь ранее склонированной библиотеке ax

 3.2 - Активировать виртуальное окружение скрапера и установить его зависимости:
  `pip install -e .`

4 - Добавление скрапера как библиотеки в основной проект. Нужно перейти в основной проект (где будет использоваться скрапер), активировать виртуальное окружение и установить скрапер:
 `pip install /path/to/scraper`

(/path/to/scraper - путь к скраперу на компьютере)

5 - Использование в коде. Импортировать и использовать дальше можно таким образом:
```
from scraper_olx_co.main import main as scraper_olx_co_main


...
input_data: str = 'тут входные данные для парсера'
result: str = scraper_olx_co_main(input_data)
print('RESULT: ', result)
```

Для тестиривания скрапера используется файл `scraping_olx_co/tests/test.py`.
В качестве тестовых данных - zip архив `scraping_olx_co/tests/scraping_pages`.
Необходимо разархивировать `scraping_olx_co/tests/scraping_pages.zip` и оставить полученную
папку на уровне файла `test.py`.
