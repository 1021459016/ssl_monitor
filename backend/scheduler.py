import threading
import time
import logging
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.ssl_monitor import SSLCertMonitor
from backend.wechat_alert import WeChatAlert
from backend.config import Config
import configparser

logger = logging.getLogger(__name__)

# 配置管理
config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'app.conf')
app_config = configparser.ConfigParser()

monitor = SSLCertMonitor()
wechat_alert = WeChatAlert()


def start_scheduled_check():
    def alert_callback(results):
        logger.info(f"定时任务回调函数开始执行，处理 {len(results)} 个证书")
        # 读取配置文件
        if os.path.exists(config_file):
            app_config.read(config_file, encoding='utf-8')
        
        alert_threshold_days = int(app_config.get('SCHEDULE', 'alert_threshold_days', fallback='30'))
        
        for cert in results:
            if cert['status'] != 'error' and cert['days_left'] <= alert_threshold_days:
                logger.info(f"发送告警: {cert['name']} ({cert['url']}) 剩余天数: {cert['days_left']}")
                wechat_alert.send_ssl_alert(cert['name'], cert['url'], cert['days_left'])
    
    def scheduled_task():
        while True:
            # 每次执行前都重新读取配置文件
            if os.path.exists(config_file):
                app_config.read(config_file, encoding='utf-8')
            
            check_interval_minutes = int(app_config.get('SCHEDULE', 'check_interval_minutes', fallback='60'))
            logger.info(f"启动定时检查任务，间隔: {check_interval_minutes} 分钟")
            
            # 执行检查并等待
            monitor.check_and_wait(check_interval_minutes, alert_callback)
    
    # 在单独的线程中运行定时任务
    task_thread = threading.Thread(target=scheduled_task, daemon=True)
    task_thread.start()


def run_scheduler():
    logger.info("正在启动定时检查任务线程...")
    scheduler_thread = threading.Thread(
        target=start_scheduled_check,
        daemon=True
    )
    scheduler_thread.start()
    
    # 增加一个短暂的延迟，确保调度线程正确启动
    time.sleep(1)
    
    return scheduler_thread

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    run_scheduler()
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("调度器已停止")