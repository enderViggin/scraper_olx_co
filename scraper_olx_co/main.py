from scraper.scraper_olx_co import Scraper



def main(input_data: str) -> str:
    result: str = Scraper().start(input_data)
    return result


if __name__ == '__main__':
    input_data: str = 'тут не должно быть пусто'
    with open('./scraper_olx_co/tests/scraping_pages/page97.html') as file: input_data = file.read()
    result: str = main(input_data)
    print('RESULT: ', result)
