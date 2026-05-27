import {
  BarChartOutlined,
  ExperimentOutlined,
  FileTextOutlined,
  FieldTimeOutlined,
  PlaySquareOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';

export const workspaceModules = [
  {
    id: 'dashboard',
    path: '/workspace/dashboard',
    title: '仪表盘',
    eyebrow: 'DASHBOARD',
    description: '汇总短剧、剧集、高光和互动数据，快速查看系统核心指标。',
    icon: <BarChartOutlined />,
    roles: ['admin'],
    status: '待接 API',
  },
  {
    id: 'dramas',
    path: '/workspace/dramas',
    title: '短剧管理',
    eyebrow: 'DRAMAS',
    description: '创建短剧，作为后续剧集、字幕和高光审核的内容容器。',
    icon: <VideoCameraOutlined />,
    roles: ['admin'],
    status: '待接 API',
  },
  {
    id: 'episodes',
    path: '/workspace/episodes',
    title: '剧集配置',
    eyebrow: 'EPISODES',
    description: '维护视频 URL、字幕 URL 或字幕正文，为 AI 分析提供输入。',
    icon: <PlaySquareOutlined />,
    roles: ['admin', 'uploader'],
    status: '待接 API',
  },
  {
    id: 'analyze',
    path: '/workspace/analyze',
    title: 'AI 高光识别',
    eyebrow: 'ANALYZE',
    description: '触发后端分析任务，将字幕转化为 draft 高光事件。',
    icon: <ExperimentOutlined />,
    roles: ['admin', 'uploader'],
    status: '待接 API',
  },
  {
    id: 'highlights',
    path: '/workspace/highlights',
    title: '高光审核发布',
    eyebrow: 'REVIEW',
    description: '查看、编辑、发布或驳回高光，守住播放端下发质量。',
    icon: <FileTextOutlined />,
    roles: ['admin'],
    status: '待接 API',
  },
  {
    id: 'jobs',
    path: '/workspace/jobs',
    title: '后台任务',
    eyebrow: 'JOBS',
    description: '提交 AI 分析等耗时任务，查看 RQ 队列执行状态与任务日志。',
    icon: <FieldTimeOutlined />,
    roles: ['admin', 'uploader'],
    status: 'RQ',
  }
];

export function canAccessWorkspaceModule(module, role) {
  return module.roles.includes(role);
}

export function getWorkspaceModulesForRole(role) {
  return workspaceModules.filter((module) => canAccessWorkspaceModule(module, role));
}

export function getDefaultWorkspacePath(role) {
  return getWorkspaceModulesForRole(role)[0]?.path ?? '/login';
}

export function getWorkspaceModuleById(id) {
  return workspaceModules.find((module) => module.id === id) ?? workspaceModules[0];
}

export function getWorkspaceModuleByPath(pathname) {
  return (
    workspaceModules.find((module) => pathname.startsWith(module.path)) ??
    workspaceModules[0]
  );
}
