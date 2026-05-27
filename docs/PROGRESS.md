# 开发进度

## 2026-05-27

### 已完成
- 新增移动端上传账号体系：`user_account` 模型、注册和登录接口、JWT token 校验、上传接口 Bearer 鉴权。
- 新增移动端单集上传接口 `POST /api/uploads/episodes`，支持上传 MP4 视频、SRT/VTT/TXT 字幕文件或字幕文本，文件保存到 `backend/uploads/`，并创建或复用短剧后写入 `episode`。
- Flutter 播放端新增上传入口和 `UploadEpisodePage`，支持注册/登录、选择 MP4、选择字幕文件、填写字幕文本、上传成功后刷新剧集列表并可跳转播放页。
- 更新 `.env.example`、`datebase/schema.sql`、`docs/API_CONTRACT.md` 和 `docs/DECISIONS.md`，同步 JWT、上传接口和本地文件保存策略。

### 已验证
- `python -m pytest tests` 通过，共 12 个测试，新增覆盖未登录上传、登录上传入库、播放端可见、非 MP4 拦截、字幕文本入库。
- `python -m compileall backend ai_service` 通过。
- `python backend/scripts/verify_demo_chain.py --base-url http://127.0.0.1:8010 --skip-video-range` 通过，确认上传相关改动未破坏 E001-E007 演示链路。
- `npm run build` 通过，管理后台生产构建仍可用；Vite 仍提示 Ant Design chunk 超过 500k。
- `flutter pub get` 通过，新增 `file_picker` 依赖。
- `flutter analyze` 通过。

### 遗留问题
- 上传视频时长仍由用户填写，暂未自动解析 MP4 duration。
- 上传后不会自动触发 AI 分析，需要在管理后台点击识别并审核发布。

## 2026-05-26

### 已完成
- 按优先级 1 完成后端结构整理：将原集中式 API 拆分为 `admin`、`player`、`interactions`、`analytics`、`demo` 路由，并抽出通用鉴权、视频 URL 处理和高光校验服务。
- 补齐后台高光管理能力：支持手动新增高光、编辑高光、归档高光、批量更新状态，并在发布状态下校验同集高光时间段重叠。
- 强化 AI 分析入库保护：缺少字幕时明确置为 `failed`，非法高光项不会直接中断整集分析，响应中返回 `invalid_count`。
- 补齐管理统计接口：新增高光互动排行、剧集高光时间线、单条高光统计，便于后续后台看板继续扩展。
- 补齐生产化最小测试集：新增 `tests/test_player_api.py`、`tests/test_interactions.py`、`tests/test_analysis.py` 和内存 SQLite 测试夹具，覆盖播放端字段隔离、draft/rejected 不下发、互动幂等、admin token、字幕缺失和高光校验。
- 将 Pydantic v2 schema 配置迁移到 `ConfigDict(from_attributes=True)`，减少测试和后续升级噪音。
- 管理后台接入新增审核和统计接口：高光审核页支持勾选后批量发布、驳回、归档；单条高光可打开统计抽屉；新增单集时间线看板和高光排行榜。
- 同步 `docs/API_CONTRACT.md`，记录新增高光管理接口、分析响应字段和 analytics 接口。
- 补齐演示数据状态：将 E006 的 6 条高光从 `draft` 发布为 `published`，恢复 E001-E007 共 54 条已发布高光的交付基线。

### 已验证
- `python -m compileall backend ai_service` 通过。
- `python -m pytest tests` 通过，共 8 个测试。
- `npm run build` 通过，管理后台生产包已重新生成；Vite 仍提示 Ant Design 相关 chunk 超过 500k，为既有体积提示。
- `python backend/scripts/verify_demo_chain.py --base-url http://127.0.0.1:8010` 通过，共 17 项检查：后端健康、E001-E007 播放端详情、7 个本地 MP4 Range 代理、播放端不泄露审核字段、管理 analytics 鉴权和新增统计接口。
- 管理端写接口冒烟通过：`POST /api/episodes/{episode_id}/highlights`、`PUT /api/highlights/{highlight_id}`、`POST /api/episodes/{episode_id}/highlights/bulk-status`、`DELETE /api/highlights/{highlight_id}`，测试高光已清理。

