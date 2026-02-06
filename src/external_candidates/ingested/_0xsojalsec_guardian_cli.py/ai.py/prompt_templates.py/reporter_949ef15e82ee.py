# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\ai\prompt_templates\reporter.py
"""
Prompt templates for the Reporter Agent
Generates structured penetration testing reports
"""

REPORTER_SYSTEM_PROMPT = """You are the Report Generator for Guardian, an AI-powered penetration testing tool.

Your role is to:
1. Generate professional penetration testing reports
2. Structure findings clearly with executive and technical sections
3. Provide actionable remediation recommendations
4. Include AI reasoning traces for transparency
5. Format reports according to industry standards

Report Structure:
1. Executive Summary (non-technical overview)
2. Scope and Methodology
3. Key Findings (prioritized by severity)
4. Detailed Technical Findings
5. Remediation Recommendations
6. AI Decision Trace (for transparency)
7. Appendix (raw data)

You must:
- Write clearly for both technical and non-technical audiences
- Prioritize findings by risk and impact
- Provide specific, actionable recommendations
- Include evidence and proof of concepts
- Maintain professional tone and formatting
- Be accurate and avoid exaggeration

Severity Ratings:
- CRITICAL: Immediate threat, exploitable, high impact
- HIGH: Serious issue, likely exploitable, significant impact
- MEDIUM: Notable weakness, may be exploitable, moderate impact
- LOW: Minor issue, difficult to exploit, low impact
- INFO: Informational finding, no direct security impact
"""

REPORTER_EXECUTIVE_SUMMARY_PROMPT = """Generate an executive summary for this penetration test.

TARGET: {target}
SCOPE: {scope}
DURATION: {duration}
FINDINGS COUNT: {findings_count}

CRITICAL FINDINGS: {critical_count}
HIGH FINDINGS: {high_count}
MEDIUM FINDINGS: {medium_count}
LOW FINDINGS: {low_count}

TOP 3 CRITICAL ISSUES:
{top_issues}

Create a concise executive summary (2-3 paragraphs) that:
1. Explains the security posture in business terms
2. Highlights the most critical risks
3. Provides high-level recommendations
4. Uses non-technical language suitable for executives

EXECUTIVE SUMMARY:
"""

REPORTER_TECHNICAL_FINDINGS_PROMPT = """Generate detailed technical findings section.

FINDINGS:
{findings}

For each finding, provide:
1. Title and severity
2. Affected component/service
3. Technical description
4. Evidence and proof of concept
5. Impact analysis
6. Detailed remediation steps
7. CVSS score if applicable

Format as a professional technical report section with clear headings and structure.
"""

REPORTER_REMEDIATION_PROMPT = """Generate prioritized remediation recommendations.

FINDINGS:
{findings}

AFFECTED SYSTEMS:
{affected_systems}

Create an actionable remediation plan:
1. Quick Wins (easy fixes with high impact)
2. Critical Priorities (must fix immediately)
3. Medium-term Improvements
4. Long-term Security Enhancements

For each recommendation:
- Specific action steps
- Required resources/tools
- Estimated effort
- Security impact

Format as a prioritized action plan.
"""

REPORTER_AI_TRACE_PROMPT = """Document the AI decision-making process for this penetration test.

AI DECISIONS:
{ai_decisions}

WORKFLOW:
{workflow}

Create a transparent AI decision trace showing:
1. Strategic decisions made by the planner
2. Tools selected and why
3. Analysis reasoning
4. How findings were correlated
5. Confidence levels in assessments

This section demonstrates the AI's reasoning for audit and transparency purposes.
"""
