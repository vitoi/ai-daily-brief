from typing import List, Dict
import jinja2
import os
from datetime import datetime
import nltk
from nltk.tokenize import sent_tokenize
import logging

class BriefGenerator:
    def __init__(self, template_dir: str = "config/templates"):
        self.template_dir = template_dir
        self.logger = logging.getLogger(__name__)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )
        
        # 下载必要的NLTK数据
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def categorize_news(self, news_items: List[Dict]) -> Dict[str, List[Dict]]:
        """将新闻按类别分类"""
        categories = {
            'research': [],
            'industry': [],
            'startups': [],
            'policy': [],
            'other': []
        }
        
        # 关键词映射
        keywords = {
            'research': ['research', 'paper', 'study', 'algorithm', 'model', 'neural', 'deep learning'],
            'industry': ['company', 'product', 'launch', 'release', 'update', 'partnership'],
            'startups': ['startup', 'funding', 'raise', 'venture', 'seed', 'series'],
            'policy': ['regulation', 'policy', 'law', 'government', 'ethics', 'guidelines']
        }
        
        for item in news_items:
            assigned = False
            title_lower = item['title'].lower()
            
            for category, words in keywords.items():
                if any(word in title_lower for word in words):
                    categories[category].append(item)
                    assigned = True
                    break
            
            if not assigned:
                categories['other'].append(item)
        
        return categories

    def generate_brief(self, news_items: List[Dict], template_name: str = "daily_brief.html") -> str:
        """生成每日简报"""
        try:
            template = self.env.get_template(template_name)
            categorized_news = self.categorize_news(news_items)
            
            # 生成简报内容
            brief_content = template.render(
                date=datetime.now().strftime("%Y-%m-%d"),
                news=categorized_news,
                total_news=len(news_items)
            )
            
            return brief_content
        except Exception as e:
            self.logger.error(f"生成简报时出错: {str(e)}")
            return ""

    def generate_summary(self, news_items: List[Dict], max_items: int = 5) -> str:
        """生成简短摘要"""
        summary = []
        for item in news_items[:max_items]:
            summary.append(f"• {item['title']} ({item['source']})")
        
        return "\n".join(summary) 