### 遗留问题
- 当前 analytics 仍是实时 SQL 聚合，适合 MVP 演示；数据量变大后应增加按剧集/日期的聚合表或缓存。
- 管理后台时间线目前使用轻量 CSS 视图，尚未引入 ECharts；后续如果要做热力图、趋势图和多维筛选，可再引入图表库并拆分 chunk。
- SQLAlchemy 模型仍使用 `datetime.utcnow` 默认值，在 Python 3.14 测试环境下会提示弃用警告；后续可统一迁移到 timezone-aware UTC 时间。

## 2026-05-25

### 已完成

- 新增只读演示链路验收脚本 `backend/scripts/verify_demo_chain.py`，用于检查后端健康状态、E001-E007 发布高光数量、播放端字段隔离、本地 MP4 Range 代理和后台 analytics 鉴权。
- 更新 README，补充演示链路验收命令，并将演示流程调整为当前数据库驱动的 E001-E007 剧集入口。
- 将 Flutter 播放端高光互动浮层停留时间从 3 秒延长到 4 秒；同步 `interaction_template.duration_ms` 默认值、种子 SQL 和当前 SQLite 模板数据为 `4000ms`。
- 进入交付物准备阶段：新增 `docs/DELIVERY_GUIDE.md`，整理 Web 演示包、截图、录屏脚本和 APK 打包要求；修正 README 中 Flutter 播放端目录和 Android 模拟器默认后端地址说明。
- 已构建管理后台生产包 `frontend/admin_web/dist` 和 Flutter Web 播放端生产包 `mobile/build/web`，并整理交付包到 `artifacts/delivery/`。
- 已补齐 Android SDK 后完成 APK 构建准备：将本地 `E:\gradle-8.12-all\gradle-8.12` 写入 Gradle wrapper 缓存，并在 Android Gradle 配置中增加阿里云 Maven 镜像源，保留官方源兜底。
- 已产出 Android release APK，并复制到 `artifacts/delivery/ignitenow-app-release.apk`。
- 新增交付启动脚本 `artifacts/delivery/start_demo.ps1` 和 `artifacts/delivery/stop_demo.ps1`，用于一键启动 / 停止后端、管理后台 Web 和 Flutter Web 播放端。

### 已验证

- `python backend/scripts/verify_demo_chain.py` 通过，共完成 17 项检查：E001-E007 播放端详情均返回 expected published 高光且不泄露 `reason`、`confidence`、`status`，7 个本地视频代理均返回 `206 video/mp4`，后台 analytics 带 token 正常、不带 token 返回 403。
- `python -m compileall backend ai_service`、`flutter analyze`、`flutter build web` 均通过；重新构建后的 Flutter Web 产物已确认高光浮层自动消失和 `ignore` 记录时间为 4 秒。
- `npm run build` 通过，产出管理后台 `dist`；Vite 仍提示 Ant Design chunk 大小超过 500k，仅为性能提示。
- `flutter build web --dart-define=API_BASE_URL=http://localhost:8000` 通过，产出 `mobile/build/web`。
- `flutter build apk --release --dart-define=API_BASE_URL=http://10.0.2.2:8000` 已产出 `mobile/build/app/outputs/flutter-apk/app-release.apk`，复制后的交付产物大小约 47.8MB。

## 2026-05-24

### 已完成

