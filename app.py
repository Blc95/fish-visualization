import webbrowser

import dash
import dash_bootstrap_components as dbc

from fishviz.data import load_bundle
from fishviz.figures.map import make_default_map
from fishviz.layout import make_layout
from fishviz.callbacks import register_callbacks


def create_app():
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )

    bundle = load_bundle()
    default_map = make_default_map(bundle)
    app.layout = make_layout(default_map)

    register_callbacks(app, bundle)
    return app


if __name__ == "__main__":
    port = 8051
    url = f"http://127.0.0.1:{port}"
    webbrowser.open_new(url)
    create_app().run(debug=False, port=port)
    
    