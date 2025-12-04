"""
配置文件管理模块
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # API配置
    API_KEY = os.getenv('DIANPING_API_KEY', '')
    API_SECRET = os.getenv('DIANPING_API_SECRET', '')
    BASE_URL = os.getenv('DIANPING_BASE_URL', 'https://api.dianping.com')
    
    # 数据存储配置
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'xlsx')  # xlsx, csv, json
    
    # 请求配置
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.API_KEY or not cls.API_SECRET:
            raise ValueError("请设置 DIANPING_API_KEY 和 DIANPING_API_SECRET 环境变量")
        return True

