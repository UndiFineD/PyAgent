// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * Tests for prj0000048 – Taskbar Config (Settings modal + osConfig persistence).
 *
 * These tests are intentionally written BEFORE @6code implements the feature.
 * They WILL FAIL until:
 *   - web/types.ts exports OsConfig and DEFAULT_OS_CONFIG (Task 1)
 *   - web/App.tsx implements Tasks 2–10 from the plan
 *
 * Test runner: Vitest 4.x (jsdom environment, globals: true)
 * DOM helpers: @testing-library/react v16 + @testing-library/user-event v14
 *
 * Login bypass strategy
 * ---------------------
 * The real Login component calls onLogin() after a 1500 ms fake-OAuth delay.
 * Waiting for that delay with vi.useFakeTimers() causes act(async)/userEvent
 * interactions to deadlock. We therefore vi.mock() Login to expose an
 * instant-fire button so all test suites start their scenario immediately
 * after a single click.
 */

// vi.mock is hoisted by Vitest before any import is resolved.
// The factory runs lazily the first time the mocked module is needed.
import { vi } from 'vitest';
vi.mock('./components/Login', () => ({
  // Instant-login stub: calls onLogin() synchronously when clicked
  Login: ({ onLogin }: { onLogin: () => void }) => (
    <button onClick={onLogin}>Mock Login</button>
  ),
}));

import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

// ── Intentionally failing imports until @6code ships Task 1 ──────────────────
// DEFAULT_OS_CONFIG evaluates to `undefined` until Task 1 ships.
// Suite 1 below asserts it via toBeDefined() which will fail cleanly.
import { DEFAULT_OS_CONFIG } from './types';
import App from './App';

// ─────────────────────────────────────────────────────────────────────────────
// Shared test helpers
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Render <App />, click the instant-fire Mock Login button, and return
 * a userEvent instance + container.
 *
 * delay:null disables userEvent's internal pointer delays so user.click()
 * resolves synchronously even when vi.useFakeTimers() is active.
 */
async function renderLoggedIn() {
  const user = userEvent.setup({ delay: null });
  const { container } = render(<App />);

  // Mock Login fires onLogin() synchronously on click – no setTimeout, no timers.
  await user.click(screen.getByRole('button', { name: 'Mock Login' }));

  // App is now in logged-in state.
  expect(screen.queryByText('NebulaOS')).not.toBeNull();

  return { user, container };
}

/**
 * Open the hamburger dropdown menu.
 * Uses class `.h-12` to target the 48px taskbar, not the 8px trigger zone
 * (both have `fixed top-0` but only the real taskbar has `h-12`).
 */
async function openDropdown(
  user: ReturnType<typeof userEvent.setup>,
  container: HTMLElement,
) {
  const taskbarEl = container.querySelector('.fixed.h-12');
  if (!taskbarEl) throw new Error('Taskbar (h-12) element not found');

  const menuBtn = taskbarEl.querySelector('.relative > button') as HTMLButtonElement | null;
  if (!menuBtn) throw new Error('Hamburger menu trigger button not found inside taskbar');

  await user.click(menuBtn);
}

/**
 * Open the dropdown and then click the "Settings" button to show the modal.
 */
async function openSettingsModal(
  user: ReturnType<typeof userEvent.setup>,
  container: HTMLElement,
) {
  await openDropdown(user, container);
  const settingsBtn = screen.getByRole('button', { name: /^settings$/i });
  await user.click(settingsBtn);
}

// ─────────────────────────────────────────────────────────────────────────────
// Suite 1 – Type contract: OsConfig + DEFAULT_OS_CONFIG
// ─────────────────────────────────────────────────────────────────────────────
// These are pure runtime checks.  The import at the top of this file already
// fails before these tests even run if DEFAULT_OS_CONFIG is not exported.

