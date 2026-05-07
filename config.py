# 全局配置常量
TRIGGER_WORDS = ["GitHub热点", "今日热门仓库", "热门仓库", "GitHub trending"]
DEFAULT_LANGUAGE = "all"
PUSH_TIME = "09:00"
SAVE_DIR = "github_trending_logs"

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/vnd.github.v3+json",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}

# 支持语言列表
SUPPORT_LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust",
    "C++", "C", "C#", "PHP", "Ruby", "Swift", "Kotlin",
    "Dart", "Vue", "React", "Shell", "HTML", "CSS"
]

# 语言简写映射
LANG_MAPPING = {
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "go": "Go",
    "java": "Java",
    "cpp": "C++",
    "c#": "C#"
}