from lxml.etree import HTML as LXML_HTML


class BasePage:
    def __init__(self, elements=None):
        self.elements = elements

    @classmethod
    def from_html(cls, html):
        return cls(elements=[LXML_HTML(html)])

    def get_elements(self):
        return self.elements

    def __iter__(self):
        return iter(self.get_page_elements())

    def get_page_elements(self):
        result = []
        for element in self.get_elements():
            result.append(self.__class__([element]))

        return result

    def get(self, index):
        if len(self.get_elements()) > 0:
            return self.__class__([self.elements[index]])
        else:
            pass  # TODO: Error?

    def len(self):
        return self.length()

    def __getitem__(self, index):
        return self.get(index)

    def length(self):
        return len(self.elements)

    def exists(self, t_val=True, f_val=False):
        if self.length() > 0:
            return t_val
        else:
            return f_val