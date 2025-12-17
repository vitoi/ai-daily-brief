import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import logging
from typing import List, Dict
import json
import os
import re
import random
import time
import urllib3
from fake_useragent import UserAgent
from ratelimit import limits, sleep_and_retry
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NewsCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # AI相关的关键词
        self.ai_keywords = [
            'AI model', 'LLM', 'Large Language Model', 'GPT', 'Claude', 'Gemini',
            'AI agent', 'autonomous agent', 'AI assistant', 'AI chatbot',
            'machine learning model', 'deep learning model', 'neural network',
            'transformer', 'diffusion model', 'stable diffusion', 'midjourney',
            'dall-e', 'sora', 'anthropic', 'openai', 'google ai', 'meta ai',
            'microsoft ai', 'amazon ai', 'apple ai',
            # 中文关键词
            '人工智能', 'AI模型', '大语言模型', 'GPT', 'Claude', 'Gemini',
            'AI助手', 'AI聊天机器人', '机器学习', '深度学习', '神经网络',
            'Transformer', '扩散模型', 'Stable Diffusion', 'Midjourney',
            'DALL-E', 'Sora', 'Anthropic', 'OpenAI', '谷歌AI', 'Meta AI',
            '微软AI', '亚马逊AI', '苹果AI'
        ]
        # 新闻源配置
        self.sources = {
            'zdnet': {
                'url': 'https://www.zdnet.com/topic/artificial-intelligence/',
                'rss_url': 'https://www.zdnet.com/news/rss.xml',
                'article_selector': 'article',
                'title_selector': 'h3 a, h4 a',
                'link_selector': 'h3 a, h4 a',
                'date_selector': 'time',
                'summary_selector': 'p.summary, p',
                'request_interval': 5,  # 请求间隔（秒）
                'max_requests_per_hour': 100  # 每小时最大请求数
            },
            'sina_tech': {
                'url': 'https://tech.sina.com.cn/rollnews.shtml',  # 新浪科技滚动新闻
                'article_selector': '.tech-news-item',
                'title_selector': 'h2 a',
                'link_selector': 'h2 a',
                'date_selector': '.time',
                'summary_selector': '.tech-news-item p',
                'request_interval': 5,
                'max_requests_per_hour': 100
            },
            'tencent_tech': {
                'url': 'https://new.qq.com/ch2/tech',  # 腾讯科技频道
                'article_selector': '.list .item',
                'title_selector': '.title',
                'link_selector': 'a',
                'date_selector': '.time',
                'summary_selector': '.detail',
                'request_interval': 5,
                'max_requests_per_hour': 100
            },
            '36kr': {
                'url': 'https://36kr.com/information/ai',  # 36氪AI资讯
                'article_selector': '.article-item',
                'title_selector': '.title-wrapper',
                'link_selector': 'a',
                'date_selector': '.time-stamp',
                'summary_selector': '.summary',
                'request_interval': 5,
                'max_requests_per_hour': 100
            },
            'theverge_ai': {
                'url': 'https://www.theverge.com/artificial-intelligence-ai',
                'article_selector': 'div.c-compact-river__entry',
                'title_selector': 'h2.c-entry-box--compact__title a',
                'link_selector': 'h2.c-entry-box--compact__title a',
                'date_selector': 'time',
                'summary_selector': 'p.p-dek',
            },
            'techcrunch_ai_rss': {
                'rss_url': 'https://techcrunch.com/tag/artificial-intelligence/feed/'
            },
            'venturebeat_ai_rss': {
                'rss_url': 'https://venturebeat.com/category/ai/feed/'
            },
        }
        
        # 初始化User-Agent生成器
        self.ua = UserAgent()
        
        # 初始化请求会话
        self.session = requests.Session()
        self.session.verify = False  # 禁用SSL验证
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',  # 添加中文语言支持
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def _check_robots_txt(self, url: str) -> bool:
        """检查目标URL是否允许爬虫访问"""
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(self.ua.random, url)
        except Exception as e:
            self.logger.warning(f"检查robots.txt失败: {str(e)}")
            return True  # 如果无法检查robots.txt，默认允许访问

    def _random_delay(self, min_seconds=2, max_seconds=5):
        """随机延迟，避免固定间隔请求"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    @sleep_and_retry
    @limits(calls=100, period=3600)  # 限制每小时最多100次请求
    def _make_request(self, url: str, max_retries=3) -> requests.Response:
        """发送HTTP请求，带有速率限制和随机User-Agent"""
        # 检查robots.txt
        if not self._check_robots_txt(url):
            self.logger.warning(f"根据robots.txt规则，不允许访问: {url}")
            raise requests.exceptions.RequestException("Access denied by robots.txt")

        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',  # 添加中文语言支持
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, headers=headers, timeout=30, verify=False)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                self.logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                self._random_delay(2, 5)  # 在重试之前等待

    def _is_ai_related(self, title: str, summary: str) -> bool:
        """检查新闻是否与AI相关"""
        text = (title + ' ' + summary).lower()
        return any(keyword.lower() in text for keyword in self.ai_keywords)

    def _parse_date(self, date_str: str) -> datetime:
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
            return dt.astimezone(timezone.utc)
        except ValueError:
            return datetime.now(timezone.utc)

    def _collect_from_zdnet_rss(self) -> List[Dict]:
        """从ZDNet RSS源收集新闻"""
        try:
            self.logger.info("开始从ZDNet RSS源收集新闻...")
            response = self._make_request(self.sources['zdnet']['rss_url'])
            feed = feedparser.parse(response.content)
            news_items = []
            
            for entry in feed.entries:
                try:
                    title = entry.title
                    link = entry.link
                    summary = entry.summary if hasattr(entry, 'summary') else ''
                    date = self._parse_date(entry.published)
                    
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': 'ZDNet AI (RSS)'
                        })
                except Exception as e:
                    self.logger.warning(f"处理RSS条目时出错: {str(e)}")
                    continue
                
                # 添加随机延迟
                self._random_delay(0.5, 1.5)
            
            self.logger.info(f"从ZDNet RSS源收集到 {len(news_items)} 条新闻")
            return news_items
        except Exception as e:
            self.logger.error(f"从ZDNet RSS源收集新闻时出错: {str(e)}")
            return []

    def _collect_from_zdnet(self) -> List[Dict]:
        """从ZDNet收集新闻"""
        try:
            self.logger.info("开始从ZDNet收集新闻...")
            
            # 尝试加载页面
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self._make_request(self.sources['zdnet']['url'])
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    self.logger.warning(f"加载页面失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                    self._random_delay(2, 5)

            # 等待页面加载
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.select(self.sources['zdnet']['article_selector'])
            except Exception as e:
                self.logger.warning("等待页面加载超时，尝试使用RSS源...")
                return self._collect_from_zdnet_rss()
            
            # 获取所有新闻文章
            news_items = []
            for article in articles:
                try:
                    # 获取标题和链接
                    title_element = None
                    link_element = None
                    for selector in self.sources['zdnet']['title_selector'].split(','):
                        selector = selector.strip()
                        try:
                            title_element = article.find(selector)
                            link_element = title_element
                            if title_element and title_element.text.strip():
                                break
                        except Exception:
                            continue
                    if not title_element or not link_element:
                        continue
                    title = title_element.text.strip()
                    link = link_element.get('href')

                    # 获取摘要
                    summary_element = None
                    for selector in self.sources['zdnet']['summary_selector'].split(','):
                        selector = selector.strip()
                        try:
                            summary_element = article.find(selector)
                            if summary_element and summary_element.text.strip():
                                break
                        except Exception:
                            continue
                    summary = summary_element.text.strip() if summary_element else ''

                    # 获取日期
                    date_element = article.find(self.sources['zdnet']['date_selector'])
                    date_str = date_element.get('datetime') if date_element else ''
                    date = self._parse_date(date_str)
                    
                    # 只收集AI相关的新闻
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': 'ZDNet AI'
                        })
                except Exception as e:
                    self.logger.warning(f"处理文章时出错: {str(e)}")
                    continue
                
                # 添加随机延迟
                self._random_delay(0.5, 1.5)
            
            self.logger.info(f"从ZDNet收集到 {len(news_items)} 条新闻")
            
            # 如果没有收集到新闻，尝试使用RSS源
            if not news_items:
                self.logger.info("未从网页收集到新闻，尝试使用RSS源...")
                return self._collect_from_zdnet_rss()
            
            return news_items
        except Exception as e:
            self.logger.error(f"从ZDNet收集新闻时出错: {str(e)}")
            # 如果网页采集失败，尝试使用RSS源
            self.logger.info("网页采集失败，尝试使用RSS源...")
            return self._collect_from_zdnet_rss()

    def _collect_from_sina_tech(self) -> List[Dict]:
        """从新浪科技收集新闻"""
        try:
            self.logger.info("开始从新浪科技收集新闻...")
            response = self._make_request(self.sources['sina_tech']['url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select(self.sources['sina_tech']['article_selector'])
            
            news_items = []
            for article in articles:
                try:
                    title_element = article.select_one(self.sources['sina_tech']['title_selector'])
                    if not title_element:
                        continue
                    
                    title = title_element.text.strip()
                    link = title_element.get('href')
                    if not link.startswith('http'):
                        link = 'https:' + link
                    
                    summary_element = article.select_one(self.sources['sina_tech']['summary_selector'])
                    summary = summary_element.text.strip() if summary_element else ''
                    
                    date_element = article.select_one(self.sources['sina_tech']['date_selector'])
                    date_str = date_element.text.strip() if date_element else ''
                    date = self._parse_date(date_str)
                    
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': '新浪科技'
                        })
                except Exception as e:
                    self.logger.warning(f"处理新浪科技文章时出错: {str(e)}")
                    continue
                
                self._random_delay(0.5, 1.5)
            
            self.logger.info(f"从新浪科技收集到 {len(news_items)} 条新闻")
            return news_items
        except Exception as e:
            self.logger.error(f"从新浪科技收集新闻时出错: {str(e)}")
            return []

    def _collect_from_tencent_tech(self) -> List[Dict]:
        """从腾讯科技收集新闻"""
        try:
            self.logger.info("开始从腾讯科技收集新闻...")
            response = self._make_request(self.sources['tencent_tech']['url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select(self.sources['tencent_tech']['article_selector'])
            
            news_items = []
            for article in articles:
                try:
                    title_element = article.select_one(self.sources['tencent_tech']['title_selector'])
                    if not title_element:
                        continue
                    
                    title = title_element.text.strip()
                    link = article.select_one(self.sources['tencent_tech']['link_selector'])['href']
                    if not link.startswith('http'):
                        link = 'https:' + link
                    
                    summary_element = article.select_one(self.sources['tencent_tech']['summary_selector'])
                    summary = summary_element.text.strip() if summary_element else ''
                    
                    date_element = article.select_one(self.sources['tencent_tech']['date_selector'])
                    date_str = date_element.text.strip() if date_element else ''
                    date = self._parse_date(date_str)
                    
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': '腾讯科技'
                        })
                except Exception as e:
                    self.logger.warning(f"处理腾讯科技文章时出错: {str(e)}")
                    continue
                
                self._random_delay(0.5, 1.5)
            
            self.logger.info(f"从腾讯科技收集到 {len(news_items)} 条新闻")
            return news_items
        except Exception as e:
            self.logger.error(f"从腾讯科技收集新闻时出错: {str(e)}")
            return []

    def _collect_from_36kr(self) -> List[Dict]:
        """从36氪收集新闻"""
        try:
            self.logger.info("开始从36氪收集新闻...")
            response = self._make_request(self.sources['36kr']['url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select(self.sources['36kr']['article_selector'])
            
            news_items = []
            for article in articles:
                try:
                    title_element = article.select_one(self.sources['36kr']['title_selector'])
                    if not title_element:
                        continue
                    
                    title = title_element.text.strip()
                    link = article.select_one(self.sources['36kr']['link_selector'])['href']
                    if not link.startswith('http'):
                        link = 'https://36kr.com' + link
                    
                    summary_element = article.select_one(self.sources['36kr']['summary_selector'])
                    summary = summary_element.text.strip() if summary_element else ''
                    
                    date_element = article.select_one(self.sources['36kr']['date_selector'])
                    date_str = date_element.text.strip() if date_element else ''
                    date = self._parse_date(date_str)
                    
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': '36氪'
                        })
                except Exception as e:
                    self.logger.warning(f"处理36氪文章时出错: {str(e)}")
                    continue
                
                self._random_delay(0.5, 1.5)
            
            self.logger.info(f"从36氪收集到 {len(news_items)} 条新闻")
            return news_items
        except Exception as e:
            self.logger.error(f"从36氪收集新闻时出错: {str(e)}")
            return []

    def _collect_from_theverge_ai(self) -> List[Dict]:
        try:
            self.logger.info("开始从The Verge AI收集新闻...")
            response = self._make_request(self.sources['theverge_ai']['url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select(self.sources['theverge_ai']['article_selector'])
            news_items = []
            for article in articles:
                try:
                    title_element = article.select_one(self.sources['theverge_ai']['title_selector'])
                    if not title_element:
                        continue
                    title = title_element.text.strip()
                    link = title_element.get('href')
                    summary_element = article.select_one(self.sources['theverge_ai']['summary_selector'])
                    summary = summary_element.text.strip() if summary_element else ''
                    date_element = article.select_one(self.sources['theverge_ai']['date_selector'])
                    date_str = date_element.get('datetime') if date_element else ''
                    date = self._parse_date(date_str)
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': 'The Verge AI'
                        })
                except Exception as e:
                    self.logger.warning(f"处理The Verge文章时出错: {str(e)}")
                    continue
                self._random_delay(0.2, 0.6)
            self.logger.info(f"从The Verge收集到 {len(news_items)} 条新闻")
            return news_items
        except Exception as e:
            self.logger.error(f"从The Verge收集新闻时出错: {str(e)}")
            return []

    def _collect_from_techcrunch_rss(self) -> List[Dict]:
        try:
            self.logger.info("开始从TechCrunch AI RSS收集新闻...")
            response = self._make_request(self.sources['techcrunch_ai_rss']['rss_url'])
            feed = feedparser.parse(response.content)
            news_items = []
            for entry in feed.entries:
                try:
                    title = entry.title
                    link = entry.link
                    summary = entry.summary if hasattr(entry, 'summary') else ''
                    date = self._parse_date(entry.published) if hasattr(entry, 'published') else datetime.now()
                    print(f"TechCrunch RSS原始标题: {title}")
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': 'TechCrunch AI (RSS)'
                        })
                except Exception as e:
                    self.logger.warning(f"处理TechCrunch RSS条目时出错: {str(e)}")
                    continue
                self._random_delay(0.2, 0.6)
            self.logger.info(f"从TechCrunch RSS收集到 {len(news_items)} 条新闻")
            return news_items
        except Exception as e:
            self.logger.error(f"从TechCrunch RSS收集新闻时出错: {str(e)}")
            return []

    def _collect_from_venturebeat_rss(self) -> List[Dict]:
        try:
            self.logger.info("开始从VentureBeat AI RSS收集新闻...")
            response = self._make_request(self.sources['venturebeat_ai_rss']['rss_url'])
            feed = feedparser.parse(response.content)
            news_items = []
            for entry in feed.entries:
                try:
                    title = entry.title
                    link = entry.link
                    summary = entry.summary if hasattr(entry, 'summary') else ''
                    date = self._parse_date(entry.published) if hasattr(entry, 'published') else datetime.now()
                    print(f"VentureBeat RSS原始标题: {title}")
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': 'VentureBeat AI (RSS)'
                        })
                except Exception as e:
                    self.logger.warning(f"处理VentureBeat RSS条目时出错: {str(e)}")
                    continue
                self._random_delay(0.2, 0.6)
            self.logger.info(f"从VentureBeat RSS收集到 {len(news_items)} 条新闻")
            return news_items
        except Exception as e:
            self.logger.error(f"从VentureBeat RSS收集新闻时出错: {str(e)}")
            return []

    def _collect_from_arxiv(self, query="artificial intelligence", max_results=20) -> List[Dict]:
        try:
            self.logger.info("开始从arXiv API收集AI论文...")
            # 使用官方API，添加适当的请求头
            base_url = "http://export.arxiv.org/api/query"
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; AI-Daily-Brief/1.0; +https://github.com/yourusername/ai-daily-brief)',
                'Accept': 'application/xml',
                'From': 'your-email@example.com'  # 建议替换为实际邮箱
            }
            
            response = self.session.get(
                base_url,
                params=params,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            news_items = []
            
            for entry in feed.entries:
                try:
                    title = entry.title
                    link = entry.link
                    summary = entry.summary if hasattr(entry, 'summary') else ''
                    date = self._parse_date(entry.published) if hasattr(entry, 'published') else datetime.now()
                    print(f"arXiv原始标题: {title}")
                    
                    # 添加更多元数据
                    authors = [author.name for author in entry.authors] if hasattr(entry, 'authors') else []
                    categories = [tag.term for tag in entry.tags] if hasattr(entry, 'tags') else []
                    
                    if self._is_ai_related(title, summary):
                        news_items.append({
                            'title': title,
                            'link': link,
                            'published': date,
                            'summary': summary,
                            'source': 'arXiv',
                            'authors': authors,
                            'categories': categories
                        })
                except Exception as e:
                    self.logger.warning(f"处理arXiv条目时出错: {str(e)}")
                    continue
                
                # 遵循arXiv API使用条款，每次请求后等待3秒
                self._random_delay(3, 5)
            
            self.logger.info(f"从arXiv收集到 {len(news_items)} 条论文")
            return news_items
        except Exception as e:
            self.logger.error(f"从arXiv收集论文时出错: {str(e)}")
            return []

    def collect_all_news(self) -> List[Dict]:
        all_news = []
        sources = [
            self._collect_from_arxiv,
            self._collect_from_techcrunch_rss,
            # self._collect_from_venturebeat_rss  # 暂时注释掉VentureBeat采集
        ]
        for source_func in sources:
            try:
                news = source_func()
                all_news.extend(news)
                self._random_delay(1, 2)
            except Exception as e:
                self.logger.error(f"收集新闻时出错: {str(e)}")
                continue
        all_news.sort(key=lambda x: x['published'], reverse=True)
        return all_news 