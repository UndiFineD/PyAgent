# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\action.py\_1_deep_research.py\deep_research.py\research_manager_4812c7681892.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\action\1_deep_research\deep_research\research_manager.py

import asyncio

from agents import Runner, gen_trace_id, trace

from planner_agent import WebSearchItem, WebSearchPlan, planner_agent

from push_agent import push_agent

from search_agent import search_agent

from writer_agent import ReportData, writer_agent


class ResearchManager:
    async def run(self, query: str):
        """Run the deep research process, yielding the status updates and the final report"""

        trace_id = gen_trace_id()

        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")

            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"

            print("Starting research...")

            search_plan = await self.plan_searches(query)

            yield "Searches planned, starting to search..."

            search_results = await self.perform_searches(search_plan)

            yield "Searches complete, writing report..."

            report = await self.write_report(query, search_results)

            yield "Report written, sending push notification..."

            await self.send_push(report)

            yield "Push notification sent, research complete"

            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query"""

        print("Planning searches...")

        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )

        print(f"Will perform {len(result.final_output.searches)} searches")

        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Perform the searches to perform for the query"""

        print("Searching...")

        num_completed = 0

        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]

        results = []

        for task in asyncio.as_completed(tasks):
            result = await task

            if result is not None:
                results.append(result)

            num_completed += 1

            print(f"Searching... {num_completed}/{len(tasks)} completed")

        print("Finished searching")

        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a search for the query"""

        input = f"Search term: {item.query}\nReason for searching: {item.reason}"

        try:
            result = await Runner.run(
                search_agent,
                input,
            )

            return str(result.final_output)

        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the report for the query"""

        print("Thinking about report...")

        input = f"Original query: {query}\nSummarized search results: {search_results}"

        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")

        return result.final_output_as(ReportData)

    async def send_push(self, report: ReportData) -> None:

        print("Pushing notification...")

        result = await Runner.run(push_agent, report.short_summary)

        print("Notification sent")

        return report