- 固化 P0 API 契约：短剧、剧集、AI 分析、高光审核发布、播放端下发、互动日志、基础统计。
- 固化高光 JSON Schema，限定 5 类高光、时间单位、分数范围和允许特效。
- 新增数据库建表和演示种子 SQL，包含核心表、索引和 `idempotency_key` 唯一约束。
- 新增 FastAPI 后端骨架和 P0 主链路接口。
- 新增 AI 服务字幕解析器和关键词 fallback 高光识别。
- 新增 React + Vite + Ant Design 管理后台最小闭环页面。
- 新增 Flutter 播放端模型、API client、匿名用户 ID、高光触发引擎、互动浮层、基础特效和日志回传。
- 更新 `.env.example`、`docker-compose.yml` 和 README 启动说明。
- 新增 DeepSeek 高光识别接入配置，AI 服务可在有 `DEEPSEEK_API_KEY` 时优先调用 DeepSeek，无 key 时继续使用 fallback。
- 新增播放端短剧/剧集入口接口，Flutter 首页可从数据库中的 `drama` / `episode` 数据进入播放页。
- 新增本地视频文件代理：数据库中的本地 MP4 路径会转换为播放端可访问的 HTTP 视频地址。
- 已将 `D:\byte\upload\videos\E001.mp4` 到 `E006.mp4` 导入当前 SQLite 数据库，归属到短剧 `那年冬至` 的第 1-6 集；保留已完成的 `E007.mp4` 第 7 集记录。
- `datebase/seed.sql` 已同步本地视频种子数据，重新初始化时可恢复 `那年冬至` 的 E001-E007 剧集配置。
- 新增 OCR 字幕导入脚本 `backend/scripts/import_ocr_subtitles.py`，可将 `D:\byte\upload\subtitles` 中的 `E001_ocr.txt` 到 `E007_ocr.txt` 清洗、去重并转换为 SRT 后写入 `episode.subtitle_content`。
- 已将 `那年冬至` E001-E007 的 OCR 字幕导入当前 SQLite 数据库，并触发 DeepSeek 分析生成后台待审核的 `draft` 高光。
- 修复 Flutter Web 默认后端地址：浏览器端默认请求 `http://localhost:8000`，Android 模拟器仍默认请求 `http://10.0.2.2:8000`。
- 修正当前 SQLite 和 `datebase/seed.sql` 中 `那年冬至` E001-E007 的本地视频路径，从不存在的 `D:\upload\videos` 改为实际存在的 `D:\byte\upload\videos`。
- 已发布 `那年冬至` E001 的 8 条高光，并完成“播放端下发 published 高光 -> Flutter Web 播放触发浮层 -> 点击互动 -> 后端日志回传 -> analytics 更新”的闭环验证。
- 已发布 `那年冬至` E002-E007 的高光，并完成主短剧 E001-E007 整季播放端下发准备；当前发布数量为 E001/E002/E003/E004/E005/E007 各 8 条，E006 为 6 条。
- 修正当前 SQLite 和 `datebase/seed.sql` 中 `那年冬至` 第 7 集标题，从占位标题 `水水水` 改为 `E007`。
- 导出 `那年冬至` E001-E007 的高光审核清单到 `artifacts/highlight_audit_E001_E007.md` 和 `artifacts/highlight_audit_E001_E007.csv`，用于逐条核对时间点、按钮文案、类型、特效、原因和字幕片段。

### 已验证

