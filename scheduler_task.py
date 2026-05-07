import time
import schedule
from datetime import datetime
from config import PUSH_TIME
from api_client import GitHubApiClient
from analyzer import RepoAnalyzer
from formatter import ReportFormatter
from file_manager import save_content_to_file

def parse_command(text):
    from config import SUPPORT_LANGUAGES, LANG_MAPPING
    text = text.strip()
    for lang in SUPPORT_LANGUAGES:
        if f"{lang}的" in text or f"{lang}语言" in text:
            return lang
    for k, v in LANG_MAPPING.items():
        if k in text.lower():
            return v
    return None

def handle_github_trend(text):
    client = GitHubApiClient()
    lang = parse_command(text)
    repos = client.fetch_trending(language=lang, days=7, limit=15)
    if not repos:
        return "❌ 网络请求失败，请检查网络后重试"
    analysis = RepoAnalyzer.full_analyze(repos)
    return ReportFormatter.full_report(repos, analysis, lang)

def daily_push_job():
    print("\n" + "="*60)
    print(f"📢 定时任务触发 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    res = handle_github_trend("今日热门仓库")
    print(res)
    now = datetime.now()
    fname = f"github_trending_{now.strftime('%Y%m%d')}_daily.txt"
    save_content_to_file(res, fname)
    print(f"\n📌 每日推送完成 - {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

def start_schedule_service():
    print("="*60)
    print("🚀 GitHub Trending 定时推送服务已启动")
    print(f"⏰ 定时推送时间: 每天 {PUSH_TIME} (北京时间)")
    print(f"📁 日志保存目录: ./github_trending_logs/")
    print("="*60)
    schedule.every().day.at(PUSH_TIME).do(daily_push_job)
    print(f"\n✅ 已设置每日 {PUSH_TIME} 自动推送")
    print("📌 按 Ctrl+C 退出程序\n")
    while True:
        schedule.run_pending()
        time.sleep(60)