# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\recipes.py\ljspeech.py\hifigan.py\train_hifigan_c7b3f1b6c25a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\recipes\ljspeech\hifigan\train_hifigan.py

import os

from trainer import Trainer, TrainerArgs

from TTS.utils.audio import AudioProcessor

from TTS.vocoder.configs import HifiganConfig

from TTS.vocoder.datasets.preprocess import load_wav_data

from TTS.vocoder.models.gan import GAN

output_path = os.path.dirname(os.path.abspath(__file__))


def main():
    config = HifiganConfig(
        batch_size=32,
        eval_batch_size=16,
        num_loader_workers=4,
        num_eval_loader_workers=4,
        run_eval=True,
        test_delay_epochs=5,
        epochs=1000,
        seq_len=8192,
        pad_short=2000,
        use_noise_augment=True,
        eval_split_size=10,
        print_step=25,
        print_eval=False,
        mixed_precision=False,
        lr_gen=1e-4,
        lr_disc=1e-4,
        data_path=os.path.join(output_path, "../LJSpeech-1.1/wavs/"),
        output_path=output_path,
    )

    # init audio processor

    ap = AudioProcessor(**config.audio.to_dict())

    # load training samples

    eval_samples, train_samples = load_wav_data(config.data_path, config.eval_split_size)

    # init model

    model = GAN(config, ap)

    # init the trainer and 🚀

    trainer = Trainer(
        TrainerArgs(),
        config,
        output_path,
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
    )

    trainer.fit()


if __name__ == "__main__":
    main()
