# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DbEnginesItem(scrapy.Item):
    # define the fields for your item here like:
    Ranking = scrapy.Field()
    Month = scrapy.Field()
    Name = scrapy.Field()
    Visible = scrapy.Field()
    Context_identifier = scrapy.Field()
    Execution_id = scrapy.Field()
    Feed_code = scrapy.Field()
    Record_create_by = scrapy.Field()
    Record_create_dt = scrapy.Field()
    Site = scrapy.Field()
    Source_country = scrapy.Field()
    Src = scrapy.Field()
    Type = scrapy.Field()

