# 短剧即时互动激发系统开发文档

## 一、文档信息

| 项目 | 内容 |
|---|---|
| 项目名称 | 剧燃引擎：基于短剧内容理解的即时互动激发系统 |
| 项目类型 | 跨平台移动端 Android 应用 / 服务端系统 / AI 内容理解系统 / Web 管理后台 |
| 前端交付平台 | Flutter 跨平台移动端，Android 优先交付 APK |
| 服务端技术 | FastAPI + MySQL + Python AI 高光识别服务 |
| 管理后台 | React + Vite + Ant Design |
| 开发周期 | 3 周 |
| 目标用户 | 短剧观看用户、内容运营人员、平台方 |
| 核心能力 | 短剧高光识别、移动端互动触发、用户反馈回传、后台审核、数据看板 |
| MVP 目标 | 跑通“字幕/视频上传 → AI 识别高光 → 后台审核 → Android 播放端互动触发 → 用户反馈回传 → 数据看板”的完整链路 |
| 最终交付物 | GitHub 项目、Android APK、项目展示录屏、飞书技术文档、最终运行成果 |

---

## 二、项目背景

短剧内容具有节奏快、反转密集、情绪刺激强、观看时间碎片化等特点。用户在观看短剧时，往往会在剧情冲突、身份反转、撒糖、打脸、悬念卡点等时刻产生强烈情绪表达需求。

当前市面上的互动方式主要依赖弹幕和评论，但这类方式存在明显问题：

1. 用户需要主动输入文字，互动成本高；
2. 打字会打断观看体验；
3. 弹幕内容质量不可控，容易遮挡画面；
4. 平台难以准确知道用户在哪些剧情节点产生强烈情绪；
5. 高光点依赖人工运营配置，难以规模化处理大量短剧内容。

因此，本项目希望通过 AI 内容理解能力，对短剧字幕、剧情片段和时间轴进行分析，自动识别冲突、反转、撒糖、爽点、悬念等剧情高光，并将高光点转化为可下发的结构化数据。

在用户观看短剧时，Flutter Android 播放端会根据高光时间点自动触发低门槛互动组件，例如情绪按钮、气泡、特效、群体反馈等，从而提升用户剧情参与感和即时情绪表达体验。

---

## 三、项目核心目标

### 3.1 总目标

构建一个完整的短剧高光识别与即时互动触发系统，实现以下闭环：

```text
短剧内容上传
→ AI 高光识别
→ 高光数据结构化存储
→ 后台审核与互动配置
→ Android 播放端时间轴触发互动
→ 用户行为回传
→ 数据看板分析
```

### 3.2 MVP 目标

三周内完成以下最小可行功能：

1. 支持上传或配置短剧视频和字幕；
2. 支持基于字幕文本进行 AI 高光识别；
3. 支持生成结构化高光点 JSON；
4. 支持高光点入库；
5. 支持后台查看、编辑、发布高光点；
6. 支持为不同高光类型匹配互动模板；
7. 支持 Flutter Android 播放端根据时间轴自动触发互动组件；
8. 支持用户点击互动按钮并回传日志；
9. 支持后台看板展示基础互动数据；
10. 支持 GitHub 代码提交、分支管理、项目录屏和最终 APK 交付。

---

## 四、项目定位

本项目不是普通视频网站，也不是单纯的聊天式 Agent，而是一个：

> 面向短剧内容消费场景的 AI 高光识别与即时互动激发系统。

它的核心价值在于：

```text
通过 AI 理解剧情，在用户情绪峰值出现的时刻，主动提供低门槛互动入口。
```

系统不是等待用户主动评论，而是在剧情反转、冲突、撒糖、爽点等节点，将合适的互动方式主动送到用户面前。

---

## 五、系统角色设计

### 5.1 内容运营人员 / 管理员

负责：

1. 创建短剧信息；
2. 上传或配置剧集视频；
3. 上传或导入字幕；
4. 触发 AI 高光识别；
5. 审核 AI 识别结果；
6. 修改高光类型、时间点和互动配置；
7. 发布高光点到用户播放端；
8. 查看用户互动数据。

### 5.2 普通用户

负责：

1. 进入 Flutter Android 短剧播放页；
2. 观看短剧视频；
3. 在剧情高光点看到互动按钮或特效；
4. 点击情绪按钮表达态度；
5. 查看群体反馈，例如“已有 2381 人选择反转了”。

### 5.3 AI 高光识别服务

负责：

1. 解析字幕；
2. 按时间轴切分剧情片段；
3. 判断每个片段是否为高光；
4. 输出高光类型、情绪、强度、置信度、理由；
5. 推荐互动模板；
6. 将结果返回给后端服务。

---

## 六、高光类型定义

MVP 阶段固定 5 类高光类型。

| 类型标识 | 中文名称 | 场景说明 | 用户情绪 | 互动方向 |
|---|---|---|---|---|
| conflict | 冲突 | 争吵、羞辱、威胁、对抗、误会爆发 | 愤怒、站队、紧张 | 支持角色、反击、吐槽 |
| reversal | 反转 | 身份揭露、真相曝光、局势逆转 | 震惊、爽感、意外 | 震惊按钮、反转提示 |
| sweet | 撒糖 | 保护、表白、暧昧、亲密接触 | 甜蜜、磕 CP | 爱心、甜度、CP 发电 |
| satisfying | 爽点 | 打脸、复仇、逆袭、反派失败 | 爽、释放、兴奋 | 爽值、爆破、打脸印章 |
| suspense | 悬念 | 未解谜团、危险逼近、断集钩子 | 好奇、焦虑、期待 | 猜测、催更、下一集 |

---

## 七、系统整体架构

### 7.1 总体架构图

```text
┌─────────────────────────────────┐
│       Flutter Android App        │
│ 视频播放 / 时间轴监听 / 互动浮层 / 日志回传 │
└───────────────┬─────────────────┘
                │ HTTP REST API + JSON
                ▼
┌─────────────────────────────────┐
│            FastAPI 后端服务       │
│ API / 鉴权 / 高光管理 / 互动日志 / 数据统计 │
└───────┬───────────────┬─────────┘
        │ SQLAlchemy     │ Python 调用 / HTTP API
        ▼               ▼
┌───────────────┐   ┌─────────────────┐
│    MySQL 数据库 │   │ Python AI 识别服务 │
│ drama/episode │   │ 字幕解析 / LLM判断 │
│ highlight/log │   │ 高光JSON输出       │
└───────────────┘   └─────────────────┘
        ▲
        │ HTTP REST API + JSON
┌─────────────────────────────────┐
│          React Web 管理后台       │
│ 短剧管理 / 高光审核 / 互动配置 / 数据看板 │
└─────────────────────────────────┘
```

### 7.2 核心数据流

```text
运营人员在 Web 后台创建短剧
        ↓
上传视频地址和字幕文件
        ↓
后端保存 episode 信息
        ↓
触发 AI 高光识别
        ↓
Python AI 服务解析字幕并输出高光 JSON
        ↓
后端校验 JSON 并写入 highlight_event
        ↓
后台审核并发布高光点
        ↓
Flutter Android App 请求播放数据
        ↓
App 播放视频并监听 currentPosition
        ↓
命中高光时间段后展示互动浮层
        ↓
用户点击情绪按钮
        ↓
App 回传互动日志
        ↓
Web 后台数据看板展示互动效果
```

---

## 八、技术栈选型

### 8.1 总体技术选型

