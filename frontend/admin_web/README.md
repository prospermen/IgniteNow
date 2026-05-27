# IgniteNow Admin Web

`frontend/admin_web/` 是 IgniteNow 的 Web 工作台前端模块。当前已完成 `P0-WEB-01` 的工程初始化，并完成 `/` 概览页视觉体验打磨；`/workspace` 作为后续承载真实功能的统一工作台骨架保留。

## 当前已完成

- 初始化 Vite + React 项目结构。
- 接入 Ant Design 和 `@ant-design/icons`。
- 建立并打磨 `/` 概览页视觉：
  - Canvas Cream 暖色背景
  - 固定浮动 pill 导航
  - hero 区短剧互动引擎预览
  - 产品价值 Before/After 叠卡动效
  - 项目亮点 bento 卡片与扫光动效
  - 核心闭环自动强调动画
  - 应用场景 mini UI 动效
  - 背景环境光呼吸动效
  - 黑色 pill CTA
- 建立两层页面结构并接入 React Router：
  - `/`：介绍型概览页，负责说明产品价值、项目亮点、核心闭环和应用场景。
  - `/login`：JWT 登录页，调用后端 `POST /api/auth/login`，根据 `role` 进入对应工作台页面。
  - `/workspace`：受前端访问守卫保护；无本地 access token 时会重定向到 `/login`，有 token 时按角色跳转默认页。
  - `/workspace/dashboard`：仪表盘空白页，仅 `admin` 可见。
  - `/workspace/dramas`：短剧管理空白页，仅 `admin` 可见。
  - `/workspace/episodes`：剧集配置空白页，`admin` 和 `uploader` 可见。
  - `/workspace/analyze`：AI 高光识别空白页，`admin` 和 `uploader` 可见。
  - `/workspace/highlights`：高光审核发布空白页，仅 `admin` 可见。
- 拆分前端模块边界：
  - `src/pages/LandingPage.jsx`：概览页组件。
  - `src/pages/WorkspaceLayout.jsx`：统一工作台布局组件。
  - `src/pages/workspace/`：工作台各路由占位页面。
  - `src/workspaceModules.jsx`：工作台导航、页面元信息和角色权限配置。
  - `src/auth.js`：当前前端访问守卫使用的本地 token 工具。
  - `src/services/apiClient.js`：统一 Axios 实例，自动携带 `Authorization: Bearer <access_token>`，遇到 `401/403` 时清理登录态并跳转 `/login`。
  - `src/services/authApi.js`：后台登录和退出登录 API 封装。
  - `src/styles/base.css`：全局基础样式。
  - `src/styles/landing.css`：概览页样式和动效。
  - `src/styles/workspace.css`：后台工作台样式。
- 在 `/workspace` 中加入 P0 后续功能导航：
  - 短剧管理
  - 剧集管理
  - AI 分析
  - 高光审核
  - 基础看板
- 调整 `/workspace` 侧边栏：
  - 顶部 `IgniteNow` 为静态品牌标识，不再作为返回入口页的链接。
  - 副标识改为版本号 `v0.1`。
  - 品牌区左侧显示当前登录用户名首字母头像；侧栏收起时仅显示头像。
  - 点击头像会打开用户菜单，可执行退出登录，清除本地登录态并返回 `/login`。
  - 左侧品牌区和右侧顶部栏统一为 65px 高度，并使用同色灰色底部分割线；侧栏收起时仍保留该分割线。
  - 侧栏菜单项和底部折叠按钮统一使用固定尺寸 SVG 图标、小圆角矩形按钮、同一套 hover 样式和一致的宽度/边距；侧栏收起后隐藏顶部标题，菜单项和底部折叠按钮都以 40px 图标按钮居中显示。
  - 去掉侧栏菜单项、折叠按钮、图标和 SVG 的浏览器默认焦点虚线框，避免图标旁出现黄色虚线框。
  - 侧栏菜单按角色过滤：`admin` 可见全部页面，`uploader` 仅可见剧集配置和 AI 高光识别。
- 配置基础工程文件：
  - `package.json`
  - `package-lock.json`
  - `vite.config.js`
  - `eslint.config.js`
  - `.gitignore`
  - `index.html`
- 新增前端源码：
  - `src/main.jsx`
  - `src/App.jsx`
  - `src/pages/LandingPage.jsx`
  - `src/pages/WorkspaceLayout.jsx`
  - `src/workspaceModules.jsx`
  - `src/styles/base.css`
  - `src/styles/landing.css`
  - `src/styles/workspace.css`

## 目录说明

