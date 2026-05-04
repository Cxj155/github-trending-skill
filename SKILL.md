## 技能名称
GitHub热门仓库分析助手

## 技能标识
github-trending-analyzer

## 版本
2.0

## 作者
自定义

## 简介
自动抓取GitHub近7天新建高星热门仓库，自动做语言分类、项目归类、数据统计，生成可视化中文报告，支持指定编程语言筛选。

## 触发词
GitHub热点、今日热门仓库、热门仓库、GitHub trending

## 能力描述
1. 默认获取全网全语言近7天新建Star最高的热门开源仓库
2. 支持指令筛选指定语言：Python、Go、Rust、Java、JS/TS、C++ 等
3. 自动统计：星标总数、Fork总数、平均星标、语言分布、许可证、热门标签
4. 智能自动分类项目：AI大模型、Web前端、后端、工具、DevOps、移动端、游戏等
5. 输出精美格式化中文报告，包含仓库详情、链接、简介、技术栈

## 使用示例
1. 今日热门仓库
2. GitHub热点
3. Python的GitHub热点
4. Go语言热门仓库
5. js的GitHub trending

## 参数说明
无需手动配置参数，自动从用户提问中识别编程语言关键词
支持简写识别：py=Python、js=JavaScript、ts=TypeScript、cpp=C++、go=Go

## 运行依赖
python3
requests

## 脚本入口
main.py

## 执行函数
github_trending_handler

## 超时时间
20

## 备注
数据来源：GitHub官方Search API
数据范围：最近7天新创建仓库，按Star降序排序