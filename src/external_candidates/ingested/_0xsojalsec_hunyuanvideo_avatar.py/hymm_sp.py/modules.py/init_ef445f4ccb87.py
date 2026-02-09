# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-HunyuanVideo-Avatar\hymm_sp\modules\__init__.py
from .models_audio import HUNYUAN_VIDEO_CONFIG, HYVideoDiffusionTransformer


def load_model(args, in_channels, out_channels, factor_kwargs):
    model = HYVideoDiffusionTransformer(
        args,
        in_channels=in_channels,
        out_channels=out_channels,
        **HUNYUAN_VIDEO_CONFIG[args.model],
        **factor_kwargs,
    )
    return model
