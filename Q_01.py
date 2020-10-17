import scrapy

class UolSpider(scrapy.Spider):
    name = 'uol_spider'
    start_urls = ['https://www.uol.com.br']

    def parse(self, response):

        dolar = response.css('.HU_currency__quote::text')
        dolar_atual = dolar[0].extract().strip()
        if dolar_atual != "":
            print('O dolar hoje é cotado a', dolar_atual, 'reais! :O' )

#scrapy runspider Q_01.py -s LOG_ENABLED=False