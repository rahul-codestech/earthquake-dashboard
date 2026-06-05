import os
import dash
from dash import dcc, html
import pandas as pd
from fetcher import fetch_earthquake_data
from visualizations import (
    create_world_map,
    create_magnitude_histogram,
    create_time_series,
    create_depth_scatter,
    create_top_regions
)

# ── Fetch Data ──────────────────────────────────────────────
df = fetch_earthquake_data(days=30, min_magnitude=2.5)

# ── Summary Stats ────────────────────────────────────────────
total      = len(df)
max_mag    = df["magnitude"].max()
max_place  = df.loc[df["magnitude"].idxmax(), "place"]
avg_mag    = round(df["magnitude"].mean(), 2)
tsunamis   = int(df["tsunami"].sum())

# ── Dash App ─────────────────────────────────────────────────
app = dash.Dash(__name__)
app.title = "Earthquake Dashboard"

CARD_STYLE = {
    "background": "#111122",
    "border": "1px solid #2a2a4a",
    "borderRadius": "12px",
    "padding": "20px",
    "textAlign": "center",
    "flex": "1",
    "minWidth": "150px"
}

app.layout = html.Div(style={"backgroundColor": "#0a0a1a", "minHeight": "100vh",
                              "fontFamily": "Segoe UI, sans-serif", "color": "white",
                              "padding": "30px"}, children=[

    # Header
    html.H1("🌍 Global Earthquake Dashboard",
            style={"textAlign": "center", "color": "#ff6b35",
                   "fontSize": "2.2rem", "marginBottom": "8px"}),
    html.P("Real-time data from USGS Earthquake API — Last 30 Days",
           style={"textAlign": "center", "color": "#888", "marginBottom": "30px"}),

    # Stats Cards
    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap",
                    "marginBottom": "30px"}, children=[
        html.Div(style=CARD_STYLE, children=[
            html.H2(total, style={"color": "#4ecdc4", "margin": "0"}),
            html.P("Total Earthquakes", style={"color": "#aaa", "margin": "5px 0 0"})
        ]),
        html.Div(style=CARD_STYLE, children=[
            html.H2(f"M{max_mag}", style={"color": "#ff6b35", "margin": "0"}),
            html.P("Strongest Quake", style={"color": "#aaa", "margin": "5px 0 0"}),
            html.Small(max_place[:30] + "...", style={"color": "#666"})
        ]),
        html.Div(style=CARD_STYLE, children=[
            html.H2(avg_mag, style={"color": "#ffe66d", "margin": "0"}),
            html.P("Avg Magnitude", style={"color": "#aaa", "margin": "5px 0 0"})
        ]),
        html.Div(style=CARD_STYLE, children=[
            html.H2(tsunamis, style={"color": "#ff4757", "margin": "0"}),
            html.P("Tsunami Alerts", style={"color": "#aaa", "margin": "5px 0 0"})
        ]),
    ]),

    # World Map
    dcc.Graph(figure=create_world_map(df), style={"marginBottom": "24px"}),

    # Two columns
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                    "gap": "24px", "marginBottom": "24px"}, children=[
        dcc.Graph(figure=create_magnitude_histogram(df)),
        dcc.Graph(figure=create_depth_scatter(df)),
    ]),

    # Time series (full width)
    dcc.Graph(figure=create_time_series(df), style={"marginBottom": "24px"}),

    # Top regions
    dcc.Graph(figure=create_top_regions(df)),

    # Footer
    html.P("Data source: USGS Earthquake Hazards Program | earthquake.usgs.gov",
           style={"textAlign": "center", "color": "#444", "marginTop": "40px",
                  "fontSize": "0.8rem"})
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    print(f"\n✅ Dashboard ready! Open: http://0.0.0.0:{port}\n")
    app.run(debug=False, host="0.0.0.0", port=port)
