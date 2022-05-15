import scrapy


class SpiderBooksSpider(scrapy.Spider):
    name = 'spider_books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    def parse(self, response):
        for book in response.css("ol.row").css('li'): 
            link = response.urljoin(book.css("h3").css("a::attr(href)").get())
            print(link)
            yield scrapy.Request(link, callback=self.parse_details)
            
            #https://us.bbcollab.com/guest/92837cf338674792a6fb263309573e27
            # name = book.css("img::attr(alt)").get()
            # price = book.css("p.price_color::text").get()
            # yield {
            #     "name": name,
            #     "preço": price,
            #     "link": f'http://books.toscrape.com/{link}'
            # }
        
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def RatingToInt(self, strRating: str) -> int:
            if strRating == 'One':
                return 1
            elif strRating == 'Two':
                return 2
            elif strRating == 'Three':
                return 3
            elif strRating == 'Four':
                return 4
            elif strRating == 'Five':
                return 5
            else:
                return 0   # Valor padrão
    
    def parse_details(self, response):
        name = response.css("h1::text").get()
        price = response.css("p.price_color::text").get()[1:]
        rating = response.css('.product_main').css('p.star-rating::attr(class)').get()[12:]
        upc    = response.css("td::text").get()

        yield {
            "name": name,
            "preço": price,
            'upc': upc,
            'rating': self.RatingToInt(rating)
        }        
