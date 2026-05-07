---
name: github-trending-skill
description: Fetch GitHub trending repositories, generate in-depth analysis reports, support scheduled push and save to TXT. TRIGGER whenever user mentions GitHub trending, hot repositories, today's popular repos, or requests GitHub stats/insights. Make sure to use this skill when user asks about "GitHub热点", "今日热门仓库", "热门仓库", "GitHub trending", "GitHub热门", or wants to discover interesting GitHub projects. Even if user asks casually like "有什么好看的GitHub项目" or "推荐几个开源项目", use this skill.
trigger: ["GitHub热点", "今日热门仓库", "热门仓库", "GitHub trending", "GitHub热门", "GitHub流行", "好看的GitHub项目", "开源项目推荐"]
entrypoint: script_entry.py
compatibility: Python 3.8+, requires requests and schedule packages
---

# GitHub热门仓库助手

## 功能说明

自动拉取 GitHub 7天内新建的热门仓库，按星标数量排序，生成包含语言分布、分类统计、主题标签的深度分析报告。

## 触发方式

| 用户输入 | 行为 |
|---------|------|
| `GitHub热点` | 获取全语言热门仓库 TOP 15 |
| `Python的GitHub热点` | 获取 Python 语言热门仓库 |
| `JavaScript的GitHub热点` | 获取 JavaScript 语言热门仓库 |
| `Go的GitHub热点` | 获取 Go 语言热门仓库 |
| `今日热门仓库` | 同 "GitHub热点"，触发每日定时推送任务 |

支持语言：Python, JavaScript, TypeScript, Java, Go, Rust, C++, C, C#, PHP, Ruby, Swift, Kotlin, Dart, Vue, React, Shell, HTML, CSS

## 输出格式

报告包含以下部分：

### 1. 基础统计
- 仓库总数
- ⭐ 总星标数（格式化显示，如 12.5K）
- 🍴 总 forks 数
- 📊 平均星标数

### 2. 语言分布
以条形图形式展示 TOP 5 语言及其仓库数量

### 3. 仓库分类
按类别统计：
- 🤖 AI/ML - 包含 AI, LLM, GPT, neural, model, deep learning, machine learning
- 🌐 Web开发 - 包含 web, react, vue, angular, frontend, ui
- ⚙️ 后端/API - 包含 api, server, backend, fastapi, express
- 🛠️ 工具类 - 包含 tool, cli, command, utility
- 💬 机器人 - 包含 bot, telegram, discord, chat
- 🐳 DevOps - 包含 docker, kubernetes, k8s, devops
- 🗄️ 数据库 - 包含 data, database, sql, mongodb
- 🎮 游戏开发 - 包含 game, gameengine, unity, unreal
- 📱 移动开发 - 包含 mobile, ios, android, flutter, reactnative
- 📦 通用 - 不属于以上分类

### 4. 热门主题
展示 TOP 8 最常见的主题标签

### 5. 最新仓库
显示最新创建的仓库名称和创建时间

### 6. 仓库详情列表
每个仓库显示：
- 仓库名称（含分类标签）
- 仓库描述
- ⭐ stars | 🍴 forks | 🐛 issues | 📄 license
- 💻 语言 | 🏷️ 主题标签
- 🔗 GitHub URL | 🌐 官网（如有）

## 执行流程

当用户触发技能时：

1. **解析指令**：识别用户指定的语言（如有）
2. **调用 API**：使用 `GitHubApiClient.fetch_trending()` 获取 7天内创建的热门仓库
3. **数据分析**：使用 `RepoAnalyzer.full_analyze()` 进行分析
4. **生成报告**：使用 `ReportFormatter.full_report()` 格式化输出
5. **返回结果**：将完整报告返回给用户

## 错误处理

| 错误情况 | 处理方式 |
|---------|---------|
| 网络请求失败 | 返回："❌ 网络请求失败，请检查网络后重试" |
| API 返回空数据 | 返回："❌ 获取数据失败，请稍后重试" |
| 未知语言 | 忽略语言筛选，返回全语言结果 |

## 定时推送配置

如需开启每日定时推送，调用 `run_daily_schedule()` 启动服务。

- 默认推送时间：每天 09:00（北京时间）
- 日志保存目录：`./github_trending_logs/`
- 文件命名格式：`github_trending_YYYYMMDD_daily.txt`

## 代码模块说明

| 文件 | 职责 |
|-----|------|
| `script_entry.py` | 对外接口，提供 `get_github_trending_report()` 函数 |
| `api_client.py` | GitHub API 调用，使用搜索接口按创建时间和 star 数排序 |
| `analyzer.py` | 数据分析，包括分类判断、语言统计、主题提取 |
| `formatter.py` | 报告格式化，包含完整报告和简洁报告两种格式 |
| `scheduler_task.py` | 定时任务调度，使用 schedule 库 |
| `file_manager.py` | 文件保存，管理日志目录和文件名 |
| `config.py` | 全局配置，包括支持的语言列表、请求头等 |

## 使用示例

```
用户: GitHub热点
助手: [生成完整分析报告]

用户: Python的GitHub热点
助手: [生成 Python 热门仓库报告]

用户: 有什么好看的开源项目吗
助手: [自动使用 GitHub热点 功能]
```