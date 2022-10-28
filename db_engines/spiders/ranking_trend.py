# Importing libraries here
import scrapy
import json
import datetime
from ..items import DbEnginesItem


# Here spider named "RankingTrendSpider" is created
class RankingTrendSpider(scrapy.Spider):
    name = 'ranking_trend'


    # Here allowed domain and start url of the website are defined that we are crawling
    allowed_domains = ['http://db-engines.com/']
    start_urls = f"https://db-engines.com/en/ranking_trend"


    # Here all Mandatory Fields Data are defined under main class that will be called using "self."
    context_identifier = "DB-Engines"
    execution_id = "621097/1"  # This will be taken automatically from zyte, for now this is hardcoded
    feed_code = "aeid5561"
    record_create_by = "aeid5561_ranking_trend"
    record_create_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %T')
    site = "https://db-engines.com/en"
    source_country = "Global"
    src = "https://db-engines.com/en/ranking_trend"
    type = "Product Ranking"


    # Here we are defining custom settings that are needed for crawling
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 20,
        'DUPEFILTER_DEBUG': True,
    }


    # Here we are defining start_requests function for starting the crawling requests
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)


    # Here we are defining parse function, inside this function we are writing code for crawling the data
    def parse(self, response):
        item = DbEnginesItem()                          # Object to store data in items.py
        data = response.xpath('//script[@type="text/javascript"]/text()').get()     # Here we are fetching script data in which all the ranking data is present


        # Here we are Removing extra data coming at front and end of the script
        str1, str2 = 'var dbe_data = [', 'var dbe_title'
        idx1, idx2 = data.index(str1), data.index(str2)
        data1 = data[idx1 + len(str1) + 1: idx2]
        data1 = data1[:-1]


        # Here we are manipulating and replacing some data to convert the coming script data from string to dictionary
        data1 = data1.replace("null", "0").replace("data", '''"data"''').replace("name", '''"name"''').replace("visible", '''"visible"''').replace("false", '''"false"''')
        data1 = data1.replace('''"Tera"data" Aster"''', '''"Teradata Aster"''').replace('''"1010"data""''', '''"1010data"''').replace('''"Tera"data""''', '''"Teradata"''')


        # Here we are splitting data to convert it from string into list
        data2 = data1.split("},")
        print("data2=====", data2)


        # Here we are passing empty lists for using it in further code to append data
        ranking = []
        name = []
        visible = []
        lst = []
        months = []


        # Here we are defining one list for the month data which will contain all the months name
        list_month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


        # Here we are using for loop and doing some manipulations for converting data coming from script to dictionary
        for d in range(len(data2)):
            data3 = data2[d].rstrip("}]")
            data3 = data3 + "}"
            data3 = json.loads(data3)
            print("data3=====", data3)
            lst.append(data3)           # Here we are appending dictionary data to create a list of dictionaries


        # Here from this for loop we are fetching all the data that are required from website by going one by one inside dictionaries
        for dict_1 in range(len(lst)):
            for i, j in lst[dict_1].items():            # Here we are iterating for "key-value" pairs
                year = 2012                             # Here we are initializing start of year and month from "november 2012" according to website
                month = 11

                if i == "data":
                    for k in lst[dict_1][i]:            # Here loop is iterating for all the ranking data present in list and then providing raking, month, visible and name data

                        if k == 0:                      # for fetching raking data
                            ranking.append("Null")
                        else:
                            ranking.append(k)

                        if month == 13:                 # for fetching month and year data
                            year += 1
                            month = 1
                        months.append(f"{list_month[month - 1]} {year}")

                        name.append(lst[dict_1]['name'])        # for fetching name data
                        month += 1

                        if lst[dict_1].get("visible") == 'false':       # for fetching visible data
                            visible.append("No")
                        else:
                            visible.append("Yes")


        # Here we are using for loop for storing all items data one by one in items.py and some data is taken from self. because we have defined it in the main class
        for i in range(len(name)):
            item["Name"] = name[i]
            item["Month"] = months[i]
            item["Ranking"] = ranking[i]
            item["Visible"] = visible[i]
            item["Context_identifier"] = self.context_identifier
            item["Execution_id"] = self.execution_id
            item["Feed_code"] = self.feed_code
            item["Record_create_by"] = self.record_create_by
            item["Record_create_dt"] = self.record_create_dt
            item["Site"] = self.site
            item["Source_country"] = self.source_country
            item["Src"] = self.src
            item["Type"] = self.type
            yield item                                      # yielding all items here

