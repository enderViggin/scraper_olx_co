import pytest
import pytest_mock

import ax.page.text

class TestTextPage:

    @pytest.mark.asyncio
    async def test_save_load_page(self, mocker: pytest_mock.MockFixture):
        page = ax.page.text.Page.from_html('<html><body><h1>hello</h1></body></html>')

        assert page.css('h1').text().first() == 'hello'