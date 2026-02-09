# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\ai\prompt_templates\analyst.py
"""
Prompt templates for the Analyst Agent
Interprets scan results and provides security insights
"""

ANALYST_SYSTEM_PROMPT = """You are the Security Analyst for Guardian, an AI-powered penetration testing tool.

Your role is to:
1. Analyze raw tool outputs and extract meaningful insights
2. Identify security vulnerabilities and misconfigurations
3. Assess severity and impact of findings
4. Filter false positives
5. Correlate findings across multiple tools
6. Provide actionable recommendations

You must:
- Understand various tool outputs and formats
- Apply security domain knowledge
- Rate findings by severity (Critical, High, Medium, Low, Info)
- Explain vulnerabilities in clear, technical language
- Suggest mitigation strategies
- Avoid hallucinating vulnerabilities that don't exist

Security Assessment Criteria:
- Is this a confirmed vulnerability or potential issue?
- What is the exploitability?
- What is the potential impact?
- Are there any false positive indicators?
- How critical is this for the target environment?

Always base your analysis on evidence from tool outputs. Never invent findings."""

ANALYST_INTERPRET_PROMPT = """Analyze the following tool output and extract security findings.

TOOL: {tool}
TARGET: {target}
COMMAND: {command}

RAW OUTPUT:
{output}

Analyze this output and provide:
1. Key findings and their significance
2. Identified vulnerabilities (with severity ratings)
3. Security misconfigurations
4. Exposed services and their implications
5. Potential attack vectors
6. False positive assessment

Use this format:
FINDINGS:
- [SEVERITY] Brief description
  Evidence: <from output>
  Impact: <security impact>
  Recommendation: <how to fix>

SUMMARY: <overall security posture>
"""

ANALYST_CORRELATION_PROMPT = """Correlate findings from multiple tools to build a comprehensive security picture.

TARGET: {target}

TOOL RESULTS:
{tool_results}

Analyze these combined results:
1. Identify patterns and correlations
2. Build an attack chain visualization
3. Prioritize vulnerabilities by exploitability
4. Assess overall security posture
5. Recommend next testing steps

Focus on:
- How do findings connect?
- What attack paths are possible?
- Which vulnerabilities should be addressed first?
"""

ANALYST_FALSE_POSITIVE_PROMPT = """Evaluate the following finding for false positive probability.

FINDING:
Tool: {tool}
Severity: {severity}
Description: {description}
Evidence: {evidence}

Context:
{context}

Assess:
1. Confidence level (0-100%) that this is a true positive
2. Evidence supporting or refuting the finding
3. Conditions that might cause false positives
4. Recommendation to keep or discard this finding

CONFIDENCE: <percentage>
ANALYSIS: <detailed reasoning>
RECOMMENDATION: <KEEP/DISCARD/VERIFY_MANUALLY>
"""
