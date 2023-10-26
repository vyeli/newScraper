# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from bs4 import BeautifulSoup

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