import os
import re

# List of files to fix
files_to_fix = [
    'src/observability/reports/export_format.py',
    'src/observability/reports/compile_result.py',
    'src/observability/reports/audit_entry.py',
    'src/observability/reports/audit_action.py',
    'src/observability/reports/annotation_manager.py',
    'src/observability/reports/aggregated_report.py',
    'src/observability/reports/access_controller.py',
    'src/observability/reports/validation_result.py',
    'src/observability/reports/subscription_manager.py',
    'src/observability/reports/subscription_frequency.py',
    'src/observability/reports/report_type.py',
    'src/observability/reports/report_template.py',
    'src/observability/reports/report_subscription.py',
    'src/observability/reports/report_search_result.py',
    'src/observability/reports/report_search_engine.py',
    'src/observability/reports/archived_report.py',
    'src/observability/reports/report_permission.py',
    'src/observability/reports/report_metric.py',
    'src/observability/reports/report_metadata.py',
    'src/observability/reports/report_localizer.py'
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()

        # Remove the erroneous docstring
        content = re.sub(r'"""Auto-extracted class from generate_agent_reports\.py"""', '', content)

        # Simple approach: find the first occurrence of a class/function and keep everything before the second occurrence
        lines = content.split('\n')
        class_count = 0
        cutoff_line = len(lines)

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(('class ', 'def ', '@dataclass')):
                class_count += 1
                if class_count == 2:
                    cutoff_line = i
                    break

        if cutoff_line < len(lines):
            content = '\n'.join(lines[:cutoff_line])

        with open(file_path, 'w') as f:
            f.write(content)

        print(f'Fixed {file_path}')

print('All files processed')