| 层级 | 技术选择 | 说明 |
|---|---|---|
| 移动端 | Flutter + Dart | 跨平台开发，Android 优先交付，适合快速实现视频播放、互动浮层和动画效果 |
| Android 打包 | Flutter Android Build | 输出 APK，作为最终移动端展示产物 |
| 移动端状态管理 | Riverpod / Provider | 管理播放状态、高光点列表、互动触发状态 |
| 视频播放 | video_player / better_player | 实现短剧播放、进度监听、暂停、播放、时间轴读取 |
| 动效实现 | Flutter AnimationController / AnimatedWidget / Lottie 可选 | 实现爱心雨、气泡、屏幕闪光、爽点爆破等互动特效 |
| 接口请求 | Dio | Flutter 端调用 FastAPI 接口，统一处理请求、响应、错误、超时 |
| 管理后台 | React + Vite + Ant Design | 用于短剧管理、高光审核、互动配置和数据看板 |
| 后台请求库 | Axios | React 后台调用 FastAPI REST API |
| 服务端 | FastAPI | 负责 API、业务逻辑、AI 调度、数据管理 |
| 数据库 | MySQL | 存储短剧、剧集、高光点、互动配置、用户互动日志 |
| ORM | SQLAlchemy | Python 后端常用 ORM，便于维护数据模型 |
| AI 服务 | Python + LLM API | 解析字幕，识别冲突、反转、撒糖、爽点、悬念等高光 |
| 文件存储 | 本地存储 / 阿里云 OSS，可先本地 | MVP 阶段可先使用本地视频和字幕文件 |
| 数据可视化 | ECharts | 管理后台展示高光分布、点击次数、热门按钮 |

### 8.2 MVP 推荐组合

```text
Flutter Android App
FastAPI
MySQL
Python AI 高光识别脚本
React + Vite 管理后台
ECharts 数据看板
```

选择理由：

1. Flutter 适合移动端交付，可以快速实现 Android 播放端，并保留未来扩展 iOS 的可能性；
2. FastAPI 适合 AI 服务对接，Python 生态适合字幕解析、LLM 调用、JSON 校验；
3. MySQL 适合结构化业务数据，短剧、剧集、高光、互动日志都适合关系型数据库；
4. React 管理后台开发效率高，后台不是主要展示端，可以快速完成 CRUD、审核和看板；
5. 整体符合交付要求：移动端选择 Android，服务端语言不限，GitHub 管理代码，录屏展示完整链路。

---

## 九、接口通信方案

### 9.1 通信方式

本项目接口通信主要采用：

```text
HTTP REST API + JSON
```

具体通信关系如下：

| 通信对象 | 通信方式 | 数据格式 | 说明 |
|---|---|---|---|
| Flutter App ↔ FastAPI 后端 | HTTP REST API | JSON | 移动端获取播放数据、回传互动日志 |
| React 管理后台 ↔ FastAPI 后端 | HTTP REST API | JSON | 后台管理短剧、剧集、高光点、看板数据 |
| FastAPI 后端 ↔ MySQL | SQL / ORM | 表结构数据 | FastAPI 通过 SQLAlchemy 操作数据库 |
| FastAPI 后端 ↔ AI 服务 | Python 函数调用 / HTTP API | JSON | MVP 阶段可内部调用，后期可拆为独立 AI 服务 |
| 播放端群体反馈 | HTTP 查询 / 轮询 | JSON | MVP 阶段不强依赖 WebSocket |

### 9.2 移动端接口请求

Flutter 端使用 Dio 请求后端接口。

```text
Flutter Android App
        ↓ Dio HTTP Request
FastAPI REST API
        ↓ JSON Response
Flutter Android App
```

移动端主要接口：

| 接口 | 方法 | 用途 |
|---|---|---|
| `/api/player/episodes/{episode_id}` | GET | 获取播放页数据 |
| `/api/interactions` | POST | 回传用户互动日志 |
| `/api/highlights/{highlight_id}/group-feedback` | GET | 获取群体反馈数据，可选 |

### 9.3 管理后台接口请求

React 管理后台使用 Axios 请求后端接口。

后台主要接口：

| 接口 | 方法 | 用途 |
|---|---|---|
| `/api/dramas` | POST / GET | 创建和查询短剧 |
| `/api/episodes` | POST / GET | 创建和查询剧集 |
| `/api/episodes/{episode_id}/analyze` | POST | 触发 AI 高光识别 |
| `/api/episodes/{episode_id}/highlights` | GET | 查询高光点列表 |
| `/api/highlights/{highlight_id}` | PUT | 修改高光点 |
| `/api/episodes/{episode_id}/highlights/publish` | POST | 批量发布高光点 |
| `/api/analytics/overview` | GET | 获取数据看板总览 |

### 9.4 AI 服务通信方案

MVP 阶段推荐：

```text
FastAPI 后端直接调用 ai_service/highlight_analyzer.py 中的 Python 方法
```

后期扩展：

```text
FastAPI 后端
   ↓ HTTP POST /ai/analyze-highlight
独立 AI 高光识别服务
```

当前项目为了降低开发复杂度，优先采用内部函数调用，保证三周内跑通完整链路。

---

## 十、系统模块拆分

### 10.1 Flutter Android 用户播放端模块

移动端是本项目的主要展示端，负责实现短剧播放、时间轴监听、互动触发、动效展示和用户行为回传。

#### 10.1.1 移动端页面结构

```text
Flutter Android App
│
├── 首页 / 剧集入口页
│   ├── 短剧列表
│   ├── 剧集列表
│   └── 进入播放页
│
├── 短剧播放页
│   ├── 视频播放器
│   ├── 高光时间轴监听
│   ├── 互动按钮浮层
│   ├── 特效动画层
│   ├── 群体反馈气泡
│   └── 用户互动日志回传
│
└── 调试 / Demo 页面
    ├── 选择测试剧集
    ├── 查看当前播放时间
    ├── 查看当前命中高光
    └── 查看接口返回 JSON
```

#### 10.1.2 Flutter 播放页核心分层

```text
PlayerPage
│
├── VideoPlayerLayer
│   └── 负责视频播放和 currentPosition 获取
│
├── HighlightTriggerEngine
│   └── 负责判断当前时间是否命中高光点
│
├── InteractionOverlay
│   └── 负责展示互动按钮
│
├── EffectLayer
│   └── 负责展示爱心雨、闪屏、气泡、爆破等动画
│
├── GroupFeedbackBubble
│   └── 负责展示“已有 xxx 人选择反转了”
│
└── InteractionLogger
    └── 负责向后端 POST /api/interactions
```

#### 10.1.3 播放端核心逻辑

```text
1. App 进入播放页；
2. 请求 GET /api/player/episodes/{episode_id}；
3. 获取 video_url 和 highlights；
4. 初始化 VideoPlayerController；
5. 播放器开始播放；
6. 定时读取 currentPosition；
7. HighlightTriggerEngine 判断是否命中高光点；
8. 如果命中且未触发过，则展示 InteractionOverlay；
9. 用户点击按钮后触发 EffectLayer 动效；
10. App 调用 POST /api/interactions 回传日志；
11. 后端写入 user_interaction_log；
12. 数据看板展示互动结果。
```

#### 10.1.4 高光触发判断规则

输入：

```text
currentTime：当前播放时间，单位秒
highlights：后端下发的高光点列表
triggeredHighlightIds：本次播放中已触发的高光 ID
```

判断规则：

1. `currentTime >= highlight.start_time`；
2. `currentTime <= highlight.end_time`；
3. `highlight_id` 不在 `triggeredHighlightIds` 中；
4. 两个高光点触发间隔不小于设定阈值，例如 10 秒；
5. 如果多个高光点时间窗口重叠，播放端优先触发 `trigger_score` 更高的一条；
6. 如果 `trigger_score` 相同，则优先触发 `confidence` 更高的一条；
7. 如果仍然相同，则优先触发开始时间更早的一条。

