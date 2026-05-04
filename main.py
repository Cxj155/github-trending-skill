#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 热门仓库助手 v2.0
Cherry Studio Skill
功能：拉取热门仓库详情并归纳整理
"""

import requests
import json
from datetime import datetime
from collections import Counter

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
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
    
    def fetch_trending(self, language=None, days=7, limit=10):
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
            return None
    
    def fetch_repo_details(self, repo_url):
        """获取单个仓库详情"""
        try:
            response = requests.get(repo_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return None
    
    def get_date(self, days_ago):
        from datetime import timedelta
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d")
    
    def format_number(self, num):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    
    def analyze_language(self, repos):
        """分析语言分布"""
        languages = [r.get("language") for r in repos if r.get("language")]
        return Counter(languages)
    
    def analyze_license(self, repos):
        """分析许可证分布"""
        licenses = [r.get("license", {}).get("name", "无许可证") for r in repos]
        return Counter(licenses)
    
    def analyze_topics(self, repos):
        """分析主题标签"""
        all_topics = []
        for repo in repos:
            topics = repo.get("topics", [])
            all_topics.extend(topics)
        return Counter(all_topics).most_common(10)
    
    def get_repo_category(self, repo):
        """根据描述和主题判断仓库分类"""
        name = repo.get("name", "").lower()
        desc = repo.get("description", "").lower()
        topics = repo.get("topics", [])
        
        combined = " ".join([name, desc] + topics).lower()
        
        if any(k in combined for k in ["ai", "llm", "gpt", "neural", "model", "deep learning", "machine learning"]):
            return "🤖 AI/ML"
        elif any(k in combined for k in ["web", "react", "vue", "angular", "frontend", "ui"]):
            return "🌐 Web开发"
        elif any(k in combined for k in ["api", "server", "backend", "fastapi", "express"]):
            return "⚙️ 后端/API"
        elif any(k in combined for k in ["tool", "cli", "command", "utility"]):
            return "🛠️ 工具类"
        elif any(k in combined for k in ["bot", "telegram", "discord", "chat"]):
            return "💬 机器人"
        elif any(k in combined for k in ["docker", "kubernetes", "k8s", "devops"]):
            return "🐳 DevOps"
        elif any(k in combined for k in ["data", "database", "sql", "mongodb"]):
            return "🗄️ 数据库"
        elif any(k in combined for k in ["game", "gameengine", "unity", "unreal"]):
            return "🎮 游戏开发"
        elif any(k in combined for k in ["mobile", "ios", "android", "flutter", "reactnative"]):
            return "📱 移动开发"
        else:
            return "📦 通用"
    
    def analyze_repos(self, repos):
        """分析并归纳仓库信息"""
        if not repos:
            return None
        
        # 基本统计
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        total_forks = sum(r.get("forks_count", 0) for r in repos)
        avg_stars = total_stars // len(repos)
        
        # 语言分布
        lang_dist = self.analyze_language(repos)
        top_langs = lang_dist.most_common(5)
        
        # 许可证分布
        license_dist = self.analyze_license(repos)
        
        # 热门主题
        top_topics = self.analyze_topics(repos)
        
        # 分类统计
        categories = [self.get_repo_category(r) for r in repos]
        cat_dist = Counter(categories)
        
        # 最新创建
        repos_sorted = sorted(repos, key=lambda x: x.get("created_at", ""), reverse=True)
        newest = repos_sorted[0] if repos_sorted else None
        
        return {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "avg_stars": avg_stars,
            "top_languages": top_langs,
            "licenses": license_dist.most_common(3),
            "topics": top_topics,
            "categories": cat_dist.most_common(5),
            "newest_repo": newest
        }
    
    def format_analysis(self, analysis, language=None):
        """格式化分析结果"""
        if not analysis:
            return "❌ 获取数据失败，请稍后重试"
        
        lang_display = f"【{language}】" if language and language != "all" else "【全语言】"
        
        # 语言分布图
        lang_bar = ""
        for lang, count in analysis["top_languages"]:
            bar = "█" * count
            lang_bar += f"   {lang}: {bar} ({count})\n"
        
        # 分类分布
        cat_bar = ""
        for cat, count in analysis["categories"]:
            cat_bar += f"   {cat} {count}个\n"
        
        # 热门主题
        topics_str = "、".join([t[0] for t in analysis["topics"][:8]]) or "暂无"
        
        # 最新仓库
        newest = analysis.get("newest_repo", {})
        newest_name = newest.get("full_name", "未知")
        newest_time = newest.get("created_at", "")[:10] if newest else "未知"
        
        analysis_text = f"""
╔══════════════════════════════════════════════════════╗
║  📊 GitHub 热门仓库数据分析报告 {lang_display}
║  🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╚══════════════════════════════════════════════════════╝

