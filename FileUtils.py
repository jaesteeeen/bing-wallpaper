#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import *
import json
from Images import Images

"""
bing_cn.json, bing_en.json
README.md, README_en.md
folder--archives 1.cn 2.en  eg: archive/CN/202209/  archive/US/202209
json format:
dic = {
       "images": [
                  {"enddate": "20220920", "url": "https://cn.bing.com/th?id=OHR.QueenFuneral_EN-US7710269016_UHD.jpg", "copyright": "Floral tributes left in London, England, following the death of Queen Elizabeth II (\u00a9 Maja Smiejkowska/Reuters)"},
                  {"enddate": "20220921", "url": "https://cn.bing.com/th?id=OHR.SitkaOtters_EN-US7714053956_UHD.jpg", "copyright": "Raft of sea otters in Sitka Sound, near Sitka, Alaska (\u00a9 Robert Harding/Offset/Shutterstock)"},
                  {"enddate": "20220922", "url": "https://cn.bing.com/th?id=OHR.PWPeaceDoves_EN-US7797522376_UHD.jpg", "copyright": "'Peace Doves' by artist Peter Walker in Liverpool Cathedral, Liverpool, England (\u00a9 PAUL ELLIS/AFP via Getty Images)"},
                  {"enddate": "20220923", "url": "https://cn.bing.com/th?id=OHR.LastDollarRoad_EN-US7923638318_UHD.jpg", "copyright": "The aspen canopy along the Last Dollar Road near Telluride, Colorado (\u00a9 Grant Ordelheide/Tandem Stills + Motion)"},
                  {"enddate": "20220924", "url": "https://cn.bing.com/th?id=OHR.GoldenJellyfish_EN-US6743816471_UHD.jpg", "copyright": "Golden jellyfish in Jellyfish Lake on the island of Eil Malk, Palau (\u00a9 Nature Picture Library/Alamy)"},
                  {"enddate": "20220925", "url": "https://cn.bing.com/th?id=OHR.DarkSkyAcadia_EN-US6966527964_UHD.jpg", "copyright": "Milky Way over Acadia National Park, Maine (\u00a9 Harry Collins/Getty Images)"},
                  {"enddate": "20220926", "url": "https://cn.bing.com/th?id=OHR.AmazonMangroves_EN-US7068770726_UHD.jpg", "copyright": "Aerial view of the Amazon River in Brazil (\u00a9 Curioso.Photography/Shutterstock)"},
                  {"enddate": "20220927", "url": "https://cn.bing.com/th?id=OHR.SusitnaRiver_EN-US7154675950_UHD.jpg", "copyright": "Caribou crossing the Susitna River during autumn, Alaska (\u00a9 Tim Plowden/Alamy)"}
                 ],
       "months": {
                  "archive": ["202201","202202","202203","202204","202205","202206","202207","202208"],
                  "active": ["202209"]
                 }
       }
"""

class FileUtils:
    def __init__(self, jsonfile, readmefile):
        self.local_json_path = PurePosixPath(jsonfile)
        self.readme_path = PurePosixPath(readmefile)
        self.dic =  {
                     "images": [],
                     "months": {
                                "archive": [],
                                "active": []
                               }
                    }

    # 读取保存的json文件
    def loadJson(self):
        if Path(self.local_json_path).exists():
            with open(self.local_json_path, "r", encoding="utf-8")as f:
                local_json = json.load(f)
                return local_json
        else:
            return self.dic

    # 将图片信息写入json文件
    def dumpImagesJson(self, jsonData, today):
        if not jsonData or jsonData == None:
            jsonData = self.dic

        with open(self.local_json_path, 'w', encoding="utf-8")as f:
            jsonData["images"].append(today.toJson())
            f.write(json.dumps(jsonData, indent=2, ensure_ascii=False))

    # 将存档年月信息写入json文件
    def dumpMonthsJson(self, jsonData, month):
        if not jsonData or jsonData == None:
            jsonData = self.dic

        with open(self.local_json_path, "w", encoding="utf-8")as f:
            f.write(json.dumps(jsonData, indent=2, ensure_ascii=False))

    # 主目录的README.md
    def writeToReadme(self, items, today, months="", region=""):
        if items == None or today == None:
            return

        # 主目录的readme只展示最近30天的图片
        with open(self.readme_path, "w", encoding="utf-8")as f:
            f.write("## Bing Wallpaper\n")
            f.write("[中文](README.md) | [English](README_EN.md)\n\n")
            f.write(today.toLarge())
            f.write('\n\n|      |      |      |\n')
            f.write('| :----: | :----: | :----: |\n')
            index = 1
            item_list = [ item for item in items["images"] ][-31:-1]
            item_list.reverse()
            for el in item_list:
                el = Images(el)
                f.write('|' + el.toString())
                if index % 3 == 0:
                    f.write('|\n')
                index += 1
            if index % 3 != 1:
                f.write('|')

            f.write("\n\n")
            if "CN" == region:
                f.write("### 历史存档:\n")
            elif "US" == region:
                f.write("### Archive:\n")
            for i in months:
                path = PurePosixPath("archive", region, i, "README.md")
                f.write("[{}-{}]({}) | ".format(i[:4], i[-2:], path))

    # 每月存档readme
    def writeToArchive(self, items, path, month):
        rows = [ item for item in items["images"] if item["enddate"].startswith(str(month)) ]
        last = rows.pop()
        rows.reverse()
        file = PurePosixPath(path, "README.md")
        with open(file, "w", encoding="utf-8")as f:
            f.write('## Bing Wallpaper ({}-{})\n'.format(month[:4],month[-2:]))
            last = Images(last)
            f.write(last.toLarge())
            if rows:
                f.write('\n\n|      |      |      |\n')
                f.write('| :----: | :----: | :----: |\n')
                index = 1
                for row in rows:
                    row = Images(row)
                    f.write('|' + row.toString())
                    if index % 3 == 0:
                        f.write('|\n')
                    index += 1
                if index % 3 != 1:
                    f.write('|')