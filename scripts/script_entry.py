# script_entry.py（最终可用版）
from scheduler_task import handle_github_trend, start_schedule_service
from file_manager import save_content_to_file

# 对外接口（给 Claude Skill 调用）
def get_github_trending_report(user_input: str) -> str:
    """对外接口：传入指令，返回完整报告文本"""
    return handle_github_trend(user_input)

def run_daily_schedule():
    """对外接口：启动每日定时推送服务"""
    start_schedule_service()

def save_report_txt(content: str, filename: str = None):
    """对外接口：保存报告到txt文件"""
    return save_content_to_file(content, filename)

# 终端运行入口（给你调试用，完全不影响Skill调用）
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 把终端输入的参数拼接成完整指令
        user_input = " ".join(sys.argv[1:])
        print(f"\n🔍 正在处理请求: {user_input}")
        print("="*60)
        # 调用核心逻辑
        result = get_github_trending_report(user_input)
        print(result)
        print("="*60)
        # 自动保存报告
        save_report_txt(result)
        print("✅ 报告已自动保存到 github_trending_logs 文件夹")
    else:
        print("⚠️  请传入指令，例如：")
        print('  python script_entry.py "GitHub热点"')
        print('  python script_entry.py "Python的GitHub热点"')