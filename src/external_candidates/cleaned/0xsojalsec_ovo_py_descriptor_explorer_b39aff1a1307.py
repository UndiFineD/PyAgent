# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\app.py\components.py\descriptor_explorer_b39aff1a1307.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\components\descriptor_explorer.py

from dataclasses import dataclass

from typing import Dict

import numpy as np

import pandas as pd

import streamlit as st

from ovo.app.components.descriptor_scatterplot import format_descriptor_name

from ovo.app.utils.protein_qc_plots import (
    descriptor_histograms,
    format_threshold_value,
    source_selectbox,
)

from ovo.core.database.models import Descriptor


@dataclass
class HistogramSettings:
    descriptor: Descriptor | None = None

    source: str | None = None

    @classmethod
    def from_query_params(cls, descriptors_by_key: dict[str, Descriptor], key_prefix: str):

        return cls(
            descriptor=(
                descriptors_by_key[st.query_params[f"{key_prefix}_descriptor"]]
                if f"{key_prefix}_descriptor" in st.query_params and f"{key_prefix}_descriptor" in descriptors_by_key
                else None
            ),
            source=(st.query_params[f"{key_prefix}_source"] if f"{key_prefix}_source" in st.query_params else None),
        )

    def update_query_params(self, key_prefix: str):

        if self.descriptor:
            st.query_params[f"{key_prefix}_descriptor"] = self.descriptor.key

        else:
            st.query_params.pop(f"{key_prefix}_descriptor", None)

        if self.source:
            st.query_params[f"{key_prefix}_source"] = self.source

        else:
            st.query_params.pop(f"{key_prefix}_source", None)


@st.fragment()
def descriptor_explorer(
    descriptors_df: pd.DataFrame,
    descriptors_by_key: Dict[str, Descriptor],
    single_design: bool = False,
):

    if descriptors_df.empty:
        st.warning("No designs found")

        return

    if not descriptors_by_key:
        st.warning("No descriptors found for the selected designs.")

        return

    key_prefix = "design_expl" if single_design else "descriptor_expl"

    settings = HistogramSettings.from_query_params(descriptors_by_key, key_prefix)

    descriptor_col, source_col, _ = st.columns([2, 1, 1])

    # Select the descriptor to plot

    descriptor_options = list(descriptors_by_key.keys())

    with descriptor_col:
        descriptor = st.selectbox(
            "Descriptor",
            format_func=lambda descriptor_key: format_descriptor_name(descriptors_by_key[descriptor_key]),
            index=(descriptor_options.index(settings.descriptor.key) if settings.descriptor is not None else 0),
            key=f"{key_prefix}_descriptor",
            options=descriptor_options,
            # force_change=preset_changed,
        )

        settings.descriptor = descriptors_by_key.get(descriptor)

    with source_col:
        settings.source = source_selectbox(settings.source, key_prefix=key_prefix)

    if not settings.descriptor:
        st.warning("Please select a descriptor to plot.")

        return

    settings.update_query_params(key_prefix)

    descriptor_values = descriptors_df[(settings.descriptor.tool, settings.descriptor.name)]

    nonnull_descriptor_values = descriptor_values.dropna().tolist()

    # Write the descriptor description and thresholds

    st.write(f"*{settings.descriptor.description}*")

    if single_design:
        avg_col, warning_col, error_col = st.columns(3)

    else:
        avg_col, median_col, warning_col, error_col = st.columns(4)

    # If there are missing values, show warning message that the distribution is only for the non-missing values

    if len(descriptor_values) > len(nonnull_descriptor_values):
        perc_missing = (1 - len(nonnull_descriptor_values) / len(descriptor_values)) * 100

        st.warning(
            f"This descriptor is missing for **{perc_missing:.2f}%** of designs. The distribution was calculated from designs with non-missing values. You can submit **full ProteinQC** to calculate the descriptor for all designs.",
            icon=":material/warning:",
        )

    with avg_col:
        avg_value = np.mean(descriptor_values)

        avg_value = format_threshold_value(settings.descriptor.name, avg_value)

        label = (
            "" if single_design else "Average "
        ) + settings.descriptor.name  # f'Average {settings.descriptor.name}'

        st.metric(label, avg_value)

    if not single_design:
        with median_col:
            median_value = np.median(descriptor_values)

            median_value = format_threshold_value(settings.descriptor.name, median_value)

            st.metric(f"Median {settings.descriptor.name}", median_value)

    with warning_col:
        warning_value = format_threshold_value(settings.descriptor.name, settings.descriptor.warning_value)

        st.metric("Warning threshold", warning_value)

    with error_col:
        error_value = format_threshold_value(settings.descriptor.name, settings.descriptor.error_value)

        st.metric("Error threshold", error_value)

    fig = descriptor_histograms(
        descriptor=settings.descriptor,
        histogram_source=settings.source,
        values=descriptor_values,
        precomputed_histogram_height=200,
        pool_histogram_height=200,
    )

    st.altair_chart(
        fig,
        width="stretch" if single_design else "content",
        key=f"descriptor_histogram_{key_prefix}",
    )
