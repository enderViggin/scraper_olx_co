from typing import List, Dict, Tuple
import re
from datetime import datetime

import lxml.html
from lxml.html import HtmlElement

from ax.page.text import Page
from ax.page.text import Result
from scraper_olx_co.scraper.data_models import (
    Object,
    Profile,
    ListOfObjects,
    ObjectFromList
)
from scraper_olx_co.scraper.scraper_exceptions import (
    FieldValueIsMissing,
    PageTypeIsNotDefined,
    ErroneousInputData
)



class ScraperUtils:
    """ Общие инструменты для скрапинга """

    def get_page(self, input_data: str) -> Page:
        page: Page = Page.from_html(input_data)
        return page


    def get_page_tree(self, input_data: str) -> HtmlElement:
        tree: HtmlElement = lxml.html.document_fromstring(input_data)
        return tree


    def get_link_of_page(self, page: Page) -> str:
        """ Получить ссылку страницы """

        result: str = page.xpath('/html/head//link[@rel="canonical"]').attr('href').first().strip()
        if result:
            return result
        else:
            raise FieldValueIsMissing('Не была получена ссылка на страницу объекта')


    def generate_tabular_data(self, tabular_data: Result) -> Dict:
        """ Формируем табличные данные в нужный вид """

        result: Dict[str, str] = {}
        dict_keys: List[str] = []
        dict_values: List[str] = []

        for count, element in enumerate(tabular_data):
            text: str = element.text().first().strip()
            if count % 2 == 0:
                dict_keys.append(text)
            else:
                dict_values.append(text)

        for key, value in zip(dict_keys, dict_values):
            result[key] = value

        return result


    def generate_tabular_data_in_list(self, tabular_data: Result) -> List[Tuple]:
        """ Формируем табличные данные в нужный вид """

        result: List[Tuple] = []
        dict_keys: List[str] = []
        dict_values: List[str] = []

        for count, element in enumerate(tabular_data):
            text: str = element.text().first().strip()
            if count % 2 == 0:
                dict_keys.append(text)
            else:
                dict_values.append(text)

        for key, value in zip(dict_keys, dict_values):
            entry: Tuple = (key, value)
            result.append(entry)

        return result


