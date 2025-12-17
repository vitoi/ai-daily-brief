import json
import requests
import logging
import os
from news_collector import NewsCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.dirname(current_dir), 'config', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def post_to_facebook(access_token, message):
    url = f'https://graph.facebook.com/v12.0/me/feed'
    data = {
        'message': message,
        'access_token': access_token
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        logger.info("Facebook 发布成功")
    else:
        logger.error(f"Facebook 发布失败: {response.text}")

def format_facebook_post(news_item):
    title = news_item['title']
    link = news_item['link']
    source = news_item['source']
    post = f"{title}\n{link}\n来源: {source}"
    return post

def publish_news_to_facebook():
    config = load_config()
    access_token = config['facebook']['access_token']
    collector = NewsCollector()
    news_items = collector.collect_all_news()
    if not news_items:
        logger.warning("没有收集到新闻")
        return
    post = format_facebook_post(news_items[0])
    post_to_facebook(access_token, post)

if __name__ == "__main__":
    publish_news_to_facebook() 