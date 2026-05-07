from collections import Counter

class RepoAnalyzer:
    @staticmethod
    def format_number(num):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)

    @staticmethod
    def analyze_language(repos):
        langs = [r.get("language") for r in repos if r.get("language")]
        return Counter(langs)

    @staticmethod
    def analyze_license(repos):
        licenses = []
        for r in repos:
            lic = r.get("license")
            licenses.append(lic.get("name", "无许可证") if lic else "无许可证")
        return Counter(licenses)

    @staticmethod
    def analyze_topics(repos):
        topics = []
        for repo in repos:
            topics.extend(repo.get("topics", []))
        return Counter(topics).most_common(10)

    @staticmethod
    def get_category(repo):
        name = repo.get("name", "").lower() if repo.get("name") else ""
        desc = repo.get("description", "").lower() if repo.get("description") else ""
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

    @staticmethod
    def full_analyze(repos):
        if not repos:
            return None

        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        total_forks = sum(r.get("forks_count", 0) for r in repos)
        avg_stars = total_stars // len(repos)

        lang_dist = RepoAnalyzer.analyze_language(repos)
        lic_dist = RepoAnalyzer.analyze_license(repos)
        top_topics = RepoAnalyzer.analyze_topics(repos)
        categories = [RepoAnalyzer.get_category(r) for r in repos]
        cat_dist = Counter(categories)

        repos_sorted = sorted(repos, key=lambda x: x.get("created_at", ""), reverse=True)
        newest = repos_sorted[0] if repos_sorted else None

        return {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "avg_stars": avg_stars,
            "repo_count": len(repos),
            "top_languages": lang_dist.most_common(5),
            "licenses": lic_dist.most_common(3),
            "topics": top_topics,
            "categories": cat_dist.most_common(5),
            "newest_repo": newest
        }