class ProfileSingleObjectScraperOlxCo(ScraperUtils):
    """ Класс для скрапинга данных профиля объекта """

    def get_name_of_profile(self, page: Page) -> str:
        """ Получаем имя профиля """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="profileCard"]//a[contains(@href, "/profile/")]/span/preceding-sibling::div')
            result: str = element.text().first().strip()
            return result


        def get_it_second_way() -> str:
            nonlocal page
            element: Result = page.xpath('//span[@data-aut-id="seller-name"]')
            result: str = element.text().first().strip()
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        name: str = get_it_first_way()
        if name: return name

        name: str = get_it_second_way()
        if name: return name

        raise FieldValueIsMissing('Не было получено имя продавца')


    def get_image_of_profile(self, page: Page) -> str:
        """ Получаем изображение продавца """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="profileCard"]//a[contains(@href, "/profile/")]//figure')
            if list(element):
                content: str = element.attr('style').first()
                content: str = re.findall(r'background-image: url\(.+?"\);', content)
                if not content: return ''
                result: str = re.findall('https://.+?"', content[0])[0][:-1]
                return result
            else:
                return ''


        def get_it_second_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="sellerInfo"]//figure/img')
            result: str = element.attr('src').first()
            return result


        def get_it_third_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="profileCard"]//a[contains(@href, "/profile/")]//figure')
            if list(element):
                content: str = element.attr('style').first()
                result: str = re.findall(r'https://.+?\)', content)[0][:-1]
                return result
            else:
                return ''


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        image: str = get_it_first_way()
        if image: return image

        image: str = get_it_second_way()
        if image: return image

        image: str = get_it_third_way()
        if image: return image

        raise FieldValueIsMissing('Не было получено изображение продавца')


    def get_link_to_seller(self, page: Page) -> str:
        """ Получаем ссылку на продавца """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('(//div[@data-aut-id="profileCard"]//a[contains(@href, "/profile/")])[1]')
            if list(element):
                result: str = 'https://www.olx.co.id' + element.attr('href').first()
            else:
                result: str = ''

            return result


        def get_it_second_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="sellerInfo"]//a[@data-aut-id="profileLinkTxt"]')
            if list(element):
                result: str = 'https://www.olx.co.id' + element.attr('href').first()
            else:
                result: str = ''

            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        link: str = get_it_first_way()
        if link: return link

        link: str = get_it_second_way()
        if link: return link

        raise FieldValueIsMissing('Не была получена ссылка на продавца')


    def get_installment_loan_payment(self, page: Page) -> str:
        """ Получаем рассрочку кредитного расчета """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="priceCard"]//div[text()="Cicilan"]/following-sibling::div[@data-aut-id="itemAdp"]')
            result: str = element.text().first().strip()
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        installment: str = get_it_first_way()
        if installment: return installment

        element: Result = page.xpath('//div[text()="Cicilan"]')

        if list(element):
            raise FieldValueIsMissing('Не была получена рассрочка кредитного расчета')
        else:
            return ''


    def get_advance_payment_of_credit_calculation(self, page: Page) -> str:
        """ Получаем авансовый платеж кредитного расчета """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="priceCard"]//div[text()="Down Payment"]/following-sibling::div[@data-aut-id="itemAdp"]')
            result: str = element.text().first().strip()
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        advance_payment: str = get_it_first_way()
        if advance_payment: return advance_payment

        element: Result = page.xpath('//div[text()="Down Payment"]')

        if list(element):
            raise FieldValueIsMissing('Не был получен авансовый платеж кредитного расчета')
        else:
            return ''


    def get_list_of_items_included_in_price(self, page: Page) -> List[Tuple]:
        """ Получаем список элементов включенных в цену """

        def get_it_first_way() -> List[Tuple]:
            nonlocal page
            elements: Result = page.xpath('//div[@data-aut-id="brandBannerListItem"]//div/p')
            result: List[Tuple] = self.generate_tabular_data_in_list(elements)
            return result


        def get_it_second_way() -> List[Tuple]:
            nonlocal page
            elements: Result = page.xpath('//div[@data-aut-id="vas-tags-banner"]//div/p')
            result: List[Tuple] = self.generate_tabular_data_in_list(elements)
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        list_of_items_included_in_price: List[Tuple] = get_it_first_way()
        if list_of_items_included_in_price: return list_of_items_included_in_price

        list_of_items_included_in_price: List[Tuple] = get_it_second_way()
        if list_of_items_included_in_price: return list_of_items_included_in_price

        element: Result = page.xpath('//h3/span[text()="Harga Sudah Termasuk"]')

        if list(element):
            raise FieldValueIsMissing('Не был получен список элементов включенных в цену')
        else:
            return []


    def get_work_schedule(self, page: Page) -> str:
        """ Получаем график работы из профиля """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="sellerInfo"]//div[text()="Buka sekarang"]/ancestor::div[2]/following-sibling::div')
            result: str = element.text().first().strip()
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        work_schedule: str = get_it_first_way()
        if work_schedule: return work_schedule

        element: Result = page.xpath('//div[text()="Buka sekarang"]')

        if list(element):
            raise FieldValueIsMissing('Не был получен график работы из профиля')
        else:
            return ''


    def get_data(self, page: Page) -> Profile:
        name: str = self.get_name_of_profile(page)
        image: str = self.get_image_of_profile(page)
        link_to_seller: str = self.get_link_to_seller(page)
        installment_loan_payment: str = self.get_installment_loan_payment(page)
        advance_payment_of_credit_calculation: str = self.get_advance_payment_of_credit_calculation(page)
        list_of_items_included_in_price: List[Tuple] = self.get_list_of_items_included_in_price(page)
        work_schedule: str = self.get_work_schedule(page)

        profile: Profile = Profile(
            name=name,
            image=image,
            link=link_to_seller,
            installment_loan_payment=installment_loan_payment,
            advance_payment_of_credit_calculation=advance_payment_of_credit_calculation,
            list_of_items_included_in_price=list_of_items_included_in_price,
            work_schedule=work_schedule,
        )
        return profile



