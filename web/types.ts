import { ReactNode } from 'react';

export type AppId = 'calculator' | 'editor' | 'paint' | 'conky' | 'settings' | 'codebuilder' | 'projectmanager';

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
