#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import asyncio
import aiohttp
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from urllib.parse import urlparse
import logging

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.models.communication_models import CascadeContext


class BugBountyIntelligenceCore(BaseAgent):
    """
    Core agent for collecting and analyzing bug bounty intelligence.

    This agent automates the collection of vulnerability reports from bug bounty platforms,
    analyzes patterns, and provides security intelligence for research and defense.
    """

    def __init__(self, agent_state_manager, cascade_context: CascadeContext):
        super().__init__(__file__)
        self.cascade_context = cascade_context
        self.agent_state_manager = agent_state_manager
        self.logger = logging.getLogger(__name__)

        # HTTP client configuration
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.session = None

        # Platform configurations
        self.platforms = {
            'hackerone': {
                'graphql_url': 'https://hackerone.com/graphql',
                'query_template': self._get_hackerone_query(),
                'page_size': 25,
                'rate_limit_delay': 1.0
            }
        }

    def _get_hackerone_query(self) -> str:
        """Get the HackerOne GraphQL query template."""
        return """
        query HacktivitySearchQuery($queryString: String!, $from: Int, $size: Int, $sort: SortInput!) {
          me {
            id
            __typename
          }
          search(
            index: HacktivityReportIndexService
            query_string: $queryString
            from: $from
            size: $size
            sort: $sort
          ) {
            __typename
            total_count
            nodes {
              __typename
              ... on HacktivityReportDocument {
                id
                _id
                reporter {
                  id
                  name
                  username
                  ...UserLinkWithMiniProfile
                  __typename
                }
                cve_ids
                cwe
                severity_rating
                upvoted: upvoted_by_current_user
                report {
                  id
                  databaseId: _id
                  title
                  substate
                  url
                  disclosed_at
                  report_generated_content {
                    id
                    hacktivity_summary
                    __typename
                  }
                  __typename
                }
                votes
                team {
                  handle
                  name
                  medium_profile_picture: profile_picture(size: medium)
                  url
                  id
                  currency
                  ...TeamLinkWithMiniProfile
                  __typename
                }
                total_awarded_amount
                latest_disclosable_action
                latest_disclosable_activity_at
                submitted_at
                __typename
              }
            }
          }
        }

        fragment UserLinkWithMiniProfile on User {
          id
          username
          __typename
        }

        fragment TeamLinkWithMiniProfile on Team {
          id
          handle
          name
          __typename
        }
        """

    async def _init_session(self):
        """Initialize HTTP session if not already done."""
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=self.timeout)

    async def collect_hackerone_reports(self, max_reports: int = 1000, query_string: str = "*:*") -> List[Dict[str, Any]]:
        """
        Collect bug bounty reports from HackerOne.

        Args:
            max_reports: Maximum number of reports to collect
            query_string: Search query string

        Returns:
            List of report data dictionaries
        """
        await self._init_session()
        reports = []
        platform_config = self.platforms['hackerone']

        from_offset = 0
        page_size = platform_config['page_size']

        while len(reports) < max_reports:
            # Prepare GraphQL query
            variables = {
                "queryString": query_string,
                "size": min(page_size, max_reports - len(reports)),
                "from": from_offset,
                "sort": {
                    "field": "disclosed_at",
                    "direction": "DESC"
                },
                "product_area": "hacktivity",
                "product_feature": "overview"
            }

            payload = {
                "operationName": "HacktivitySearchQuery",
                "variables": variables,
                "query": platform_config['query_template']
            }

            try:
                if self.session is None:
                    self.logger.error("Session is not initialized")
                    break

                async with self.session.post(
                    platform_config['graphql_url'],
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:

                    if response.status != 200:
                        self.logger.error(f"HackerOne API error: {response.status}")
                        break

                    data = await response.json()

                    if 'data' not in data or 'search' not in data['data']:
                        self.logger.error("Unexpected API response structure")
                        break

                    nodes = data['data']['search']['nodes']
                    if not nodes:
                        break  # No more results

                    for node in nodes:
                        if len(reports) >= max_reports:
                            break

                        report_data = self._parse_hackerone_report(node)
                        if report_data:
                            reports.append(report_data)

                    from_offset += page_size

                    # Rate limiting
                    await asyncio.sleep(platform_config['rate_limit_delay'])

            except Exception as e:
                self.logger.error(f"Error collecting HackerOne reports: {e}")
                break

        return reports

    def _parse_hackerone_report(self, node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse a single HackerOne report node into structured data."""
        try:
            report = node.get('report', {})
            if not report:
                return None

            return {
                'platform': 'hackerone',
                'report_id': report.get('databaseId'),
                'title': report.get('title', ''),
                'url': report.get('url', ''),
                'disclosed_at': report.get('disclosed_at'),
                'substate': report.get('substate'),
                'reporter': {
                    'username': node.get('reporter', {}).get('username'),
                    'name': node.get('reporter', {}).get('name')
                },
                'team': {
                    'handle': node.get('team', {}).get('handle'),
                    'name': node.get('team', {}).get('name'),
                    'url': node.get('team', {}).get('url')
                },
                'severity_rating': node.get('severity_rating'),
                'cve_ids': node.get('cve_ids', []),
                'cwe': node.get('cwe'),
                'votes': node.get('votes', 0),
                'total_awarded_amount': node.get('total_awarded_amount'),
                'submitted_at': node.get('submitted_at'),
                'latest_activity': node.get('latest_disclosable_activity_at'),
                'summary': report.get('report_generated_content', {}).get('hacktivity_summary', ''),
                'collected_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error parsing report: {e}")
            return None

    async def analyze_vulnerability_patterns(self, reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze patterns in collected vulnerability reports.

        Args:
            reports: List of report data

        Returns:
            Analysis results dictionary
        """
        analysis = {
            'total_reports': len(reports),
            'severity_distribution': {},
            'cwe_distribution': {},
            'team_distribution': {},
            'temporal_trends': {},
            'common_keywords': {},
            'cve_trends': {},
            'bounty_distribution': {}
        }

        # Severity analysis
        severity_counts = {}
        for report in reports:
            severity = report.get('severity_rating', 'unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        analysis['severity_distribution'] = severity_counts

        # CWE analysis
        cwe_counts = {}
        for report in reports:
            cwe = report.get('cwe')
            if cwe:
                cwe_id = f"CWE-{cwe}" if isinstance(cwe, int) else str(cwe)
                cwe_counts[cwe_id] = cwe_counts.get(cwe_id, 0) + 1
        analysis['cwe_distribution'] = dict(sorted(cwe_counts.items(), key=lambda x: x[1], reverse=True)[:20])

        # Team analysis
        team_counts = {}
        for report in reports:
            team = report.get('team', {}).get('handle')
            if team:
                team_counts[team] = team_counts.get(team, 0) + 1
        analysis['team_distribution'] = dict(sorted(team_counts.items(), key=lambda x: x[1], reverse=True)[:20])

        # Temporal analysis
        monthly_counts = {}
        for report in reports:
            disclosed_at = report.get('disclosed_at')
            if disclosed_at:
                try:
                    date = datetime.fromisoformat(disclosed_at.replace('Z', '+00:00'))
                    month_key = f"{date.year}-{date.month:02d}"
                    monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
                except:
                    pass
        analysis['temporal_trends'] = dict(sorted(monthly_counts.items()))

        # Keyword analysis from titles
        keywords = {}
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'cannot'}

        for report in reports:
            title = report.get('title', '').lower()
            words = re.findall(r'\b\w+\b', title)
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    keywords[word] = keywords.get(word, 0) + 1

        analysis['common_keywords'] = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:50])

        # CVE analysis
        cve_counts = {}
        for report in reports:
            cves = report.get('cve_ids', [])
            for cve in cves:
                cve_counts[cve] = cve_counts.get(cve, 0) + 1
        analysis['cve_trends'] = dict(sorted(cve_counts.items(), key=lambda x: x[1], reverse=True)[:20])

        # Bounty analysis
        bounty_ranges = {'0': 0, '1-100': 0, '101-500': 0, '501-1000': 0, '1001-5000': 0, '5000+': 0}
        for report in reports:
            amount = report.get('total_awarded_amount', 0) or 0
            if amount == 0:
                bounty_ranges['0'] += 1
            elif amount <= 100:
                bounty_ranges['1-100'] += 1
            elif amount <= 500:
                bounty_ranges['101-500'] += 1
            elif amount <= 1000:
                bounty_ranges['501-1000'] += 1
            elif amount <= 5000:
                bounty_ranges['1001-5000'] += 1
            else:
                bounty_ranges['5000+'] += 1
        analysis['bounty_distribution'] = bounty_ranges

        return analysis

    async def search_similar_vulnerabilities(self, target_description: str, reports: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar vulnerabilities based on description.

        Args:
            target_description: Description to search for
            reports: List of reports to search in
            limit: Maximum number of results

        Returns:
            List of similar reports
        """
        target_words = set(re.findall(r'\b\w+\b', target_description.lower()))
        target_words = {word for word in target_words if len(word) > 3}

        scored_reports = []

        for report in reports:
            title = report.get('title', '').lower()
            summary = report.get('summary', '').lower()

            report_words = set(re.findall(r'\b\w+\b', title + ' ' + summary))
            report_words = {word for word in report_words if len(word) > 3}

            # Calculate Jaccard similarity
            intersection = target_words.intersection(report_words)
            union = target_words.union(report_words)

            if union:
                similarity = len(intersection) / len(union)
                if similarity > 0.1:  # Minimum similarity threshold
                    scored_reports.append((similarity, report))

        # Sort by similarity and return top results
        scored_reports.sort(key=lambda x: x[0], reverse=True)
        return [report for _, report in scored_reports[:limit]]

    async def generate_intelligence_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a human-readable intelligence report.

        Args:
            analysis: Analysis results

        Returns:
            Formatted report string
        """
        report = []
        report.append("# Bug Bounty Intelligence Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        report.append(f"## Overview")
        report.append(f"- Total Reports Analyzed: {analysis['total_reports']}")
        report.append("")

        report.append("## Severity Distribution")
        for severity, count in analysis['severity_distribution'].items():
            percentage = (count / analysis['total_reports']) * 100
            report.append(f"- {severity}: {count} ({percentage:.1f}%)")
        report.append("")

        report.append("## Top CWE Categories")
        for cwe, count in list(analysis['cwe_distribution'].items())[:10]:
            percentage = (count / analysis['total_reports']) * 100
            report.append(f"- {cwe}: {count} ({percentage:.1f}%)")
        report.append("")

        report.append("## Most Active Programs")
        for team, count in list(analysis['team_distribution'].items())[:10]:
            report.append(f"- {team}: {count} reports")
        report.append("")

        report.append("## Bounty Distribution")
        for range_name, count in analysis['bounty_distribution'].items():
            if count > 0:
                percentage = (count / analysis['total_reports']) * 100
                report.append(f"- ${range_name}: {count} ({percentage:.1f}%)")
        report.append("")

        report.append("## Common Vulnerability Keywords")
        keywords = list(analysis['common_keywords'].items())[:20]
        for keyword, count in keywords:
            report.append(f"- {keyword}: {count}")
        report.append("")

        return "\n".join(report)

    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute intelligence gathering task.

        Expected task_data format:
        {
            'action': 'collect_reports' | 'analyze_patterns' | 'search_similar' | 'generate_report',
            'platform': 'hackerone',  # for collect_reports
            'max_reports': 1000,      # for collect_reports
            'query_string': '*:*',    # for collect_reports
            'reports': [...],         # for analyze_patterns, search_similar
            'target_description': '', # for search_similar
            'analysis': {...}         # for generate_report
        }
        """
        action = task_data.get('action', 'collect_reports')

        if action == 'collect_reports':
            platform = task_data.get('platform', 'hackerone')
            max_reports = task_data.get('max_reports', 1000)
            query_string = task_data.get('query_string', '*:*')

            if platform == 'hackerone':
                reports = await self.collect_hackerone_reports(max_reports, query_string)
                return {'reports': reports, 'count': len(reports)}
            else:
                return {'error': f'Unsupported platform: {platform}'}

        elif action == 'analyze_patterns':
            reports = task_data.get('reports', [])
            if not reports:
                return {'error': 'reports required for analyze_patterns action'}

            analysis = await self.analyze_vulnerability_patterns(reports)
            return {'analysis': analysis}

        elif action == 'search_similar':
            reports = task_data.get('reports', [])
            target_description = task_data.get('target_description', '')
            limit = task_data.get('limit', 10)

            if not reports or not target_description:
                return {'error': 'reports and target_description required for search_similar action'}

            similar_reports = await self.search_similar_vulnerabilities(target_description, reports, limit)
            return {'similar_reports': similar_reports, 'count': len(similar_reports)}

        elif action == 'generate_report':
            analysis = task_data.get('analysis', {})
            if not analysis:
                return {'error': 'analysis required for generate_report action'}

            report = await self.generate_intelligence_report(analysis)
            return {'intelligence_report': report}

        else:
            return {'error': f'Unknown action: {action}'}

    async def close(self):
        """Clean up resources."""
        if self.session:
            await self.session.close()
            self.session = None
