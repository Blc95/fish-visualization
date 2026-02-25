import plotly.express as px

from fishviz.data import DataBundle


def make_default_map(bundle: DataBundle):
    """
    Minimal default map so the app can boot.
    Uses zone-level fish counts merged into bundle.df as 'Fish Count_Zone'.
    """
    df = bundle.df
    geojson = bundle.geojson

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="Zone",
        featureidkey="properties.Zone",
        color="Fish Count_Zone",
        mapbox_style="carto-positron",
        center={"lat": 55.95, "lon": 8.66},
        zoom=8,
        opacity=0.8,
        title="Fish Count Across Zones",
    )

    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig