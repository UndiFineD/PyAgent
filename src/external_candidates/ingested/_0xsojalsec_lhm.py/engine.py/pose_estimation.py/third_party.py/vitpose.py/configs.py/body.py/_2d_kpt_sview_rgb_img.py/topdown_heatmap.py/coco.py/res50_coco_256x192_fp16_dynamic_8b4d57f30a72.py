# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\configs\body\2d_kpt_sview_rgb_img\topdown_heatmap\coco\res50_coco_256x192_fp16_dynamic.py
_base_ = ["./res50_coco_256x192.py"]

# fp16 settings
fp16 = dict(loss_scale="dynamic")
