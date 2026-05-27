import { getWorkspaceModuleById } from '../../workspaceModules.jsx';
import WorkspacePlaceholderPage from './WorkspacePlaceholderPage.jsx';

export default function DramasPage() {
  return <WorkspacePlaceholderPage module={getWorkspaceModuleById('dramas')} />;
}