为避免播放端漏触发或重复触发，后端在下发前应尽量保证同一集的已发布高光点不存在时间重叠。

伪代码：

```dart
void checkHighlightTrigger(double currentTime) {
  for (final highlight in highlights) {
    final isInRange =
        currentTime >= highlight.startTime &&
        currentTime <= highlight.endTime;

    final notTriggered =
        !triggeredHighlightIds.contains(highlight.highlightId);

    if (isInRange && notTriggered) {
      currentHighlight = highlight;
      showInteractionOverlay(highlight);
      triggeredHighlightIds.add(highlight.highlightId);
      break;
    }
  }
}
```

#### 10.1.5 移动端互动组件

MVP 阶段至少实现：

| 互动组件 | 是否必须 | 说明 |
|---|---|---|
| 情绪按钮 | 必须 | 用户点击表达情绪 |
| 点击气泡 | 必须 | 点击后飞出“+1”“反转了”等反馈 |
| 基础特效 | 必须 | 例如屏幕闪光、爱心飘动、爆破缩放 |
| 群体反馈 | 建议 | 展示已有多少人点击 |
| 复杂弹幕 | 不建议 | 容易偏离项目重点 |
| WebSocket 实时同步 | 可选 | MVP 可先用接口轮询或静态统计 |

MVP 最小实现：

```text
情绪按钮 + 点击气泡 + 屏幕闪光 / 爱心动画 + 日志回传
```

---

### 10.2 Web 管理后台模块

Web 管理后台主要面向内容运营人员，不作为主要用户端，但需要支持完整业务闭环。

#### 10.2.1 短剧管理

功能点：

1. 新增短剧；
2. 编辑短剧信息；
3. 删除短剧；
4. 查看短剧列表；
5. 查看某部短剧下的所有剧集。

字段：

```text
短剧标题
短剧简介
封面图
分类标签
创建时间
剧集数量
状态
```

#### 10.2.2 剧集管理

功能点：

1. 上传或配置视频；
2. 上传或配置字幕；
3. 设置集数；
4. 查看视频时长；
5. 查看处理状态；
6. 触发 AI 高光识别。

字段：

```text
剧集 ID
所属短剧 ID
集数
标题
视频地址
字幕地址
视频时长
处理状态
创建时间
```

#### 10.2.3 AI 高光识别结果展示

功能点：

1. 选择某一集；
2. 点击“开始识别”；
3. 后端调用 AI 服务；
4. AI 服务输出高光点；
5. 系统将高光点写入数据库；
6. 管理后台展示识别结果。

展示字段：

```text
开始时间
结束时间
高光类型
情绪类型
强度分数
置信度
识别理由
推荐互动
状态
```

#### 10.2.4 高光点审核与编辑

功能点：

1. 查看高光点列表；
2. 修改开始时间；
3. 修改结束时间；
4. 修改高光类型；
5. 修改情绪类型；
6. 修改强度分数；
7. 修改识别理由；
8. 删除错误高光点；
9. 手动新增高光点；
10. 发布或下架高光点。

页面建议：

```text
左侧：视频播放器
右侧：高光点列表
底部：高光时间轴
弹窗：高光编辑表单
```

#### 10.2.5 互动模板配置

默认模板：

| 高光类型 | 按钮文案 | 特效 | 展示位置 | 展示时长 |
|---|---|---|---|---|
| conflict | 气死我了 / 替她反击 / 支持女主 | anger_bar | bottom | 3000ms |
| reversal | 我惊了 / 反转了 / 太爽了 | screen_flash | bottom | 3000ms |
| sweet | 磕到了 / 太甜了 / 锁死 | heart_rain | right | 3000ms |
| satisfying | 爽 / 打脸成功 / 终于来了 | boom_effect | bottom | 3000ms |
| suspense | 快更 / 别卡这里 / 我猜到了 | countdown | bottom | 3000ms |

#### 10.2.6 数据看板

核心指标：

```text
曝光次数 impression_count
点击次数 click_count
点击率 click_rate
互动人数 user_count
平均触发强度 avg_intensity
热门按钮 top_action
```

功能点：

1. 展示总短剧数量；
2. 展示总剧集数量；
3. 展示总高光点数量；
4. 展示总互动次数；
5. 展示高光类型分布；
6. 展示各类高光点击率；
7. 展示热门互动按钮；
8. 展示单集高光时间轴热力图；
9. 展示高光点排行榜。

---

### 10.3 后端服务模块

后端服务是整个系统的数据中枢，主要承担以下职责：

| 职责 | 说明 |
|---|---|
| 内容管理 | 管理短剧、剧集、视频、字幕等基础数据 |
| AI 分析调度 | 接收分析请求，调用 AI 高光识别服务 |
| 高光数据管理 | 存储、查询、修改、发布高光点 |
| 互动配置管理 | 根据高光类型生成或修改互动按钮和特效配置 |
| 播放端数据下发 | 给 Flutter 播放页返回视频地址和已发布高光点 |
| 用户行为采集 | 接收用户点击、曝光、忽略、长按等互动日志 |
| 数据统计分析 | 计算曝光次数、点击次数、点击率、高光类型分布、热门按钮等指标 |

后端建议采用分层结构：

```text
HTTP Request
    ↓
Router / Controller 层
    ↓
Schema 校验层
    ↓
Service 业务逻辑层
    ↓
Repository / ORM 数据访问层
    ↓
Database
```

推荐目录：

```text
backend/app/
  routers/        # API 路由层
  schemas/        # 请求和响应结构
  services/       # 业务逻辑层
  repositories/   # 数据访问层，可选
  models/         # ORM 数据模型
  database.py
  main.py
```

---

### 10.4 AI 高光识别 Prompt 设计

AI 高光识别是本项目的核心能力，不能只依赖“调用大模型”这一笼统描述。为了保证不同成员实现结果一致，项目统一使用固定 Prompt 模板，并要求模型严格输出 JSON。

#### 10.4.1 Prompt 设计目标

Prompt 需要完成以下目标：

1. 输入一段带时间轴的字幕内容；
2. 判断字幕中是否存在剧情高光；
3. 识别高光类型，包括 conflict、reversal、sweet、satisfying、suspense；
4. 输出开始时间、结束时间、情绪类型、强度、置信度、判断理由；
5. 推荐对应互动按钮和特效；
6. 严格返回 JSON，不返回解释性自然语言。

#### 10.4.2 字幕输入格式

AI 服务会先将 `.srt` 字幕解析为结构化片段，再按 30 到 60 秒窗口切片。

输入示例：

```text
episode_id: ep_001
subtitle_segments:
[
  {"start": 120.5, "end": 123.0, "text": "你以为我真的不知道真相吗？"},
  {"start": 123.1, "end": 126.2, "text": "其实三年前救你的人不是他，是我。"},
  {"start": 126.3, "end": 130.0, "text": "什么？原来一直是你？"}
]
```

#### 10.4.3 基础 Prompt 模板

