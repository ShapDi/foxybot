import os
from loguru import logger
import json
from datetime import datetime

import googleapiclient.discovery
import googleapiclient.errors


logger.add("logs.log", format="{time} {level} {message} {name}", level="ERROR")




API_KEY = "AIzaSyDQ7UJO7azG6w6pRCrngIEZ30n4_jFyCDc"

class YouTubeAggregator():
    api_service_name = 'youtube'
    api_version = 'v3'
    API = "AIzaSyDQ7UJO7azG6w6pRCrngIEZ30n4_jFyCDc"
    def __init__(self,links ):
        self._links = links

    @classmethod
    def get_settings(cls):
        youtube = googleapiclient.discovery.build(
            cls.api_service_name, cls.api_version, developerKey = cls.API)
        return youtube

    @staticmethod
    def string_conversion(ids:list):
        line = ''
        for id in ids:
            line = line + f"{id},"
    @staticmethod
    def date_formatting(time):
        time = str(time).split('T')[0]
        time = datetime.strptime(time,"%Y-%m-%d").strftime("%d.%m.%Y")
        return time


    def data_cleaning(self):
        self._links = [(link).replace("https://youtube.com/shorts/","").replace("https://www.youtube.com/shorts/","").replace("?feature=share4","").replace("?feature=share3","").replace("?feature=share","") for link in self._links]

    def get_parts(self):
        for i in range(0,len(self._links),50):
            yield self._links[i:i+50]

    def start_request(self,data):
        request = self.get_settings().videos().list(
            part="id,snippet,statistics",
            id=data
        )
        response = request.execute()
        return response

    def get_data(self):
            self.data_cleaning()
            data = []
            for portion_id in self.get_parts():
                self.string_conversion(portion_id)
                resalt = self.start_request(portion_id)
                resalt = resalt["items"]
                try:
                    resalt = [{f"https://www.youtube.com/shorts/{media['id']}":{"viewCount":media['statistics'].get('viewCount'),
                                                                            "commentCount":media['statistics'].get('commentCount'),
                                                                            "likeCount": media['statistics'].get('likeCount'),
                                                                            "date":f"{self.date_formatting(media['snippet']['publishedAt'])}"}} for media in resalt]
                except Exception as f:
                    logger.error(f'{f} ')
                data = data + resalt
            return data












