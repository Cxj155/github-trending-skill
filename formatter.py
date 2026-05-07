from datetime import datetime
from analyzer import RepoAnalyzer

class ReportFormatter:
    @staticmethod
    def format_analysis(analysis, language=None):
        if not analysis:
            return "❌ 获取数据失败，请稍后重试"

        lang_display = f"【{language}】" if language and language != "all" else "【全语言】"
        lang_bar = ""
        for lang, count in analysis["top_languages"]:
            bar = "█" * count
            lang_bar += f"   {lang}: {bar} ({count})\n"

        cat_bar = ""
        for cat, count in analysis["categories"]:
            cat_bar += f"   {cat} {count}个\n"

        topics_str = "、".join([t[0] for t in analysis["topics"][:8]]) or "暂无"
        newest = analysis.get("newest_repo", {})
        newest_name = newest.get("full_name", "未知")
        newest_time = newest.get("created_at", "")[:10] if newest else "未知"

        return f"""
📈 【基础统计】
   仓库总数: {analysis['repo_count']} 个
   ⭐ 总星标: {RepoAnalyzer.format_number(analysis['total_stars'])}
   🍴 总 forks: {RepoAnalyzer.format_number(analysis['total_forks'])}
   📊 平均星标: {RepoAnalyzer.format_number(analysis['avg_stars'])}

🌐 【语言分布】
{lang_bar}📂 【仓库分类】
{cat_bar}

🏷️ 【热门主题】
   {topics_str}

🆕 【最新仓库】
   📦 {newest_name}
   ⏰ 创建时间: {newest_time}
"""

    @staticmethod
    def format_repo_list(repos):
        if not repos:
            return ""
        text = f"""
╔══════════════════════════════════════════════════════╗
║  📋 热门仓库详情列表
╚══════════════════════════════════════════════════════╝
"""
        for i, repo in enumerate(repos, 1):
            name = repo.get("full_name", "未知")
            desc = repo.get("description") or "暂无描述"
            stars = RepoAnalyzer.format_number(repo.get("stargazers_count", 0))
            forks = RepoAnalyzer.format_number(repo.get("forks_count", 0))
            language = repo.get("language") or "-"
            lic = repo.get("license", {}).get("name", "无") if repo.get("license") else "无"
            issues = repo.get("open_issues_count", 0)
            url = repo.get("html_url", "")
            category = RepoAnalyzer.get_category(repo)
            topics = repo.get("topics", [])[:5]
            topics_str = " ".join([f"`{t}`" for t in topics]) if topics else ""
            homepage = repo.get("homepage") or ""

            text += f"""
┌──────────────────────────────────────────────────────┐
│ 🔷 #{i} {name} {category}
├──────────────────────────────────────────────────────┤
│ 📝 {desc}
├──────────────────────────────────────────────────────┤
│ ⭐ {stars} | 🍴 {forks} | 🐛 {issues} | 📄 {lic}
│ 💻 {language} | 🏷️ {topics_str}
├──────────────────────────────────────────────────────┤
│ 🔗 {url}
│ 🌐 {homepage if homepage else '无官网'}
└──────────────────────────────────────────────────────┘
"""
        return text

    @staticmethod
    def full_report(repos, analysis, language=None):
        if not repos:
            return "❌ 获取数据失败，请稍后重试"

        header = f"""
╔══════════════════════════════════════════════════════╗
║  🐙 GitHub 热门仓库深度分析报告
║  📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} | 语言: {language or '全部'}
╚══════════════════════════════════════════════════════╝
"""
        analysis_sec = ReportFormatter.format_analysis(analysis, language)
        list_sec = ReportFormatter.format_repo_list(repos)
        footer = """

╔══════════════════════════════════════════════════════╗
║  💡 使用提示
║  • 指定语言：「Python的GitHub热点」
║  • 支持语言：Python/JavaScript/TypeScript/Go/Java等
║  • 数据来源：GitHub API (7天内新建仓库TOP排序)
╚══════════════════════════════════════════════════════╝
"""
        return header + analysis_sec + list_sec + footer