```text
你是一个短剧剧情分析助手，任务是根据带时间轴的字幕片段，识别剧情高光点。

请只识别以下 5 类高光：
1. conflict：冲突、争吵、威胁、误会爆发、角色对抗
2. reversal：身份揭露、真相曝光、局势逆转、剧情反转
3. sweet：表白、保护、亲密互动、暧昧、撒糖
4. satisfying：打脸、复仇、逆袭、反派失败、爽点释放
5. suspense：危险逼近、谜团未解、断集钩子、强悬念

请根据字幕内容输出高光点。要求：
- start_time 和 end_time 必须来自输入字幕时间轴，单位为秒
- start_time 必须小于 end_time
- 单个高光点时长建议为 3 到 15 秒
- intensity 和 confidence 必须是 0 到 1 的小数
- 如果没有明显高光，返回 highlights: []
- 不要输出 Markdown
- 不要输出解释性文字
- 只返回合法 JSON

输出 JSON 格式如下：
{
  "episode_id": "输入的 episode_id",
  "highlights": [
    {
      "start_time": 120.5,
      "end_time": 130.0,
      "highlight_type": "reversal",
      "emotion": "shock",
      "intensity": 0.92,
      "confidence": 0.87,
      "reason": "三年前救人真相被揭露，角色关系发生反转",
      "suggested_interaction": {
        "interaction_type": "emotion_buttons",
        "buttons": ["我惊了", "反转了", "太爽了"],
        "effect": "screen_flash",
        "display_duration": 3000
      }
    }
  ]
}

下面是待分析字幕：
{subtitle_segments}
```

#### 10.4.4 AI 输出约束

后端接收到 AI 输出后必须进行二次校验：

```text
1. 判断是否为合法 JSON；
2. 检查 episode_id 是否匹配；
3. 检查 highlight_type 是否属于枚举值；
4. 检查 start_time < end_time；
5. 检查 intensity、confidence 是否在 0 到 1 之间；
6. 检查高光点是否与同一剧集中已发布高光点发生时间重叠；
7. 过滤 confidence < 0.6 的高光点；
8. 对重叠高光按 trigger_score 或 confidence 保留优先级更高的一条。
```

#### 10.4.5 LLM 调用超时设置

LLM 高光识别可能需要较长时间，尤其当字幕片段较多时。MVP 阶段建议设置：

```text
单次 LLM 请求超时时间：60 到 120 秒
推荐默认值：90 秒
失败重试次数：最多 2 次
```

如果使用 `httpx` 调用外部模型服务，可以采用类似配置：

```python
httpx.AsyncClient(timeout=90)
```

当前 Demo 可以同步调用，但如果 AI 分析耗时超过 30 秒，后续应改造为异步任务队列。

---

## 十一、数据库设计

### 11.0 主键与 ID 生成策略

MVP 阶段所有业务表主键统一使用 `VARCHAR(64)`，ID 推荐使用带业务前缀的 UUID 或 ULID：

```text
drama_ + uuid/ulid
ep_ + uuid/ulid
hl_ + uuid/ulid
log_ + uuid/ulid
```

说明：

1. MVP 阶段优先保证开发简单和数据可读性；
2. 如果后续数据量扩大，建议使用 ULID 或雪花 ID，减少随机 UUID 对 MySQL B+ 树索引的影响；
3. 所有 ID 由后端生成，前端不直接生成业务主键。

### 11.1 drama：短剧表

```sql
CREATE TABLE drama (
  id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  cover_url VARCHAR(500),
  category VARCHAR(100),
  status VARCHAR(50) DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

| 字段 | 类型 | 说明 |
|---|---|---|
| id | VARCHAR | 短剧 ID |
| title | VARCHAR | 短剧名称 |
| description | TEXT | 短剧简介 |
| cover_url | VARCHAR | 封面地址 |
| category | VARCHAR | 分类 |
| status | VARCHAR | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 11.2 episode：剧集表

```sql
CREATE TABLE episode (
  id VARCHAR(64) PRIMARY KEY,
  drama_id VARCHAR(64) NOT NULL,
  episode_no INT NOT NULL,
  title VARCHAR(255),
  video_url VARCHAR(500),
  subtitle_url VARCHAR(500),
  duration FLOAT,
  analyze_status VARCHAR(50) DEFAULT 'pending',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (drama_id) REFERENCES drama(id)
);
```

| 字段 | 类型 | 说明 |
|---|---|---|
| id | VARCHAR | 剧集 ID |
| drama_id | VARCHAR | 所属短剧 ID |
| episode_no | INT | 第几集 |
| title | VARCHAR | 剧集标题 |
| video_url | VARCHAR | 视频地址 |
| subtitle_url | VARCHAR | 字幕地址 |
| duration | FLOAT | 视频时长，单位秒 |
| analyze_status | VARCHAR | AI 分析状态 |

### 11.3 highlight_event：高光事件表

```sql
CREATE TABLE highlight_event (
  id VARCHAR(64) PRIMARY KEY,
  episode_id VARCHAR(64) NOT NULL,
  start_time FLOAT NOT NULL,
  end_time FLOAT NOT NULL,
  highlight_type VARCHAR(50) NOT NULL,
  emotion VARCHAR(50),
  intensity FLOAT DEFAULT 0,
  confidence FLOAT DEFAULT 0,
  trigger_score FLOAT DEFAULT 0,
  reason TEXT,
  status VARCHAR(50) DEFAULT 'draft',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (episode_id) REFERENCES episode(id)
);
```

| 字段 | 说明 |
|---|---|
| id | 高光 ID |
| episode_id | 所属剧集 ID |
| start_time | 高光开始时间，单位秒 |
| end_time | 高光结束时间，单位秒 |
| highlight_type | 高光类型 |
| emotion | 情绪类型 |
| intensity | 情绪强度，0 到 1 |
| confidence | 模型置信度，0 到 1 |
| trigger_score | 触发分数 |
| reason | AI 判断理由 |
| status | draft / published / rejected / archived |

### 11.4 interaction_config：互动配置表

```sql
CREATE TABLE interaction_config (
  id VARCHAR(64) PRIMARY KEY,
  highlight_id VARCHAR(64) NOT NULL,
  interaction_type VARCHAR(50) DEFAULT 'emotion_buttons',
  config_json JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (highlight_id) REFERENCES highlight_event(id)
);
```

config_json 示例：

```json
{
  "buttons": [
    { "key": "shock", "text": "我惊了" },
    { "key": "reversal", "text": "反转了" },
    { "key": "satisfying", "text": "太爽了" }
  ],
  "effect": {
    "type": "screen_flash",
    "duration": 1200
  },
  "display": {
    "position": "bottom",
    "duration": 3000,
    "auto_hide": true
  }
}
```

### 11.5 user_interaction_log：用户互动日志表

```sql
CREATE TABLE user_interaction_log (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64),
  episode_id VARCHAR(64) NOT NULL,
  highlight_id VARCHAR(64) NOT NULL,
  action_type VARCHAR(50) NOT NULL,
  action_value VARCHAR(100),
  watch_time FLOAT,
  idempotency_key VARCHAR(128),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (episode_id) REFERENCES episode(id),
  FOREIGN KEY (highlight_id) REFERENCES highlight_event(id)
);
```

| 字段 | 说明 |
|---|---|
| id | 日志 ID |
| user_id | 用户 ID，MVP 可用匿名 ID |
| episode_id | 剧集 ID |
| highlight_id | 高光 ID |
| action_type | click / ignore / long_press |
| action_value | 用户点击的按钮 key |
| watch_time | 点击时视频播放时间 |
| idempotency_key | 防重复提交 key |
| created_at | 创建时间 |

### 11.6 highlight_stats：高光统计表，可选

```sql
CREATE TABLE highlight_stats (
  id VARCHAR(64) PRIMARY KEY,
  highlight_id VARCHAR(64) NOT NULL UNIQUE,
  impression_count INT DEFAULT 0,
  click_count INT DEFAULT 0,
  ignore_count INT DEFAULT 0,
  top_action VARCHAR(100),
  top_action_count INT DEFAULT 0,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (highlight_id) REFERENCES highlight_event(id)
);
```

该表用于群体反馈和数据看板的快速查询。

字段说明：

| 字段 | 说明 |
|---|---|
| impression_count | 互动组件曝光次数，即高光点被展示的次数 |
| click_count | 用户点击互动按钮次数 |
| ignore_count | 互动组件展示后用户未点击次数 |
| top_action | 当前点击次数最多的按钮 key |
| top_action_count | 当前热门按钮对应的点击次数 |

`top_action` 不能简单使用最后一次点击的 `action_value` 覆盖。正确逻辑是：

```sql
SELECT action_value, COUNT(*) AS count
FROM user_interaction_log
WHERE highlight_id = :highlight_id
  AND action_type = 'click'
