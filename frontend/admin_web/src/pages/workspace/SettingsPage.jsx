import { getWorkspaceModuleById } from '../../workspaceModules.jsx';
import WorkspacePlaceholderPage from './WorkspacePlaceholderPage.jsx';

export default function SettingsPage() {
  return <WorkspacePlaceholderPage module={getWorkspaceModuleById('settings')} />;
}
