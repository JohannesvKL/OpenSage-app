import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

@st.cache_resource
def plot_ms2_spectrum(spec, title, color):
    """
    Takes a pandas Series (spec) and generates a needle plot with m/z and intensity dimension, also annotate ions.

    Args:
        spec: Pandas Series representing the mass spectrum with 
              "mzarray" {ions m/z ratio}, "intarray" {ion intensities} and "anotarray" {ions annotation} columns.
        title: Title of the plot.
        color: Color of the line in the plot.

    Returns:
        A Plotly Figure object representing the needle plot of the mass spectrum.
    """

    # Every Peak is represented by three dots in the line plot: (x, 0), (x, y), (x, 0)
    def create_spectra(x, y, zero=0):
        x = np.repeat(x, 3)
        y = np.repeat(y, 3)
        y[::3] = y[2::3] = zero
        return pd.DataFrame({"mz": x, "intensity": y})

    df = create_spectra(spec["mzarray"], spec["intarray"])
    fig = px.line(df, x="mz", y="intensity")
    fig.update_traces(line_color=color,  line_width=1)
    fig.update_layout(
        showlegend=True,
        title_text=title,
        xaxis_title="m/z",
        yaxis_title="intensity",
        plot_bgcolor="rgb(255,255,255)",
    )
    fig.layout.template = "plotly_white"
    fig.update_yaxes(fixedrange=True)

    # Annotate every line with a string
    for mz, intensity, annotation in zip(spec["mzarray"], spec["intarray"], spec["anotarray"]):
        if intensity < 0.3:
            yshift_ = 60  # Adjust this value for peaks with high intensity
        else:
            yshift_ = 20  # Adjust this value for peaks with low intensity

        # change the annotation colour according to ion-type
        if "MI" in annotation:
            annotation_color = '#ff0000' 
        elif "y" in annotation:
            annotation_color = 'green' 
        elif "[M" in annotation:
            annotation_color = 'darkmagenta'
        else:
            annotation_color = 'blue'  # Default color for other annotations

        #add annotations
        fig.add_annotation(
            x=mz,
            y=intensity,
            text=annotation,
            showarrow=False,
            arrowhead=1,
            arrowcolor=color,
            font=dict(size=12, color=annotation_color),
            xshift=0,
            yshift=yshift_,
            textangle=90 #verticle
        )

    return fig

@st.cache_resource
def plot_ms2_spectrum_full(spec, title, base_color):
    """
    Takes a pandas Series (spec) and generates a needle plot with m/z and intensity dimension, also annotates ions.
    
    Args:
        spec: Pandas Series representing the mass spectrum with 
              "mzarray" {ions m/z ratio}, "intarray" {ion intensities} and "anotarray" {ions annotation} columns.
        title: Title of the plot.
        base_color: Base color for the line.

    Returns:
        A Plotly Figure object representing the needle plot of the mass spectrum.
    """
    
    # Every Peak is represented by three dots in the line plot: (x, 0), (x, y), (x, 0)
    def create_spectra(x, y, zero=0):
        x = np.repeat(x, 3)
        y = np.repeat(y, 3)
        y[::3] = y[2::3] = zero
        return pd.DataFrame({"mz": x, "intensity": y})

    df = create_spectra(spec["mzarray"], spec["intarray"])

    # Create a scatter plot with the base color
    fig = go.Figure()

    # Add base line with a meaningful name
    fig.add_trace(go.Scatter(
        x=df["mz"], y=df["intensity"], 
        mode='lines', 
        line=dict(color=base_color, width=1),
        name='Annotated peaks'  
    ))

    # Annotate every line with a string if annotation exists
    for mz, intensity, annotation in zip(spec["mzarray"], spec["intarray"], spec["anotarray"]):
        if pd.isna(annotation) or annotation.strip() == "":
            continue  # Skip annotation if it's missing or empty

        if intensity < 0.3:
            yshift_ = 60  # Adjust this value for peaks with high intensity
        else:
            yshift_ = 20  # Adjust this value for peaks with low intensity

        # Change the annotation color according to ion-type
        if "MI" in annotation:
            annotation_color = '#ff0000'  # Red for MI
        elif "y" in annotation:
            annotation_color = 'green'  # Green for y
        elif "[M" in annotation:
            annotation_color = 'darkmagenta'  # Dark Magenta for M
        else:
            annotation_color = 'blue'  # Default color for other annotations

        # Add annotation
        fig.add_annotation(
            x=mz,
            y=intensity,
            text=annotation,
            showarrow=False,
            arrowhead=1,
            arrowcolor=annotation_color,
            font=dict(size=12, color=annotation_color),
            xshift=0,
            yshift=yshift_,
            textangle=90  # Vertical
        )

        # Add a vertical line at the position of the peak with the annotation color
        fig.add_trace(go.Scatter(
            x=[mz, mz],
            y=[0, intensity],
            mode='lines',
            line=dict(color=annotation_color, width=1),
            showlegend=False
        ))

    fig.update_layout(
        showlegend=True,
        title_text=title,
        xaxis_title="m/z",
        yaxis_title="intensity",
        plot_bgcolor="rgb(255,255,255)",
    )
    fig.layout.template = "plotly_white"
    fig.update_yaxes(fixedrange=True)

    return fig