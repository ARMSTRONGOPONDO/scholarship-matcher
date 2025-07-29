# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GovChatbotFAQItem(scrapy.Item):
    # Data fields for the FAQ items
    question = scrapy.Field()
    answer = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    date_posted = scrapy.Field()
    date_updated = scrapy.Field()
    image = scrapy.Field()
