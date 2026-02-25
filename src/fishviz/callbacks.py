# src/fishviz/callbacks.py
from __future__ import annotations

import dash
from dash import html
from dash.dependencies import Input, Output, State

from fishviz.data import DataBundle
from fishviz.figures.charts import (
    create_histogram_all_creeks_all_years,
    create_histogram_all_creeks_specific_year,
    create_histogram_all_years,
    create_histogram_specific_year,
    create_histogram_top_catchers,
    create_stacked_area_chart,
    create_sunburst_chart,
    create_violin_plot_length,
)


def register_callbacks(app: dash.Dash, bundle: DataBundle) -> None:
    # -------------------------
    # Map click -> selected zone
    # -------------------------
    @app.callback(
        Output("selected-zone", "data"),
        Input("geojson-layer", "clickData"),
    )
    def update_selected_zone(clickData):
        if clickData and "points" in clickData and clickData["points"]:
            return clickData["points"][0]["location"].strip().lower()
        return None

    # -------------------------
    # Histogram (all years / year drilldown)
    # -------------------------
    @app.callback(
        Output("histogram-all-years", "figure"),
        Input("selected-zone", "data"),
        Input("selected-year", "data"),
    )
    def update_histogram(selected_zone, selected_year):
        if not selected_zone and selected_year == "All Years":
            return create_histogram_all_creeks_all_years(bundle.summary_df)

        if not selected_zone and selected_year != "All Years":
            return create_histogram_all_creeks_specific_year(bundle.summary_df, selected_year)

        if selected_zone and selected_year == "All Years":
            return create_histogram_all_years(bundle.summary_df, selected_zone)

        return create_histogram_specific_year(bundle.summary_df, selected_zone, selected_year)

    # -------------------------
    # Stacked area chart
    # -------------------------
    @app.callback(
        Output("stacked-area-chart", "figure"),
        Input("selected-zone", "data"),
        Input("selected-year", "data"),
    )
    def update_stacked_area(selected_zone, selected_year):
        return create_stacked_area_chart(
            bundle.summary_df,
            selected_zone=selected_zone,
            selected_year=selected_year,
        )

    # -------------------------
    # Sunburst chart
    # -------------------------
    @app.callback(
        Output("sunburst-chart", "figure"),
        Input("selected-zone", "data"),
        Input("selected-year", "data"),
    )
    def update_sunburst(selected_zone, selected_year):
        return create_sunburst_chart(
            bundle.summary_df,
            selected_zone=selected_zone,
            selected_year=selected_year,
        )

    # -------------------------
    # Top catchers histogram
    # -------------------------
    @app.callback(
        Output("histogram-top-catchers", "figure"),
        Input("selected-zone", "data"),
        Input("selected-year", "data"),
    )
    def update_top_catchers(selected_zone, selected_year):
        return create_histogram_top_catchers(
            bundle.summary_df,
            selected_zone=selected_zone,
            selected_year=selected_year,
        )

    # -------------------------
    # Click histogram bar -> selected year
    # -------------------------
    @app.callback(
        Output("selected-year", "data"),
        Input("histogram-all-years", "clickData"),
        prevent_initial_call=True,
    )
    def update_selected_year(clickData):
        if clickData and "points" in clickData and clickData["points"]:
            clicked_x = clickData["points"][0].get("x")
            try:
                return int(clicked_x)
            except (TypeError, ValueError):
                raise dash.exceptions.PreventUpdate
        raise dash.exceptions.PreventUpdate

    # -------------------------
    # Violin plot (length)
    # -------------------------
    @app.callback(
        Output("violin-plot-length", "figure"),
        Input("selected-zone", "data"),
        Input("selected-year", "data"),
    )
    def update_violin(selected_zone, selected_year):
        return create_violin_plot_length(
            bundle.summary_df,
            selected_zone=selected_zone,
            selected_year=selected_year,
        )

    # -------------------------
    # Offcanvas toggle + content
    # -------------------------
    @app.callback(
        Output("offcanvas", "is_open"),
        Output("offcanvas-content", "children"),
        Input("open-offcanvas", "n_clicks"),
        State("offcanvas", "is_open"),
        State("selected-zone", "data"),
        State("selected-year", "data"),
        prevent_initial_call=True,
    )
    def toggle_offcanvas(n_clicks, is_open, selected_zone, selected_year):
        is_open = not is_open

        zone_info = (
            f"Selected Zone: {selected_zone.capitalize()}"
            if selected_zone
            else "No zone selected"
        )
        year_info = f"Selected Year: {selected_year}" if selected_year else "All years selected"

        content = [
            html.P("Dynamic Information Panel"),
            html.P(zone_info),
            html.P(year_info),
            html.P("This panel provides dynamically updated information based on the current selections."),
        ]

        return is_open, content