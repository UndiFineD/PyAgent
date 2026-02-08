# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_videos.py\_2018.py\eop.py\reusables.py\sick_pi_creature_a84a73f5f41d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-videos\_2018\eop\reusables\sick_pi_creature.py

from _2018.eop.reusables.eop_constants import *

from for_3b1b_videos.pi_creature import *


class SicklyPiCreature(PiCreature):
    CONFIG = {"sick_color": SICKLY_GREEN}

    def get_slightly_sick(self):

        self.save_state()

        self.set_color(self.sick_color)

    def get_sick(self):

        self.get_slightly_sick()

        self.change_mode("sick")

    def get_better(self):

        self.restore()
