#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import *
import calendar
import requests
from FileUtils import FileUtils
from Images import Images



class Wallpaper:

    def __init__(self, **kwargs):
        self.bing_url = "https://www.bing.com"
        self.api = kwargs["url"]
        self.headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42"
                        }
        self.jsonfile = kwargs["jsonfile"]
        self.readme = kwargs["readme"]
        self.file = FileUtils(self.jsonfile, self.readme)
        self.region = kwargs["region"]

    def get_wallpaper(self):
        result = requests.get(self.api, headers=self.headers).json()

        file = FileUtils(self.jsonfile, self.readme)
        all = file.loadJson()

        if not result.get("images"):
            print("API接口出错啦! 请检查接口!")
        
        today = Images(result["images"][0], self.bing_url)
        if all.get("images") and today.date in [ items["enddate"] for items in all["images"] ]:
            print('数据已存在')
        else:
            file.dumpImagesJson(all, today)
            temp = [ item["enddate"][:6] for item in all["images"] ]
            months = list(set(temp))
            months.sort(key=temp.index)
            months.reverse()
            region = self.region
            file.writeToReadme(all, today, months, region)
            print('更新完成')

    def archive(self):
        file = FileUtils(self.jsonfile, self.readme)
        all = file.loadJson()
        if not all["months"]["archive"]:
            if all["months"]["active"]:
                months = all["months"]["active"]
            else:
                temp = [ item["enddate"][:6] for item in all["images"] ]
                months = list(set(temp))
                months.sort(key=temp.index)
        elif all["months"]["archive"]:
            if all["months"]["active"]:
                months = all["months"]["active"]
            else:
                old_archive = all["months"]["archive"]
                total = [ item["enddate"][:6] for item in all["images"] ]
                months = list(set(total) - set(old_archive))
        
        for month in months:
            path = PurePosixPath("archive", self.region, month)
            Path(path).mkdir(parents=True, exist_ok=True)
            file.writeToArchive(all, path, month)
            lastdate = month + str(calendar.monthrange(int(month[:4]), int(month[-2:]))[1])
            if lastdate in [ item["enddate"] for item in all["images"] ]:
                if all["months"]["active"]:
                    all["months"]["active"].remove(month)
                all["months"]["archive"].append(month)
            else:
                if not all["months"]["active"]:
                    all["months"]["active"].append(month)
            file.dumpMonthsJson(all,month)


cn = {"url": "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=zh-cn&setlang=en-us",
      "jsonfile": "bing.json",
      "readme": "README.md",
      "region": "CN"
     }

en = {"url": "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=en-us&setlang=en-us",
      "jsonfile": "bing_en.json",
      "readme": "README_EN.md",
      "region": "US"
     }   

if __name__ == "__main__":
    cnwp = Wallpaper(**cn)
    cnwp.get_wallpaper()
    cnwp.archive()
    enwp = Wallpaper(**en)
    enwp.get_wallpaper()
    enwp.archive()