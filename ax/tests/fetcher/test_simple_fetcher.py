import pytest

import ax.page.base

from lxml.etree import HTML as LXML_HTML

class TestSimpleFetcher:

    @pytest.mark.asyncio
    async def test_simple_fetcher(self):
        elements = LXML_HTML("<html><body></body></html>")

        page = ax.page.base.BasePage(elements)

        assert page.elements == elements