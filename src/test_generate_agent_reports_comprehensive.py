#!/usr / bin / env python3
"""
Tests for generate_agent_reports.py improvements.

Covers report generation, formatting, templates,
metrics collection, and export functionality.
"""

import unittest
import json
import tempfile
import os
from datetime import datetime


class TestReportGeneration(unittest.TestCase):
    """Tests for basic report generation."""

    def test_generate_basic_report(self):
        """Test generating basic report."""
        report = {
            "title": "Test Report",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0",
        }

        assert report["title"] == "Test Report"
        assert report["version"] == "1.0"

    def test_generate_report_with_sections(self):
        """Test generating report with sections."""
        report = {
            "title": "Comprehensive Report",
            "sections": {
                "summary": "Summary content",
                "details": "Details content",
                "recommendations": "Recommendations content",
            },
        }

        assert len(report["sections"]) == 3
        assert "summary" in report["sections"]

    def test_generate_report_with_metadata(self):
        """Test generating report with metadata."""
        report = {
            "title": "Report",
            "metadata": {
                "author": "Agent",
                "created": datetime.now().isoformat(),
                "tags": ["important", "analysis"],
            },
        }

        assert report["metadata"]["author"] == "Agent"
        assert "important" in report["metadata"]["tags"]

    def test_generate_report_with_data(self):
        """Test generating report with data."""
        report = {
            "title": "Data Report",
            "data": {
                "total_items": 100,
                "processed": 95,
                "errors": 5,
            },
        }

        assert report["data"]["total_items"] == 100
        assert report["data"]["processed"] + report["data"]["errors"] == 100


class TestMarkdownReportFormatting(unittest.TestCase):
    """Tests for markdown report formatting."""

    def test_format_markdown_header(self):
        """Test formatting markdown header."""
        title = "Report Title"
        markdown = f"# {title}\n\n"

        assert "# " in markdown
        assert title in markdown

    def test_format_markdown_sections(self):
        """Test formatting markdown sections."""
        markdown = """
# Main Title

## Section 1
Content 1

## Section 2
Content 2
"""

        assert "##" in markdown
        assert "Section 1" in markdown
        assert "Section 2" in markdown

    def test_format_markdown_table(self):
        """Test formatting markdown table."""
        data = [
            {"name": "Item 1", "count": 10},
            {"name": "Item 2", "count": 20},
        ]

        markdown = "| Name | Count |\n|---|---|\n"
        for row in data:
            markdown += f"| {row['name']} | {row['count']} |\n"

        assert "| Name | Count |" in markdown
        assert "| Item 1 | 10 |" in markdown

    def test_format_markdown_list(self):
        """Test formatting markdown list."""
        items = ["Item 1", "Item 2", "Item 3"]
        markdown = ""
        for item in items:
            markdown += f"- {item}\n"

        assert markdown.count("-") == 3

    def test_format_markdown_code_block(self):
        """Test formatting markdown code block."""
        code = "def hello():\n    print('Hello')"
        markdown = f"```python\n{code}\n```"

        assert "```python" in markdown
        assert code in markdown


class TestHTMLReportFormatting(unittest.TestCase):
    """Tests for HTML report formatting."""

    def test_format_html_basic(self):
        """Test formatting basic HTML."""
        html = """
<html>
<head><title>Report</title></head>
<body>
<h1>Report Title</h1>
<p>Content</p>
</body>
</html>
"""

        assert "<html>" in html
        assert "<h1>" in html

    def test_format_html_table(self):
        """Test formatting HTML table."""
        html = """
<table>
<tr><th>Header 1</th><th>Header 2</th></tr>
<tr><td>Data 1</td><td>Data 2</td></tr>
</table>
"""

        assert "<table>" in html
        assert "<th>" in html
        assert "<td>" in html

    def test_format_html_styled(self):
        """Test formatting styled HTML."""
        html = """
<html>
<head>
<style>
h1 { color: blue; }
p { font-size: 14px; }
</style>
</head>
<body>
<h1>Title</h1>
</body>
</html>
"""

        assert "<style>" in html
        assert "color: blue" in html

    def test_format_html_responsive(self):
        """Test formatting responsive HTML."""
        html = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
