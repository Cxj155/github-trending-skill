#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 热门仓库助手
Cherry Studio Skill
"""

import requests
import json
from datetime import datetime
import time
import schedule

# ============== 配置区 ==============
TRIGGER_WORDS = ["GitHub热点", "今日热门仓库", "热门仓库", "GitHub trending"]
DEFAULT_LANGUAGE = "all"
# ============== 配置区 ==============

class GitHubTrending:
    def __init__(self):
        self.base_url = "https://api.github.com/search/repositories"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/vnd.github.v3+json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
    
    def fetch_trending(self, language=None, days=1, limit=10):
        """获取GitHub热门仓库"""
        lang = language if language else "all"
        query = f"created:>{self.get_date(days)}"
        if lang != "all":
            query += f" language:{lang}"
        
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            return f"❌ 网络错误: {str(e)}"
    
    def get_date(self, days_ago):
        """获取N天前的日期"""
        from datetime import timedelta
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d")
    
    def format_repo(self, repo, index):
        """格式化单个仓库信息"""
        name = repo.get("full_name", "未知")
        description = repo.get("description") or "暂无描述"
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        language = repo.get("language") or "未知"
        url = repo.get("html_url", "")
        
        stars_str = self.format_number(stars)
        forks_str = self.format_number(forks)
        
        return f"""
🔷 {index}. {name}
   📝 {description}
   ⭐ {stars_str} | 🍴 {forks_str} | 💻 {language}
   🔗 {url}
"""
    
    def format_number(self, num):
        """格式化数字（K/M单位）"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    
    def format_trending(self, repos, language=None, days=1):
        """格式化热门仓库列表"""
        if isinstance(repos, str):
            return repos
        
        if not repos:
            return "📭 今日暂无热门仓库数据"
        
        lang_display = f"{language}语言" if language and language != "all" else "全部语言"
        header = f"""
╔══════════════════════════════════════════════════════╗
║  🐙 GitHub 热门仓库 - {lang_display} ({days}天内创建)
║  🕐 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╚══════════════════════════════════════════════════════╝
"""
        
        body = ""
        for i, repo in enumerate(repos, 1):
            body += self.format_repo(repo, i)
        
        footer = f"""
╔══════════════════════════════════════════════════════╗
║  📊 共获取 {len(repos)} 个热门仓库
║  💡 提示: 可指定语言，如「Python的GitHub热点」
╚══════════════════════════════════════════════════════╝
"""
        
        return header + body + footer

def parse_command(text):
    """解析用户命令，提取语言参数"""
    text = text.strip()
    languages = [
        "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", 
        "C++", "C", "C#", "PHP", "Ruby", "Swift", "Kotlin", 
        "Dart", "Vue", "React", "Shell"
    ]
    
    for lang in languages:
        if f"{lang}的" in text or f"{lang}语言" in text:
            return lang
    
    if "Python" in text:
        return "Python"
    elif "JavaScript" in text or "JS" in text:
        return "JavaScript"
    elif "TypeScript" in text or "TS" in text:
        return "TypeScript"
    
    return None

def github_trending_handler(text):
    """处理GitHub热门请求"""
    trending = GitHubTrending()
    language = parse_command(text)
    repos = trending.fetch_trending(language=language, days=7, limit=10)
    return trending.format_trending(repos, language=language, days=7)

def daily_push():
    """每日定时推送"""
    trending = GitHubTrending()
    repos = trending.fetch_trending(days=7, limit=10)
    message = trending.format_trending(repos)
    print(f"\n{'='*50}\n📢 每日推送 - 北京时间 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*50}")
    print(message)
    return message

# ==================== 主程序 ====================
if __name__ == "__main__":
    import sys
    
    # 测试模式
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = github_trending_handler(user_input)
        print(result)
    else:
        # 默认执行（模拟触发）
        print("🚀 GitHub Trending 助手已启动")
        print("📌 支持以下触发词：", "、".join(TRIGGER_WORDS))
        print("💡 示例：「Python的GitHub热点」")
        print("\n" + "="*50)
        result = github_trending_handler("今日热门仓库")
        print(result)
        
        # 设置定时任务（北京时间9点）
        print("\n⏰ 已设置每日北京时间 9:00 自动推送")
        # 注意：定时推送需要在实际使用时启用
        # schedule.every().day.at("09:00").do(daily_push)
        # while True:
        #     schedule.run_pending()
        #     time.sleep(60)