class SingleObjectScraperOlxCo(ScraperUtils):
    """ Класс для скрапинга отдельного объекта """

    def get_name_of_object(self, page: Page) -> str:
        """ Получаем название объекта """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//h1[@data-aut-id="itemTitle"]')
            result: str = element.text().first().strip()
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        name: str = get_it_first_way()
        if name: return name

        raise FieldValueIsMissing('Не было получено название объекта')


    def get_price_of_object(self, page: Page) -> str:
        """ Получаем цену объекта """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="itemPrice"]')
            result: str = element.text().first().strip()
            return result


        def get_it_second_way() -> str:
            nonlocal page
            element: Result = page.xpath('//span[@data-aut-id="itemPrice"]')
            result: str = element.text().first().strip()
            return result


        def get_it_third_way() -> str:
            nonlocal page
            element: Result = page.xpath('//span[@data-aut-id="itemPrice"]/ancestor::section[1]/span[contains(text(), "Rp")]')
            result: str = element.text().first().strip()
            return result

        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        price: str = get_it_first_way()
        if price: return price

        price: str = get_it_second_way()
        if price: return price

        price: str = get_it_third_way()
        if price: return price

        element: Result = page.xpath('//*[@data-aut-id="itemPrice"]')
        content: str = element.text().first().strip()

        if content:
            raise FieldValueIsMissing('Не была получена цена объекта')
        else:
            return ''


    def get_signature_of_object(self, page: Page) -> str:
        """ Получаем подпись объекта """

        def get_it_first_way() -> str:
            nonlocal page
            
            number_of_elements: int = len(list(page.xpath(
                '//span[@data-aut-id="itemPrice"]/following-sibling::h1[@data-aut-id="itemTitle"]/ancestor::section/*'
            )))
            
            if number_of_elements == 4:
                result: str = page.xpath(
                    '//span[@data-aut-id="itemPrice"]/ancestor::section/h1/preceding-sibling::span[1]'
                ).text().first().strip()
            elif number_of_elements == 3:
                result: str = 'no signature'
            else:
                result: str = ''

            return result


        def get_it_second_way() -> str:
            nonlocal page

            number_of_elements: int = len(list(page.xpath(
                '//h1[@data-aut-id="itemTitle"]/following-sibling::div[@data-aut-id="itemParameters"]/ancestor::div[1]/*'
            )))
            

            if number_of_elements == 4:
                result: str = page.xpath(
                    '//h1[@data-aut-id="itemTitle"]/following-sibling::div[@data-aut-id="itemParameters"]/preceding-sibling::div[1]'
                ).text().first().strip()
                if not result: result = 'no signature'
            else:
                result: str = 'no signature'

            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        signature: str = get_it_first_way()
        if signature: return signature

        signature: str = get_it_second_way()
        if signature: return signature

        raise FieldValueIsMissing('Не была получена подпись объекта')


    def get_address_of_object(self, page: Page) -> str:
        """ Получаем адрес объекта """

        def get_it_first_way() -> str:
            nonlocal page
            
            element: Result = page.xpath('//div[@data-aut-id="itemLocation"]//span')
            result: str = element.text().first().strip()
            return result


        def get_it_second_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="sellerInfo"]//a[contains(@href, "oogle.com/maps")]/span/ancestor::a/preceding-sibling::div')
            result: str = element.text().first().strip()
            return result


        def get_it_third_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[@data-aut-id="overviewDetails"]//div[text()="Lokasi"]/following-sibling::div')
            result: str = element.text().first().strip()
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        address: str = get_it_first_way()
        if address: return address

        address: str = get_it_second_way()
        if address: return address

        address: str = get_it_third_way()
        if address: return address

        raise FieldValueIsMissing('Не был получен адрес объекта')


    def get_list_of_images_of_object(self, page: Page) -> List[str]:
        """ Получаем список изображений объекта """

        def get_it_first_way() -> List[str]:
            nonlocal page
            result: List[str] = []
            list_of_elements: List[str] = page.xpath(
                '//div[@data-aut-id="gallery-thumbnail"]//button[contains(@style, "background-image: url(")]'
            ).attr('style')

            for element in list_of_elements:
                content: str = re.findall(r'background-image: url\(.+?"\);', element)[0]
                content: str = re.findall('https://.+?"', content)[0][:-1]
                if content in result: continue
                result.append(content)

            return result


        def get_it_second_way() -> List[str]:
            nonlocal page
            result: List[str] = []
            list_of_elements: Result = page.xpath(
                '//div[contains(@class, "-slider")]//figure/img'
            )

            for element in list_of_elements:
                content: str = element.attr('src').first()
                if content in result: continue
                result.append(content)

            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        list_of_images: List[str] = get_it_first_way()
        if list_of_images: return list_of_images

        list_of_images: List[str] = get_it_second_way()
        if list_of_images: return list_of_images

        raise FieldValueIsMissing('Не был получен список изображений объекта')


    def get_list_of_details_of_object(self, page: Page) -> List[Tuple]:
        """ Получаем список деталей объекта """

        def get_it_first_way() -> List[Tuple]:
            nonlocal page
            
            list_of_elements: Result = page.xpath(
                '//div[@data-aut-id="itemParams"]//div/span[contains(@data-aut-id, "key") or contains(@data-aut-id, "value")]'
            )
            result: List[Tuple] = self.generate_tabular_data_in_list(list_of_elements)
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        list_of_details: List[Tuple] = get_it_first_way()
        if list_of_details: return list_of_details

        element: Result = page.xpath('//h3[@data-aut-id="itemDescriptonTitle"]/span[text()="Detail"]')
        
        if list(element):
            raise FieldValueIsMissing('Не был получен список деталей объекта')
        else:
            return []


    def get_description_of_object(self, page: Page) -> str:
        """ Получаем описание объекта """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath(
                '//div[@data-aut-id="itemDescriptionContent"]'
            )
            result: str = element.text().first().strip()
            return result


        def get_it_second_way() -> str:
            nonlocal page
            elements: Result = page.xpath(
                '//h4[@data-aut-id="itemDescriptonTitle"]/ancestor::div[1]/div'
            ).text()
            result: str = '\n'.join(elements)
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        description: str = get_it_first_way()
        if description: return description

        description: str = get_it_second_way()
        if description: return description

        raise FieldValueIsMissing('Не было получено описание объекта')


    def get_object_overview_data(self, page: Page) -> List:
        """ Получаем данные обзора объекта """

        def get_it_first_way() -> List:
            nonlocal page
            elements: Result = page.xpath(
                '//h3[@data-aut-id="adOverview"]/ancestor::div[1]//picture/ancestor::div[1]/following-sibling::div/div'
            )
            if elements:
                result: List[Tuple] = self.generate_tabular_data_in_list(elements)
            else:
                result: List = []

            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        object_overview_data: List = get_it_first_way()
        if object_overview_data: return object_overview_data

        element: Result = page.xpath('//h3[@data-aut-id="adOverview"]')
        if list(element):
            raise FieldValueIsMissing('Не были получены данные обзора объекта')
        else:
            return []


    def get_ad_id(self, page: Page, tree: HtmlElement) -> str:
        """ Получаем идентификатор объявления """

        def get_it_first_way() -> str:
            nonlocal page
            element: Result = page.xpath('//strong[contains(text(), "ID IKLAN")]')
            content: str = element.text().first().strip()
            content: List = re.findall(r'\d+', content)

            if content:
                result: str = content[0]
            else:
                result: str = ''

            return result


        def get_it_second_way() -> str:
            nonlocal page
            element: Result = page.xpath('//div[contains(text(), "ID IKLAN")]')
            content: str = element.text().first().strip()
            content: List = re.findall(r'\d+', content)

            if content:
                result: str = content[0]
            else:
                result: str = ''

            return result


        def get_it_third_way() -> str:
            nonlocal page, tree
            element: Result = tree.xpath('//strong[contains(text(), "ID IKLAN")]')
            content: str = element[0].text_content().strip()
            content: List = re.findall(r'\d+', content)

            if content:
                result: str = content[0]
            else:
                result: str = ''

            return result



        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        ad_id: str = get_it_first_way()
        if ad_id: return ad_id

        ad_id: str = get_it_second_way()
        if ad_id: return ad_id

        ad_id: str = get_it_third_way()
        if ad_id: return ad_id

        raise FieldValueIsMissing('Не был получен ID объявления')


    def get_object_data(self, page: Page, tree: HtmlElement) -> Object:
        """ Получаем данные объекта """

        scraping_date: datetime = datetime.utcnow()
        link: str = self.get_link_of_page(page)
        name: str = self.get_name_of_object(page)
        price: str = self.get_price_of_object(page)
        signature: str = self.get_signature_of_object(page)
        address: str = self.get_address_of_object(page)
        list_of_images_of_object: List[str] = self.get_list_of_images_of_object(page)
        list_of_details_of_object: List[Tuple] = self.get_list_of_details_of_object(page)
        description: str = self.get_description_of_object(page)
        object_overview_data: List = self.get_object_overview_data(page)
        ad_id: str = self.get_ad_id(page, tree)
        profile: Profile = ProfileSingleObjectScraperOlxCo().get_data(page)

        object: Object = Object(
            scraping_date=scraping_date,
            link=link,
            name=name,
            price=price,
            signature=signature,
            address=address,
            list_of_images_of_object=list_of_images_of_object,
            list_of_details_of_object=list_of_details_of_object,
            description=description,
            object_overview_data=object_overview_data,
            ad_id=ad_id,
            profile=profile,
        )
        return object


    def start(self, page: Page, tree: HtmlElement) -> str:
        object: Object = self.get_object_data(page, tree)
        result: str = object.json()
        return result



