import streamlit as st
import pandas as pd
import json
from pathlib import Path
import hashlib
from dotenv import load_dotenv
import os

# Load .env credentials
load_dotenv()
VALID_USERNAME = os.getenv("DASHBOARD_USERNAME")
VALID_PASSWORD_HASH = os.getenv("DASHBOARD_PASSWORD_HASH")

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

# Auth function
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False

    if st.session_state.auth:
        return True

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == VALID_USERNAME and hash_password(password) == VALID_PASSWORD_HASH:
            st.session_state.auth = True
        else:
            st.error("Invalid credentials")
    return False

# Enforce login
if not check_password():
    st.stop()

# -------- DASHBOARD LOGIC -------- #
st.set_page_config(page_title="Urgency Dashboard", layout="wide")

st.title("🚨 AI Support Triage Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filters")

file_path = st.sidebar.text_input("Ticket file path (.json)", value="data/sample_tickets_anonymized_clustered_scored.json")

if not Path(file_path).exists():
    st.error("📁 File not found. Please check the path.")
    st.stop()

with open(file_path, "r", encoding="utf-8") as f:
    tickets = json.load(f)

df = pd.DataFrame(tickets)
df["urgency_score"] = pd.to_numeric(df["urgency_score"])

# Filters
min_score = float(st.sidebar.slider("Minimum urgency score", 0.0, 1.0, 0.5, step=0.1))
df = df[df["urgency_score"] >= min_score]

if "cluster_id" in df.columns:
    cluster_options = sorted(df["cluster_id"].dropna().unique())
    selected_clusters = st.sidebar.multiselect("Cluster ID", cluster_options, default=cluster_options)
    df = df[df["cluster_id"].isin(selected_clusters)]

if "channel" in df.columns:
    channel_options = sorted(df["channel"].dropna().unique())
    selected_channels = st.sidebar.multiselect("Channel", channel_options, default=channel_options)
    df = df[df["channel"].isin(selected_channels)]

# Main Table
st.subheader(f"📋 {len(df)} Ticket(s) with Urgency ≥ {min_score}")
st.dataframe(
    df[["ticket_id", "subject", "urgency_score", "urgency_reason", "cluster_id", "channel", "timestamp"]],
    use_container_width=True
)

# Highlight top N
st.subheader("🔥 Top 5 Most Urgent Tickets")
st.table(
    df.sort_values("urgency_score", ascending=False)
      .head(5)[["ticket_id", "subject", "urgency_score", "urgency_reason"]]
)
