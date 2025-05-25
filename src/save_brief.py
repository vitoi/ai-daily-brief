import os
import json
from datetime import datetime
from news_collector import NewsCollector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def save_as_markdown(news_items, output_dir='briefs'):
    """
    将新闻保存为 Markdown 格式
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成文件名（使用当前日期）
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'AI_Daily_Brief_{date_str}.md'
    filepath = os.path.join(output_dir, filename)
    
    # 生成 Markdown 内容
    content = f"""# AI Daily Brief - {date_str}

## 今日要闻

"""
    
    # 按来源分类新闻
    news_by_source = {}
    for item in news_items:
        source = item['source']
        if source not in news_by_source:
            news_by_source[source] = []
        news_by_source[source].append(item)
    
    # 添加每个来源的新闻
    for source, items in news_by_source.items():
        content += f"\n### {source}\n\n"
        for item in items:
            content += f"- [{item['title']}]({item['link']})\n"
            if item.get('summary'):
                content += f"  - {item['summary']}\n"
            content += f"  - 发布时间: {item['published']}\n\n"
    
    # 添加统计信息
    content += f"\n## 统计信息\n\n"
    content += f"- 总新闻数: {len(news_items)}\n"
    for source, items in news_by_source.items():
        content += f"- {source}: {len(items)} 条\n"
    
    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"简报已保存到: {filepath}")
    return filepath

def save_as_json(news_items, output_dir='briefs'):
    """
    将新闻保存为 JSON 格式
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'AI_Daily_Brief_{date_str}.json'
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2, default=datetime_handler)
    
    logger.info(f"JSON 数据已保存到: {filepath}")
    return filepath

def main():
    collector = NewsCollector()
    news_items = collector.collect_all_news()
    
    if not news_items:
        logger.warning("没有收集到新闻")
        return
    
    # 保存为 Markdown
    md_file = save_as_markdown(news_items)
    
    # 保存为 JSON
    json_file = save_as_json(news_items)
    
    logger.info(f"今日简报已保存，共 {len(news_items)} 条新闻")

if __name__ == "__main__":
    main() 