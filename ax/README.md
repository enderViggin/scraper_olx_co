Ax - библиотека для парсинга html страниц

Начало работы:

1. Установить зависимости из файла requirements.txt

2. Использование:

```
from ax.ax.page.text import Page
from ax.ax.page.text import Result
```


```
html: str = """
<html>
    <head></head>
    <body>
        <div class="wrapper">
            <div class="main-block">
                <div class="first-card card">
                    <h2 class="card-title">Грейпфрут красный</h2>
                    <div class="card-description">
                        Красный грейпфрут - случайный гибрид помело и апельсина. От помело фрукт унаследовал свой крупный размер, а от
                        апельсина - сочность и легкую горчинку. Грейпфруты можно есть свежими, а можно использовать для приготовления блюд.
                        Например, салат с грейпфрутом и креветками - необычный пример того, как можно по-новому раскрыть вкус знакомого фрукта.
                        Главное - полностью очистить дольки грейпфрута от пленок, в которых и содержатся горчащие гликозиды.
                    </div>
                    <div class="card-price">105.00р./кг</div>
                    <a href="/product/buy/824398">Купить</a>
                </div>
                <div class="second-card card">
                    <h2 class="card-title">Яблоки голден</h2>
                    <div class="card-description">
                        Яблоки сорта Голден имеют зеленый оттенок кожуры и белую хрустящую мякоть. Они прекрасно подходят для приготовления
                        шарлотки. Также эти фрукты используют в рецепте вкусных и ароматных булочек с корицей. Из яблок получаются очень
                        полезные и питательные соки. Они рекомендованы к употреблению людям, соблюдающим диетическое питание.
                    </div>
                    <div class="card-price">90.00р./кг</div>
                    <a href="/product/buy/814343">Купить</a>
                </div>
            </div>
        </div>
    </body>
</html>
"""
```

```
# Создаем объект через который дальше будем работать
page: Page = Page.from_html(html)

## XPATH

# Получить текст какого-то элемента, результат будет в списке
# Output: ['Красный грейпфрут - случайный гибрид помело и апельсина. От ...', 'Яблоки сорта Голден имеют зеленый оттенок кожуры и белую хрус...']
list_of_elements: Result = page.xpath('//div[@class="card-description"]').text()


# Будет возвращен первый элемент из списка
# Output: 'Яблоки сорта Голден имеют зеленый оттенок кожуры и белую хрус...'
result: str = page.xpath('//div[contains(@class, "second-card")]').text().first()


### CSS

# Будет получено текстовое содержимое всех тегов h2 страницы
list_of_elements: Result = page.css('h2.card-title')

for element in list_of_elements:
    title_content: str = element.text()


### XPATH CSS

# Можно также совмещать xpath и css
# Output: ['Кинза', 'Яблоки голден']
list_of_elements: Result = page.xpath('//div[contains(@class, "card")]').css('h2.card-title').text()

for element in list_of_elements:
    element: str = element.strip()


# Получить атрибут тега можно так
list_of_links: Result = page.xpath('//div[contains(@class, "card")]//a').attr('href')
```
