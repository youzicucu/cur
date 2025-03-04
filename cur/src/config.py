import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
FOOTBALL_DATA_API_KEY = "f279e848892a4c29a9566eee5c0efc6b"
JUHE_API_KEY = "cae363180b05da7f0e1e403983c333b5"
WEATHER_API_KEY = "65c9108e18384fd7b86124602252502"
OPENWEATHER_API_KEY = "2dd63557fd0634766c1acf002af83dec"

# API端点
FOOTBALL_DATA_BASE_URL = "http://api.football-data.org/v2"
JUHE_BASE_URL = "http://apis.juhe.cn/fapig/football/query"
WEATHER_BASE_URL = "http://api.weatherapi.com/v1"
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"

# 爬虫配置
SOCCERSTATS_URL = "https://www.soccerstats.com"
FBREF_URL = "https://fbref.com"

# 数据库配置
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "football_predictions"

# 模型配置
MODEL_PARAMS = {
    "poisson": {
        "iterations": 1000,
        "burn_in": 100
    },
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": 42
    },
    "lstm": {
        "units": 64,
        "dropout": 0.2,
        "epochs": 100,
        "batch_size": 32
    }
}

# 网页配置
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your-secret-key-here")
DEBUG = True 