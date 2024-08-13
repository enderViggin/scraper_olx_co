# -*- coding: utf-8 -*-

from ax.ax.page.base import BasePage

from cssselect import GenericTranslator, SelectorError
import lxml


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


class Page(BasePage):



    def get_url(self):
        return None




    def click(self):
        for element in self.getElements():
            try:
                element.click()
            except:
                pass  # TODO: Error check

    def mouse_move(self):
        pass

    def _select(self, selector_type, selector):
        result = []
        if selector_type == 'CSS_SELECTOR':
            selector = GenericTranslator().css_to_xpath(selector)

        for element in self.get_elements():
            result += element.xpath(selector)

        return Page(result)

    def xpath(self, selector):
        return self._select('XPATH', selector)

    def css(self, selector):
        return self._select('CSS_SELECTOR', selector)

    def text(self):
        result = Result([])
        for element in self.get_elements():
            result.append(''.join(itertext(element)))

        return result

    def attr(self, name):
        result = Result([])
        for element in self.get_elements():
            try:
                result.append(element.get(name))
            except Exception as e:
                print(e)
                pass  # TODO: Handle errors?
        return result

    def send_keys(self, keys):
        pass

    def screenshot(self, output):
        pass

