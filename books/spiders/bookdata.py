# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class BookdataSpider(scrapy.Spider):
    name = 'bookdata'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        links= response.xpath("//h3/a/@href").extract()
        
        for link in links:
            abs_url= response.urljoin(link)
            yield Request(abs_url,callback=self.parse_book)

        next_page= response.xpath('//a[text()="next"]/@href').extract_first()
        next_page= response.urljoin(next_page)
        yield Request(next_page)    

    def parse_book(self,response):

        page_url= str(response)
        page_url= page_url.replace("<200 ","")
        page_url= page_url.replace(">","")
        name= response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()').extract()
        price= response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()').extract()
        img= str(response.xpath('//*[@id="product_gallery"]/div/div/div/img/@src').extract_first())
        img=img.replace('../../','http://books.toscrape.com/')
        description= response.xpath('//*[@id="content_inner"]/article/p/text()').extract()
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        upc= response.xpath('//th[text()="UPC"]/following-sibling::td/text()').extract_first()
        p_type= response.xpath('//th[text()="Product Type"]/following-sibling::td/text()').extract_first()
        price1= response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').extract_first()
        price2= response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').extract_first()
        tax= response.xpath('//th[text()="Tax"]/following-sibling::td/text()').extract_first()
        avilability= response.xpath('//th[text()="Availability"]/following-sibling::td/text()').extract_first()
        reviews= response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').extract_first()
        category= response.xpath('//*[@id="default"]/div[1]/div/ul/li[3]/a/text()').extract()

        yield {
            'title': name,
            'price': price,
            'page_url': page_url,
            'image_url': img,
            'rating': rating,
            'description': description,
            'upc': upc,
            'product_type': p_type,
            'category': category,
            'price_without_tax': price1,
            'price_with_tax': price2,
            'tax': tax,
            'availability': avilability,
            'number_of_reviews': reviews
        }
