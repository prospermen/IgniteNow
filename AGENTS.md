# Agent 操作手册

本文件约束所有 AI Agent 在本仓库中的工作方式。先理解系统，再规划任务，最后做小而可验证的改动。

## 0. 项目定位

IgniteNow 是一个大型全栈 MVP 系统：

```text
字幕/视频配置
→ AI 高光识别
→ 后端入库与审核发布
→ Flutter Android 播放端时间轴触发互动
→ 用户行为回传
→ 管理后台数据看板
```

本项目不是单点 Demo。任何改动都必须考虑端到端链路、API 契约、数据模型、状态机和演示可验收性。

## 1. 工作前必须读取

在修改代码、配置、数据库或接口前，必须先读取：

- `docs/PROGRESS.md`
- `docs/DECISIONS.md`
- `docs/API_CONTRACT.md`
- `docs/HIGHLIGHT_SCHEMA.json`
- `docs/TASK_BREAKDOWN.md`

根据任务范围再读取相关模块代码和文档。小型纯文档修改不需要强行读取无关模块源码。

## 2. Harness Engineering 原则

### 2.0 标准工作流

1. 先确认任务目标、影响模块和验收标准。
2. 搜索现有实现、组件、接口和文档约定。
3. 给出最小改动方案，必要时拆成可并行或可分阶段的任务。
4. 实施改动，并保持模块边界清晰。
5. 运行与改动范围匹配的验证。
6. 只更新受影响的文档，最后说明改动、验证和风险。

### 2.1 明确上下文

- 不凭记忆猜接口字段、状态值、目录结构或启动命令。
- 对跨端字段，必须以 `docs/API_CONTRACT.md` 和 `docs/HIGHLIGHT_SCHEMA.json` 为准。

### 2.2 小步可验证

- 每次改动应有清晰目标、有限范围和可验证结果。
- 不一次性重写多个模块，除非任务明确要求并且已拆分验收点。
- 每个功能至少提供一种验证方式：单元测试、接口请求、页面运行、Flutter 运行、SQL 校验或手工验收步骤。
- 验证范围应与风险匹配：小改动做局部验证，跨模块改动做链路验证。

### 2.3 契约优先

- 修改 API、数据库字段、高光 JSON、状态机、枚举值前，必须先更新或同步以下文档：
  - `docs/API_CONTRACT.md`
  - `docs/HIGHLIGHT_SCHEMA.json`
  - `docs/DECISIONS.md`
- 后端、管理后台、Flutter、AI 服务之间不得出现未记录的隐式字段。
- 播放端接口只能返回已发布高光，不得暴露后台审核字段，例如 `reason`、`confidence`、`status=draft`。

### 2.4 可恢复与可追踪

- 任务进度、验证结果、遗留问题和技术取舍必须记录到对应文档。
- 不删除用户已有改动，不执行破坏性 git 或文件操作，除非用户明确要求。
- 遇到不确定的业务规则，先查文档；仍不确定时做保守假设，并记录在文档中。

## 3. 模块边界

| 模块 | 目录 | 主要职责 |
|---|---|---|
| 后端服务 | `backend/` | FastAPI、业务规则、数据访问、AI 调度、统计聚合 |
| AI 服务 | `ai_service/` | 字幕解析、Prompt、LLM/规则识别、高光 JSON 输出 |
| 管理后台 | `frontend/admin_web/` | 短剧/剧集管理、高光审核发布、数据看板 |
| Flutter 播放端 | `flutter/` | 播放器、时间轴监听、互动浮层、动效、日志回传 |
| 数据库 | `datebase/` | 建表 SQL、索引、初始化数据、迁移脚本 |
| 文档 | `docs/` | API 契约、任务拆解、进度、技术决策、交付说明 |
| 素材 | `assets/` | 示例视频、字幕、截图、演示素材 |

跨模块改动必须说明影响范围，并保持接口、字段、状态一致。

## 4. 代码复用与系统 Review

### 4.1 复用优先

