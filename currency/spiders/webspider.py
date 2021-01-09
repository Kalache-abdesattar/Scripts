import scrapy
import time
import re 


class WebSpider(scrapy.Spider):
    count = 0
    UNTIL_END = 43
    sonnet_heads = []
    pagination = []
    beg_quotes = []
    end_quotes = []

    name = 'SpiderBot'
    start_urls = [
        'https://www.williamshakespeare.net/poems.jsp']


    def parse(self, response):
       time.sleep(2)

       if WebSpider.count == 0:
           heads = response.css("#poem_table a::text").extract()

           for i in range(len(heads) - 1):
               regex_digit = re.compile(r"\d{1,3}")
               digit = regex_digit.findall(heads[i])
               WebSpider.sonnet_heads.append(digit)
               WebSpider.pagination = [x for x in WebSpider.sonnet_heads if x != []]

       elif WebSpider.count > 0:
            poem = response.css("p::text").extract()
            poem.pop()
            yield {'poem': poem}

            for i in range(len(poem)-3):
                 quote1 = re.compile(r"^\s*[a-zA-Z',!?]{1,20}")
                 WebSpider.beg_quotes.append(quote1.findall(poem[i]))

                 quote2 = re.compile(r"[a-zA-Z,?!'.;:]*$")
                 WebSpider.end_quotes.append(quote2.findall(poem[i]))


       next_page = "https://www.williamshakespeare.net/sonnet-{0}.jsp".format(WebSpider.pagination[WebSpider.count][0])


       if WebSpider.count <= len(WebSpider.pagination) - UNTIL_END:
           WebSpider.count += 1
           yield response.follow(next_page, callback=self.parse)















