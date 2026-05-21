# IgniteNow

## 概览

即燃引擎：基于短剧内容理解的即时互动激发系统。

本项目面向短剧观看场景，通过 AI 分析字幕与剧情时间轴，识别剧情高光，并在 Flutter Android 播放端的关键时间点触发低门槛互动组件。用户点击后的行为会回传到后端，最终在 Web 管理后台形成审核、发布和数据看板闭环。

## 核心功能

- 短剧、剧集、视频和字幕管理
- AI 高光识别
- 高光点结构化存储、编辑、审核和发布
- 按时间轴触发可交互的特效
- 用户互动回传
- 后台数据看板统计曝光、点击、点击率和热门按钮

## 开发状态

详见 [docs/PROGRESS.md](docs/PROGRESS.md)

## 项目架构

```text
IgniteNow/
├── backend/                 # FastAPI 后端服务：API、业务逻辑、AI 调度、数据统计
├── ai_service/              # Python AI 高光识别服务：字幕解析、Prompt、LLM 调用
├── frontend/
│   └── admin_web/           # React + Vite 管理后台
├── flutter/                 # Flutter Android 播放端
├── datebase/                # 数据库脚本：建表 SQL、初始化数据、迁移文件
├── assets/                  # 示例视频、字幕、截图和演示素材
├── docs/
│   ├── PROGRESS.md          # 开发进度
│   ├── API_CONTRACT.md      # API 契约
│   ├── HIGHLIGHT_SCHEMA.json # 高光结构约束
│   ├── DECISIONS.md         # 技术决策记录
│   └── 原始开发文档 v1.1.md
├── docker-compose.yml       # Docker Compose 本地编排入口
├── .env.example             # 本地环境变量示例
├── .dockerignore
├── .gitignore
├── AGENTS.md
└── README1.md
```

## 技术栈

| 模块 | 技术 |
|---|---|
| 待完善 | 待完善 |


## 部署方式

### 方式一：脚本安装

### 方式二：Docker Compose

使用 Docker Compose 部署


