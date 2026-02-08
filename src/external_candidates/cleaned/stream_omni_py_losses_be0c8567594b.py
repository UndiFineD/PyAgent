# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\stream_omni.py\cosyvoice.py\examples.py\magicdata_read.py\cosyvoice.py\cosyvoice.py\utils.py\losses_be0c8567594b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\CosyVoice\examples\magicdata-read\cosyvoice\cosyvoice\utils\losses.py

import torch

import torch.nn.functional as F


def tpr_loss(disc_real_outputs, disc_generated_outputs, tau):

    loss = 0

    for dr, dg in zip(disc_real_outputs, disc_generated_outputs):
        m_DG = torch.median((dr - dg))

        L_rel = torch.mean((((dr - dg) - m_DG) ** 2)[dr < dg + m_DG])

        loss += tau - F.relu(tau - L_rel)

    return loss


def mel_loss(real_speech, generated_speech, mel_transforms):

    loss = 0

    for transform in mel_transforms:
        mel_r = transform(real_speech)

        mel_g = transform(generated_speech)

        loss += F.l1_loss(mel_g, mel_r)

    return loss
