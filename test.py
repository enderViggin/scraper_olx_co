import os

from selenium.webdriver import Chrome

from scraper.scraper_olx_co import Scraper



def get_input_data_via_file() -> str:
    """ Функция для тестов. Получаем входные данные для скрапинга через файл """

    file_name: str = f'./scraping_pages/page1.html'
    with open(file_name) as file:
        content: str = file.read()
        return content


def get_input_data_via_selenium() -> None:
    """ Функция для тестов. Получаем входные данные для парсинга через selenium """
                                
    count: int = 101 # Номер последней сохраненной страницы
    browser = Chrome()                                    
                                                      
    while True:                                                              
       count += 1
       file_name: str = f'./scraping_pages/page{count}.html'
       response: str = input('Did the page load?')                                                          
       if response == 'q': break
       html: str = browser.page_source  
       with open(file_name, 'w') as file:                                     
           file.write(html)
       print(f'Page is saved - {file_name}\n')

    browser.quit()


def scrape_all_saved_pages():
    """ Функция для тестов. Скрапим все сохраненные страницы из папки scraping_pages """

    for count, file_name in enumerate(os.listdir('./scraping_pages')):                                                       
        path: str = f'./scraping_pages/{file_name}'

        print(f'\n\n##### №{count} {file_name}')                                  
        with open(path) as file:       
            input_data: str = file.read()
            result: str = Scraper().start(input_data)

        print('\n\n##### END OF SCRAPING')
        if not result: continue                  
        with open(f'./result/result_{file_name.split(".")[0]}.json', 'w') as file:
             file.write(result)


if __name__ == '__main__':
    scrape_all_saved_pages()
    # get_input_data_via_selenium()
