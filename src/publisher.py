import tweepy
import logging
from typing import Dict
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import git
import shutil

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

    def _setup_email(self):
        """设置邮件配置"""
        email_config = self.config.get('email', {})
        self.smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = email_config.get('smtp_port', 587)
        self.sender_email = email_config.get('sender_email')
        self.sender_password = email_config.get('sender_password')
        self.recipient_email = email_config.get('recipient_email')

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

    def send_email(self, subject: str, html_content: str) -> bool:
        """发送邮件"""
        try:
            # 设置邮件配置
            self._setup_email()

            if not all([self.sender_email, self.sender_password, self.recipient_email]):
                self.logger.warning("邮件配置不完整，跳过邮件发送")
                return False

            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email

            # 添加HTML内容
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # 发送邮件
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            server.quit()

            self.logger.info("邮件发送成功")
            return True
        except Exception as e:
            self.logger.error(f"发送邮件时出错: {str(e)}")
            return False

    def deploy_to_github_pages(self, html_file_path: str) -> bool:
        """部署到GitHub Pages"""
        try:
            github_config = self.config.get('github_pages', {})
            repo_url = github_config.get('repo_url')
            branch = github_config.get('branch', 'gh-pages')
            local_repo_path = github_config.get('local_repo_path', 'github_pages_repo')

            if not repo_url:
                self.logger.warning("GitHub Pages配置不完整，跳过部署")
                return False

            # 如果本地仓库不存在，克隆它
            if not os.path.exists(local_repo_path):
                self.logger.info(f"克隆GitHub Pages仓库: {repo_url}")
                repo = git.Repo.clone_from(repo_url, local_repo_path, branch=branch)
            else:
                repo = git.Repo(local_repo_path)
                # 拉取最新更改
                repo.git.pull('origin', branch)

            # 复制HTML文件到仓库
            filename = os.path.basename(html_file_path)
            dest_path = os.path.join(local_repo_path, filename)
            shutil.copy2(html_file_path, dest_path)

            # 创建索引文件（如果不存在）
            index_path = os.path.join(local_repo_path, 'index.html')
            if not os.path.exists(index_path):
                # 创建一个简单的索引页面
                index_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Daily Brief Archive</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .brief-link {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        .brief-link a {{ text-decoration: none; color: #2563eb; }}
        .brief-link a:hover {{ color: #1d4ed8; }}
    </style>
</head>
<body>
    <h1>AI Daily Brief Archive</h1>
    <div class="brief-link">
        <a href="{filename}">Latest Brief - {datetime.now().strftime('%Y-%m-%d')}</a>
    </div>
</body>
</html>'''
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(index_content)

            # 提交更改
            repo.index.add([filename, 'index.html'])
            repo.index.commit(f"Update AI Daily Brief - {datetime.now().strftime('%Y-%m-%d')}")

            # 推送更改
            origin = repo.remote(name='origin')
            origin.push(branch)

            self.logger.info("成功部署到GitHub Pages")
            return True
        except Exception as e:
            self.logger.error(f"部署到GitHub Pages时出错: {str(e)}")
            return False

    def publish_brief(self, brief_content: str, summary: str, html_file_path: str = None) -> Dict[str, bool]:
        """发布简报到多个渠道"""
        results = {
            'twitter': False,
            'email': False,
            'github_pages': False
        }

        # 发布到Twitter
        twitter_config = self.config.get('twitter', {})
        if twitter_config.get('consumer_key'):
            twitter_content = f"🤖 AI Daily Brief - {datetime.now().strftime('%Y-%m-%d')}\n\n{summary}"
            results['twitter'] = self.post_to_twitter(twitter_content)

        # 发送邮件
        email_config = self.config.get('email', {})
        if email_config.get('sender_email'):
            subject = f"🤖 AI Daily Brief - {datetime.now().strftime('%Y-%m-%d')}"
            results['email'] = self.send_email(subject, brief_content)

        # 部署到GitHub Pages
        github_config = self.config.get('github_pages', {})
        if github_config.get('repo_url') and html_file_path:
            results['github_pages'] = self.deploy_to_github_pages(html_file_path)

        return results 