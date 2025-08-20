import os
import sys
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.ssl_monitor import SSLCertMonitor
from backend.wechat_alert import WeChatAlert
from backend.config import Config
import threading
import json
import configparser
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
monitor = SSLCertMonitor()
wechat_alert = WeChatAlert()

# 配置管理
config_file = os.path.join(os.path.dirname(__file__), 'config', 'app.conf')
app_config = configparser.ConfigParser()

# 初始化配置文件
if not os.path.exists(config_file):
    app_config['SCHEDULE'] = {
        'check_interval_minutes': '60',
        'alert_threshold_days': '30'
    }
    with open(config_file, 'w', encoding='utf-8') as f:
        app_config.write(f)
else:
    app_config.read(config_file, encoding='utf-8')

@app.route('/api/alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    success, message = wechat_alert.send_ssl_alert(
        name=data['name'],
        url=data['url'],
        days_left=data['days_left']
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/sites', methods=['GET'])
def get_sites():
    return jsonify(monitor.sites)

@app.route('/api/sites', methods=['POST'])
def add_site():
    data = request.get_json()
    monitor.add_site(data['name'], data['url'])
    return jsonify({'status': 'success'})

@app.route('/api/sites/<path:url>', methods=['DELETE'])
def remove_site(url):
    monitor.remove_site(url)
    return jsonify({'status': 'success'})

@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'frontend'), 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'frontend'), filename)

@app.route('/api/certificates', methods=['GET'])
def get_certificates():
    results = monitor.check_all_sites()
    return jsonify(results)

@app.route('/api/config', methods=['GET'])
def get_config():
    # 读取配置文件
    if os.path.exists(config_file):
        app_config.read(config_file, encoding='utf-8')
    
    return jsonify({
        'check_interval_minutes': int(app_config.get('SCHEDULE', 'check_interval_minutes', fallback='60')),
        'alert_threshold_days': int(app_config.get('SCHEDULE', 'alert_threshold_days', fallback='30'))
    })

@app.route('/api/config', methods=['POST'])
def save_config():
    data = request.get_json()
    
    # 更新配置
    if not app_config.has_section('SCHEDULE'):
        app_config.add_section('SCHEDULE')
    
    app_config.set('SCHEDULE', 'check_interval_minutes', str(data.get('check_interval_minutes', 60)))
    app_config.set('SCHEDULE', 'alert_threshold_days', str(data.get('alert_threshold_days', 30)))
    
    # 保存到文件
    with open(config_file, 'w') as f:
        app_config.write(f)
    
    return jsonify({'status': 'success'})

# 启动定时任务线程
# 使用gunicorn启动时，需要确保定时任务只启动一次
if not hasattr(app, '_scheduler_started'):
    from backend.scheduler import run_scheduler
    scheduler_thread = run_scheduler()
    app._scheduler_started = True
    logger.info("定时任务线程已启动")

if __name__ == '__main__':
    logger.info("Flask应用开始监听 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)