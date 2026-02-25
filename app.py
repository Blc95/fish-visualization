import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from fishviz.data import load_bundle
from fishviz.figures.map import make_default_map
from fishviz.layout import make_layout
from fishviz.callbacks import register_callbacks
from fishviz.figures.charts import (
    create_histogram_all_years,
    create_histogram_top_catchers,
    create_stacked_area_chart,
    create_sunburst_chart,
    create_violin_plot_length,
)

from fishviz.initial_figures import make_initial_figures


def create_app():
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )

    bundle = load_bundle()
    default_map = make_default_map(bundle)
    figs = make_initial_figures(bundle)

    app.layout = make_layout(
        default_map,
        figs["sunburst"],
        figs["hist_all_years"],
        figs["hist_top_catchers"],
        figs["stacked_area"],
        figs["violin"],
    )

    register_callbacks(app, bundle)
    return app


if __name__ == "__main__":
    port = 8051
    url = f"http://127.0.0.1:{port}"
    create_app().run(debug=False, port=port)