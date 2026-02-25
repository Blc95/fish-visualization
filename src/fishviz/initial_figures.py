# src/fishviz/initial_figures.py
from __future__ import annotations

from typing import Dict
import plotly.graph_objects as go

from fishviz.data import DataBundle
from fishviz.figures.charts import (
    create_histogram_all_years,
    create_histogram_top_catchers,
    create_stacked_area_chart,
    create_sunburst_chart,
    create_violin_plot_length,
)

def make_initial_figures(bundle: DataBundle) -> Dict[str, go.Figure]:
    """
    Build the figures used for the first paint (before any callbacks run).
    """
    summary = bundle.summary_df

    return {
        "sunburst": create_sunburst_chart(summary),
        "hist_all_years": create_histogram_all_years(summary, None),
        "hist_top_catchers": create_histogram_top_catchers(summary),
        "stacked_area": create_stacked_area_chart(summary),
        "violin": create_violin_plot_length(summary),
    }
