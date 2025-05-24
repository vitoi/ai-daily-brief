import json
import tweepy
from news_collector import NewsCollector
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.dirname(current_dir), 'config', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def setup_twitter_api():
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

def post_tweet_v2(api, text):
    try:
        api.update_status(text)
        logger.info("推文发布成功")
    except Exception as e:
        logger.error(f"推文发布失败: {str(e)}")

def format_tweet(news_item):
    title = news_item['title']
    link = news_item['link']
    source = news_item['source']
    available_space = 280 - len(link) - 3
    if len(title) > available_space:
        title = title[:available_space-3] + "..."
    tweet = f"{title}\n{link}\n来源: {source}"
    return tweet

def publish_news_v2():
    api = setup_twitter_api()
    collector = NewsCollector()
    news_items = collector.collect_all_news()
    if not news_items:
        logger.warning("没有收集到新闻")
        return
    tweet = format_tweet(news_items[0])
    post_tweet_v2(api, tweet)

if __name__ == "__main__":
    publish_news_v2() 