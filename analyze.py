import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Title
st.title("COVID-19 Metadata Analysis")

# Load data
st.subheader("Loading dataset...")
df = pd.read_csv("metadata.csv", low_memory=False)
st.write("Dataset shape:", df.shape)
st.write(df.head())

# Info about missing values
st.subheader("Missing values per column")
missing = df.isnull().sum()
st.bar_chart(missing)

# Summary statistics
st.subheader("Summary statistics")
st.write(df.describe(include="all"))

# Extract years
df['year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
st.subheader("Unique publication years")
st.write(sorted(df['year'].dropna().unique()))

# Top 5 journals
st.subheader("Top 5 Journals")
top_journals = df['journal'].value_counts().head(5)
st.write(top_journals)

# Plot top journals
st.subheader("Top Journals Visualization")
fig, ax = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax, palette="viridis")
st.pyplot(fig)

# Abstract word count
st.subheader("Abstract Word Count Distribution")
df['abstract_word_count'] = df['abstract'].dropna().apply(lambda x: len(str(x).split()))
fig2, ax2 = plt.subplots()
sns.histplot(df['abstract_word_count'], bins=50, kde=True, ax=ax2)
st.pyplot(fig2)
