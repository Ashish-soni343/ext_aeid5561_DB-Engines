import scrapy
import json
import datetime
from ..items import DbEnginesItem


class RankingTrendSpider(scrapy.Spider):
    name = 'ranking_trend'
    project_id = 'rank123'

    allowed_domains = ['http://db-engines.com/']
    start_urls = f"https://db-engines.com/en/ranking_trend"

    # Mandatory Fields Data
    context_identifier = "DB-Engines"
    execution_id = ""
    feed_code = "aeid5561"
    record_create_by = "aeid5561_ranking_trend"
    record_create_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %T')
    site = "https://db-engines.com/en"
    source_country = "Global"
    src = "https://db-engines.com/en/ranking_trend"
    type = "Product Ranking"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 20,
        'DUPEFILTER_DEBUG': True,
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        item = DbEnginesItem()  # Object to store data in items.py
        data = response.xpath('//script[@type="text/javascript"]/text()').get()


        # Removing extra data coming at front and last
        str1, str2 = 'var dbe_data = [', 'var dbe_title'
        idx1, idx2 = data.index(str1), data.index(str2)
        data1 = data[idx1 + len(str1) + 1: idx2]
        data1 = data1[:-1]
        # print("data1===", data1)


        data1 = data1.replace("null", "0").replace("data", '''"data"''').replace("name", '''"name"''').replace(
            "visible", '''"visible"''').replace("false", '''"false"''')
        data1 = data1.replace('''"Tera"data" Aster"''', '''"Teradata Aster"''').replace('''"1010"data""''',
                                                                                        '''"1010data"''').replace(
            '''"Tera"data""''', '''"Teradata"''')



        # splitting data to convert it from string into list
        data2 = data1.split("},")
        print("data2=====", data2)

        ranking = []
        name = []
        visible = []
        lst = []
        months = []
        list_month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


        for d in range(len(data2)):
            data3 = data2[d].rstrip("}]")
            data3 = data3 + "}"
            data3 = json.loads(data3)
            print("data3=====", data3)
            lst.append(data3)


        for dict_1 in range(len(lst)):
            for i, j in lst[dict_1].items():
                year = 2012
                month = 11
                if i == "data":
                    for k in lst[dict_1][i]:

                        if k == 0:                      #
                            ranking.append("Null")
                        else:
                            ranking.append(k)

                        if month == 13:
                            year += 1
                            month = 1

                        months.append(f"{list_month[month-1]} {year}")
                        name.append(lst[dict_1]['name'])
                        month += 1

                        if lst[dict_1].get("visible") == 'false':
                            visible.append("No")
                        else:
                            visible.append("Yes")



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
            yield item







        # for item["Name"] in name:
        #     yield item
        # for item["Ranking"] in ranking:
        #     yield item


        # for visible1 in visible:
        #     item["Visible"] = visible1


        # new_data = {"Ranking": ranking,
        #             "Name": name,
        #             "Visible": visible}


        # df = pd.DataFrame(new_data)

    # for i in range(len(name1)):
    #     items["month"] = {name1[i]: data_lst[i]}
    #     yield items
