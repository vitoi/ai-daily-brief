import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tweepy
import logging
from typing import List, Dict
import os
from dotenv import load_dotenv

class Publisher:
    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self._setup_email()
        self._setup_twitter()

    def _setup_email(self):
        """设置邮件发送配置"""
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.sender_email = os.getenv('SENDER_EMAIL')

    def _setup_twitter(self):
        """设置Twitter API配置"""
        self.twitter_client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

    def send_email(self, recipients: List[str], subject: str, html_content: str) -> bool:
        """发送邮件"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(recipients)
            
            # 添加HTML内容
            msg.attach(MIMEText(html_content, 'html'))
            
            # 连接SMTP服务器并发送
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            self.logger.info(f"成功发送邮件到 {len(recipients)} 个收件人")
            return True
        except Exception as e:
            self.logger.error(f"发送邮件时出错: {str(e)}")
            return False

    def post_to_twitter(self, content: str) -> bool:
        """发布到Twitter"""
        try:
            # 如果内容超过280个字符，需要分段发送
            if len(content) > 280:
                # 简单的分段逻辑，可以改进
                parts = [content[i:i+270] for i in range(0, len(content), 270)]
                for part in parts:
                    self.twitter_client.create_tweet(text=part)
            else:
                self.twitter_client.create_tweet(text=content)
            
            self.logger.info("成功发布到Twitter")
            return True
        except Exception as e:
            self.logger.error(f"发布到Twitter时出错: {str(e)}")
            return False

    def publish_brief(self, brief_content: str, summary: str, recipients: List[str]) -> Dict[str, bool]:
        """发布简报到所有渠道"""
        results = {
            'email': False,
            'twitter': False
        }
        
        # 发送邮件
        if recipients:
            results['email'] = self.send_email(
                recipients=recipients,
                subject=f"AI Daily Brief - {os.getenv('BRIEF_DATE', 'Today')}",
                html_content=brief_content
            )
        
        # 发布到Twitter
        results['twitter'] = self.post_to_twitter(summary)
        
        return results 