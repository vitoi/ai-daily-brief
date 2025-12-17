#!/usr/bin/env python3
"""
AI Daily Brief - 本地简报服务器

启动一个简单的本地Web服务器来查看和归档简报。
"""

import os
import json
import http.server
import socketserver
from pathlib import Path
from datetime import datetime
import urllib.parse

class BriefHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器"""

    def do_GET(self):
        """处理GET请求"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self.serve_index()
        elif path.startswith('/briefs/'):
            # 直接提供HTML文件
            super().do_GET()
        elif path == '/api/briefs':
            self.serve_api_briefs()
        else:
            super().do_GET()

    def serve_index(self):
        """提供主页"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # 获取所有简报文件
        briefs_dir = Path('.')
        html_files = list(briefs_dir.glob('daily_brief_*.html'))
        html_files.sort(reverse=True)  # 最新的在前

        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Daily Brief Archive</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #2563eb, #1e40af);
            color: white;
            padding: 40px 20px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .brief-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .brief-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .brief-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .brief-date {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2563eb;
            margin-bottom: 10px;
        }}
        .brief-link {{
            display: inline-block;
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
        }}
        .brief-link:hover {{
            color: #1d4ed8;
            text-decoration: underline;
        }}
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI Daily Brief Archive</h1>
        <p>个人AI新闻简报归档</p>
    </div>

    <div class="stats">
        <h2>📊 统计信息</h2>
        <p>总共归档了 <strong>{len(html_files)}</strong> 期简报</p>
        <p>最新更新: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
    </div>

    <h2>📰 简报列表</h2>
    <div class="brief-grid">
'''

        for html_file in html_files[:30]:  # 只显示最近30期
            # 从文件名提取日期
            filename = html_file.name
            date_str = filename.replace('daily_brief_', '').replace('.html', '')
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                display_date = date_obj.strftime('%Y年%m月%d日')
            except:
                display_date = date_str

            html_content += f'''
        <div class="brief-card">
            <div class="brief-date">{display_date}</div>
            <a href="/briefs/{filename}" class="brief-link" target="_blank">查看简报 →</a>
        </div>
'''

        html_content += '''
    </div>
</body>
</html>'''

        self.wfile.write(html_content.encode('utf-8'))

    def serve_api_briefs(self):
        """提供简报API"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        # 获取简报文件列表
        briefs_dir = Path('.')
        html_files = list(briefs_dir.glob('daily_brief_*.html'))
        html_files.sort(reverse=True)

        briefs = []
        for html_file in html_files[:10]:  # 只返回最近10期
            filename = html_file.name
            date_str = filename.replace('daily_brief_', '').replace('.html', '')
            briefs.append({
                'date': date_str,
                'filename': filename,
                'url': f'/briefs/{filename}'
            })

        response = {
            'total': len(html_files),
            'briefs': briefs
        }

        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

def run_server(port=8000):
    """运行本地服务器"""
    # 创建briefs目录软链接（如果不存在）
    briefs_dir = Path('briefs')
    if not briefs_dir.exists():
        try:
            os.symlink('.', 'briefs')
        except:
            pass  # Windows可能不支持软链接

    print(f"🚀 启动AI Daily Brief本地服务器")
    print(f"📱 访问地址: http://localhost:{port}")
    print(f"❌ 按 Ctrl+C 停止服务器")

    with socketserver.TCPServer(("", port), BriefHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 服务器已停止")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
