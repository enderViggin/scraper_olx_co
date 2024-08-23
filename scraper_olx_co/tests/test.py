import os
import sys
import re

from selenium.webdriver import Chrome

sys.path.append(os.path.abspath('.'))
from scraper_olx_co.scraper.scraper_olx_co import Scraper



def get_input_data_via_selenium() -> None:
    """ Функция для тестов. Получаем входные данные для парсинга через selenium """
                                
    count: int = 101 # Номер последней сохраненной страницы
    browser = Chrome()                                    
                                                      
    while True:                                                              
       count += 1
       file_name: str = f'./scraper_olx_co/tests/scraping_pages/page{count}.html'
       response: str = input('Did the page load?')                                                          
       if response == 'q': break
       html: str = browser.page_source  
       with open(file_name, 'w') as file:                                     
           file.write(html)
       print(f'Page is saved - {file_name}\n')

    browser.quit()


def scrape_all_saved_pages():
    """ Функция для тестов. Скрапим все сохраненные страницы из папки scraping_pages """

    for count, file_name in enumerate(os.listdir('./scraper_olx_co/tests/scraping_pages')):
        path: str = f'./scraper_olx_co/tests/scraping_pages/{file_name}'
        if not re.findall(r'/page\d+?\.html$', path): continue

        print(f'\n\n##### №{count} {file_name}')                                  
        with open(path) as file:       
            input_data: str = file.read()
            result: str = Scraper().start(input_data)

        print('\n\n##### END OF SCRAPING')
        if not result: continue                  
        with open(f'./scraper_olx_co/tests/result_of_scraping/result_{file_name.split(".")[0]}.json', 'w') as file:
             file.write(result)


if __name__ == '__main__':
    # get_input_data_via_selenium()
    scrape_all_saved_pages()
