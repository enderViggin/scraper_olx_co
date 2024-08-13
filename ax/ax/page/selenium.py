from cssselect import GenericTranslator, SelectorError
import lxml
from lxml.etree import HTML, tostring
from itertools import chain
import codecs
import re
from selenium.webdriver.common.by import By


def stringify_children(node):
    return lxml.etree.tostring(node, pretty_print=False)


def itertext(self):
    tag = self.tag
    if not isinstance(tag, str) and tag is not None:
        return
    if self.text:
        yield self.text
    for e in self:
        if not isinstance(e, lxml.etree._Comment):
            for s in e.itertext():
                yield s
            if e.tail:
                yield e.tail


class Result(list):
    def __init__(self, *args, **kwargs):
        super(Result, self).__init__(args[0])

    def __getitem__(self, i):
        return super(Result, self).__getitem__(i)

    def empty(self):
        if len(self) > 0:
            return False
        else:
            return True

    def first(self):
        if not self.empty():
            return list.__getitem__(self, 0)
        else:
            return ''

    def fetch(self, regexp):
        result = Result([])
        for item in self:
            search = re.search(regexp, item, re.IGNORECASE)
            if search:
                result.append(search.group(1))

        return result


class SeleniumPageHandler:
    def __init__(self, elements=None):
        self.elements = elements

    def __getitem__(self, index):
        return self.get(index)

    def getElements(self):
        return self.elements

    def __iter__(self):
        return iter(self.getPageElements())

    def getPageElements(self):
        result = []
        for element in self.getElements():
            result.append(SeleniumPageHandler([element]))

        return result

    def __getitem__(self, index):
        return self.get(index)

    def get(self, index):
        if len(self.getElements()) > 0:
            return SeleniumPageHandler([self.elements[index]])
        else:
            pass  # TODO: Error?

    def is_displayed(self, index=0):
        if self.elements:
            return self.elements[index].is_displayed()
        else:
            return False

    def length(self):
        return len(self.getElements())

    def exists(self, t_val=True, f_val=False):
        if self.length() > 0:
            return t_val
        else:
            return f_val

    def click(self):
        for element in self.getElements():
            try:
                if element.is_displayed():
                    element.click()
            except Exception as e:
                print(e)
                pass  # TODO: Error check

    def mouse_move(self):
        raise NotImplementedError

    def _select(self, selector_type, selector):
        result = []
        for element in self.getElements():
            try:
                result += element.find_elements(selector_type, selector)
            except Exception as e:
                print(e)
                pass


        page = SeleniumPageHandler(result)
        return page

    def xpath(self, selector):
        return self._select(By.XPATH, selector)

    def css(self, selector):
        return self._select(By.CSS_SELECTOR, selector)

    def text(self):
        result = Result([])
        for element in self.getElements():
            result.append(element.text)

        return result

    def self_text(self):
        result = Result([])
        for element in self.getElements():
            result.append(element.text)

        return result

    def html(self):
        result = Result([])
        for element in self.getElements():
            result.append(element.get_attribute('innerHTML'))
            #result.append(stringify_children(element))

        return result

    def attr(self, name):
        result = Result([])
        for element in self.getElements():
            try:
                result.append(element.get_attribute(name))
            except:
                pass  # TODO: Handle errors?
        return result

    def send_keys(self, keys):
        raise NotImplementedError

    def screenshot(self, output):
        raise NotImplementedError

    def len(self):
        return len(self.elements)

    def save_to_file(self, filename):
        with codecs.open(filename, "w", "utf-8-sig") as file:
            file.write(self.html)

    def load_from_file(self, filename):
        with codecs.open(filename, "r", "utf-8-sig") as file:
            self.update(file.read())
