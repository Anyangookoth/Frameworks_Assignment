# Part 4: Streamlit Application

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import os

# Function to load and clean data
@st.cache_data
def load_data():
    """
    Loads and cleans the metadata.csv file.
    """
    try:
        # Load the data, using low_memory=False to handle the mixed types warning
        df = pd.read_csv('metadata.csv', low_memory=False)
    except FileNotFoundError:
        st.error("metadata.csv not found. Please ensure it's in the project directory.")
        st.stop()
    
    # Drop columns with too many missing values, as per Part 2 of the assignment
    # who_covidence_id, mag_id, arxiv_id, pmc_json_files, pdf_json_files
    cols_to_drop = ['mag_id', 'arxiv_id', 'pdf_json_files', 'pmc_json_files']
    df = df.drop(columns=cols_to_drop)

    # Convert publish_time to datetime and extract the year
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year

    # Drop rows with no title
    df.dropna(subset=['title'], inplace=True)
    
    # Calculate abstract word count
    df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)

    return df

# Load the data
df = load_data()

# Create the app layout and display
st.title("CORD-19 Data Explorer 🔬")
st.write("This application provides a simple exploration of the COVID-19 research papers using the CORD-19 dataset.")

# Display a sample of the data
st.header("1. Sample of the Data")
st.dataframe(df.head())

# Perform and display visualizations
st.header("2. Key Visualizations")

# Q: Plot number of publications over time
st.subheader("Publications Over Time")
if 'year' in df.columns:
    year_counts = df['year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(year_counts.index, year_counts.values)
    ax.set_title('Number of Publications by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    st.pyplot(fig)
else:
    st.warning("Could not plot publications over time.")

# Q: Create a bar chart of top publishing journals
st.subheader("Top 10 Publishing Journals")
if 'journal' in df.columns:
    top_journals = df['journal'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax)
    ax.set_title('Top 10 Journals by Publication Count')
    ax.set_xlabel('Number of Publications')
    ax.set_ylabel('Journal')
    st.pyplot(fig)
else:
    st.warning("Could not plot top journals.")