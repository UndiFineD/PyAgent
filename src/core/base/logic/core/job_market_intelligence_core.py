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

# Job Market Intelligence Core - Automated Job Data Collection and Analysis
# Based on patterns from 2026-SWE-College-Jobs repository

import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from src.core.base.common.base_core import BaseCore


@dataclass
class JobPosting:
    """Represents a job posting with all relevant data"""
    company_name: str
    company_url: Optional[str]
    job_title: str
    job_locations: str
    job_url: str
    salary: Optional[float]
    salary_currency: str = "USD"
    salary_interval: str = "yr"  # yr, hr, etc.
    posting_date: datetime
    job_type: str  # intern, new_grad, etc.
    company_type: str  # faang, quant, other
    is_usa: bool = True
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    @property
    def age_days(self) -> int:
        """Calculate how many days ago the job was posted"""
        return (datetime.now() - self.posting_date).days

    @property
    def salary_display(self) -> str:
        """Format salary for display"""
        if not self.salary:
            return ""

        if self.salary >= 1000:
            salary_str = f"${(self.salary / 1000):.0f}k"
        else:
            salary_str = f"${self.salary:.0f}"

        return f"{salary_str}/{self.salary_interval}"


@dataclass
class JobMarketStats:
    """Statistics about the job market"""
    total_jobs: int
    avg_salary: Optional[float]
    top_companies: List[Tuple[str, int]]
    top_locations: List[Tuple[str, int]]
    salary_ranges: Dict[str, int]
    posting_trends: Dict[str, int]  # jobs posted in last N days
    company_types: Dict[str, int]