describe('prj0000048 – types: OsConfig and DEFAULT_OS_CONFIG (Task 1)', () => {
  it('DEFAULT_OS_CONFIG is exported from ./types', () => {
    expect(DEFAULT_OS_CONFIG).toBeDefined();
  });

  it('DEFAULT_OS_CONFIG.taskbarAlwaysVisible defaults to false', () => {
    expect(DEFAULT_OS_CONFIG.taskbarAlwaysVisible).toBe(false);
  });

  it('DEFAULT_OS_CONFIG has the full OsConfig shape (only expected keys)', () => {
    expect(typeof DEFAULT_OS_CONFIG.taskbarAlwaysVisible).toBe('boolean');
    expect(Object.keys(DEFAULT_OS_CONFIG)).toContain('taskbarAlwaysVisible');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Suite 2 – Hamburger dropdown contains a Settings button (Task 8)
// ─────────────────────────────────────────────────────────────────────────────

describe('prj0000048 – App: Settings button in hamburger dropdown (Task 8)', () => {
  beforeEach(() => { localStorage.clear(); });

  it('opening the dropdown reveals a "Settings" button', async () => {
    const { user, container } = await renderLoggedIn();
    await openDropdown(user, container);

    const btn = screen.queryByRole('button', { name: /^settings$/i });
    expect(btn).not.toBeNull();
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Suite 3 – Settings modal behaviour (Task 9)
// ─────────────────────────────────────────────────────────────────────────────

describe('prj0000048 – App: Settings modal (Task 9)', () => {
  beforeEach(() => { localStorage.clear(); });

  it('clicking Settings opens modal with "Always show taskbar" label', async () => {
    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    expect(screen.queryByText(/always show taskbar/i)).not.toBeNull();
  });

  it('Settings modal has a role="switch" toggle defaulting to aria-checked="false"', async () => {
    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    const toggle = screen.getByRole('switch');
    expect(toggle).not.toBeNull();
    expect(toggle.getAttribute('aria-checked')).toBe('false');
  });

  it('toggling the switch flips aria-checked to "true"', async () => {
    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    const toggle = screen.getByRole('switch');
    await user.click(toggle);

    expect(toggle.getAttribute('aria-checked')).toBe('true');
  });

  it('toggling persists taskbarAlwaysVisible=true to localStorage key "nebula-os-config"', async () => {
    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    await user.click(screen.getByRole('switch'));

    const raw = localStorage.getItem('nebula-os-config');
    expect(raw).not.toBeNull();
    const parsed = JSON.parse(raw!);
    expect(parsed.taskbarAlwaysVisible).toBe(true);
  });

  it('Settings modal loads stored value: toggle starts aria-checked="true" when stored', async () => {
    localStorage.setItem('nebula-os-config', JSON.stringify({ taskbarAlwaysVisible: true }));

    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    const toggle = screen.getByRole('switch');
    expect(toggle.getAttribute('aria-checked')).toBe('true');
  });

  it('modal closes when its backdrop is clicked', async () => {
    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    // The backdrop is a div.fixed.inset-0[class*="z-[60]"] rendered when settingsOpen is true.
    // CSS attribute substring selectors treat the value as a literal string, so the
    // square brackets inside the quotes are NOT parsed as CSS selector syntax – this is valid.
    const backdrop = container.querySelector('[class*="z-[60]"]') as HTMLElement | null;
    expect(backdrop).not.toBeNull();
    await user.click(backdrop!);

    await waitFor(() => {
      expect(screen.queryByText(/always show taskbar/i)).toBeNull();
    });
  });

  it('modal closes when the X button is clicked', async () => {
    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    // The modal panel has class bg-os-window rounded-xl; the close button is its first <button>
    const modalPanel = container.querySelector('.rounded-xl.shadow-2xl') as HTMLElement | null;
    expect(modalPanel).not.toBeNull();
    const closeBtn = modalPanel!.querySelector('button') as HTMLButtonElement | null;
    expect(closeBtn).not.toBeNull();
    await user.click(closeBtn!);

    await waitFor(() => {
      expect(screen.queryByText(/always show taskbar/i)).toBeNull();
    });
  });

  it('modal closes on Escape key press (Task 10)', async () => {
    const { user, container } = await renderLoggedIn();
    await openSettingsModal(user, container);

    await user.keyboard('{Escape}');

    await waitFor(() => {
      expect(screen.queryByText(/always show taskbar/i)).toBeNull();
    });
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Suite 4 – taskbarAlwaysVisible guard in hideTaskbar (Task 7)
//
// Uses vi.useFakeTimers() to control the 2000 ms hide timeout without waiting.
// Uses synchronous fireEvent (not async userEvent) for mouse events to avoid
// the userEvent/act/fake-timer deadlock under vi.useFakeTimers().
// ─────────────────────────────────────────────────────────────────────────────

import { fireEvent } from '@testing-library/react';

describe('prj0000048 – App: taskbarAlwaysVisible guard in hideTaskbar (Task 7)', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    localStorage.clear();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('taskbar stays visible after mouse-leave when taskbarAlwaysVisible=true', () => {
    localStorage.setItem('nebula-os-config', JSON.stringify({ taskbarAlwaysVisible: true }));

    const { container } = render(<App />);
    // Synchronous login via fireEvent (no async issues with fake timers)
    act(() => { fireEvent.click(screen.getByRole('button', { name: 'Mock Login' })); });

    // The 48px taskbar (not the 8px trigger zone)
    const taskbar = container.querySelector('.fixed.h-12') as HTMLElement;
    expect(taskbar).not.toBeNull();

    // Show taskbar then trigger hide
    act(() => { fireEvent.mouseEnter(taskbar); });
    act(() => { fireEvent.mouseLeave(taskbar); });
    // Guard: taskbarAlwaysVisible=true → hideTaskbar() returns early
    act(() => { vi.advanceTimersByTime(3000); });

    expect(taskbar.className).not.toContain('-translate-y-full');
  });

  it('taskbar auto-hides after mouse-leave when taskbarAlwaysVisible=false', () => {
    localStorage.setItem('nebula-os-config', JSON.stringify({ taskbarAlwaysVisible: false }));

    const { container } = render(<App />);
    act(() => { fireEvent.click(screen.getByRole('button', { name: 'Mock Login' })); });

    const taskbar = container.querySelector('.fixed.h-12') as HTMLElement;
    expect(taskbar).not.toBeNull();

    // Show then trigger hide
    act(() => { fireEvent.mouseEnter(taskbar); });
    act(() => { fireEvent.mouseLeave(taskbar); });
    act(() => { vi.advanceTimersByTime(3000); }); // past 2000 ms delay

    // Taskbar should now be hidden
    expect(taskbar.className).toContain('-translate-y-full');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Suite 5 – osConfig persistence useEffect writes to localStorage (Task 6)
// ─────────────────────────────────────────────────────────────────────────────

describe('prj0000048 – App: osConfig persistence useEffect (Task 6)', () => {
  beforeEach(() => { localStorage.clear(); });

  it('"nebula-os-config" key is written to localStorage on App mount', async () => {
    await renderLoggedIn();
    // The saveOsConfig effect fires once on mount with the loaded (default) value
    expect(localStorage.getItem('nebula-os-config')).not.toBeNull();
  });

  it('stored value is valid JSON with taskbarAlwaysVisible field', async () => {
    await renderLoggedIn();
    const raw = localStorage.getItem('nebula-os-config');
    expect(raw).not.toBeNull();
    const parsed = JSON.parse(raw!);
    expect(typeof parsed.taskbarAlwaysVisible).toBe('boolean');
  });
});
