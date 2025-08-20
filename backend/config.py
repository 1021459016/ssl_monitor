import os
from dotenv import load_dotenv

# 加载配置目录中的.env文件
env_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    # 企业微信配置
    CORP_ID = os.getenv('CORP_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    AGENT_ID = os.getenv('AGENT_ID')
    
    # 监控配置
    CHECK_INTERVAL_DAYS = int(os.getenv('CHECK_INTERVAL_DAYS', 1))
    ALERT_BEFORE_DAYS = int(os.getenv('ALERT_BEFORE_DAYS', 30))
    
    # 示例网站列表
    SAMPLE_SITES = [
        {'name': 'Example', 'url': 'example.com'},
        {'name': 'Google', 'url': 'google.com'},
        {'name': 'GitHub', 'url': 'github.com'}
    ]