- 写新代码前，先搜索是否已有相同职责的 service、model、schema、component、hook、widget、client、utility 或 SQL 片段。
- 优先复用和扩展已有代码，不重复实现同类逻辑。
- 新增抽象必须有明确收益：减少真实重复、统一跨端契约、降低复杂度或贴合已有架构。
- 同一业务规则只能有一个主要实现位置；其他模块通过调用、组合或共享契约使用它。

### 4.2 定期系统 Review

- 每完成一个阶段性任务后，应从系统角度 review 当前实现是否存在：
  - 重复代码或重复组件
  - 前后端字段不一致
  - 数据模型与 API 契约不一致
  - 业务逻辑散落在多个地方
  - 过早抽象或过度工程化
- 发现问题时，优先记录到 `docs/PROGRESS.md` 或 `docs/DECISIONS.md`；如果影响当前任务验收，应在本次任务内修正。
- Review 的目标是让系统更清晰、更可验证，而不是做无关重构。

## 5. 后端工程规则

- 使用 FastAPI + SQLAlchemy。
- API 路径、请求体、响应体必须写入 `docs/API_CONTRACT.md`。
- 管理后台写接口必须校验 `X-Admin-Token`。
- 播放端接口仅返回移动端必要字段。
- 互动日志必须支持幂等写入，使用 `idempotency_key`。
- AI 分析接口必须处理：
  - 字幕不存在
  - AI 调用失败
  - 非法 JSON
  - 非法高光类型
  - 时间范围错误
  - 重复分析
- 状态机必须遵循：
  - `episode.analyze_status`: `pending`、`processing`、`success`、`failed`
  - `highlight_event.status`: `draft`、`published`、`rejected`、`archived`

## 6. AI 服务规则

- AI 输出必须符合 `docs/HIGHLIGHT_SCHEMA.json`。
- 时间单位统一为秒，类型为 number/float。
- 不允许后端直接信任 LLM 输出，必须做结构和业务校验。
- 必须提供无 LLM Key 时可运行的 fallback 方案，保证演示链路可用。

## 7. Flutter 播放端规则

- 网络请求使用统一 API client。
- 首次启动生成匿名 `user_id`，后续持久化复用。
- 高光触发必须避免重复触发。
- 用户行为至少支持：
  - `impression`
  - `click`
  - `ignore`
- 回传日志必须携带 `idempotency_key`。

## 8. 管理后台规则

- 使用 React + Vite + Ant Design。
- 后台接口统一通过 API client 调用，并自动携带 `X-Admin-Token`。

## 9. 数据库规则

- 建表、索引、初始数据放在 `datebase/`。
- 表结构变化必须同步：
  - SQL 文件
  - SQLAlchemy model
  - API schema
  - `docs/API_CONTRACT.md`
- 核心表至少包括：
  - `drama`
  - `episode`
  - `highlight_event`
  - `interaction_template`
  - `user_interaction_log`
- `user_interaction_log.idempotency_key` 必须唯一。

## 10. 文档维护规则

每次任务结束前，只根据实际影响更新相关文档：

- `docs/PROGRESS.md`: 做了什么、如何验证、剩余问题。
- `docs/DECISIONS.md`: 新增或改变的技术决策。
- `docs/API_CONTRACT.md`: API 或字段变化。
- `docs/HIGHLIGHT_SCHEMA.json`: 高光 JSON 结构变化。
- `README.md`: 启动方式或目录说明变化。

文档必须反映实际代码，不写无法运行的理想状态。
如果本次改动不影响某份文档，不要为了“完成流程”制造无意义更新。

## 11. 禁止事项

- 禁止绕过文档直接发明跨端字段。
- 禁止在未更新 API 契约的情况下修改接口响应。
- 禁止大范围重构与当前任务无关的代码。
- 禁止删除或回滚用户已有改动，除非用户明确要求。
- 禁止提交密钥、Token、真实用户数据或不可公开素材。

## 12. 完成定义

一个任务只有同时满足以下条件，才算完成：

1. 代码或文档已按范围修改。
2. 相关契约、状态或决策文档已同步。
3. 至少执行了一种合理验证，或明确说明无法验证的原因。
4. 最终回复说明：
   - 改了哪些文件
   - 如何验证
   - 是否有遗留风险
