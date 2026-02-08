# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-make-circuit-boards\src\atopile\kicad_plugin\reloadgroup.py
import logging
from pathlib import Path

import pcbnew

from .common import (
    footprints_by_uuid,
    get_footprint_uuid,
    get_layout_map,
    groups_by_name,
)

log = logging.getLogger(__name__)


class ReloadGroup(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Reload Group"
        self.category = "Reload Group Layout Atopile"
        self.description = "Layout components on PCB in same spatial relationships as components on schematic"
        self.show_toolbar_button = True
        self.icon_file_name = str(Path(__file__).parent / "reload.png")
        self.dark_icon_file_name = self.icon_file_name

    def Run(self):
        board: pcbnew.BOARD = pcbnew.GetBoard()
        board_path = board.GetFileName()

        existing_groups = groups_by_name(board)
        footprints = footprints_by_uuid(board)

        for group_name, group_data in get_layout_map(board_path).items():
            # If the group doesn't yet exist in the layout
            # create it and add it to the board
            if group_name in existing_groups:
                g = existing_groups[group_name]
            else:
                g = pcbnew.PCB_GROUP(board)
                g.SetName(group_name)
                board.Add(g)

            # Make sure all the footprints in the group are up to date
            footprints_in_group = {get_footprint_uuid(fp) for fp in g.GetItems() if isinstance(fp, pcbnew.FOOTPRINT)}
            expected_footprints = set(group_data["uuid_map"].keys())
            for fp_uuid in footprints_in_group - expected_footprints:
                g.RemoveItem(footprints[fp_uuid])
            for fp_uuid in expected_footprints - footprints_in_group:
                g.AddItem(footprints[fp_uuid])


ReloadGroup().register()
