import pytest

import ax.page.base

from lxml.etree import HTML as LXML_HTML

class TestBasePage:

    @pytest.mark.asyncio
    async def test_base_page(self):
        elements = LXML_HTML("<html><body></body></html>")

        page = ax.page.base.BasePage(elements)

        assert page.elements == elements