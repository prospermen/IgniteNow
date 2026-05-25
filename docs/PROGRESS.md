# 项目进度 (移动端聚焦)

## 2026-05-23
### 当前目标
实现移动端抖音风格的垂直视频流，包含内存池管理逻辑和基础社交交互 UI。

### 已完成
- **核心垂直视频流实现** (`mobile/lib/`):
    - `video_model.dart`: 定义了基础视频数据模型。
    - `video_pool_manager.dart`: 实现了滑动窗口内存管理，确保仅保留 3 个活跃控制器以防 OOM。
    - `video_feed_view.dart`: 使用 `PageView.builder` 实现了垂直物理滑动。
- **TikTok UI 界面完善**:
    - `video_widgets.dart`: 实现了顶部导航、右侧操作栏（点赞、评论等）、底部信息栏及底部导航栏。
    - 在 `VideoFeedView` 中成功整合了所有 UI 覆盖层。
- **分支规范调整**:
    - 已根据《原始开发文档 v1.1》第 16 节，从 `jenny` 切换至 `dev`，并创建了 `feature/mobile-interaction` 分支进行开发。

### 正在进行
- [ ] 升级 `VideoItem` 支持动态交互状态 (`isLiked`, `isBookmarked`, `isFollowing`)。
- [ ] 创建 `video_api_service.dart` 作为前端与后端的 API 抽象层。
- [ ] 将 UI 按钮点击事件绑定至服务层，并实现“乐观 UI”更新逻辑。

### 验证结果
- **内存安全**: 验证了滑出窗口的控制器会被正确执行 `dispose()`。
- **代码规范**: 严格遵循英文注释与命名规范，代码中无中文字符。
- **UI 整合**: 垂直滑动与覆盖层显示正常。

### 遗留风险
- 模拟视频 URL 依赖外部网络，网络不稳定可能导致播放失败。
- 尚未实现加载超时或网络错误的 UI 反馈逻辑。
