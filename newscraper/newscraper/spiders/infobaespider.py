import scrapy
from newscraper.items import NewItem



custom_settings = {
    "FEEDS": {
        "infobaedata.json": {"format": "json", "overwrite": True},
    }
}


class InfobaeSpider(scrapy.Spider):
    name = "infobae"
    allowed_domains = ["infobae.com"]
    start_urls = ["https://www.infobae.com/politica"]

    def parse(self, response):
       news = response.css("a.feed-list-card")
       for new in news:
           url = new.css("a").attrib["href"]
           yield response.follow(url, callback=self.parse_new)
        
    def parse_new(self, response):
       
        new_item = NewItem()

        new_item["url"] = response.url
        new_item["title"] = response.css("h1.article-headline::text").get()
        new_item["subtitle"] = response.css("h2.article-subheadline::text").get()
        new_item["date"] = response.css("span.sharebar-article-date::text").get()
        new_item["body"] = response.css("div.body-nota p::text").getall()

        yield new_item


    