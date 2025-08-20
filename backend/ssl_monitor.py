import json
import ssl
import socket
import os
import logging
from datetime import datetime
from urllib.parse import urlparse
import schedule
import time

logger = logging.getLogger(__name__)


class SSLCertMonitor:
    def __init__(self, sites_file=None):
        # sites.json文件在项目根目录
        self.sites_file = sites_file or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sites.json')
        self.sites = self._load_sites()
    
    def _load_sites(self):
        try:
            with open(self.sites_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Invalid sites.json format: expected list")
                logger.info(f"成功加载 {len(data)} 个站点")
                return data
        except FileNotFoundError:
            logger.error(f"文件未找到: {self.sites_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
            return []
        except Exception as e:
            logger.error(f"加载站点时发生未知错误: {e}")
            return []
    
    def add_site(self, name, url):
        self.sites.append({'name': name, 'url': url})
        self._save_sites()
    
    def remove_site(self, url):
        self.sites = [site for site in self.sites if site['url'] != url]
        self._save_sites()
    
    def _save_sites(self):
        with open(self.sites_file, 'w') as f:
            json.dump(self.sites, f, indent=2)
    
    def get_cert_info(self, url):
        try:
            logger.info(f"开始检查证书: {url}")
            hostname = urlparse(f'https://{url}').hostname or url
            context = ssl.create_default_context()
            
            # 增加连接和SSL握手的超时时间
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                # 设置SSL握手超时
                sock.settimeout(10)
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_left = (expire_date - datetime.now()).days
                    
                    logger.info(f"证书检查完成: {url}, 剩余天数: {days_left}")
                    return {
                        'url': url,
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'expire_date': expire_date.isoformat(),
                        'days_left': days_left,
                        'status': 'valid'
                    }
        except Exception as e:
            logger.error(f"证书检查失败: {url}, 错误: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'status': 'error'
            }
    
    def check_all_sites(self):
        logger.info(f"开始检查所有 {len(self.sites)} 个站点的SSL证书")
        results = []
        for site in self.sites:
            result = self.get_cert_info(site['url'])
            result['name'] = site['name']
            results.append(result)
        logger.info(f"完成检查所有站点，共 {len(results)} 个结果")
        return results
    
    def start_scheduled_check(self, interval_days=1, callback=None):
        schedule.every(interval_days).days.do(self._run_check_with_callback, callback)
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def check_and_wait(self, interval_minutes=60, callback=None):
        """执行一次检查并等待指定的时间间隔"""
        logger.info(f"执行定时检查任务，将在 {interval_minutes} 分钟后再次执行")
        results = self.check_all_sites()
        if callback:
            logger.info("调用回调函数")
            callback(results)
        else:
            logger.warning("未设置回调函数")
        
        # 等待指定的时间间隔（分钟）
        logger.info(f"等待 {interval_minutes} 分钟")
        time.sleep(interval_minutes * 60)
        
    def start_scheduled_check_minutes(self, interval_minutes=60, callback=None):
        """执行一次检查并等待指定的时间间隔"""
        logger.info(f"执行定时检查任务，将在 {interval_minutes} 分钟后再次执行")
        results = self.check_all_sites()
        if callback:
            logger.info("调用回调函数")
            callback(results)
        else:
            logger.warning("未设置回调函数")
        
        # 等待指定的时间间隔（分钟）
        logger.info(f"等待 {interval_minutes} 分钟")
        time.sleep(interval_minutes * 60)
    
    def _run_check_with_callback(self, callback):
        logger.info("执行定时检查任务")
        results = self.check_all_sites()
        if callback:
            logger.info("调用回调函数")
            callback(results)
        else:
            logger.warning("未设置回调函数")