import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from typing import List, Dict
import json
import os

class NewsCollector:
    def __init__(self, config_path: str = "config/news_sources.json"):
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.sources = self._load_sources()

    def _load_sources(self) -> Dict:
        """加载新闻源配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)['sources']
        except FileNotFoundError:
            self.logger.error(f"配置文件未找到: {self.config_path}")
            return []

    def collect_rss_news(self, source: Dict) -> List[Dict]:
        """从RSS源收集新闻"""
        try:
            feed = feedparser.parse(source['url'])
            news_items = []
            
            for entry in feed.entries:
                # 只获取最近24小时的新闻
                if datetime.now() - datetime(*entry.published_parsed[:6]) > timedelta(hours=24):
                    continue
                
                news_items.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'summary': entry.summary,
                    'source': source['name']
                })
            
            return news_items
        except Exception as e:
            self.logger.error(f"从 {source['name']} 收集新闻时出错: {str(e)}")
            return []

    def collect_web_news(self, source: Dict) -> List[Dict]:
        """从网页源收集新闻"""
        try:
            response = requests.get(source['url'], headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []
            
            # 根据配置的CSS选择器提取新闻
            for article in soup.select(source['selector']):
                title = article.select_one(source['title_selector'])
                link = article.select_one(source['link_selector'])
                
                if title and link:
                    news_items.append({
                        'title': title.text.strip(),
                        'link': link.get('href', ''),
                        'published': datetime.now().isoformat(),
                        'summary': '',
                        'source': source['name']
                    })
            
            return news_items
        except Exception as e:
            self.logger.error(f"从 {source['name']} 收集新闻时出错: {str(e)}")
            return []

    def collect_all_news(self) -> List[Dict]:
        """收集所有新闻源的新闻"""
        all_news = []
        
        for source in self.sources:
            if source['type'] == 'rss':
                news = self.collect_rss_news(source)
            elif source['type'] == 'web':
                news = self.collect_web_news(source)
            else:
                continue
                
            all_news.extend(news)
        
        # 按发布时间排序
        all_news.sort(key=lambda x: x['published'], reverse=True)
        return all_news 