GROUP BY action_value
ORDER BY count DESC
LIMIT 1;
```

MVP 阶段可以在数据看板查询时实时计算 `top_action`；如果需要提升性能，再将统计结果缓存到 `highlight_stats` 表。

---

## 十二、JSON 数据结构设计

### 12.1 AI 高光识别输出 JSON

```json
{
  "episode_id": "ep_001",
  "highlights": [
    {
      "start_time": 128.5,
      "end_time": 138.0,
      "highlight_type": "reversal",
      "emotion": "shock",
      "intensity": 0.92,
      "confidence": 0.87,
      "reason": "男主真实身份被揭露，剧情关系发生反转",
      "suggested_interaction": {
        "interaction_type": "emotion_buttons",
        "buttons": ["我惊了", "反转了", "太爽了"],
        "effect": "screen_flash",
        "display_duration": 3000
      }
    }
  ]
}
```

### 12.2 播放端下发 JSON

播放端下发的 `video_url` 必须是完整 URL，或者由 Flutter 端通过 `Config.baseUrl + video_url` 拼接。为了降低移动端播放出错概率，MVP 阶段建议后端直接返回完整 URL。

```json
{
  "episode_id": "ep_001",
  "title": "第 1 集：身份反转",
  "video_url": "https://api.example.com/static/videos/ep001.mp4",
  "duration": 420,
  "highlights": [
    {
      "highlight_id": "hl_001",
      "start_time": 128.5,
      "end_time": 138.0,
      "highlight_type": "reversal",
      "emotion": "shock",
      "interaction": {
        "buttons": [
          { "key": "shock", "text": "我惊了" },
          { "key": "reversal", "text": "反转了" },
          { "key": "satisfying", "text": "太爽了" }
        ],
        "effect": {
          "type": "screen_flash",
          "duration": 1200
        },
        "display": {
          "position": "bottom",
          "duration": 3000,
          "auto_hide": true
        }
      }
    }
  ]
}
```

### 12.3 用户互动回传 JSON

用户互动回传需要携带 `idempotency_key`，用于避免网络重试或重复点击导致多次写入。

```json
{
  "user_id": "anonymous_001",
  "episode_id": "ep_001",
  "highlight_id": "hl_001",
  "action_type": "click",
  "action_value": "reversal",
  "watch_time": 130.2,
  "idempotency_key": "md5_user_highlight_action_minute"
}
```

`idempotency_key` 由 Flutter 端生成并随请求携带。推荐规则：

```text
idempotency_key = md5(user_id + highlight_id + action_type + minute_timestamp)
```

其中 `minute_timestamp` 表示分钟级时间戳，例如 `2026-05-21T13:45`。这样可以避免同一用户在短时间内对同一高光点重复提交同类行为。

---

## 十三、后端 API 设计

### 13.1 API 模块总览

| 模块 | 路径前缀 | 作用 |
|---|---|---|
| 短剧管理 | `/api/dramas` | 管理短剧基础信息 |
| 剧集管理 | `/api/episodes` | 管理视频、字幕、剧集状态 |
| AI 分析 | `/api/episodes/{id}/analyze` | 触发高光识别 |
| 高光管理 | `/api/highlights` | 查询、编辑、发布高光点 |
| 互动配置 | `/api/interaction-configs` | 管理按钮和特效配置 |
| 播放端 | `/api/player` | 给 Flutter App 下发播放数据 |
| 用户互动 | `/api/interactions` | 接收用户点击日志 |
| 数据看板 | `/api/analytics` | 返回统计数据 |

### 13.2 创建短剧 API

```http
POST /api/dramas
```

请求体：

```json
{
  "title": "霸总追妻",
  "description": "都市情感短剧，主打反转与爽点",
  "cover_url": "/covers/drama001.jpg",
  "category": "都市情感"
}
```

响应体：

```json
{
  "success": true,
  "data": {
    "id": "drama_001",
    "title": "霸总追妻",
    "category": "都市情感",
    "created_at": "2026-05-20T10:00:00+08:00"
  }
}
```

### 13.3 创建剧集 API

```http
POST /api/episodes
```

请求体：

```json
{
  "drama_id": "drama_001",
  "episode_no": 1,
  "title": "第 1 集：身份反转",
  "video_url": "https://api.example.com/static/videos/ep001.mp4",
  "subtitle_url": "/subtitles/ep001.srt",
  "duration": 420
}
```

响应体：

```json
{
  "success": true,
  "data": {
    "id": "ep_001",
    "drama_id": "drama_001",
    "episode_no": 1,
    "title": "第 1 集：身份反转",
    "analyze_status": "pending"
  }
}
```

### 13.4 触发 AI 识别 API

```http
POST /api/episodes/{episode_id}/analyze
```

请求体：

```json
{
  "force_reanalyze": false
}
```

同步响应体：

```json
{
  "success": true,
  "data": {
    "episode_id": "ep_001",
    "analyze_status": "success",
    "highlight_count": 6
  },
  "message": "AI 高光识别完成"
}
```

处理逻辑：

```text
1. 根据 episode_id 查询剧集；
2. 校验 subtitle_url 是否存在；
3. 如果已经 success 且 force_reanalyze=false，则拒绝重复分析或返回已有结果；
4. 更新 episode.analyze_status = processing；
5. 调用 AI 高光识别服务，LLM 请求超时时间建议设置为 90 秒；
6. 校验 AI 返回 JSON 是否合法；
7. 过滤低置信度高光点，例如 confidence < 0.6 的结果不入库；
8. 检查同一集高光时间窗口是否重叠；
9. 如果发生重叠，优先保留 trigger_score 或 confidence 更高的高光点；
10. 写入 highlight_event 表；
11. 为每个高光点生成默认 interaction_config；
12. 更新 episode.analyze_status = success；
13. 返回高光数量。
```

### 13.5 查询分析状态 API

```http
GET /api/episodes/{episode_id}/analyze-status
```

响应体：

```json
{
  "success": true,
  "data": {
    "episode_id": "ep_001",
    "analyze_status": "processing",
    "highlight_count": 0,
    "updated_at": "2026-05-20T10:15:00+08:00"
  }
}
```

### 13.6 获取高光点列表 API

```http
GET /api/episodes/{episode_id}/highlights
```

响应体：

```json
{
  "success": true,
  "data": {
    "episode_id": "ep_001",
    "highlights": [
      {
        "highlight_id": "hl_001",
        "start_time": 128.5,
        "end_time": 138.0,
        "highlight_type": "reversal",
        "emotion": "shock",
        "intensity": 0.92,
        "confidence": 0.87,
        "trigger_score": 0.90,
        "status": "draft",
        "reason": "男主真实身份被揭露"
      }
    ]
  }
}
```

### 13.7 修改高光点 API

```http
PUT /api/highlights/{highlight_id}
```

请求体：

```json
{
  "start_time": 128.5,
  "end_time": 138.0,
  "highlight_type": "reversal",
  "emotion": "shock",
  "intensity": 0.92,
  "confidence": 0.87,
  "reason": "男主真实身份被揭露，剧情发生反转",
  "status": "published"
}
```

校验规则：

```text
1. start_time 必须小于 end_time；
2. highlight_type 必须属于预设枚举；
3. intensity、confidence 必须在 0 到 1 之间；
4. status 必须属于 draft/published/rejected/archived；
5. 已发布的高光必须存在 interaction_config；
6. 同一 episode 下，published 状态的高光点时间区间不能重叠；
7. 如果编辑后的时间区间与已有 published 高光冲突，后端返回 409 CONFLICT；
8. 管理后台需要提示“该时间段已存在高光点，请调整开始或结束时间”。
```

时间冲突判断方式：

```text
new_start < existing_end AND new_end > existing_start
```

只要满足该条件，就说明两个时间窗口存在重叠。

### 13.8 批量发布高光点 API

```http
POST /api/episodes/{episode_id}/highlights/publish
```

请求体：

```json
{
  "highlight_ids": ["hl_001", "hl_002", "hl_003"]
}
```

响应体：

```json
{
  "success": true,
  "data": {
    "published_count": 3
  },
  "message": "高光点批量发布成功"
}
```

### 13.9 获取播放页数据 API

```http
GET /api/player/episodes/{episode_id}
```

响应体：

```json
{
  "success": true,
  "data": {
    "episode_id": "ep_001",
    "title": "第 1 集：身份反转",
    "video_url": "https://api.example.com/static/videos/ep001.mp4",
    "duration": 420,
    "highlights": [
      {
        "highlight_id": "hl_001",
        "start_time": 128.5,
        "end_time": 138.0,
        "highlight_type": "reversal",
        "emotion": "shock",
        "interaction": {
          "buttons": [
            { "key": "shock", "text": "我惊了" },
            { "key": "reversal", "text": "反转了" },
            { "key": "satisfying", "text": "太爽了" }
          ],
          "effect": {
            "type": "screen_flash",
            "duration": 1200
          },
          "display": {
            "position": "bottom",
            "duration": 3000,
            "auto_hide": true
          }
        }
      }
    ]
  }
}
```

后端处理逻辑：

```text
1. 查询 episode；
2. 查询该 episode 下 status=published 的高光点；
3. 按 start_time 升序排序；
4. 查询每个高光点的 interaction_config；
5. 过滤掉没有互动配置的高光点；
6. 组装成播放端 JSON；
7. 返回给 Flutter App。
```

### 13.10 用户互动回传 API

```http
POST /api/interactions
```

请求体：

```json
{
  "user_id": "anonymous_001",
  "episode_id": "ep_001",
  "highlight_id": "hl_001",
  "action_type": "click",
  "action_value": "reversal",
  "watch_time": 130.2,
  "idempotency_key": "f2a7c9d8e1"
}
```

响应体：

```json
{
  "success": true,
  "message": "互动行为已记录"
}
```

校验规则：

```text
1. episode_id 必须存在；
2. highlight_id 必须存在；
3. highlight_id 必须属于当前 episode_id；
4. action_type 必须属于 impression/click/ignore/long_press；
5. watch_time 建议在高光时间附近，但 MVP 可不强制；
6. user_id 为空时，后端可生成 anonymous_id；
7. idempotency_key 必须存在；
8. 后端基于 idempotency_key 做短时间去重，避免重复写入。
```

说明：

```text
action_type = impression 表示互动组件被展示；
action_type = click 表示用户点击按钮；
action_type = ignore 表示组件自动消失但用户未点击。
```

点击率计算方式：

```text
click_rate = click_count / impression_count
```

### 13.11 数据看板 API

#### 总览数据

```http
GET /api/analytics/overview
```

响应体：

```json
{
  "success": true,
  "data": {
    "drama_count": 5,
    "episode_count": 20,
    "highlight_count": 126,
    "published_highlight_count": 88,
    "interaction_count": 3580,
    "click_count": 2400,
    "ignore_count": 1180,
    "avg_click_rate": 0.42
  }
}
```

#### 高光类型分布

```http
GET /api/analytics/highlight-types
```

#### 高光点排行榜

```http
GET /api/analytics/highlight-ranking
```

#### 热门按钮

```http
GET /api/analytics/top-actions
```

---

## 十四、状态机设计

### 14.1 AI 分析状态机

`episode.analyze_status` 使用以下状态：

| 状态 | 含义 |
|---|---|
| pending | 待分析 |
| processing | 分析中 |
| success | 分析成功 |
| failed | 分析失败 |

状态流转：

```text
pending → processing → success
pending → processing → failed
failed → processing → success
success → processing → success
```

### 14.2 高光点状态机

`highlight_event.status` 使用以下状态：

| 状态 | 含义 |
|---|---|
| draft | AI 生成后待审核 |
| published | 已发布，可下发到播放端 |
| rejected | 已驳回，不下发 |
| archived | 已归档 |

状态流转：

```text
draft → published
draft → rejected
published → draft
published → archived
rejected → draft
```

---

## 十五、项目目录结构

```text
drama-interaction-engine/
│
├── mobile_flutter/                 # Flutter Android 播放端
│   ├── lib/
│   │   ├── main.dart
│   │   ├── pages/
│   │   │   ├── drama_list_page.dart
│   │   │   └── player_page.dart
│   │   ├── models/
│   │   │   ├── episode.dart
│   │   │   ├── highlight.dart
│   │   │   └── interaction.dart
│   │   ├── services/
│   │   │   ├── api_client.dart
│   │   │   └── interaction_service.dart
│   │   ├── widgets/
│   │   │   ├── video_player_layer.dart
│   │   │   ├── interaction_overlay.dart
│   │   │   ├── effect_layer.dart
│   │   │   └── group_feedback_bubble.dart
│   │   └── controllers/
│   │       └── player_controller.dart
│   │
│   ├── pubspec.yaml
│   └── android/
│
├── admin_web/                      # React 管理后台
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                        # FastAPI 服务端
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── database.py
│   ├── requirements.txt
│   └── README.md
│
├── ai_service/                     # AI 高光识别服务
│   ├── subtitle_parser.py
│   ├── highlight_analyzer.py
│   ├── prompt_template.md
│   └── test_samples/
│
├── docs/                           # 飞书文档同步资料
│   ├── 技术方案.md
│   ├── 接口文档.md
│   ├── 数据库设计.md
│   ├── 排期计划.md
│   └── AI辅助说明.md
│
├── assets/
│   ├── demo_videos/
│   ├── demo_subtitles/
│   └── screenshots/
│
├── README.md
└── .gitignore
```

---

## 十六、GitHub 与 Git 分支管理

### 16.1 分支设计

| 分支名称 | 用途 |
|---|---|
| main | 最终稳定版本，只合并可展示成果 |
| dev | 日常开发集成分支 |
| feature/mobile-player | Flutter 播放端开发 |
| feature/mobile-interaction | 移动端互动组件和动效开发 |
| feature/backend-api | 后端 API 开发 |
| feature/ai-highlight | AI 高光识别服务开发 |
| feature/admin-web | Web 管理后台开发 |
| feature/analytics | 数据看板开发 |
| docs/feishu-tech-doc | 技术文档、接口文档、排期文档维护 |

### 16.2 开发流程

```text
1. 从 dev 创建 feature 分支；
2. 在 feature 分支完成具体功能；
3. 提交 commit；
4. 推送到 GitHub；
5. 发起 Pull Request；
6. 组员 Code Review；
7. 合并到 dev；
8. 阶段验收后合并到 main。
```

### 16.3 Commit 规范

```text
feat: 新增功能
fix: 修复问题
docs: 修改文档
style: 样式调整
refactor: 重构代码
test: 测试相关
chore: 工程配置调整
```

示例：

```text
feat: implement flutter video player page
feat: add highlight trigger engine
feat: add interaction log api
fix: resolve duplicate highlight trigger issue
docs: update delivery schedule and AI usage section
```

---

## 十七、工作项拆分与排期

### 17.1 三周开发排期

| 周期 | 阶段目标 | 主要任务 | 交付结果 |
|---|---|---|---|
| 第 1 周 | 完成基础架构和数据链路 | 搭建 GitHub 仓库、确定分支规范、初始化 Flutter 项目、初始化 FastAPI 项目、设计 MySQL 表、完成基础 API、准备测试视频和字幕 | 项目可运行，数据库可连接，Flutter 可进入播放页，后端可返回测试数据 |
| 第 2 周 | 跑通 AI 高光识别和移动端触发 | 完成字幕解析、LLM 高光识别、生成 JSON、写入高光表、Flutter 请求播放数据、监听播放时间、命中高光后展示互动按钮 | 可以从字幕生成高光点，Android 播放端能自动触发互动 |
| 第 3 周 | 完成闭环、优化演示和交付 | 完成互动日志回传、后台高光审核、基础数据看板、Android APK 打包、展示录屏、飞书文档完善、README 补充 | 完成 GitHub 项目、APK、录屏、飞书技术文档和最终答辩材料 |

### 17.2 详细工作项拆分

| 模块 | 工作项 | 优先级 | 负责人 |
|---|---|---|---|
| 项目管理 | 创建 GitHub 仓库、分支规范、README | P0 | 项目负责人 |
| Flutter 移动端 | 初始化 Flutter 项目 | P0 | 移动端 |
| Flutter 移动端 | 实现短剧播放页 | P0 | 移动端 |
| Flutter 移动端 | 实现视频播放时间监听 | P0 | 移动端 |
| Flutter 移动端 | 实现高光触发判断逻辑 | P0 | 移动端 |
| Flutter 移动端 | 实现互动按钮浮层 | P0 | 移动端 |
| Flutter 移动端 | 实现点击气泡和基础动效 | P1 | 移动端 |
| Flutter 移动端 | 实现互动日志回传 | P0 | 移动端 |
| 后端服务 | 搭建 FastAPI 项目结构 | P0 | 后端 |
| 后端服务 | 实现 drama / episode API | P0 | 后端 |
| 后端服务 | 实现 player 数据下发 API | P0 | 后端 |
| 后端服务 | 实现 interactions 日志回传 API | P0 | 后端 |
| 后端服务 | 实现 analytics 基础统计 API | P1 | 后端 |
| AI 服务 | 实现字幕解析 | P0 | AI / 后端 |
| AI 服务 | 设计高光识别 Prompt | P0 | AI / 后端 |
| AI 服务 | 输出结构化 highlights JSON | P0 | AI / 后端 |
| AI 服务 | 接入后端分析接口 | P0 | AI / 后端 |
| 管理后台 | 实现短剧/剧集列表 | P1 | Web |
| 管理后台 | 实现高光点审核和发布 | P1 | Web |
| 管理后台 | 实现基础数据看板 | P1 | Web |
| 文档 | 编写飞书技术文档 | P0 | 全员 |
| 文档 | 补充流程图、排期、AI辅助说明 | P0 | 项目负责人 |
| 交付 | Android APK 打包 | P0 | 移动端 |
| 交付 | 项目展示录屏 | P0 | 全员 |

### 17.3 三人组队分工建议

| 角色 | 负责内容 |
|---|---|
| 成员 A：移动端负责人 | Flutter Android App、视频播放、互动浮层、动效、日志回传 |
| 成员 B：后端 / AI 负责人 | FastAPI、MySQL、AI 高光识别、API、数据校验 |
| 成员 C：管理后台 / 文档负责人 | React 管理后台、数据看板、飞书文档、录屏脚本、README |

如果团队人数较少，优先级应调整为：

```text
Flutter 播放端 > 后端 API > AI 高光识别 > 高光审核后台 > 数据看板 > UI 美化
```

---

## 十八、开发优先级

### 18.1 P0 必须完成

```text
□ GitHub 仓库创建完成
□ 使用 Git 分支管理代码
□ Flutter Android 项目可运行
□ Android 播放页可播放短剧视频
□ 后端可返回 episode 播放数据
□ 后端可返回 highlights 高光点数据
□ Flutter 可监听视频播放时间
□ Flutter 可根据 start_time / end_time 自动触发互动浮层
□ 用户点击互动按钮后可回传日志
□ 后端可保存 user_interaction_log
□ AI 服务可基于字幕输出结构化高光 JSON
□ 管理后台可查看高光点
□ 飞书技术文档完整
□ 项目展示录屏完成
```

### 18.2 P1 尽量完成

```text
□ 管理后台支持编辑高光时间和类型
□ 管理后台支持发布 / 驳回高光点
□ Flutter 支持至少 2 种互动特效
□ 数据看板展示总互动次数
□ 数据看板展示高光类型分布
□ 数据看板展示热门互动按钮
□ Android APK 正常安装运行
```

### 18.3 P2 有时间再做

```text
□ WebSocket 实时群体反馈
□ 用户登录系统
□ 权限管理
□ 高光热力图
□ 多剧集连续播放
□ 更复杂的动效系统
□ OSS / COS 文件上传
□ AI 多模态视频画面理解
```

---

## 十九、错误处理与幂等性设计

### 19.1 API 异常分类

| 异常类型 | 原因 | HTTP 状态码 | 处理方案 |
|---|---|---|---|
| 参数验证失败 | 字段缺失、格式错误 | 400 | 返回错误提示，让客户端重新输入 |
| 资源不存在 | episode_id/highlight_id 不存在 | 404 | 返回 NOT_FOUND，前端引导用户操作 |
| 业务规则冲突 | 高光点重叠、状态冲突 | 409 | 返回详细冲突信息，让用户解决 |
| 权限不足 | 用户无编辑权限 | 403 | 返回权限拒绝，MVP 可暂不实现 |
| 服务依赖异常 | AI 调用失败、数据库连接错误 | 500 / 503 | 记录日志，返回统一错误，支持重试 |
| 请求过于频繁 | 短时间内大量请求 | 429 | 返回限流提示，建议客户端等待后重试 |

### 19.2 AI 分析接口错误处理

```text
场景 1：字幕不存在或无法读取
处理：检查文件是否存在，记录错误日志，返回 400，更新 analyze_status = failed。