```text
frontend/admin_web/
├── src/
│   ├── pages/
│   │   ├── LandingPage.jsx      # 概览页
│   │   ├── WorkspaceLayout.jsx  # /workspace 工作台布局
│   │   └── workspace/           # /workspace/* 占位页面
│   ├── workspaceModules.jsx     # 工作台导航、模块元信息和角色权限
│   ├── auth.js                  # 登录 token 本地读写工具
│   ├── services/                # Axios client 与认证 API
│   ├── styles/
│   │   ├── base.css             # 全局基础样式
│   │   ├── landing.css          # 概览页样式与动效
│   │   └── workspace.css        # 后台工作台样式
│   ├── App.jsx                  # React Router 路由配置
│   └── main.jsx                 # React 挂载入口、Ant Design ConfigProvider 与主题 token
├── index.html           # Vite HTML 入口
├── vite.config.js       # Vite 配置，默认端口 5173
├── eslint.config.js     # ESLint 配置
├── package.json         # npm scripts 与依赖声明
├── package-lock.json    # 依赖锁定文件
├── .gitignore           # 忽略 node_modules、dist、日志文件
└── README.md            # 本文档
```

## 认证设计

JWT 登录认证方案、前后端联动方式和后续接入提醒，见：

```text
frontend/admin_web/AUTHENTICATION.md
```

## 本地启动

第一次启动前先安装依赖：

```bash
npm install
```

启动开发服务器：

```bash
npm run dev
```

入口页：

```text
http://localhost:5173/
```

## 常用命令

```bash
npm run build
```

执行生产构建，输出到 `dist/`。

```bash
npm exec eslint .
```

执行当前前端目录的 ESLint 检查。

```bash
npm run preview
```

本地预览生产构建结果。

## 已验证结果

截至 2026-05-26，已完成以下验证：

- `npm install` 成功。
- `npm exec eslint .` 通过。
- `npm run build` 通过。
- `npm run dev -- --host 127.0.0.1` 启动后，`http://127.0.0.1:5173/` 返回 HTTP 200。
- `/workspace` 已接入 React Router，并按角色自动跳转默认页面。

当前构建产物中 JS 约 836 kB，Vite 会提示 chunk 超过 500 kB。该提示主要来自当前单包构建与 Ant Design 依赖体积，不影响本地运行；等页面和路由变多后，可通过动态 import、路由级拆分或 manual chunks 优化。

## 接下来需要完善

后续工作应按 `docs/TASK_BREAKDOWN.md` 的 P0-WEB 顺序推进：

| ID | 内容 | 当前状态 |
|---|---|---|
| `P0-WEB-02` | API client 封装，统一 Axios service，并自动携带 Bearer JWT | 已完成认证基础封装，业务 API 待接 |
| `P0-WEB-03` | 短剧列表/创建页 | 未完成 |
| `P0-WEB-04` | 剧集列表/创建页，支持视频 URL、字幕 URL/字幕内容 | 未完成 |
| `P0-WEB-05` | AI 分析触发按钮 | 未完成 |
| `P0-WEB-06` | 高光审核页，支持查看、编辑、发布、驳回 | 未完成 |
| `P0-WEB-07` | 基础看板页，展示 overview 指标 | 未完成 |

## 尚未完成

- 已接入后端 JWT 登录 API，但后台业务页面仍未接入真实数据 API。
- 已实现统一 Axios client，并自动注入 `Authorization: Bearer <access_token>`。
- 尚未配置模块内 `.env.example`；后端 API 地址可通过 `VITE_API_BASE_URL` 覆盖，默认 `http://localhost:8000`。
- 当前 `/workspace` 只是工作台骨架，不具备真实创建、编辑、发布或查询能力。
- 已引入 `react-router-dom`；当前 `/workspace/*` 页面内容区留空，仅保留工作台框架、侧边导航和顶部标题描述。
- 尚未实现错误提示、加载态、空状态、表单校验和接口异常处理。
- 尚未实现端到端验收链路。
- 概览页已完成当前阶段视觉打磨，后续若继续调整，应优先保持 `LandingPage.jsx` 与 `landing.css` 内聚，避免影响 `/workspace` 工作台样式。

## 后续开发建议

下一步建议优先做 `P0-WEB-02`：

1. 新增模块内 `.env.example` 或环境变量说明，约定 `VITE_API_BASE_URL`。
2. 在 `src/services/` 下继续补齐短剧、剧集、高光和看板 API 方法。
3. 根据 `docs/API_CONTRACT.md` 中的后端契约实现具体业务页面。
4. 对 `/workspace/*` 页面补加载态、空状态、错误态和 401/403 行为验收。

注意：修改 API 字段、请求体或响应体前，必须先同步 `docs/API_CONTRACT.md`；高光 JSON 结构以 `docs/HIGHLIGHT_SCHEMA.json` 为准。
