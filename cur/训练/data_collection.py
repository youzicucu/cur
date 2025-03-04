import sys
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import json

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import (
    FOOTBALL_DATA_API_KEY, JUHE_API_KEY,
    WEATHER_API_KEY, OPENWEATHER_API_KEY,
    FOOTBALL_DATA_BASE_URL, JUHE_BASE_URL,
    WEATHER_BASE_URL, OPENWEATHER_BASE_URL,
    SOCCERSTATS_URL, FBREF_URL
)

class DataCollector:
    def __init__(self):
        self.headers = {
            'X-Auth-Token': FOOTBALL_DATA_API_KEY
        }
        
    def get_football_data_matches(self):
        """从football-data.org获取比赛数据"""
        url = f"{FOOTBALL_DATA_BASE_URL}/matches"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_juhe_matches(self):
        """从聚合数据获取比赛数据"""
        params = {
            'key': JUHE_API_KEY
        }
        response = requests.get(JUHE_BASE_URL, params=params)
        return response.json()
    
    def get_weather_data(self, city):
        """获取天气数据"""
        # WeatherAPI.com
        weather_params = {
            'key': WEATHER_API_KEY,
            'q': city,
            'days': 3
        }
        weather_response = requests.get(f"{WEATHER_BASE_URL}/forecast.json", 
                                     params=weather_params)
        
        # OpenWeatherMap
        openweather_params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        openweather_response = requests.get(f"{OPENWEATHER_BASE_URL}/weather", 
                                          params=openweather_params)
        
        return {
            'weather_api': weather_response.json(),
            'openweather': openweather_response.json()
        }
    
    def scrape_soccerstats(self):
        """从Soccerstats爬取数据"""
        response = requests.get(SOCCERSTATS_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 实现具体的爬虫逻辑
        return {}
    
    def scrape_fbref(self):
        """从FBref爬取数据"""
        response = requests.get(FBREF_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 实现具体的爬虫逻辑
        return {}
    
    def collect_all_data(self):
        """收集所有数据并整合"""
        data = {
            'football_data': self.get_football_data_matches(),
            'juhe': self.get_juhe_matches(),
            'soccerstats': self.scrape_soccerstats(),
            'fbref': self.scrape_fbref()
        }
        
        # 为每场比赛添加天气数据
        for match in data['football_data']['matches']:
            if 'venue' in match:
                weather = self.get_weather_data(match['venue'])
                match['weather'] = weather
                time.sleep(1)  # 避免API限制
        
        return data
    
    def save_data(self, data, filename):
        """保存收集的数据"""
        save_dir = '/content/drive/MyDrive/football_data'
        os.makedirs(save_dir, exist_ok=True)
        
        with open(f'{save_dir}/{filename}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    collector = DataCollector()
    
    print("开始收集数据...")
    data = collector.collect_all_data()
    
    # 使用当前时间戳作为文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    collector.save_data(data, f'football_data_{timestamp}.json')
    
    print("数据收集完成并保存")

if __name__ == "__main__":
    main() 