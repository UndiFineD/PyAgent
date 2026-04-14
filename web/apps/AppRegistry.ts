/**
 * AppRegistry — central registry for all NebulaOS applications.
 *
 * To add a new app:
 *  1. Create web/apps/YourApp.tsx and export `appMeta: AppMeta` from it.
 *  2. Import the component + appMeta here and add one entry to APP_REGISTRY.
 *
 * No changes needed anywhere else — the hamburger menu builds itself from
 * this registry, grouped by `category` in the order defined by CATEGORY_ORDER.
 */
import React from 'react';
import {
  Calculator as LucideCalculator,
  FileText,
  Palette,
  Monitor,
  Bot,
  LayoutDashboard,
  Database,
  MessageSquare,
  Activity,
  GitFork,
  Package,
} from 'lucide-react';

import type { AppMeta } from '../types';

// ── App component + appMeta imports ─────────────────────────────────────────
import { Calculator,        appMeta as calculatorMeta        } from './Calculator';
import { Editor,            appMeta as editorMeta            } from './Editor';
import { Paint,             appMeta as paintMeta             } from './Paint';
import { Conky,             appMeta as conkyMeta             } from './Conky';
import { CodeBuilder,       appMeta as codebuilderMeta       } from './CodeBuilder';
import { ProjectManager,    appMeta as projectmanagerMeta    } from './ProjectManager';
import AutoMemBenchmark,  { appMeta as autobenchmarkMeta     } from './AutoMemBenchmark';
import { AgentChat,         appMeta as agentchatMeta         } from './AgentChat';
import { FLMDashboard,      appMeta as flmdashboardMeta      } from './FLMDashboard';
import { OrchestrationGraph, appMeta as orchestrationgraphMeta } from './OrchestrationGraph';
import { PluginMarketplace, appMeta as pluginmarketplaceMeta } from './PluginMarketplace';

// ── AppEntry ─────────────────────────────────────────────────────────────────

export interface AppEntry extends AppMeta {
  Component: React.ComponentType;
  Icon: React.FC<{ size?: number; className?: string }>;
  iconColor: string;
  width: number;
  height: number;
  hasMenu: boolean;
}

// ── Registry ─────────────────────────────────────────────────────────────────

export const APP_REGISTRY: Record<string, AppEntry> = {
  // ── AI Agents ──────────────────────────────────────────────────────────────
  [agentchatMeta.id]: {
    ...agentchatMeta,
    Component: AgentChat,
    Icon: MessageSquare,
    iconColor: 'text-violet-400',
    width: 900,
    height: 650,
    hasMenu: false,
  },
  [codebuilderMeta.id]: {
    ...codebuilderMeta,
    Component: CodeBuilder,
    Icon: Bot,
    iconColor: 'text-purple-400',
    width: 900,
    height: 600,
    hasMenu: true,
  },
  [orchestrationgraphMeta.id]: {
    ...orchestrationgraphMeta,
    Component: OrchestrationGraph,
    Icon: GitFork,
    iconColor: 'text-amber-400',
    width: 900,
    height: 600,
    hasMenu: false,
  },
  [autobenchmarkMeta.id]: {
    ...autobenchmarkMeta,
    Component: AutoMemBenchmark,
    Icon: Database,
    iconColor: 'text-cyan-400',
    width: 1100,
    height: 700,
    hasMenu: false,
  },
  [projectmanagerMeta.id]: {
    ...projectmanagerMeta,
    Component: ProjectManager,
    Icon: LayoutDashboard,
    iconColor: 'text-indigo-400',
    width: 1100,
    height: 650,
    hasMenu: false,
  },

  // ── System ─────────────────────────────────────────────────────────────────
  [conkyMeta.id]: {
    ...conkyMeta,
    Component: Conky,
    Icon: Monitor,
    iconColor: 'text-green-400',
    width: 300,
    height: 500,
    hasMenu: false,
  },
  [flmdashboardMeta.id]: {
    ...flmdashboardMeta,
    Component: FLMDashboard,
    Icon: Activity,
    iconColor: 'text-emerald-400',
    width: 900,
    height: 600,
    hasMenu: false,
  },
  [pluginmarketplaceMeta.id]: {
    ...pluginmarketplaceMeta,
    Component: PluginMarketplace,
    Icon: Package,
    iconColor: 'text-teal-400',
    width: 800,
    height: 600,
    hasMenu: false,
  },

  // ── Utilities ──────────────────────────────────────────────────────────────
  [calculatorMeta.id]: {
    ...calculatorMeta,
    Component: Calculator,
    Icon: LucideCalculator,
    iconColor: 'text-orange-400',
    width: 320,
    height: 450,
    hasMenu: false,
  },
  [editorMeta.id]: {
    ...editorMeta,
    Component: Editor,
    Icon: FileText,
    iconColor: 'text-blue-400',
    width: 600,
    height: 400,
    hasMenu: true,
  },
  [paintMeta.id]: {
    ...paintMeta,
    Component: Paint,
    Icon: Palette,
    iconColor: 'text-pink-400',
    width: 800,
    height: 600,
    hasMenu: true,
  },
};

/** Ordered categories for the hamburger menu */
export const CATEGORY_ORDER: string[] = ['AI Agents', 'System', 'Utilities'];
