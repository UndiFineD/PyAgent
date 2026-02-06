# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\vid_rhythm\rhythm_detector.py
import json
import os

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from environment.agents.base import BaseTool
from pydantic import BaseModel, Field
from scipy.signal import find_peaks


class RhythmDetector(BaseTool):
    """
    Application scenario: Rhythm-cut music video creating
    Agent that analyzes music file to detect rhythm points.
    It creates cut points for video editing based on music rhythms.
    """

    def __init__(self):
        super().__init__()
        self.frame_length = 2048
        self.hop_length = 512
        self.audio_data = None
        self.sr = None
        self.last_analysis = None
        self.audio_file_path = None
        self.base_filename = None

    class InputSchema(BaseTool.BaseInputSchema):
        audio_path: str = Field(
            ..., description="File path to the audio to be analyzed"
        )

    class OutputSchema(BaseModel):
        rhythm_analysis_dir: str = Field(
            ..., description="Directory containing audio rhythm analysis results"
        )

    def _load_audio(self, audio_file):
        """
        Load an audio file for analysis.

        Args:
            audio_file (str): Path to the audio file

        Returns:
            bool: True if loading was successful
        """
        try:
            self.audio_data, self.sr = librosa.load(audio_file, sr=None)
            self.audio_file_path = audio_file
            self.base_filename = os.path.splitext(os.path.basename(audio_file))[0]
            return True
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False

    def _detect_rhythm_points(
        self,
        energy_threshold=0.2,
        min_interval=0.2,
        smoothing_window=5,
        mask_ranges=None,
    ):
        """
        Detect rhythm points in the loaded audio.

        Args:
            energy_threshold (float): Threshold for peak detection
            min_interval (float): Minimum time between detected points (seconds)
            smoothing_window (int): Window size for smoothing the RMS curve
            mask_ranges (list): List of (start, end) tuples for masking detection

        Returns:
            dict: Rhythm detection results
        """
        if self.audio_data is None:
            print("No audio loaded. Please load an audio file first.")
            return None

        # Calculate RMS energy
        rms = librosa.feature.rms(
            y=self.audio_data,
            frame_length=self.frame_length,
            hop_length=self.hop_length,
        )[0]

        # Normalize RMS
        rms_normalized = rms / np.max(rms)

        # Apply smoothing
        if smoothing_window > 1:
            kernel = np.ones(smoothing_window) / smoothing_window
            rms_normalized = np.convolve(rms_normalized, kernel, mode="same")

        # Find peaks
        min_samples_interval = int(min_interval * self.sr / self.hop_length)
        peaks, _ = find_peaks(
            rms_normalized, height=energy_threshold, distance=min_samples_interval
        )

        # Convert peaks to timestamps
        timestamps = librosa.frames_to_time(
            peaks, sr=self.sr, hop_length=self.hop_length
        )

        # Apply masking if provided
        if mask_ranges is not None and len(mask_ranges) > 0:
            # Filter out timestamps that fall within masked ranges
            filtered_timestamps = []
            masked_timestamps = []

            for ts in timestamps:
                is_masked = False
                for start_time, end_time in mask_ranges:
                    if start_time <= ts <= end_time:
                        is_masked = True
                        masked_timestamps.append(ts)
                        break

                if not is_masked:
                    filtered_timestamps.append(ts)

            print(f"Masked out {len(masked_timestamps)} rhythm points.")
            timestamps = np.array(filtered_timestamps)

        # Create results dictionary
        rhythm_points = []
        for i, timestamp in enumerate(timestamps):
            rhythm_points.append({"id": i + 1, "timestamp": round(timestamp, 3)})

        result = {"beat_data": {"count": len(rhythm_points), "beats": rhythm_points}}

        # If masking was applied, add it to the result
        if mask_ranges is not None and len(mask_ranges) > 0:
            result["mask_ranges"] = [
                {"start": start, "end": end} for start, end in mask_ranges
            ]

        # Calculate times for plotting
        times = librosa.frames_to_time(
            np.arange(len(rms_normalized)), sr=self.sr, hop_length=self.hop_length
        )

        # Store analysis for later use
        self.last_analysis = {
            "rms_normalized": rms_normalized,
            "times": times,
            "timestamps": timestamps,
            "energy_threshold": energy_threshold,
            "mask_ranges": mask_ranges,
        }

        return result

    def _plot_rhythm_detection(
        self, figsize=(15, 12), show_plot=False, save_path=None, dpi=300
    ):
        """
        Plot the rhythm detection results.

        Args:
            figsize (tuple): Figure size
            show_plot (bool): Whether to display the plot
            save_path (str): Path to save the plot
            dpi (int): DPI for the saved plot

        Returns:
            bool: True if plotting was successful
        """
        if self.last_analysis is None:
            print("No analysis available. Please run detect_rhythm_points first.")
            return False

        rms_normalized = self.last_analysis["rms_normalized"]
        times = self.last_analysis["times"]
        timestamps = self.last_analysis["timestamps"]
        energy_threshold = self.last_analysis["energy_threshold"]
        mask_ranges = self.last_analysis["mask_ranges"]

        plt.figure(figsize=figsize)

        # Plot waveform
        plt.subplot(3, 1, 1)
        librosa.display.waveshow(self.audio_data, sr=self.sr, alpha=0.6)
        plt.vlines(timestamps, -1, 1, color="r", linestyle="--", label="Rhythm Points")

        # Highlight masked regions if provided
        if mask_ranges is not None:
            for start_time, end_time in mask_ranges:
                plt.axvspan(start_time, end_time, color="gray", alpha=0.3)

        plt.title("Waveform with Detected Rhythm Points")
        plt.ylabel("Amplitude")
        plt.legend()

        # Plot RMS energy
        plt.subplot(3, 1, 2)
        plt.plot(times, rms_normalized, label="RMS Energy")
        plt.vlines(timestamps, 0, 1, color="r", linestyle="--", label="Rhythm Points")
        plt.axhline(
            y=energy_threshold,
            color="g",
            linestyle="-",
            label=f"Threshold ({energy_threshold})",
        )

        # Highlight masked regions if provided
        if mask_ranges is not None:
            for start_time, end_time in mask_ranges:
                label = "Masked Region" if start_time == mask_ranges[0][0] else ""
                plt.axvspan(start_time, end_time, color="gray", alpha=0.3, label=label)

        plt.title("RMS Energy")
        plt.ylabel("Normalized Energy")
        plt.legend()

        # Plot spectrogram
        plt.subplot(3, 1, 3)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.audio_data)), ref=np.max)
        librosa.display.specshow(D, sr=self.sr, x_axis="time", y_axis="log")
        plt.colorbar(format="%+2.0f dB")
        plt.vlines(timestamps, 0, self.sr / 2, color="r", linestyle="--", alpha=0.7)

        # Highlight masked regions if provided
        if mask_ranges is not None:
            for start_time, end_time in mask_ranges:
                plt.axvspan(start_time, end_time, color="gray", alpha=0.3)

        plt.title("Spectrogram with Rhythm Points")
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (s)")

        plt.tight_layout()

        # Save plot if path is provided
        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches="tight")
            print(f"Plot saved to {save_path}")

        # Show plot if requested
        if show_plot:
            plt.show()
        else:
            plt.close()

        return True

    def _analyze_rhythm_distribution(self, show_plot=True, save_path=None, dpi=300):
        """
        Analyze the distribution of rhythm intervals.

        Args:
            show_plot (bool): Whether to display the plot
            save_path (str): Path to save the plot
            dpi (int): DPI for the saved plot

        Returns:
            dict: Statistics about the rhythm distribution
        """
        if self.last_analysis is None:
            print("No analysis available. Please run detect_rhythm_points first.")
            return None

        timestamps = self.last_analysis["timestamps"]

        if len(timestamps) < 2:
            print("Not enough rhythm points to analyze intervals.")
            return None

        intervals = np.diff(timestamps)

        plt.figure(figsize=(12, 6))

        # Histogram of intervals
        plt.subplot(1, 2, 1)
        plt.hist(intervals, bins=20, alpha=0.7)
        plt.axvline(
            np.mean(intervals),
            color="r",
            linestyle="--",
            label=f"Mean: {np.mean(intervals):.3f}s",
        )
        plt.axvline(
            np.median(intervals),
            color="g",
            linestyle="-",
            label=f"Median: {np.median(intervals):.3f}s",
        )
        plt.title("Histogram of Rhythm Intervals")
        plt.xlabel("Interval (s)")
        plt.ylabel("Count")
        plt.legend()

        # Plot the intervals over time
        plt.subplot(1, 2, 2)
        plt.plot(timestamps[:-1], intervals, "o-")
        plt.axhline(
            np.mean(intervals), color="r", linestyle="--", label=f"Mean Interval"
        )
        plt.title("Rhythm Intervals Over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Interval (s)")
        plt.legend()

        plt.tight_layout()

        # Save plot if path is provided
        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches="tight")
            print(f"Rhythm distribution plot saved to {save_path}")

        # Show plot if requested
        if show_plot:
            plt.show()
        else:
            plt.close()

        # Calculate statistics
        statistics = {
            "mean": float(np.mean(intervals)),
            "median": float(np.median(intervals)),
            "min": float(np.min(intervals)),
            "max": float(np.max(intervals)),
            "std_dev": float(np.std(intervals)),
        }

        print(f"Interval Statistics:")
        print(f"  Mean: {statistics['mean']:.3f}s")
        print(f"  Median: {statistics['median']:.3f}s")
        print(f"  Min: {statistics['min']:.3f}s")
        print(f"  Max: {statistics['max']:.3f}s")
        print(f"  Std Dev: {statistics['std_dev']:.3f}s")

        return statistics

    def _save_rhythm_points(self, output_file=None):
        """
        Save rhythm points to a JSON file.

        Args:
            output_file (str): Path to save the JSON file. If None, uses the base filename.

        Returns:
            bool: True if saving was successful
        """
        if self.last_analysis is None:
            print("No analysis available. Please run detect_rhythm_points first.")
            return False

        if output_file is None:
            # Create directory if it doesn't exist
            os.makedirs("music_analysis", exist_ok=True)
            output_file = f"music_analysis/{self.base_filename}_rhythm_points.json"

        timestamps = self.last_analysis["timestamps"]
        mask_ranges = self.last_analysis["mask_ranges"]

        # Create results dictionary
        rhythm_points = []
        for i, timestamp in enumerate(timestamps):
            rhythm_points.append({"id": i + 1, "timestamp": round(float(timestamp), 3)})

        result = {"beat_data": {"count": len(rhythm_points), "beats": rhythm_points}}

        # If masking was applied, add it to the result
        if mask_ranges is not None and len(mask_ranges) > 0:
            result["mask_ranges"] = [
                {"start": start, "end": end} for start, end in mask_ranges
            ]

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Rhythm points saved to {output_file}")

        return True

    def execute(self, **kwargs):
        """
        Run the complete music analysis pipeline to detect rhythm points and create visualizations.
        """
        # Validate input parameters
        params = self.InputSchema(**kwargs)

        energy_threshold = 0.4
        min_interval = 3.0
        smoothing_window = 5
        mask_start_time = 0.0
        mask_end_time = 5.0

        # Define paths for music data and analysis
        current_dir = os.getcwd()
        video_edit_dir = os.path.join(current_dir, "dataset/video_edit")
        rhythm_analysis_dir = os.path.join(video_edit_dir, "audio_analysis")

        # Create directory if it doesn't exist
        os.makedirs(rhythm_analysis_dir, exist_ok=True)

        print(f"Saving analysis results to: {rhythm_analysis_dir}")

        # Resolve the audio file path
        audio_file = os.path.join(current_dir, params.audio_path)

        # Ensure the audio file exists
        if not os.path.exists(audio_file):
            print(f"Error: Audio file '{audio_file}' does not exist")
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        print(f"Analyzing music file: {os.path.basename(audio_file)}")

        if not self._load_audio(audio_file):
            print(f"Error: Could not load audio file '{audio_file}'")
            raise RuntimeError(f"Failed to load audio file: {audio_file}")

        # Define mask ranges - times in seconds where you don't want to detect rhythm points
        mask_ranges = [(mask_start_time, mask_end_time)]

        # Detect rhythm points
        rhythm_data = self._detect_rhythm_points(
            energy_threshold=energy_threshold,
            min_interval=min_interval,
            smoothing_window=smoothing_window,
            mask_ranges=mask_ranges,
        )

        # Print results
        print(f"Detected {rhythm_data['beat_data']['count']} rhythm points.")

        # Plot and save results
        plot_path = os.path.join(rhythm_analysis_dir, "rhythm_detection.png")
        self._plot_rhythm_detection(show_plot=False, save_path=plot_path, dpi=300)

        # Analyze rhythm distribution and save
        distribution_path = os.path.join(rhythm_analysis_dir, "rhythm_distribution.png")
        self._analyze_rhythm_distribution(
            show_plot=False, save_path=distribution_path, dpi=300
        )

        # Save to JSON
        json_path = os.path.join(rhythm_analysis_dir, "cut_points.json")
        self._save_rhythm_points(json_path)

        print(f"Analysis complete! Results saved to {rhythm_analysis_dir}")

        return {"rhythm_analysis_dir": rhythm_analysis_dir}