class ObjectFromListScraperOlxCo():
    """ Класс для скрапинга объектов из списка """

    def get_object_links(self, page: Page) -> List[str]:
        """ Получаем список ссылок объектов """

        def get_it_first_way() -> List[str]:
            nonlocal page
            result: List[str] = []
            list_of_elements: Result = page.xpath('//ul[@data-aut-id="itemsList"]/li[@data-aut-id="itemBox"]/a')

            for element in list_of_elements:
                content: str = element.attr('href').first()
                entry: str = 'https://www.olx.co.id' + content
                result.append(entry)

            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        object_links: List[str] = get_it_first_way()
        if object_links: return object_links

        raise FieldValueIsMissing('Не был получен список ссылок объектов')


    def get_names_of_object(self, page: Page) -> List[str]:
        """ Получаем названия объектов """

        def get_it_first_way() -> List[str]:
            nonlocal page
            elements: Result = page.xpath('//ul[@data-aut-id="itemsList"]/li[@data-aut-id="itemBox"]/a//span[@data-aut-id="itemTitle"]')
            result: str = elements.text()
            return result


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        names_of_object: List[str] = get_it_first_way()
        if names_of_object: return names_of_object

        raise FieldValueIsMissing('Не был получен список ссылок объектов')


    def get_data(self, page: Page) -> ListOfObjects:

        list_of_elements: List[ObjectFromList] = []
        object_links: List[str] = self.get_object_links(page)
        names_of_object: List[str] = self.get_names_of_object(page)

        for link, name in zip(object_links, names_of_object):
            entry: ObjectFromList = ObjectFromList(
                link=link,
                name=name
            )
            list_of_elements.append(entry)

        result: ListOfObjects = ListOfObjects(objects_from_list=list_of_elements)
        return result


    def start(self, page: Page) -> str:
        objects: ListOfObjects = self.get_data(page)
        result: str = objects.json()
        return result



