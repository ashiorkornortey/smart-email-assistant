import os
import sqlite3
import pandas as pd
import streamlit as st
import altair as alt
import spacy

DB = os.path.join(os.path.dirname(__file__), "..", "data", "emails.sqlite")
conn = sqlite3.connect(DB)
df = pd.read_sql_query("SELECT * FROM emails", conn)
conn.close()

st.set_page_config(page_title="Smart Email Assistant", layout="wide")
st.title("Naa's Smart Email Assistant Dashboard")

total_emails = len(df)
newsletters = df[df['category'] == "Newsletter"].shape[0] if 'category' in df.columns else 0
high_priority = df[df['priority'] == "High"].shape[0] if 'priority' in df.columns else 0
unique_senders = df['sender'].nunique() if 'sender' in df.columns else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Emails", total_emails)
col2.metric("Newsletters", newsletters)
col3.metric("High Priority", high_priority)
col4.metric("Unique Senders", unique_senders)

st.sidebar.header("Filters")
categories = df['category'].dropna().unique().tolist() if 'category' in df.columns else []
selected_cats = st.sidebar.multiselect("Select Categories", categories, default=categories)
df_filtered = df[df['category'].isin(selected_cats)] if categories else df

st.subheader("Emails by Category")
if not df_filtered.empty and 'category' in df_filtered.columns:
    cat_counts = df_filtered['category'].value_counts()
    st.bar_chart(cat_counts)

st.subheader("Top Senders")
if not df_filtered.empty and 'sender' in df_filtered.columns:
    top_senders = df_filtered['sender'].value_counts().head(10)
    st.table(top_senders)

st.subheader("High Priority Emails")
if 'priority' in df_filtered.columns and not df_filtered[df_filtered['priority']=="High"].empty:
    st.table(df_filtered[df_filtered['priority']=="High"][['sender','subject','category','draft_reply']])
else:
    st.write("No high priority emails.")

st.subheader("Sample Draft Replies")
if 'draft_reply' in df_filtered.columns and not df_filtered['draft_reply'].isnull().all():
    st.table(df_filtered[['sender','subject','draft_reply']].head(10))
