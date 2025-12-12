import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.config import config

st.set_page_config(page_title="Prompt Engineering Analysis", layout="wide")

st.title("Prompt Engineering Effectiveness Analysis")
st.markdown("""
This dashboard visualizes the performance of different prompting strategies on logic puzzles.
Performance is measured by **Vector Distance** (Cosine Distance) to the ground truth. 
**Lower distance is better.**
""")

# Load Data
results_path = config.paths.results
if not results_path.exists():
    st.error(f"Results file not found at {results_path}. Please run `python src/main.py` first.")
    st.stop()

df = pd.read_csv(results_path)

# Sidebar
st.sidebar.header("Filter Results")
all_strategies = df['strategy'].unique()
selected_strategies = st.sidebar.multiselect(
    "Select Strategies", 
    all_strategies, 
    default=all_strategies
)

if not selected_strategies:
    st.warning("Please select at least one strategy.")
    st.stop()

filtered_df = df[df['strategy'].isin(selected_strategies)]

# Metrics
st.header("Statistical Summary")
summary = filtered_df.groupby('strategy')['vector_distance'].agg(['mean', 'std', 'count']).sort_values('mean')
st.dataframe(summary)

# Plots
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mean Distance Comparison")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=filtered_df, x='strategy', y='vector_distance', errorbar='sd', palette='viridis', ax=ax1)
    ax1.set_title("Mean Vector Distance (Lower is Better)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with col2:
    st.subheader("Distance Distribution")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=filtered_df, x='strategy', y='vector_distance', palette='viridis', inner="quartile", ax=ax2)
    ax2.set_title("Distribution of Distances")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.markdown("---")
st.markdown("### References")
st.markdown("- Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.")
