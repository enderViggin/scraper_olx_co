

class FieldValueIsMissing(Exception):
    """
    Это исключение возникает когда не удается получить значение какого-то поля
    """
    pass


class PageTypeIsNotDefined(Exception):
    """
    Это исключение возникает когда не удается определить тип страницы для пасринга
    """
    pass


class ErroneousInputData(Exception):
    """
    Это исключение возникает когда скраперу предоставляются ошибочные входные данные
    """
    pass
