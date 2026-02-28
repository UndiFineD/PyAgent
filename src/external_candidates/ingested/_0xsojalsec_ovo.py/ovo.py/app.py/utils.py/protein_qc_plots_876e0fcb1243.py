# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\utils\protein_qc_plots.py
import json
import os
from typing import Callable, Dict, List

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from ovo import Descriptor
from ovo.core.logic.proteinqc_logic import get_cmap, get_descriptor_plot_setting
from ovo.core.utils.colors import darken

FLAG_ICONS = {
    "missing": ":material/question_mark:",
    "green": ":material/check_circle:",
    "yellow": ":material/warning:",
    "orange": ":material/error:",
}

SOURCE_OPTIONS = {
    "all": "PDB: All structures",
    "non-human_only": "PDB: Non-human only",
    "human_only": "PDB: Human only",
    "human+non-human": "PDB: Human or human-interacting",
    "short (<=100)": "PDB: Short (<= 100aa)",
    "medium (101-300)": "PDB: Medium length (101-300aa)",
    "long (301-1000)": "PDB: Long (301-1000aa)",
    "very long (>1000)": "PDB: Very long (> 1000aa)",
}


@st.cache_data()
def load_histograms() -> Dict[str, Dict[str, Dict[str, List[float]]]]:
    """
    Load precomputed PDB histograms for all tools.
    The histograms are computed for the data between 1st and 99th percentile.

    Returns:
    {'descriptor': {'all': {'x': [0, 1, 2, ...], 'y': [0.1, 0.2, ...]}, 'non-human_only': ..., 'human_only': ..., 'human+non-human}, ...}}}}
    x - bin edges
    y - bin heights
    """
    histograms = {}
    for toolname in [
        "esm_1v",
        "esm_if",
        "proteinsol",
        "sequence_composition",
        "protparams",
        "dssp",
        "length",
        "mdanalysis",
        "peppatch",
    ]:
        data = load_plots_data(f"histograms/pdb/{toolname}_q01_q99.json")
        histograms.update({f"proteinqc|{key}": value for key, value in data.items()})
    return histograms


def load_plots_data(file_path: str) -> dict:
    ovo_resources_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "resources")
    )
    with open(os.path.join(ovo_resources_path, file_path), "r") as f:
        data = json.load(f)
    return data


@st.cache_data
def get_histogram_alt(
    bins: np.ndarray,
    y: np.ndarray,
    color_by: str,
    thresholds: List[float] = None,
    reverse_colors: bool = False,
    width: int = None,
    height: int = None,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    value: float = None,
    value_label: str = None,
) -> alt.Chart:
    """
    Create Altair histogram from precomputed data.

    Args:
    bins: bin edges in the precomputed histograms
    y: bin heights in the precomputed histograms
    color_by: coloring method, one of 'reference', 'thresholds', 'plddt', 'rmsd', or other color schemes supported by get_cmap
    thresholds: list of thresholds for color_by='thresholds'
    reverse_colors: reverse the color scale
    width: width of the chart
    height: height of the chart
    title: title of the chart
    x_label: label for the x-axis
    y_label: label for the y-axis
    value: single value to highlight on the histogram
    value_label: label for the highlighted value
    """

    # Create DataFrame for Altair
    bin_centers = bins[:-1] + np.diff(bins) / 2
    total_height_sum = np.sum(y)  # Sum of heights for normalization
    data = pd.DataFrame(
        {
            "bin_center": bin_centers,
            "height": y,
            "normalized_height": y / total_height_sum,  # Normalized for color mapping
        }
    )
    max_height = data["normalized_height"].max()
    darken_factor = 1.2
    cmap: None | Callable = None
    if color_by == "reference":
        color = alt.value("#bbbbbb")
    elif (color_by == "thresholds" and thresholds is not None) or color_by in [
        "plddt",
        "rmsd",
    ]:
        # use colormap if applicable in histogram
        min_val = data["bin_center"].min()
        max_val = data["bin_center"].max()
        cmap = get_cmap(
            color_by, min_val, max_val, thresholds, reverse_colors=reverse_colors
        )
        data["flag_color"] = (
            data["bin_center"].apply(cmap).apply(darken, factor=darken_factor)
        )
        color = alt.Color("flag_color:N", legend=None, scale=None)
    else:
        color = alt.value("#444444")

    bar_width = min(5.0, 1 + 150 / len(bins))
    chart = (
        alt.Chart(data)
        .mark_bar(width=bar_width)
        .encode(
            x=alt.X("bin_center:Q", title=None, axis=alt.Axis(title=x_label)),
            y=alt.Y(
                "normalized_height:Q",
                axis=alt.Axis(title=y_label, labels=False, ticks=False, domain=False),
            ),  # Hide y axis label and ticks
            color=color,
            tooltip=[],
        )
    )

    if cmap:
        band_data = pd.DataFrame(
            {
                "x0": bins[:-1],
                "x1": bins[1:],
                "y0": max_height * -0.05,
                "y1": max_height * -0.09,
            }
        )
        band_data["color"] = (
            ((band_data["x0"] + band_data["x1"]) / 2)
            .apply(cmap)
            .apply(darken, factor=darken_factor)
        )
        gradient_band = (
            alt.Chart(band_data)
            .mark_rect(opacity=0.5)
            .encode(
                x="x0:Q",
                x2="x1:Q",
                y="y0:Q",
                y2="y1:Q",
                color=alt.Color("color:N", scale=None, legend=None),
                tooltip=[],
            )
        )

        chart = (chart + gradient_band).resolve_scale(color="independent")

    if value is not None:
        value_data = pd.DataFrame(
            {"x": [value], "y": [max_height * -0.15], "label": value_label}
        )
        triangle = (
            alt.Chart(value_data)
            .mark_point(shape="triangle-up", color="black", size=90, filled=True)
            .encode(x="x:Q", y="y:Q", tooltip=[])
        )

        chart = chart + triangle

        if value_label:
            align = "right" if value >= np.mean(bins) else "left"
            label = (
                alt.Chart(value_data)
                .mark_text(
                    align=align,
                    baseline="top",
                    fontSize=12,
                    dx=8 * (-1 if align == "right" else 1),
                )
                .encode(
                    x="x:Q",
                    y="y:Q",
                    text="label:N",
                    tooltip=[],
                )
            )
            chart = chart + label

    if title:
        chart = chart.properties(title=title)

    if width:
        chart = chart.properties(width=width)

    if height:
        chart = chart.properties(height=height)

    return chart