class Scraper(ScraperUtils):

    def check_input_data(self, input_data: str) -> None:
        """ Проверяем входные данные """

        if input_data == 'тут не должно быть пусто':
            raise ErroneousInputData('В скрапер не были переданы входные данные')

        if not input_data.strip():
            raise ErroneousInputData('В скрапер были отправлены пустые входные данные')


    def find_out_what_to_scrap(self, page: Page) -> str:
        """ Определяем что именно будем скрапить """

        name_of_object: Result = page.xpath('//h1[@data-aut-id="itemTitle"]')
        list_of_objects_from_issue: Result = page.xpath('//ul[@data-aut-id="itemsList"]')

        if list(name_of_object):
            return 'single_object'
        elif list(list_of_objects_from_issue):
            return 'object_from_list'
        else:
            raise PageTypeIsNotDefined('Не определен тип страницы для скрапинга')


    def start(self, input_data: str) -> str:

        self.check_input_data(input_data)
        page: Page = self.get_page(input_data)
        tree: HtmlElement = self.get_page_tree(input_data)

        what_to_scrap: str = self.find_out_what_to_scrap(page)

        if what_to_scrap == 'single_object':
            result: str = SingleObjectScraperOlxCo().start(page, tree)
        elif what_to_scrap == 'object_from_list':
            result: str = ObjectFromListScraperOlxCo().start(page)
        else:
            raise PageTypeIsNotDefined('Не определен тип страницы для скрапинга')

        return result
