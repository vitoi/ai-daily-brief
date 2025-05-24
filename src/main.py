import logging
import schedule
import time
from datetime import datetime
from news_collector import NewsCollector
from brief_generator import BriefGenerator
from publisher import Publisher
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_daily_brief.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_and_publish_brief():
    """生成并发布每日简报"""
    try:
        # 初始化组件
        collector = NewsCollector()
        generator = BriefGenerator()
        publisher = Publisher()
        
        # 收集新闻
        logger.info("开始收集新闻...")
        news_items = collector.collect_all_news()
        logger.info(f"收集到 {len(news_items)} 条新闻")
        
        if not news_items:
            logger.warning("没有收集到新闻，跳过本次简报生成")
            return
        
        # 生成简报
        logger.info("生成简报...")
        brief_content = generator.generate_brief(news_items)
        summary = generator.generate_summary(news_items)
        
        # 打印简报内容到控制台
        print("\n=== AI Daily Brief ===")
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"共收集到 {len(news_items)} 条新闻\n")
        print("=== 简报摘要 ===")
        print(summary)
        print("\n=== 完整简报 ===")
        print(brief_content)
        
        # 保存简报到本地文件
        brief_filename = f"daily_brief_{datetime.now().strftime('%Y-%m-%d')}.html"
        with open(brief_filename, "w", encoding="utf-8") as f:
            f.write(brief_content)
        logger.info(f"简报已保存到 {brief_filename}")
        
        # 发布简报
        logger.info("发布简报...")
        results = publisher.publish_brief(brief_content, summary)
        
        # 记录发布结果
        for channel, success in results.items():
            if success:
                logger.info(f"成功发布到 {channel}")
            else:
                logger.error(f"发布到 {channel} 失败")
                
    except Exception as e:
        logger.error(f"生成和发布简报时出错: {str(e)}")

def main():
    """主程序入口"""
    # 直接运行一次简报生成
    generate_and_publish_brief()

if __name__ == "__main__":
    main() 