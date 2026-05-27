export const ADMIN_ACCESS_TOKEN_KEY = 'ignitenow_admin_access_token';
export const ADMIN_USER_NAME_KEY = 'ignitenow_admin_user_name';
export const ADMIN_USER_ROLE_KEY = 'ignitenow_admin_user_role';

export function hasAdminAccessToken() {
  return Boolean(window.localStorage.getItem(ADMIN_ACCESS_TOKEN_KEY));
}

export function getAdminAccessToken() {
  return window.localStorage.getItem(ADMIN_ACCESS_TOKEN_KEY);
}

export function saveAdminAccessToken(token) {
  window.localStorage.setItem(ADMIN_ACCESS_TOKEN_KEY, token);
}

export function saveAdminUserName(userName) {
  window.localStorage.setItem(ADMIN_USER_NAME_KEY, userName);
}

export function saveAdminUserRole(role) {
  window.localStorage.setItem(ADMIN_USER_ROLE_KEY, role);
}

export function saveAdminSession(session) {
  saveAdminAccessToken(session.accessToken);
  saveAdminUserName(session.username);
  saveAdminUserRole(session.role);
}

export function getAdminUserName() {
  return window.localStorage.getItem(ADMIN_USER_NAME_KEY) || 'admin';
}

export function getAdminUserRole() {
  return window.localStorage.getItem(ADMIN_USER_ROLE_KEY) || '';
}

export function clearAdminSession() {
  window.localStorage.removeItem(ADMIN_ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(ADMIN_USER_NAME_KEY);
  window.localStorage.removeItem(ADMIN_USER_ROLE_KEY);
}
