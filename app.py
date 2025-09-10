
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go

# Load the original CSV file
csv_file = "TEST for DASH Student Performance Evaluation for 2025-2026 (Rising 9-12) (Responses) - WIP Rising 11.csv"
df = pd.read_csv(csv_file)

# Define subject score columns (Y-axis 1: 0 to 6)
subject_columns = [
    "English DG", "English JS", "Judaics IC", "Judaics AM", "Judaics RO",
    "Math TH", "Math RP", "Math CS", "Math LS",
    "History MS", "History BW",
    "Science SF", "Science VG", "Science JK", "Science AR",
    "SPE average"
]

# Define percentile score columns (Y-axis 2: 0 to 100)
percentile_columns = [
    "PreACT Composite Percentile PreACT", "PreACT Reading PreACT",
    "PreACT English Percentile PreACT", "PreACT Math Percentile PreACT",
    "PreACT Science Percentile PreACT", "PSAT Percentile Total",
    "PSAT EBRW percentile", "PSAT Math Percentile"
]

# Function to compute mean and confidence interval
def compute_ci(series):
    series_clean = series.dropna()
    mean = series_clean.mean()
    sem = stats.sem(series_clean)
    ci = stats.t.interval(0.95, len(series_clean)-1, loc=mean, scale=sem) if len(series_clean) > 1 else (mean, mean)
    return pd.Series({"Mean": mean, "Lower CI": ci[0], "Upper CI": ci[1]})

# Compute summary statistics
subject_summary = df[subject_columns].apply(compute_ci).T
percentile_summary = df[percentile_columns].apply(compute_ci).T

# Plotting
fig = go.Figure()

# Add subject score bars with confidence intervals
fig.add_trace(go.Bar(
    x=subject_summary.index,
    y=subject_summary["Mean"],
    name="Subject Scores",
    error_y=dict(
        type='data',
        symmetric=False,
        array=subject_summary["Upper CI"] - subject_summary["Mean"],
        arrayminus=subject_summary["Mean"] - subject_summary["Lower CI"]
    ),
    marker_color='blue',
    yaxis='y1'
))

# Add percentile score bars with confidence intervals
fig.add_trace(go.Bar(
    x=percentile_summary.index,
    y=percentile_summary["Mean"],
    name="Percentile Scores",
    error_y=dict(
        type='data',
        symmetric=False,
        array=percentile_summary["Upper CI"] - percentile_summary["Mean"],
        arrayminus=percentile_summary["Mean"] - percentile_summary["Lower CI"]
    ),
    marker_color='orange',
    yaxis='y2'
))

# Update layout for dual Y-axis
fig.update_layout(
    title="Percentile Distribution with Confidence Intervals",
    xaxis=dict(title="Metrics"),
    yaxis=dict(title="Subject Scores", range=[0, 6]),
    yaxis2=dict(title="Percentile Scores", overlaying='y', side='right', range=[0, 100]),
    barmode='group',
    legend=dict(x=0.5, y=1.1, orientation='h'),
    height=600
)

# Streamlit UI
st.title("DASH Student Performance Evaluation (2025-2026)")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Summary Table: Subject Scores")
st.dataframe(subject_summary.style.format("{:.2f}"))

st.subheader("Summary Table: Percentile Scores")
st.dataframe(percentile_summary.style.format("{:.2f}"))
