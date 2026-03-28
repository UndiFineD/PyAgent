import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ProjectManager } from './ProjectManager';

// Copy of extractSection for unit testing — or import if exported
function extractSection(raw: string, heading: string): string {
  const start = raw.indexOf(`## ${heading}`);
  if (start === -1) return `Section "${heading}" not found.`;
  const after = raw.indexOf('\n## ', start + 1);
  return after === -1 ? raw.slice(start) : raw.slice(start, after);
}

describe('extractSection', () => {
  const sample = '# Doc\n\n## Alpha\nAlpha content\n\n## Beta\nBeta content\n\n## Gamma\nGamma';

  it('extracts a mid-document section', () => {
    const result = extractSection(sample, 'Alpha');
    expect(result).toContain('Alpha content');
    expect(result).not.toContain('Beta content');
  });

  it('extracts the last section', () => {
    const result = extractSection(sample, 'Gamma');
    expect(result).toContain('Gamma');
    expect(result).toContain('## Gamma');
  });

  it('returns not-found message for missing heading', () => {
    expect(extractSection(sample, 'Missing')).toContain('not found');
  });
});

describe('ProjectManager ideas panel', () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it('renders active ideas queue rows from /api/ideas', async () => {
    globalThis.fetch = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/api/projects')) {
        return {
          ok: true,
          json: async () => ([
            {
              id: 'prj0000093',
              name: 'Ideas Autosync',
              lane: 'In Sprint',
              summary: 'Frontend panel integration',
              branch: 'prj0000093-projectmanager-ideas-autosync',
              pr: null,
              priority: 'P2',
              budget_tier: 'S',
              tags: ['ideas'],
              created: '2026-03-28',
              updated: '2026-03-28',
            },
          ]),
        } as Response;
      }
      if (url.includes('/api/ideas')) {
        return {
          ok: true,
          json: async () => ([
            {
              idea_id: 'idea000093',
              rank: 93,
              title: 'Auto Sync Ideas',
              source_path: 'docs/project/ideas/idea000093-auto-sync.md',
              mapped_project_ids: ['prj0000093'],
            },
          ]),
        } as Response;
      }
      throw new Error(`Unexpected URL: ${url}`);
    }) as typeof fetch;

    render(<ProjectManager />);

    await waitFor(() => {
      expect(screen.queryByText('Ideas Autosync')).not.toBeNull();
    });

    expect(screen.queryByText('Active Ideas Queue')).not.toBeNull();
    expect(screen.queryByText('Auto Sync Ideas')).not.toBeNull();
    expect(screen.queryByText('idea000093')).not.toBeNull();
    expect(screen.queryByText('docs/project/ideas/idea000093-auto-sync.md')).not.toBeNull();

    const fetchCalls = (globalThis.fetch as ReturnType<typeof vi.fn>).mock.calls.map(
      ([input]) => String(input),
    );
    expect(fetchCalls).toContain('/api/ideas?implemented=exclude&implemented_mode=active_or_released&sort=rank&order=asc');
  });

  it('renders ideas empty state when ideas queue is empty', async () => {
    globalThis.fetch = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/api/projects')) {
        return {
          ok: true,
          json: async () => ([
            {
              id: 'prj0000093',
              name: 'Ideas Autosync',
              lane: 'In Sprint',
              summary: 'Frontend panel integration',
              branch: 'prj0000093-projectmanager-ideas-autosync',
              pr: null,
              priority: 'P2',
              budget_tier: 'S',
              tags: ['ideas'],
              created: '2026-03-28',
              updated: '2026-03-28',
            },
          ]),
        } as Response;
      }
      if (url.includes('/api/ideas')) {
        return {
          ok: true,
          json: async () => ([]),
        } as Response;
      }
      throw new Error(`Unexpected URL: ${url}`);
    }) as typeof fetch;

    render(<ProjectManager />);

    await waitFor(() => {
      expect(screen.queryByText('Ideas Autosync')).not.toBeNull();
    });

    expect(screen.queryByText('Active Ideas Queue')).not.toBeNull();
    expect(screen.queryByText('No active ideas in queue.')).not.toBeNull();
  });

  it('keeps project board usable when ideas fetch fails', async () => {
    globalThis.fetch = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/api/projects')) {
        return {
          ok: true,
          json: async () => ([
            {
              id: 'prj0000093',
              name: 'Ideas Autosync',
              lane: 'In Sprint',
              summary: 'Frontend panel integration',
              branch: 'prj0000093-projectmanager-ideas-autosync',
              pr: null,
              priority: 'P2',
              budget_tier: 'S',
              tags: ['ideas'],
              created: '2026-03-28',
              updated: '2026-03-28',
            },
          ]),
        } as Response;
      }
      if (url.includes('/api/ideas')) {
        return {
          ok: false,
          status: 503,
          json: async () => ({}),
        } as Response;
      }
      throw new Error(`Unexpected URL: ${url}`);
    }) as typeof fetch;

    render(<ProjectManager />);

    await waitFor(() => {
      expect(screen.queryByText('Ideas Autosync')).not.toBeNull();
    });

    expect(screen.queryByText(/Ideas unavailable:/i)).not.toBeNull();
    expect(screen.queryByText('Active Ideas Queue')).not.toBeNull();
  });
});