class JobMarketIntelligenceCore(BaseCore):
    """
    Job Market Intelligence Core for automated job data collection and analysis.

    Provides capabilities to collect, analyze, and present job market intelligence
    including salary trends, company hiring patterns, and market insights.
    """

    def __init__(self):
        super().__init__()
        self.job_database: List[JobPosting] = []
        self.data_sources: List[str] = []
        self.last_update: Optional[datetime] = None

    async def initialize(self) -> bool:
        """Initialize the job market intelligence core"""
        try:
            # Initialize with default data sources
            await self.add_default_sources()
            self.logger.info("Job Market Intelligence Core initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Job Market Intelligence Core: {e}")
            return False

    async def add_default_sources(self) -> None:
        """Add default job data sources"""
        default_sources = [
            "https://github.com/speedyapply/2026-SWE-College-Jobs",
            "https://github.com/speedyapply/2026-AI-College-Jobs",
            "https://www.levels.fyi",
            "https://www.glassdoor.com",
            "https://www.indeed.com"
        ]

        for source in default_sources:
            await self.add_data_source(source)

    async def add_data_source(self, source_url: str) -> None:
        """Add a job data source"""
        if source_url not in self.data_sources:
            self.data_sources.append(source_url)
            self.logger.info(f"Added data source: {source_url}")

    async def remove_data_source(self, source_url: str) -> bool:
        """Remove a job data source"""
        if source_url in self.data_sources:
            self.data_sources.remove(source_url)
            self.logger.info(f"Removed data source: {source_url}")
            return True
        return False

    async def collect_job_data(
        self,
        job_type: str = "intern",
        is_usa: bool = True,
        company_type: Optional[str] = None,
        max_age_days: int = 120
    ) -> List[JobPosting]:
        """
        Collect job data from configured sources

        Args:
            job_type: Type of jobs to collect (intern, new_grad, etc.)
            is_usa: Whether to collect USA jobs
            company_type: Company category filter (faang, quant, other)
            max_age_days: Maximum age of job postings to collect

        Returns:
            List of collected job postings
        """
        collected_jobs = []

        # Simulate data collection from various sources
        # In a real implementation, this would scrape or API-call actual job sites

        # For demonstration, create sample job data
        sample_jobs = await self._generate_sample_jobs(job_type, is_usa, company_type, max_age_days)
        collected_jobs.extend(sample_jobs)

        # Update database
        for job in collected_jobs:
            if job not in self.job_database:
                self.job_database.append(job)

        self.last_update = datetime.now()
        self.logger.info(f"Collected {len(collected_jobs)} job postings")
        return collected_jobs

    async def _generate_sample_jobs(
        self,
        job_type: str,
        is_usa: bool,
        company_type: Optional[str],
        max_age_days: int
    ) -> List[JobPosting]:
        """Generate sample job data for demonstration"""
        companies = {
            "faang": ["Google", "Meta", "Amazon", "Apple", "Netflix", "Microsoft"],
            "quant": ["Jane Street", "Two Sigma", "Citadel", "Jump Trading", "DRW"],
            "other": ["Stripe", "Databricks", "Snowflake", "Coinbase", "Roblox"]
        }

        jobs = []
        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        for comp_type, comp_list in companies.items():
            if company_type and comp_type != company_type:
                continue

            for company in comp_list[:3]:  # Limit for demo
                for i in range(2):  # 2 jobs per company
                    posting_date = datetime.now() - timedelta(days=i * 10)
                    if posting_date < cutoff_date:
                        continue

                    job = JobPosting(
                        company_name=company,
                        company_url=f"https://www.{company.lower().replace(' ', '')}.com",
                        job_title=f"Software Engineer {job_type.title()}",
                        job_locations="San Francisco, CA" if is_usa else "London, UK",
                        job_url=f"https://{company.lower().replace(' ', '')}.com/careers/job{i}",
                        salary=150000 if job_type == "new_grad" else 50,
                        salary_interval="yr" if job_type == "new_grad" else "hr",
                        posting_date=posting_date,
                        job_type=job_type,
                        company_type=comp_type,
                        is_usa=is_usa,
                        tags=["software-engineering", job_type, comp_type]
                    )
                    jobs.append(job)

        return jobs

    async def analyze_market_data(
        self,
        job_type: Optional[str] = None,
        company_type: Optional[str] = None,
        is_usa: Optional[bool] = None
    ) -> JobMarketStats:
        """
        Analyze collected job market data

        Args:
            job_type: Filter by job type
            company_type: Filter by company type
            is_usa: Filter by location

        Returns:
            Market statistics
        """
        # Filter jobs
        filtered_jobs = self.job_database

        if job_type:
            filtered_jobs = [j for j in filtered_jobs if j.job_type == job_type]
        if company_type:
            filtered_jobs = [j for j in filtered_jobs if j.company_type == company_type]
        if is_usa is not None:
            filtered_jobs = [j for j in filtered_jobs if j.is_usa == is_usa]

        if not filtered_jobs:
            return JobMarketStats(0, None, [], [], {}, {}, {})

        # Calculate statistics
        salaries = [j.salary for j in filtered_jobs if j.salary]
        avg_salary = sum(salaries) / len(salaries) if salaries else None

        # Top companies
        company_counts = {}
        for job in filtered_jobs:
            company_counts[job.company_name] = company_counts.get(job.company_name, 0) + 1
        top_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        # Top locations
        location_counts = {}
        for job in filtered_jobs:
            locations = [loc.strip() for loc in job.job_locations.split(',')]
            for loc in locations:
                location_counts[loc] = location_counts.get(loc, 0) + 1
        top_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        # Salary ranges
        salary_ranges = {}
        for job in filtered_jobs:
            if job.salary:
                if job.salary < 50000:
                    range_key = "<$50k"
                elif job.salary < 100000:
                    range_key = "$50k-$100k"
                elif job.salary < 150000:
                    range_key = "$100k-$150k"
                else:
                    range_key = ">$150k"
                salary_ranges[range_key] = salary_ranges.get(range_key, 0) + 1

        # Posting trends (last 30, 60, 90 days)
        now = datetime.now()
        posting_trends = {
            "last_30_days": len([j for j in filtered_jobs if (now - j.posting_date).days <= 30]),
            "last_60_days": len([j for j in filtered_jobs if (now - j.posting_date).days <= 60]),
            "last_90_days": len([j for j in filtered_jobs if (now - j.posting_date).days <= 90])
        }

        # Company types
        company_types = {}
        for job in filtered_jobs:
            company_types[job.company_type] = company_types.get(job.company_type, 0) + 1

        return JobMarketStats(
            total_jobs=len(filtered_jobs),
            avg_salary=avg_salary,
            top_companies=top_companies,
            top_locations=top_locations,
            salary_ranges=salary_ranges,
            posting_trends=posting_trends,
            company_types=company_types
        )

    async def generate_market_report(
        self,
        job_type: Optional[str] = None,
        company_type: Optional[str] = None,
        is_usa: Optional[bool] = None,
        output_format: str = "markdown"
    ) -> str:
        """
        Generate a market intelligence report

        Args:
            job_type: Filter by job type
            company_type: Filter by company type
            is_usa: Filter by location
            output_format: Output format (markdown, json, html)

        Returns:
            Formatted report
        """
        stats = await self.analyze_market_data(job_type, company_type, is_usa)

        if output_format == "json":
            return json.dumps(asdict(stats), indent=2, default=str)

        elif output_format == "markdown":
            return await self._generate_markdown_report(stats, job_type, company_type, is_usa)

        else:
            raise ValueError(f"Unsupported format: {output_format}")

    async def _generate_markdown_report(
        self,
        stats: JobMarketStats,
        job_type: Optional[str],
        company_type: Optional[str],
        is_usa: Optional[bool]
    ) -> str:
        """Generate markdown format report"""
        title = "Job Market Intelligence Report"
        if job_type:
            title += f" - {job_type.title()}"
        if company_type:
            title += f" ({company_type.title()})"
        if is_usa is not None:
            title += f" {'USA' if is_usa else 'International'}"

        report = f"# {title}\n\n"
        report += f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"**Total Jobs Analyzed:** {stats.total_jobs}\n\n"

        if stats.avg_salary:
            report += f"**Average Salary:** ${stats.avg_salary:,.0f}\n\n"

        # Top Companies
        if stats.top_companies:
            report += "## Top Companies\n\n"
            report += "| Company | Job Count |\n"
            report += "|---------|-----------|\n"
            for company, count in stats.top_companies[:10]:
                report += f"| {company} | {count} |\n"
            report += "\n"

        # Top Locations
        if stats.top_locations:
            report += "## Top Locations\n\n"
            report += "| Location | Job Count |\n"
            report += "|----------|-----------|\n"
            for location, count in stats.top_locations[:10]:
                report += f"| {location} | {count} |\n"
            report += "\n"

        # Salary Distribution
        if stats.salary_ranges:
            report += "## Salary Distribution\n\n"
            report += "| Range | Count |\n"
            report += "|-------|-------|\n"
            for range_key, count in stats.salary_ranges.items():
                report += f"| {range_key} | {count} |\n"
            report += "\n"

        # Posting Trends
        if stats.posting_trends:
            report += "## Recent Posting Trends\n\n"
            for period, count in stats.posting_trends.items():
                period_name = period.replace("last_", "").replace("_", " ")
                report += f"- **{period_name}:** {count} jobs\n"
            report += "\n"

        # Company Types
        if stats.company_types:
            report += "## Company Categories\n\n"
            for comp_type, count in stats.company_types.items():
                report += f"- **{comp_type.title()}:** {count} companies\n"
            report += "\n"

        return report

    async def export_job_data(
        self,
        filepath: str,
        job_type: Optional[str] = None,
        company_type: Optional[str] = None,
        output_format: str = "json"
    ) -> None:
        """
        Export job data to file

        Args:
            filepath: Output file path
            job_type: Filter by job type
            company_type: Filter by company type
            output_format: Export format (json, csv)
        """
        # Filter jobs
        filtered_jobs = self.job_database

        if job_type:
            filtered_jobs = [j for j in filtered_jobs if j.job_type == job_type]
        if company_type:
            filtered_jobs = [j for j in filtered_jobs if j.company_type == company_type]

        if output_format == "json":
            data = [asdict(job) for job in filtered_jobs]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)

        elif output_format == "csv":
            import csv
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                if filtered_jobs:
                    fieldnames = list(asdict(filtered_jobs[0]).keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for job in filtered_jobs:
                        writer.writerow(asdict(job))

        self.logger.info(f"Exported {len(filtered_jobs)} jobs to {filepath}")

    async def get_market_insights(
        self,
        focus_area: str = "salary"
    ) -> Dict[str, Any]:
        """
        Generate market insights and recommendations

        Args:
            focus_area: Area to focus insights on (salary, companies, locations)

        Returns:
            Dictionary of insights and recommendations
        """
        stats = await self.analyze_market_data()

        insights = {
            "market_health": "healthy" if stats.total_jobs > 100 else "limited",
            "recommendations": [],
            "trends": [],
            "opportunities": []
        }

        if focus_area == "salary":
            if stats.avg_salary:
                insights["trends"].append(f"Average salary: ${stats.avg_salary:,.0f}")
                if stats.avg_salary > 120000:
                    insights["recommendations"].append("Market salaries are competitive")
                else:
                    insights["recommendations"].append("Consider negotiating for higher compensation")

            # Salary range insights
            if stats.salary_ranges:
                max_range = max(stats.salary_ranges.items(), key=lambda x: x[1])
                insights["trends"].append(f"Most common salary range: {max_range[0]}")

        elif focus_area == "companies":
            if stats.top_companies:
                top_company = stats.top_companies[0]
                insights["opportunities"].append(f"High hiring activity at {top_company[0]} ({top_company[1]} positions)")

            if stats.company_types:
                dominant_type = max(stats.company_types.items(), key=lambda x: x[1])
                insights["trends"].append(f"Dominant company type: {dominant_type[0]}")

        return insights

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.job_database.clear()
        self.data_sources.clear()
        self.logger.info("Job Market Intelligence Core cleaned up")
