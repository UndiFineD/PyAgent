# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_videos.py\_2018.py\eop.py\chapter1.py\just_randy_flipping_coin_95c161e61526.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-videos\_2018\eop\chapter1\just_randy_flipping_coin.py

from _2018.eop.reusable_imports import *

from manim_imports_ext import *


class JustFlipping(Scene):
    def construct(self):
        randy = CoinFlippingPiCreature(color=MAROON_E, flip_height=1).shift(2 * DOWN)

        self.add(randy)

        self.wait(2)

        for i in range(10):
            self.wait()

            self.play(FlipCoin(randy))


class JustFlippingWithResults(Scene):
    def construct(self):
        randy = CoinFlippingPiCreature(color=MAROON_E, flip_height=1).shift(2 * DOWN)

        self.add(randy)

        self.wait(2)

        for i in range(10):
            self.wait()

            self.play(FlipCoin(randy))

            result = random.choice(["H", "T"])

            if result == "H":
                coin = UprightHeads().scale(3)

            else:
                coin = UprightTails().scale(3)

            coin.move_to(2 * UP + 2.5 * LEFT + i * 0.6 * RIGHT)

            self.play(FadeIn(coin))
