# Design: Dependabot-Renovate Integration

## Architecture Overview
Dual-tool strategy for dependency management:
- **Dependabot**: GitHub Actions, Docker, security-focused
- **Renovate**: Python, Node.js, general-purpose dependencies

## Configuration Strategy

### Renovate Configuration (renovate.json)
- Extends from recommended presets
- Groups related dependencies (monorepos)
- Enables automerge for patch/digest/security updates
- Disables automerge for major/minor versions
- 3-day minimum release age for stability

### Dependabot Configuration (dependabot.yml)
- Manages GitHub Actions ecosystem
- Python pip with selective ignores
- Docker image updates
- Weekly schedule, Sunday 3 AM UTC
- Max 5 open PRs per ecosystem

## Key Design Decisions

1. **Tool Separation**: Avoid conflicts by assigning ecosystems
   - Dependabot: GitHub Actions (native support)
   - Renovate: Everything else (better support)

2. **Safety-First Automerge**:
   - Only patch/digest/security updates auto-merge
   - Major/minor require manual review
   - 3-day minimum release age prevents early adoption

3. **Single Schedule**: Weekly Monday 3 AM UTC
   - Consistent across both tools
   - Admin-friendly, predictable
   - Less noisy than daily checks

## Risk Mitigation
- No automerge for major versions (breaking changes)
- No automerge for minor versions (new features, potential bugs)
- Security updates get priority fast-track
- Proper labeling for issue tracking

## Implementation Files
1. `.github/renovate.json` - Primary config file
2. `.github/dependabot.yml` - Secondary config file
3. `MAINTENANCE.md` - Documentation

---
**Status:** Design Complete | **Next:** Implementation
