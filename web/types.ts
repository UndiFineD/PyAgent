import { ReactNode } from 'react';

/** Unique kebab-case app identifier. Add new apps to AppRegistry.ts — no change needed here. */
export type AppId = string;

/** Minimal metadata every app must export as `appMeta`. */
export interface AppMeta {
  /** Kebab-case identifier — must match the key in APP_REGISTRY */
  id: string;
  /** Human-readable title shown in the window title bar and menu */
  title: string;
  /** Menu category used to group entries in the hamburger menu */
  category: string;
}

export interface WindowState {
  id: string;
  appId: AppId;
  title: string;
  component: ReactNode;
  x: number;
  y: number;
  width: number;
  height: number;
  zIndex: number;
  isMinimized: boolean;
  isMaximized: boolean;
  hasMenu?: boolean;
}

export interface Theme {
  id: 'dark' | 'light' | 'retro';
  name: string;
}

export interface User {
  name: string;
  email: string;
  avatar: string;
}

export interface OsConfig {
  taskbarAlwaysVisible: boolean;
}

export const DEFAULT_OS_CONFIG: OsConfig = {
  taskbarAlwaysVisible: false,
};