场景 2：AI 服务调用超时或失败
处理：设置调用超时，失败后重试，记录错误日志，返回 503，更新 analyze_status = failed。

场景 3：AI 返回不合法 JSON
处理：捕获解析异常，保存原始响应，返回格式错误，更新 analyze_status = failed。

场景 4：高光点数据校验失败
处理：对每个高光点做校验，过滤不合法数据。如果全部不合法，则标记 failed。
```

### 19.3 幂等性设计

#### AI 分析接口幂等性

问题：管理员多次点击“开始识别”，可能生成重复高光点。

解决：

```text
1. 使用 episode_id 作为幂等性 key；
2. analyze_status = processing 时拒绝新请求；
3. analyze_status = success 且 force_reanalyze=false 时返回已有结果；
4. force_reanalyze=true 时，先清理旧高光点，再重新生成。
```

#### 用户互动日志幂等性

问题：用户点击后，前端可能重复发送相同日志。

解决：

```text
1. Flutter 端在互动组件展示时生成 impression 类型日志；
2. 用户点击后生成 click 类型日志；
3. 如果组件自动消失且用户未点击，生成 ignore 类型日志；
4. 每条日志都由 Flutter 端生成 idempotency_key；
5. 推荐规则：idempotency_key = md5(user_id + highlight_id + action_type + minute_timestamp)；
6. 后端对 idempotency_key 建立唯一索引或短时间唯一校验；
7. 如果收到重复 idempotency_key，直接返回 success，不重复写入。
```

数据库建议：

```sql
CREATE UNIQUE INDEX uk_interaction_idempotency
ON user_interaction_log(idempotency_key);
```

---

## 二十、安全与数据校验

### 20.0 用户标识与基础鉴权

#### 20.0.1 Flutter 匿名用户 ID 生成策略

MVP 阶段不强制实现完整登录系统，但必须保证同一台设备上的用户有稳定匿名 ID。

实现方式：

```text
1. App 首次启动时生成 UUID；
2. 将 UUID 保存到 SharedPreferences；
3. 后续每次启动 App 都读取同一个 UUID；
4. 请求互动日志接口时，将该 UUID 作为 user_id；
5. 如果本地 UUID 丢失，则重新生成。
```

示例：

```text
user_id = anonymous_ + uuid_v4
```

这样可以支持同一用户去重、互动统计和基础行为分析。

#### 20.0.2 管理后台基础鉴权

MVP 阶段可以不做完整登录注册，但管理后台接口不能完全裸露。建议使用简单的 `X-Admin-Token` 作为后台管理接口保护。

请求示例：

```http
X-Admin-Token: demo-admin-token
```

需要校验的接口包括：

```text
POST /api/dramas
POST /api/episodes
POST /api/episodes/{episode_id}/analyze
PUT /api/highlights/{highlight_id}
POST /api/episodes/{episode_id}/highlights/publish
GET /api/analytics/overview
```

Flutter 播放端只允许访问播放数据和互动上报接口，不应该直接访问后台管理接口。

### 20.1 播放端数据安全

播放端接口必须只返回：

```text
status = published
```

播放端不应看到：

```text
confidence
reason
status=draft 的高光
被驳回的高光
```

### 20.2 AI 返回结果校验

后端不能直接信任大模型输出，必须检查：

```text
1. 是否是合法 JSON；
2. highlight_type 是否在枚举范围内；
3. start_time 是否小于 end_time；
4. intensity/confidence 是否为 0 到 1；
5. buttons 是否为空；
6. effect 是否在允许范围内。
```

### 20.3 时间单位统一

全系统统一使用秒：

```text
start_time、end_time、watch_time 都使用秒，类型为 float。
```

---

## 二十一、本地开发启动说明

为了方便评审和团队成员运行项目，README.md 中必须包含本地启动步骤。建议按以下结构编写。

### 21.1 环境要求

```text
Flutter SDK 3.x
Dart 3.x
Android Studio / Android Emulator
Python 3.10+
MySQL 8.x
Node.js 18+
pnpm / npm
```

### 21.2 后端启动

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 21.3 数据库配置

`.env` 示例：

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/drama_interaction
ADMIN_TOKEN=demo-admin-token
STATIC_BASE_URL=http://localhost:8000/static
LLM_TIMEOUT_SECONDS=90
```