📈 【基础统计】
   仓库总数: {len(analysis['top_languages']) * 2 if analysis else 0} 个
   ⭐ 总星标: {self.format_number(analysis['total_stars'])}
   🍴 总 forks: {self.format_number(analysis['total_forks'])}
   📊 平均星标: {self.format_number(analysis['avg_stars'])}

🌐 【语言分布】
{lang_bar}

📂 【仓库分类】
{cat_bar}

🏷️ 【热门主题】
   {topics_str}

🆕 【最新仓库】
   📦 {newest_name}
   ⏰ 创建时间: {newest_time}
"""
        return analysis_text
    
    def format_repos_list(self, repos):
        """格式化仓库列表详情"""
        if not repos:
            return ""
        
        repos_text = f"""
╔══════════════════════════════════════════════════════╗
║  📋 热门仓库详情列表
╚══════════════════════════════════════════════════════╝
"""
        
        for i, repo in enumerate(repos, 1):
            name = repo.get("full_name", "未知")
            desc = repo.get("description") or "暂无描述"
            stars = self.format_number(repo.get("stargazers_count", 0))
            forks = self.format_number(repo.get("forks_count", 0))
            language = repo.get("language") or "-"
            license_name = repo.get("license", {}).get("name", "无")
            issues = repo.get("open_issues_count", 0)
            url = repo.get("html_url", "")
            category = self.get_repo_category(repo)
            topics = repo.get("topics", [])[:5]
            topics_str = " ".join([f"`{t}`" for t in topics]) if topics else ""
            homepage = repo.get("homepage") or ""
            
            repos_text += f"""
┌──────────────────────────────────────────────────────┐
│ 🔷 #{i} {name} {category}
├──────────────────────────────────────────────────────┤
│ 📝 {desc}
├──────────────────────────────────────────────────────┤
│ ⭐ {stars} | 🍴 {forks} | 🐛 {issues} | 📄 {license_name}
│ 💻 {language} | 🏷️ {topics_str}
├──────────────────────────────────────────────────────┤
│ 🔗 {url}
│ 🌐 {homepage if homepage else '无官网'}
└──────────────────────────────────────────────────────┘
"""
        
        return repos_text
    
    def format_full_report(self, repos, analysis, language=None):
        """生成完整报告"""
        if not repos:
            return "❌ 获取数据失败，请稍后重试"
        
        header = f"""
╔══════════════════════════════════════════════════════╗
║  🐙 GitHub 热门仓库深度分析报告
║  📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} | 语言: {language or '全部'}
╚══════════════════════════════════════════════════════╝
"""
        
        analysis_section = self.format_analysis(analysis, language)
        list_section = self.format_repos_list(repos)
        
        footer = f"""

╔══════════════════════════════════════════════════════╗
║  💡 使用提示
║  • 指定语言：「Python的GitHub热点」
║  • 支持语言：Python/JavaScript/TypeScript/Go/Java等
║  • 数据来源：GitHub API (7天内新建仓库TOP排序)
╚══════════════════════════════════════════════════════╝
"""
        
        return header + analysis_section + list_section + footer

def parse_command(text):
    """解析用户命令，提取语言参数"""
    text = text.strip()
    languages = [
        "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", 
        "C++", "C", "C#", "PHP", "Ruby", "Swift", "Kotlin",
        "Dart", "Vue", "React", "Shell", "HTML", "CSS"
    ]
    
    for lang in languages:
        if f"{lang}的" in text or f"{lang}语言" in text:
            return lang
    
    mapping = {
        "js": "JavaScript",
        "ts": "TypeScript",
        "py": "Python",
        "go": "Go",
        "java": "Java",
        "cpp": "C++",
        "c#": "C#"
    }
    
    for k, v in mapping.items():
        if k in text.lower():
            return v
    
    return None

def github_trending_handler(text):
    """处理GitHub热门请求"""
    trending = GitHubTrending()
    language = parse_command(text)
    
    # 获取热门仓库
    repos = trending.fetch_trending(language=language, days=7, limit=15)
    
    if not repos:
        return "❌ 网络请求失败，请检查网络后重试"
    
    # 分析数据
    analysis = trending.analyze_repos(repos)
    
    # 生成完整报告
    return trending.format_full_report(repos, analysis, language)

# ==================== 主程序 ====================
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行模式
        user_input = " ".join(sys.argv[1:])
        result = github_trending_handler(user_input)
        print(result)
    else:
        # 测试模式
        print("🚀 GitHub Trending 深度分析助手已启动")
        print("="*60)
        
        # 测试全部语言
        print("\n📌 测试: 今日热门仓库")
        result = github_trending_handler("今日热门仓库")
        print(result)