# report_gen

**File**: `src\logic\agents\security\scanners\mobile\apk_deeplens\report_gen.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 521  
**Complexity**: 19 (moderate)

## Overview

Python module containing implementation for report_gen.

## Classes (2)

### `util`

A static class for which contain some useful variables and methods

**Methods** (2):
- `mod_print(text_output, color)`
- `mod_log(text, color)`

### `ReportGen`

**Inherits from**: object

Class ReportGen implementation.

**Methods** (17):
- `__init__(self, apk_name, manifest, res_path, source_path, template_path, out_path)`
- `render_template(self, template_name, datas, escape)`
- `list_to_html(self, list_items)`
- `grenerate_html_report(self, report, html_report_path)`
- `load_template(self, template_path)`
- `grep_keyword(self, keyword, txt_ouput)`
- `add_sundarta_for_grep(self, grep_result, regexp)`
- `add_html_tag(self, grep_result, regexp)`
- `get_build_information(self)`
- `extract_permissions(self, manifest)`
- ... and 7 more methods

## Dependencies

**Imports** (7):
- `datetime`
- `json`
- `logging`
- `os`
- `re`
- `subprocess`
- `xhtml2pdf.pisa`

---
*Auto-generated documentation*
