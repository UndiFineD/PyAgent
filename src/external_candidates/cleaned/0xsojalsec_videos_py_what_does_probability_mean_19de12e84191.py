# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_videos.py\_2018.py\eop.py\what_does_probability_mean_19de12e84191.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-videos\_2018\eop\what_does_probability_mean.py

from manim_imports_ext import *


class WhatDoesItReallyMean(TeacherStudentsScene):
    CONFIG = {
        "default_pi_creature_kwargs": {
            "color": MAROON_E,
            "flip_at_start": True,
        },
    }

    def construct(self):

        student_q = OldTexText("What does", "``probability''", "\emph{actually}", "mean?")

        student_q.set_color_by_tex("probability", YELLOW)

        self.student_says(student_q, target_mode="sassy")

        self.wait()

        question_bubble = VGroup(student_q, students[1].bubble)

        scaled_qb = question_bubble.copy()

        scaled_qb.scale(0.4).to_corner(UL)

        self.play(Transform(question_bubble, scaled_qb))

        self.wait()

        self.teacher_says("Don't worry -- philosophy can come later!")

        self.wait()