- `python -m compileall backend ai_service` 通过。
- FastAPI TestClient 主链路通过：`/health`、`/api/demo/seed`、`/api/episodes/1/analyze`、`/api/episodes/1/highlights/publish`、`/api/player/episodes/1`、`/api/interactions`、`/api/analytics/overview`。
- `npm install` 和 `npm run build` 通过；Vite 仅提示 Ant Design chunk 偏大，不影响运行。
- `flutter pub get` 通过。
- `flutter analyze` 通过，无静态分析问题。
- DeepSeek 接入后验证：未配置 `DEEPSEEK_API_KEY` 时，`POST /api/episodes/1/analyze` 自动走 `fallback_rules` 并生成 3 条高光。
- 播放端入口接口验证：`GET /api/player/dramas`、`GET /api/player/dramas/1/episodes` 可返回数据库短剧和剧集数据。
- 本地视频代理验证：`D:\byte\upload\videos\E007.mp4` 存在时，`GET /api/player/episodes/3` 返回 `/video` 代理地址，`GET /api/player/episodes/3/video` 返回 MP4 文件。
- 本地视频批量验证：`GET /api/player/episodes/4..9` 均返回 `/video` 代理地址，`GET /api/player/episodes/{id}/video` 支持 `Range: bytes=0-1023` 并返回 `206 video/mp4`。
- OCR 字幕导入验证：E001-E007 清洗后分别得到 89、98、51、31、66、31、75 条可解析 SRT cue，`python -m compileall backend ai_service` 通过。
- DeepSeek live 分析验证：E001-E005/E007 各生成 8 条 `draft` 高光，E006 生成 6 条 `draft` 高光；播放端接口暂不返回这些未发布高光。
- Flutter Web 地址验证：`flutter analyze` 和 `flutter build web` 通过；Playwright 访问 `http://localhost:62880` 时确认 `/api/player/dramas`、`/api/player/dramas/2/episodes`、`/api/player/dramas/1/episodes` 均从 `localhost:8000` 返回 200。
- Flutter Web 播放验证：`GET /api/player/episodes/4` 返回 `/video` 代理地址，`GET /api/player/episodes/4/video` 支持 `Range` 并返回 `206 video/mp4`；Playwright 点击 E001 后确认浏览器请求视频代理成功且无请求失败。
- E001 互动闭环验证：发布后 `GET /api/player/episodes/4` 下发 8 条高光且不暴露 `reason`、`confidence`、`status`；Playwright 跳转到首个高光时间点后触发浮层并点击按钮，`user_interaction_log` 新增 E001 的 `impression` 和 `click`，analytics 指标随之更新。
- 整季发布验证：`GET /api/player/dramas/2/episodes` 返回 E001-E007，发布高光数分别为 8、8、8、8、8、6、8；`GET /api/player/episodes/{id}` 对 E001-E007 均返回 `/video` 代理地址和 published 高光，且不暴露 `reason`、`confidence`、`status`。
- 整季视频代理验证：E001-E007 的 `GET /api/player/episodes/{id}/video` 均支持 `Range: bytes=0-1023` 并返回 `206 video/mp4`。
- E002 互动抽样验证：Playwright 打开 Flutter Web，进入 E002 播放页，跳转到首个高光时间点后触发浮层并点击按钮；`user_interaction_log` 新增 E002 首个高光的 `impression` 和 `click`，当前 `GET /api/analytics/overview` 返回 `highlight_count=60`、`published_highlight_count=54`、`interaction_count=46`、`click_count=7`、`avg_click_rate=0.28`。
- 高光审核清单验证：从 `backend/ignitenow.db` 导出 54 条 published 高光，按 E001-E007 分布为 8、8、8、8、8、6、8；Markdown 与 CSV 均为 UTF-8 内容，无 `\u` 字面量和问号占位。

### 遗留问题

- OCR 字幕来自视频画面识别，可能仍存在错字、漏字和重复语义；发布前需要在管理后台审核高光时间点和按钮文案。
- 演示短剧 `逆光归来` 仍使用公开演示 MP4；主短剧 `那年冬至` 已接入本地 MP4 资源。
- APK 打包、展示录屏和截图素材仍待完成。
## 2026-05-27 后端权限收口

### 已完成
- 新增后台账号托管接口 `POST /api/auth/admin/users`，公开注册仍只创建 `uploader`，后台可用 `role=admin` 的 Bearer JWT 访问管理接口。
- `require_admin` 支持 `X-Admin-Token` 和 admin Bearer token 双轨鉴权。
- 收口账号密码登录契约：`/api/auth/login` 和 `/api/auth/me` 响应新增 `expires_in` 与嵌套 `user`，默认 JWT 有效期调整为 120 分钟，并新增无 refresh token 版本的 `POST /api/auth/logout` 占位接口。
- `GET /api/dramas`、`GET /api/episodes`、`GET /api/episodes/{episode_id}/highlights` 已纳入后台鉴权，防止后台审核字段未授权暴露。
- `POST /api/interactions` 新增匿名身份与 `idempotency_key` 前缀一致性校验；非匿名 `user_id` 必须携带匹配的 Bearer token。
- 同步 `docs/API_CONTRACT.md`、`docs/DECISIONS.md` 与测试用例。

### 已验证
- `python -m compileall backend ai_service` 通过。
- `python -m pytest tests/test_auth_permissions.py tests/test_interactions.py tests/test_analysis.py tests/test_player_api.py tests/test_uploads.py` 通过，共 20 个测试。

### 遗留问题
- 管理后台前端仍使用 `X-Admin-Token` 自动请求，尚未做账号密码登录 UI；后端已准备 admin JWT 能力。
- 播放端仍是匿名互动，不强制用户登录；当前只做匿名身份和幂等键一致性校验。
