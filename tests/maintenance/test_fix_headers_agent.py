import os
from pathlib import Path

import pytest

from src.maintenance.fix_headers.fix_headers_agent import FixHeadersAgent


def test_preserve_bom_and_encoding(tmp_path: Path):
    agent = FixHeadersAgent(dry_run=True)
    content = "\ufeff# -*- coding: utf-8 -*-\nprint(\"hi\")\n"

    out = agent.add_header(content)

    # BOM should be preserved and encoding comment must remain
    assert out.startswith(agent.HEADER_TEMPLATE)
    assert "coding: utf-8" in out
    assert out.count("\ufeff") == 1


def test_remove_old_license_but_preserve_other_comments(tmp_path: Path):
    agent = FixHeadersAgent(dry_run=True)
    old = (
        "#!/usr/bin/env python3\n"
        "# Copyright 2020 Someone\n"
        "# Licensed under the Apache License\n"
        "# NOTE: internal comment that should remain\n"
        "print(\"ok\")\n"
    )

    out = agent.add_header(old)

    assert "Copyright 2020" not in out
    assert agent.HEADER_TEMPLATE in out
    assert "# NOTE: internal comment that should remain" in out


def test_keep_unrelated_top_comment(tmp_path: Path):
    agent = FixHeadersAgent(dry_run=True)
    src = "# NOTE: temporary comment\nprint('x')\n"

    out = agent.add_header(src)

    # Unrelated top comment must be preserved
    assert "# NOTE: temporary comment" in out
    assert out.startswith(agent.HEADER_TEMPLATE)