### 21.4 管理后台启动

```bash
cd admin_web
npm install
npm run dev
```

### 21.5 Flutter Android 启动

```bash
cd mobile_flutter
flutter pub get
flutter run
```

Flutter 端需要配置后端地址：

```dart
class Config {
  static const String baseUrl = "http://10.0.2.2:8000"; // Android 模拟器访问本机服务
}
```

如果使用真机调试，需要将 `baseUrl` 改为电脑局域网 IP。

---

## 二十二、项目展示录屏方案

建议录屏控制在 3 到 5 分钟。

### 22.1 录屏流程

```text
1. 展示 GitHub 项目结构；
2. 展示飞书技术文档目录；
3. 启动后端 FastAPI 服务；
4. 打开 Web 管理后台；
5. 创建短剧和剧集；
6. 上传或选择字幕文件；
7. 点击 AI 高光识别；
8. 展示识别出的高光点 JSON；
9. 在后台审核并发布高光点；
10. 打开 Android 模拟器或真机；
11. 进入 Flutter 短剧播放页；
12. 视频播放到高光时间点；
13. 互动按钮自动弹出；
14. 点击“反转了 / 太爽了 / 磕到了”；
15. 展示气泡或特效反馈；
16. 回到后台数据看板；
17. 展示互动日志和统计数据。
```

