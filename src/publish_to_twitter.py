import json
import tweepy
from news_collector import NewsCollector
from datetime import datetime, timezone
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """加载Twitter配置"""
    try:
        # 获取当前文件所在目录的父目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(current_dir), 'config', 'config.json')
        
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        raise

def setup_twitter_api():
    """设置Twitter API客户端"""
    config = load_config()
    auth = tweepy.OAuthHandler(
        config['twitter']['consumer_key'],
        config['twitter']['consumer_secret']
    )
    auth.set_access_token(
        config['twitter']['access_token'],
        config['twitter']['access_token_secret']
    )
    return tweepy.API(auth)

def format_tweet(news_item):
    """格式化推文内容"""
    # 确保标题和链接不超过280字符
    title = news_item['title']
    link = news_item['link']
    source = news_item['source']
    
    # 计算可用空间（考虑链接长度和换行符）
    available_space = 280 - len(link) - 3  # 3是换行符的长度
    
    # 如果标题太长，截断它
    if len(title) > available_space:
        title = title[:available_space-3] + "..."
    
    # 构建推文
    tweet = f"{title}\n{link}\n来源: {source}"
    return tweet

def publish_news():
    """收集新闻并发布到Twitter"""
    try:
        # 初始化Twitter API
        api = setup_twitter_api()
        
        # 收集新闻
        collector = NewsCollector()
        news_items = collector.collect_all_news()
        
        if not news_items:
            logger.warning("没有收集到新闻")
            return
        
        # 发布新闻
        for news_item in news_items:
            try:
                tweet = format_tweet(news_item)
                api.update_status(tweet)
                logger.info(f"成功发布推文: {tweet[:50]}...")
            except Exception as e:
                logger.error(f"发布推文失败: {str(e)}")
                continue
        
        logger.info(f"成功发布 {len(news_items)} 条新闻到Twitter")
        
    except Exception as e:
        logger.error(f"发布过程出错: {str(e)}")
        raise

if __name__ == "__main__":
    publish_news() 