import { getWorkspaceModuleById } from '../../workspaceModules.jsx';
import WorkspacePlaceholderPage from './WorkspacePlaceholderPage.jsx';

export default function EpisodesPage() {
  return <WorkspacePlaceholderPage module={getWorkspaceModuleById('episodes')} />;
}
