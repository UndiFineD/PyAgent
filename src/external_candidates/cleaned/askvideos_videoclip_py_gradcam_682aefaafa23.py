# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\askvideos_videoclip.py\video_llama.py\common.py\gradcam_682aefaafa23.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AskVideos-VideoCLIP\video_llama\common\gradcam.py

import numpy as np

from matplotlib import pyplot as plt

from scipy.ndimage import filters

from skimage import transform as skimage_transform

def getAttMap(img, attMap, blur=True, overlap=True):

    attMap -= attMap.min()

    if attMap.max() > 0:

        attMap /= attMap.max()

    attMap = skimage_transform.resize(attMap, (img.shape[:2]), order=3, mode="constant")

    if blur:

        attMap = filters.gaussian_filter(attMap, 0.02 * max(img.shape[:2]))

        attMap -= attMap.min()

        attMap /= attMap.max()

    cmap = plt.get_cmap("jet")

    attMapV = cmap(attMap)

    attMapV = np.delete(attMapV, 3, 2)

    if overlap:

        attMap = (

            1 * (1 - attMap**0.7).reshape(attMap.shape + (1,)) * img

            + (attMap**0.7).reshape(attMap.shape + (1,)) * attMapV

        )

    return attMap

