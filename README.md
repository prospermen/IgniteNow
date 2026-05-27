# IgniteNow

## 概览

即燃引擎：基于短剧内容理解的即时互动激发系统。

本项目面向短剧观看场景，通过 AI 分析字幕与剧情时间轴，识别剧情高光，并在 Flutter Android 播放端的关键时间点触发低门槛互动组件。用户点击后的行为会回传到后端，最终在 Web 工作台形成上传、识别、审核、发布和数据看板闭环。

## 核心功能

- 短剧、剧集、视频和字幕管理
- AI 高光识别
- 高光点结构化存储、编辑、审核和发布
- 按时间轴触发可交互的特效
- 用户互动回传
- 工作台数据看板统计曝光、点击、点击率和热门按钮

## 开发状态

详见 [docs/PROGRESS.md](docs/PROGRESS.md)

## 项目架构

```text
IgniteNow/
├── backend/                 # FastAPI 后端服务：API、业务逻辑、AI 调度、数据统计
├── ai_service/              # Python AI 高光识别服务：字幕解析、Prompt、LLM 调用
├── frontend/
│   └── admin_web/           # React + Vite Web 工作台
├── mobile/                  # Flutter Android / Web 播放端
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
└── README.md
```

## 技术栈

| 模块 | 技术 |
|---|---|
| 后端服务 | FastAPI + SQLAlchemy，本地可用 PostgreSQL |
| AI 服务 | Python 字幕解析 + 关键词 fallback，高光 JSON Schema 校验 |
| Web 工作台 | React + Vite + Ant Design |
| 移动端 | Flutter + video_player + http + shared_preferences |
| 数据库 | PostgreSQL（推荐）/ SQLite，核心 SQL 位于 `datebase/` |

## 本地启动

### 1. 后端

```powershell
docker compose up -d redis
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后台 RQ worker 需要单独开一个终端运行：

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m app.worker
```

### 大语言模型 (LLM) 高光识别配置：
如果不配置，系统也能通过关键词降级运行。

```powershell
$env:LLM_API_KEY="你的 LLM API Key"
$env:LLM_BASE_URL="https://api.openai.com/v1"
$env:LLM_MODEL="gpt-4o-mini"
```

如果不设置 `LLM_API_KEY`，系统会自动使用本地关键词 fallback，演示链路仍然可运行。API Key 只放在环境变量或本地 `.env`，不要提交到仓库。

验证：

```powershell
Invoke-RestMethod http://localhost:8000/health
python backend/scripts/bootstrap_admin.py
$login = Invoke-RestMethod -Method Post http://localhost:8000/api/auth/login -Body (@{username="admin"; password="上一步输出的密码"} | ConvertTo-Json) -ContentType "application/json"
$headers = @{Authorization="Bearer $($login.data.access_token)"}
Invoke-RestMethod -Method Post http://localhost:8000/api/demo/seed -Headers $headers
```

导入 OCR 字幕并触发分析：

```powershell
python backend/scripts/import_ocr_subtitles.py D:\byte\upload\subtitles --drama-id 2 --dry-run
python backend/scripts/import_ocr_subtitles.py D:\byte\upload\subtitles --drama-id 2

$body = @{force_reanalyze=$true} | ConvertTo-Json
foreach ($id in 4,5,6,7,8,9,3) {
  Invoke-RestMethod -Method Post "http://localhost:8000/api/episodes/$id/analyze" -Headers $headers -Body $body -ContentType "application/json"
}
```

这一步只生成后台可审核的 `draft` 高光；确认 OCR 字幕和高光时间点后，再在管理后台发布到播放端。

### 2. 管理后台

```powershell
cd frontend/admin_web
npm install
npm run dev
```

默认访问 `http://localhost:5173`。

生产环境可先构建前端，再由 FastAPI 托管 `frontend/admin_web/dist`：

```powershell
cd frontend/admin_web
npm run build
cd ../..
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

此时可直接访问 `http://localhost:8000/login` 和 `http://localhost:8000/workspace`。

### 3. Flutter 播放端

```powershell
cd mobile
flutter pub get
flutter run
```

Flutter Web 默认通过 `http://localhost:8000` 访问后端；Android 模拟器默认通过 `http://10.0.2.2:8000` 访问电脑本机后端。如需改地址：

```powershell
flutter run --dart-define=API_BASE_URL=http://你的局域网IP:8000
```

### 4. 演示链路验收

后端启动后，可运行只读验收脚本确认 E001-E007 的播放链路仍然完整：

```powershell
python backend/scripts/verify_demo_chain.py
```

该脚本会检查后端健康状态、`那年冬至` E001-E007 的发布高光数量、播放端接口是否只下发 `published` 高光、是否隐藏 `reason` / `confidence` / `status` 等后台字段、本地 MP4 代理是否支持 `Range`，以及后台 analytics 接口鉴权和核心统计字段。

如果当前机器没有本地视频文件，可先跳过视频 Range 检查：

```powershell
python backend/scripts/verify_demo_chain.py --skip-video-range
```

## 演示流程

1. 启动后端。
2. 运行 `python backend/scripts/verify_demo_chain.py` 确认 E001-E007 后端下发和视频代理正常。
3. 启动 Flutter Web 或 Android 播放端。
4. 在首页选择 `那年冬至` 的任一剧集进入播放页。
5. 播放到高光时间点后出现互动浮层，点击按钮后回传日志。
6. 回到后台刷新，看板中的互动和点击率更新。

## 交付物准备

交付说明见 [docs/DELIVERY_GUIDE.md](docs/DELIVERY_GUIDE.md)。

当前推荐交付 Web 演示包：管理后台 `frontend/admin_web/dist`、播放端 `mobile/build/web`、截图素材和高光审核清单统一整理到 `artifacts/delivery/`。APK 命令已整理，但本机仍需安装 Android SDK 后才能产出可安装包。

## 部署方式

### 方式一：脚本安装

### 方式二：Docker Compose (推荐)

使用 Docker Compose 一键启动完整环境（FastAPI 后端、RQ Worker、Redis、PostgreSQL）。

```bash
# 复制环境变量文件
cp .env.example .env
# 启动服务
docker compose up --build -d
```

注：由于使用 Compose 编排，各服务都在同一个 Docker 虚拟网络下，配置中已默认将 `DATABASE_URL` 指向内部的 `postgres` 容器，并将 `REDIS_URL` 设为 `redis://redis:6379/0`。

## 访问
在浏览器中打开 `http://YOUR_SERVER_IP:8000`

如果 admin 密码是自动生成的，在 log 中查找:
```bash
docker compose logs app | grep "admin password"
```