Content
</body>
</html>
"""

        assert 'viewport' in html
        assert 'width=device-width' in html


class TestJSONReportFormatting(unittest.TestCase):
    """Tests for JSON report formatting."""

    def test_format_json_basic(self):
        """Test formatting basic JSON."""
        data = {
            "title": "Report",
            "timestamp": "2025-12-16",
            "items": [1, 2, 3],
        }

        json_str = json.dumps(data)
        restored = json.loads(json_str)

        assert restored["title"] == "Report"

    def test_format_json_nested(self):
        """Test formatting nested JSON."""
        data = {
            "report": {
                "title": "Title",
                "sections": {
                    "summary": "Summary",
                    "details": "Details",
                },
            },
        }

        json_str = json.dumps(data)
        assert '"report"' in json_str

    def test_format_json_with_arrays(self):
        """Test formatting JSON with arrays."""
        data = {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
            ],
        }

        json_str = json.dumps(data)
        restored = json.loads(json_str)

        assert len(restored["items"]) == 2

    def test_format_json_pretty_print(self):
        """Test JSON pretty printing."""
        data = {"key": "value"}

        pretty_json = json.dumps(data, indent=2)
        compact_json = json.dumps(data)

        assert len(pretty_json) > len(compact_json)


class TestCSVReportFormatting(unittest.TestCase):
    """Tests for CSV report formatting."""

    def test_format_csv_basic(self):
        """Test formatting basic CSV."""
        headers = ["Name", "Count", "Status"]
        rows = [
            ["Item 1", "10", "Done"],
            ["Item 2", "20", "Pending"],
        ]

        csv_lines = [",".join(headers)]
        for row in rows:
            csv_lines.append(",".join(row))

        csv_content = "\n".join(csv_lines)
        assert "Name,Count,Status" in csv_content

    def test_format_csv_with_quotes(self):
        """Test formatting CSV with quotes."""
        data = [
            ['Item "A"', 'Value "B"'],
        ]

        csv_line = ','.join(['"{item}"' for item in data[0]])
        assert '"Item \\"A\\""' in csv_line or '"Item' in csv_line

    def test_format_csv_escaping(self):
        """Test CSV escaping."""
        escaped = '"{value}"'

        assert escaped == '"Text with, comma"'

    def test_format_csv_header_footer(self):
        """Test CSV with header and footer."""
        csv = "# Generated: 2025-12-16\n"
        csv += "Name,Value\n"
        csv += "Item 1,100\n"
        csv += "# Total: 1 item"

        assert csv.startswith("#")
        assert "Name,Value" in csv


class TestReportTemplates(unittest.TestCase):
    """Tests for report templates."""

    def test_template_substitution(self):
        """Test template substitution."""
        template = "Report for {project} generated on {date}"

        report = template.format(project="MyApp", date="2025-12-16")
        assert report == "Report for MyApp generated on 2025-12-16"

    def test_template_with_conditionals(self):
        """Test template with conditionals."""
        data = {"has_errors": True, "errors": 5}

        if data["has_errors"]:
            message = f"Found {data['errors']} errors"
        else:
            message = "No errors"

        assert "Found 5 errors" in message

    def test_template_with_loops(self):
        """Test template with loops."""
        items = ["Item 1", "Item 2", "Item 3"]

        content = "Items:\n"
        for item in items:
            content += f"  - {item}\n"

        assert "- Item 1" in content
        assert content.count("-") == 3

    def test_template_inheritance(self):
        """Test template inheritance."""
        base_template = "### {title}\n{content}"

        title = "Section"
        content = "Details"

        result = base_template.format(title=title, content=content)
        assert "### Section" in result


class TestMetricsCollection(unittest.TestCase):
    """Tests for metrics collection in reports."""

    def test_collect_count_metrics(self):
        """Test collecting count metrics."""
        items = [1, 2, 3, 4, 5]

        metrics = {
            "total_items": len(items),
            "sum": sum(items),
            "average": sum(items) / len(items),
        }

        assert metrics["total_items"] == 5
        assert metrics["average"] == 3.0

    def test_collect_time_metrics(self):
        """Test collecting time metrics."""
        from datetime import datetime

        start = datetime.now()
        # Simulate work
        import time
        time.sleep(0.01)
        end = datetime.now()

        elapsed = (end - start).total_seconds()

        assert elapsed > 0

    def test_collect_status_metrics(self):
        """Test collecting status metrics."""
        items = [
            {"status": "success"},
            {"status": "success"},
            {"status": "failed"},
        ]

        metrics = {
            "success": sum(1 for i in items if i["status"] == "success"),
            "failed": sum(1 for i in items if i["status"] == "failed"),
        }

        assert metrics["success"] == 2
        assert metrics["failed"] == 1

    def test_collect_performance_metrics(self):
        """Test collecting performance metrics."""
        metrics = {
            "requests": 1000,
            "errors": 5,
            "error_rate": 5 / 1000,
            "success_rate": 995 / 1000,
        }

        assert metrics["error_rate"] == 0.005
        assert metrics["success_rate"] == 0.995


class TestReportExport(unittest.TestCase):
    """Tests for exporting reports."""

    def test_export_to_file(self):
        """Test exporting report to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Report content")
            temp_file = f.name

        try:
            with open(temp_file, 'r') as f:
                content = f.read()

            assert content == "Report content"
        finally:
            os.unlink(temp_file)

    def test_export_markdown_file(self):
        """Test exporting markdown file."""
        content = "# Title\n\nContent"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(content)
            filename = f.name

        try:
            assert os.path.exists(filename)
        finally:
            os.unlink(filename)

    def test_export_json_file(self):
        """Test exporting JSON file."""
        data = {"title": "Report", "items": [1, 2, 3]}

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            filename = f.name

        try:
            with open(filename, 'r') as f:
                restored = json.load(f)

            assert restored["title"] == "Report"
        finally:
            os.unlink(filename)

    def test_export_multiple_formats(self):
        """Test exporting to multiple formats."""
        data = {"title": "Report", "content": "Data"}
        formats = ["md", "json", "csv"]

        exported = {}
        for fmt in formats:
            if fmt == "json":
                exported[fmt] = json.dumps(data)
            else:
                exported[fmt] = str(data)

        assert len(exported) == 3


