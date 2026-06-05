import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_world_map(df):
    """Interactive world map with earthquake locations"""
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        color="magnitude",
        size="magnitude",
        hover_name="place",
        hover_data={"magnitude": True, "depth_km": True, "time": True},
        color_continuous_scale="YlOrRd",
        size_max=15,
        title="🌍 Global Earthquake Map (Last 30 Days)",
        projection="natural earth"
    )
    fig.update_layout(
        paper_bgcolor="#0a0a1a",
        plot_bgcolor="#0a0a1a",
        font_color="white",
        title_font_size=20,
        geo=dict(
            bgcolor="#0a0a1a",
            landcolor="#1a2a3a",
            oceancolor="#0d1b2a",
            showocean=True,
            showland=True,
            showcountries=True,
            countrycolor="#2a3a4a"
        )
    )
    return fig


def create_magnitude_histogram(df):
    """Magnitude distribution chart"""
    fig = px.histogram(
        df,
        x="magnitude",
        nbins=30,
        color_discrete_sequence=["#ff6b35"],
        title="📊 Magnitude Distribution"
    )
    fig.update_layout(
        paper_bgcolor="#0a0a1a",
        plot_bgcolor="#111122",
        font_color="white",
        xaxis_title="Magnitude",
        yaxis_title="Count",
        bargap=0.1
    )
    return fig


def create_time_series(df):
    """Earthquakes over time"""
    daily = df.groupby("date").agg(
        count=("magnitude", "count"),
        avg_mag=("magnitude", "mean"),
        max_mag=("magnitude", "max")
    ).reset_index()

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Daily Earthquake Count", "Average Magnitude per Day"),
        vertical_spacing=0.12
    )
    fig.add_trace(go.Bar(
        x=daily["date"], y=daily["count"],
        marker_color="#4ecdc4", name="Count"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["avg_mag"],
        line=dict(color="#ff6b35", width=2),
        name="Avg Magnitude"
    ), row=2, col=1)

    fig.update_layout(
        paper_bgcolor="#0a0a1a",
        plot_bgcolor="#111122",
        font_color="white",
        title_text="📅 Earthquake Trends Over Time",
        showlegend=False,
        height=500
    )
    return fig


def create_depth_scatter(df):
    """Magnitude vs Depth scatter plot"""
    fig = px.scatter(
        df,
        x="depth_km",
        y="magnitude",
        color="magnitude",
        color_continuous_scale="Inferno",
        hover_name="place",
        title="🔭 Magnitude vs Depth",
        labels={"depth_km": "Depth (km)", "magnitude": "Magnitude"}
    )
    fig.update_layout(
        paper_bgcolor="#0a0a1a",
        plot_bgcolor="#111122",
        font_color="white"
    )
    return fig


def create_top_regions(df):
    """Top 10 most affected regions"""
    # Extract country/region from 'place' field
    df["region"] = df["place"].str.extract(r",\s*(.+)$")[0].fillna(df["place"])
    top = df.groupby("region").size().reset_index(name="count").nlargest(10, "count")

    fig = px.bar(
        top,
        x="count",
        y="region",
        orientation="h",
        color="count",
        color_continuous_scale="Reds",
        title="🌐 Top 10 Most Active Regions"
    )
    fig.update_layout(
        paper_bgcolor="#0a0a1a",
        plot_bgcolor="#111122",
        font_color="white",
        yaxis=dict(autorange="reversed")
    )
    return fig
