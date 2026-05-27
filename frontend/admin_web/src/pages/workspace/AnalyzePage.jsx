import { getWorkspaceModuleById } from '../../workspaceModules.jsx';
import WorkspacePlaceholderPage from './WorkspacePlaceholderPage.jsx';

export default function AnalyzePage() {
  return <WorkspacePlaceholderPage module={getWorkspaceModuleById('analyze')} />;
}
