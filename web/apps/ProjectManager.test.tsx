import { describe, it, expect } from 'vitest';

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