def update_bin_edges(
    values: List[float], bins: List[float], y: list[float]
) -> tuple[np.ndarray, np.ndarray]:
    """
    Given bins for a histogram and a list of values, extend the bins if the values are outside the range of the bins.
    """

    bin_width = np.diff(bins[:2])[0]

    min_bin = bins[0]
    max_bin = bins[-1]

    # If the second distribution has a wider range, extend the bins
    if (min_value := np.min(values)) < min_bin:
        # Create extra bins on the left
        extra_left = np.arange(min_bin - bin_width, min_value - bin_width, -bin_width)[
            ::-1
        ]
        bins = np.concatenate([extra_left, bins])
        y = np.concatenate([np.zeros(len(extra_left)), y])

    if (max_value := np.max(values)) > max_bin:
        # Create extra bins on the right
        extra_right = np.arange(max_bin + bin_width, max_value + bin_width, bin_width)
        bins = np.concatenate([bins, extra_right])
        y = np.concatenate([y, np.zeros(len(extra_right))])

    return bins, y


def descriptor_histograms(
    descriptor: Descriptor,
    histogram_source: str,
    values: List[float],
    value: float = None,
    value_label: str = None,
    color_by: str = "default",
    precomputed_histogram_height: int = 150,
    pool_histogram_height: int = 150,
    width: int = 600,
):
    """
    Create a combined histogram plot for a descriptor. The top histogram is the precomputed histogram and the bottom histogram is the pool histogram from the passed values.

    Parameters:
    descriptor (Descriptor): descriptor object
    histogram_source (str): Source of the histogram
    values (List[float]): Values for the pool/selected designs histogram
    value (float): Single value to highlight on the histogram
    value_label (str): Label for the highlighted value
    color_by (str): Color by 'thresholds', None, or values returned by get_descriptor_plot_setting
    precomputed_histogram_height (int): Height of the precomputed histogram
    pool_histogram_height (int): Height of the pool histogram
    width (int): Maximum width of the chart in pixels
    """
    thresholds, reverse_colors, default_color_by = get_descriptor_plot_setting(
        descriptor
    )
    if color_by == "default":
        color_by = default_color_by

    histograms = load_histograms()
    if descriptor.key not in histograms:
        bins = np.linspace(np.min(values), np.max(values), 50)
        fig1 = None
    else:
        data = histograms[descriptor.key][histogram_source]
        bins, ref_y = update_bin_edges(values, data["x"], data["y"])

        # Precomputed histogram
        fig1 = get_histogram_alt(
            bins=bins,
            y=ref_y,
            y_label="Reference",
            height=precomputed_histogram_height,
            width=width,
            color_by="reference",
        )

    fig2 = get_histogram_alt(
        bins=bins,
        y=np.histogram(values, bins)[0],
        x_label=descriptor.name,
        y_label="Designs",
        height=pool_histogram_height,
        width=width,
        color_by=color_by,
        thresholds=thresholds,
        reverse_colors=reverse_colors,
        value=value,
        value_label=value_label,
    )

    if not fig1:
        # Return only the pool histogram
        return fig2.properties(height=pool_histogram_height + 80).configure_axis(
            grid=False
        )
    # Stack the two histograms

    return (
        alt.vconcat(fig1, fig2)
        .resolve_legend(color="independent")
        .resolve_scale(
            x="shared",  # Share the x-axis scale between the two histograms
            y="independent",  # Independent y-axis to scale correctly
        )
        .configure_axis(grid=False)
    )


@st.cache_data
def format_threshold_value(descriptor_name: str, value) -> str | None:
    """
    Format the threshold values for display.

    If the descriptor is a percentage (0-1), multiply by 100 and add a percentage sign.
    If the descriptor is 'Sequence length', round to the nearest integer.
    Otherwise, round to two decimal places.
    """
    if pd.isna(value) or value == "":
        return None
    # TODO store this logic in the Descriptor object instead
    if "%" in descriptor_name:
        return f"{value:.2f} %"
    elif descriptor_name == "Sequence length":
        return f"{value:.0f}"
    else:
        return f"{value:.2f}"


def source_selectbox(value: str, key_prefix: str):
    options = list(SOURCE_OPTIONS)
    return st.selectbox(
        label="Reference distribution",
        format_func=SOURCE_OPTIONS.get,
        help="""
        Select the background distribution to compare the pool/selection distribution to.  
        The **"all"** option includes all PDB structures.  
        The **"non-human only"** option includes only non-human proteins.  
        The **"human only"** option includes only human proteins.  
        The **"human+non-human"** option includes proteins from human+non-human complexes.  
        The **"short"** (≤100), **"medium"** (101-300), **"long"** (301-1000), and **"very long"** (>1000) options include proteins with the corresponding sequence length.""",
        index=options.index(value) if value else 0,
        key=f"{key_prefix}_source",
        options=options,
    )
