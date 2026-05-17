import requests
from datetime import datetime, timedelta
from config import HEADERS

class GitHubApiClient:
    def __init__(self):
        self.base_url = "https://api.github.com/search/repositories"
        self.headers = HEADERS

    def _get_date(self, days_ago):
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d")

    def fetch_trending(self, language=None, days=7, limit=15):
        lang = language if language else "all"
        query = f"created:>{self._get_date(days)}"
        if lang != "all":
            query += f" language:{lang}"

        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }

        try:
            resp = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=15
            )
            resp.raise_for_status()
            return resp.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            return None

    def fetch_repo_detail(self, repo_url):
        try:
            resp = requests.get(repo_url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except:
            return None