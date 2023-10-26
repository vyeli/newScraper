# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from dateutil import parser, tz
from datetime import timedelta

class NewscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        if adapter.get("date"):
            if len(adapter.get("date")) > 1:
                date_str = adapter.get("date")[1]
            else:
                date_str = adapter.get("date")[0]     

            tzinfos = {"EST": tz.gettz("US/Eastern")}
            parsed_date = parser.parse(date_str, tzinfos=tzinfos)
            eastern_time = parsed_date.astimezone(tz.gettz('US/Eastern'))

            arg_time = eastern_time - timedelta(hours=1)
            formatted_time_arg = arg_time.strftime('%Y/%m/%d %H:%M %Z')
            formatted_time_arg = formatted_time_arg.replace("EDT", "AR")
            adapter["date"] = formatted_time_arg

        return item


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .items import NewItem

class MongoPipeline():

    def __init__(self, mongodburi):
        self.mongodburi = mongodburi
        self.mongodb_dbname = "news"
        self.collection = "articles"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodburi=crawler.settings.get("MONGODB_URI"),
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongodburi)
        self.db = self.client[self.mongodb_dbname]

    
    def process_item(self, item, spider):
        data = dict(NewItem(item))
        self.db[self.collection].insert_one(data)
        return item

    def close_spider(self, spider):
        self.client.close()