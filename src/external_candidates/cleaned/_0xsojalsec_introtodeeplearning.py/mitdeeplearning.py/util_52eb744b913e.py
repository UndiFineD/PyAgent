# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-introtodeeplearning\mitdeeplearning\util.py
import time
from string import Formatter

import matplotlib.pyplot as plt
import numpy as np
from IPython import display as ipythondisplay


def display_model(model):
    import tensorflow as tf

    tf.keras.utils.plot_model(model, to_file="tmp.png", show_shapes=True)
    return ipythondisplay.Image("tmp.png")


def plot_sample(x, y, vae, backend="tf"):
    """Plot original and reconstructed images side by side.

    Args:
        x: Input images array of shape [B, H, W, C] (TF) or [B, C, H, W] (PT)
        y: Labels array of shape [B] where 1 indicates a face
        vae: VAE model (TensorFlow or PyTorch)
        framework: 'tf' or 'pt' indicating which framework to use
    """
    plt.figure(figsize=(2, 1))

    if backend == "tf":
        idx = np.where(y == 1)[0][0]
        _, _, _, recon = vae(x)
        recon = np.clip(recon, 0, 1)

    elif backend == "pt":
        import torch

        y = y.detach().cpu().numpy()
        face_indices = np.where(y == 1)[0]
        idx = face_indices[0] if len(face_indices) > 0 else 0

        with torch.inference_mode():
            _, _, _, recon = vae(x)
        recon = torch.clamp(recon, 0, 1)
        recon = recon.permute(0, 2, 3, 1).detach().cpu().numpy()
        x = x.permute(0, 2, 3, 1).detach().cpu().numpy()

    else:
        raise ValueError("framework must be 'tf' or 'pt'")

    plt.subplot(1, 2, 1)
    plt.imshow(x[idx])
    plt.grid(False)

    plt.subplot(1, 2, 2)
    plt.imshow(recon[idx])
    plt.grid(False)

    if backend == "pt":
        plt.show()


class LossHistory:
    def __init__(self, smoothing_factor=0.0):
        self.alpha = smoothing_factor
        self.loss = []

    def append(self, value):
        self.loss.append(self.alpha * self.loss[-1] + (1 - self.alpha) * value if len(self.loss) > 0 else value)

    def get(self):
        return self.loss


class PeriodicPlotter:
    def __init__(self, sec, xlabel="", ylabel="", scale=None):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.sec = sec
        self.scale = scale

        self.tic = time.time()

    def plot(self, data):
        if time.time() - self.tic > self.sec:
            plt.cla()

            if self.scale is None:
                plt.plot(data)
            elif self.scale == "semilogx":
                plt.semilogx(data)
            elif self.scale == "semilogy":
                plt.semilogy(data)
            elif self.scale == "loglog":
                plt.loglog(data)
            else:
                raise ValueError("unrecognized parameter scale {}".format(self.scale))

            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            ipythondisplay.clear_output(wait=True)
            ipythondisplay.display(plt.gcf())

            self.tic = time.time()


def create_grid_of_images(xs, size=(5, 5)):
    """Combine a list of images into a single image grid by stacking them into an array of shape `size`"""

    grid = []
    counter = 0
    for i in range(size[0]):
        row = []
        for j in range(size[1]):
            row.append(xs[counter])
            counter += 1
        row = np.hstack(row)
        grid.append(row)
    grid = np.vstack(grid)
    return grid