### 22.2 答辩表达重点

```text
我们不是简单做一个短剧播放器，而是通过 AI 识别剧情高光，在用户情绪峰值自动触发低门槛互动，并将互动数据回流到后台形成分析闭环。
```

---

## 二十三、最终交付物清单

| 交付物 | 内容 |
|---|---|
| GitHub 项目 | 包含 mobile_flutter、backend、ai_service、admin_web、docs |
| Android APK | Flutter 打包生成的 Android 安装包 |
| 项目展示录屏 | 展示从后台配置到移动端互动触发的完整流程 |
| 飞书技术文档 | 包含模块拆解、技术选型、流程图、排期、分工、AI辅助说明 |
| README.md | 项目介绍、启动方式、目录说明、演示流程 |
| 测试数据 | 示例短剧视频、字幕、高光 JSON、接口返回示例 |
| 最终产物截图 | 移动端播放页、互动触发、后台审核、数据看板截图 |

---

## 二十四、AI 辅助开发说明

本项目允许并鼓励使用 AI 辅助开发。团队在以下环节使用 AI 提升开发效率：

| 使用环节 | AI 辅助内容 | 人工处理方式 |
|---|---|---|
| 需求分析 | 辅助拆解短剧互动场景、用户角色和业务流程 | 团队根据项目要求筛选和调整 |
| 技术方案 | 辅助比较 Flutter、React Native、Web 等技术方案 | 最终选择 Flutter Android 优先 |
| 数据结构设计 | 辅助设计 drama、episode、highlight_event、interaction_log 等表结构 | 人工检查字段合理性和关联关系 |
| API 设计 | 辅助生成接口路径、请求体、响应体和错误码 | 后端成员根据实际实现调整 |
| AI 高光识别 | 辅助设计 Prompt、输出 JSON 格式、分类枚举 | 人工验证高光类型和时间点准确性 |
| Flutter 开发 | 辅助生成播放页、互动浮层、动画组件代码思路 | 移动端成员调试和修改 |
| 文档编写 | 辅助整理模块拆解、流程图、排期和答辩话术 | 团队人工确认最终内容 |
| 测试排查 | 辅助分析接口错误、字段不一致、触发逻辑异常 | 开发成员实际运行验证 |

### 24.1 AI 使用边界

```text
1. AI 生成内容不直接作为最终代码提交，必须经过人工审查；
2. 涉及数据库字段、接口格式、业务状态机的内容由团队统一确认；
3. AI 高光识别结果必须经过后台人工审核后才能发布到播放端；
4. 项目最终运行结果、录屏和答辩展示由团队自行验证。
```

---

## 二十五、项目总结

本项目最终选择 Flutter 作为跨平台移动端技术方案，并以 Android APK 作为主要前端展示产物。服务端采用 FastAPI + MySQL + Python AI 服务，形成以下完整闭环：

```text
AI 高光识别
→ 后台审核发布
→ 移动端即时互动
→ 用户行为回传
→ 数据看板分析
```

项目的核心亮点在于：

1. 将 AI 内容理解能力用于短剧高光识别；
2. 将传统评论/弹幕式互动升级为低门槛即时互动；
3. 使用 Flutter 实现 Android 播放端互动触发；
4. 通过 FastAPI 和 MySQL 构建稳定的数据闭环；
5. 通过 GitHub 分支管理、飞书文档和录屏满足完整交付要求。

最终交付重点不是做一个复杂的视频平台，而是完整证明：

> 系统可以理解剧情高光，在正确的时间点触发正确的互动，并把用户反馈沉淀为可分析的数据。

