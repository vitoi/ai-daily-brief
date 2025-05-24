import tweepy
import logging
from typing import Dict
import os
import json
from datetime import datetime

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
            # 将内容分成多条推文
            lines = content.split('\n')
            tweets = []
            current_tweet = []
            current_length = 0
            
            for line in lines:
                # 如果当前行加上当前推文长度超过270（留出空间给序号和链接），开始新的推文
                if current_length + len(line) + 1 > 270:
                    tweets.append('\n'.join(current_tweet))
                    current_tweet = [line]
                    current_length = len(line)
                else:
                    current_tweet.append(line)
                    current_length += len(line) + 1  # +1 for newline
            
            # 添加最后一条推文
            if current_tweet:
                tweets.append('\n'.join(current_tweet))
            
            # 发布所有推文
            for i, tweet in enumerate(tweets, 1):
                # 添加序号和链接
                if len(tweets) > 1:
                    tweet = f"{i}/{len(tweets)} {tweet}"
                self.twitter_client.create_tweet(text=tweet)
            
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
        twitter_content = f"🤖 AI Daily Brief - {datetime.now().strftime('%Y-%m-%d')}\n\n{summary}"
        results['twitter'] = self.post_to_twitter(twitter_content)
        
        return results 