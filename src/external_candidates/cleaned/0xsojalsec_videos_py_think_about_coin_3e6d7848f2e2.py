# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_videos.py\_2018.py\eop.py\chapter1.py\think_about_coin_3e6d7848f2e2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-videos\_2018\eop\chapter1\think_about_coin.py

from _2018.eop.reusable_imports import *

from manim_imports_ext import *


class RandyThinksAboutCoin(PiCreatureScene):
    def construct(self):

        randy = self.get_primary_pi_creature()

        randy.center()

        self.add(randy)

        self.wait()

        h_or_t = BinaryOption(UprightHeads().scale(3), UprightTails().scale(3), text_scale=1.5)

        self.think(h_or_t, direction=LEFT)

        v = 0.3

        self.play(
            h_or_t[0].shift,
            v * UP,
            h_or_t[2].shift,
            v * DOWN,
        )

        self.play(
            h_or_t[0].shift,
            2 * v * DOWN,
            h_or_t[2].shift,
            2 * v * UP,
        )

        self.play(
            h_or_t[0].shift,
            v * UP,
            h_or_t[2].shift,
            v * DOWN,
        )

        self.wait()