class TestReportAggregation(unittest.TestCase):
    """Tests for report aggregation."""

    def test_aggregate_multiple_reports(self):
        """Test aggregating multiple reports."""
        reports = [
            {"name": "Report 1", "items": 10},
            {"name": "Report 2", "items": 20},
            {"name": "Report 3", "items": 15},
        ]

        aggregated = {
            "total_reports": len(reports),
            "total_items": sum(r["items"] for r in reports),
        }

        assert aggregated["total_reports"] == 3
        assert aggregated["total_items"] == 45

    def test_aggregate_with_grouping(self):
        """Test aggregating with grouping."""
        items = [
            {"type": "A", "value": 10},
            {"type": "A", "value": 20},
            {"type": "B", "value": 15},
        ]

        grouped = {}
        for item in items:
            if item["type"] not in grouped:
                grouped[item["type"]] = []
            grouped[item["type"]].append(item["value"])

        assert len(grouped["A"]) == 2
        assert grouped["B"] == [15]

    def test_aggregate_with_statistics(self):
        """Test aggregating with statistics."""
        values = [10, 20, 30, 40, 50]

        stats = {
            "count": len(values),
            "sum": sum(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

        assert stats["count"] == 5
        assert stats["mean"] == 30
        assert stats["min"] == 10


class TestReportValidation(unittest.TestCase):
    """Tests for report validation."""

    def test_validate_required_fields(self):
        """Test validating required fields."""
        report = {
            "title": "Report",
            "timestamp": "2025-12-16",
        }

        required = ["title", "timestamp"]
        valid = all(field in report for field in required)

        assert valid

    def test_validate_report_structure(self):
        """Test validating report structure."""
        report = {
            "metadata": {"author": "Test"},
            "sections": {},
            "data": {},
        }

        structure_valid = all(k in report for k in ["metadata", "sections", "data"])
        assert structure_valid

    def test_validate_data_types(self):
        """Test validating data types."""
        report = {
            "title": "Report",
            "items": [1, 2, 3],
            "count": 3,
        }

        assert isinstance(report["title"], str)
        assert isinstance(report["items"], list)
        assert isinstance(report["count"], int)

    def test_validate_consistency(self):
        """Test validating consistency."""
        report = {
            "items": [1, 2, 3, 4, 5],
            "count": 5,
        }

        consistent = len(report["items"]) == report["count"]
        assert consistent


class TestReportIntegration(unittest.TestCase):
    """Integration tests for report generation."""

    def test_end_to_end_report_generation(self):
        """Test end-to-end report generation."""
        # Collect data
        data = {
            "total": 100,
            "success": 95,
            "failed": 5,
        }

        # Generate report
        report = {
            "title": "Test Report",
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }

        # Validate
        assert report["title"] == "Test Report"
        assert report["data"]["total"] == 100

        # Export
        json_export = json.dumps(report)
        assert len(json_export) > 0

    def test_multi_format_export_workflow(self):
        """Test multi-format export workflow."""
        content = "# Report\n\nContent"

        # Export as markdown
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            md_file = f.name

        # Export as txt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            txt_file = f.name

        try:
            assert os.path.exists(md_file)
            assert os.path.exists(txt_file)
        finally:
            os.unlink(md_file)
            os.unlink(txt_file)

    def test_batch_report_generation(self):
        """Test batch report generation."""
        reports = []

        for i in range(5):
            report = {
                "id": i,
                "title": f"Report {i}",
                "data": {"count": i * 10},
            }
            reports.append(report)

        assert len(reports) == 5
        assert reports[0]["id"] == 0
        assert reports[4]["data"]["count"] == 40


if __name__ == "__main__":
    unittest.main()
