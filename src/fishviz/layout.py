from dash import dcc, html


def make_layout(
    default_map_fig,
    sunburst_fig,
    hist_all_years_fig,
    hist_top_catchers_fig,
    stacked_area_fig,
    violin_fig,
):
    return html.Div(
        [
            html.H1("Fish Visualization", style={"margin": "16px 0"}),

            # Stores used by callbacks later
            dcc.Store(id="selected-zone", data=None),
            dcc.Store(id="selected-year", data="All Years"),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                id="sunburst-chart",
                                figure=sunburst_fig,
                                style={"height": "350px"},
                            ),
                            dcc.Graph(
                                id="histogram-top-catchers",
                                figure=hist_top_catchers_fig,
                                style={"height": "350px", "marginTop": "16px"},
                            ),
                        ],
                        style={"width": "40%", "paddingRight": "16px"},
                    ),
                    html.Div(
                        [
                            dcc.Graph(
                                id="geojson-layer",
                                figure=default_map_fig,
                                config={"scrollZoom": True},
                                style={"height": "700px"},
                            ),
                        ],
                        style={"width": "60%"},
                    ),
                ],
                style={"display": "flex", "alignItems": "flex-start"},
            ),

            html.Div(
                [
                    dcc.Graph(
                        id="histogram-all-years",
                        figure=hist_all_years_fig,
                        style={"height": "350px"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                dcc.Graph(
                                    id="stacked-area-chart",
                                    figure=stacked_area_fig,
                                    style={"height": "350px"},
                                ),
                                style={"width": "50%", "paddingRight": "12px"},
                            ),
                            html.Div(
                                dcc.Graph(
                                    id="violin-plot-length",
                                    figure=violin_fig,
                                    style={"height": "350px"},
                                ),
                                style={"width": "50%"},
                            ),
                        ],
                        style={"display": "flex"},
                    ),
                ],
                style={"marginTop": "16px"},
            ),
        ],
        style={"margin": "0 24px"},
    )