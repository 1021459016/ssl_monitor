import requests
import json

class WeChatAlert:
    def __init__(self):
        self.webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d5d6cf9f-f7db-4d60-b0a5-78a6e0b98ae9"

    def send_ssl_alert(self, name, url, days_left):
        markdown_content = f"""
### SSL证书到期告警
**网站名称**: {name}
**URL**: {url}
**剩余天数**: <font color=\"warning\">{days_left}</font>天

请及时处理证书续期问题！
"""
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": markdown_content
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=10  # 添加超时时间
            )
            data = response.json()
            if data.get('errcode') == 0:
                return True, "告警发送成功"
            else:
                return False, data.get('errmsg', '未知错误')
        except Exception as e:
            return False, str(e)