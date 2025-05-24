import tweepy
import logging
from typing import Dict
import os
import json

class Publisher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._load_config()
        self._setup_twitter()

    def _load_config(self):
        """加载配置文件"""
        try:
            with open('config/config.json', 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            self.logger.error(f"加载配置文件时出错: {str(e)}")
            self.config = {}

    def _setup_twitter(self):
        """设置Twitter API配置"""
        twitter_config = self.config.get('twitter', {})
        self.twitter_client = tweepy.Client(
            consumer_key=twitter_config.get('consumer_key'),
            consumer_secret=twitter_config.get('consumer_secret'),
            access_token=twitter_config.get('access_token'),
            access_token_secret=twitter_config.get('access_token_secret')
        )

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

    def publish_brief(self, brief_content: str, summary: str) -> Dict[str, bool]:
        """发布简报到Twitter"""
        results = {
            'twitter': False
        }
        
        # 发布到Twitter
        results['twitter'] = self.post_to_twitter(summary)
        
        return results 