import { getWorkspaceModuleById } from '../../workspaceModules.jsx';
import WorkspacePlaceholderPage from './WorkspacePlaceholderPage.jsx';

export default function HighlightsPage() {
  return <WorkspacePlaceholderPage module={getWorkspaceModuleById('highlights')} />;
}
