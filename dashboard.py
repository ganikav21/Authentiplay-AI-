import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Authentiplay Dashboard", layout="centered")

st.title(" Authentiplay - Piracy Detection Dashboard")
st.subheader("AI-powered Sports Media Protection System")

# -----------------------------
# INPUT SIMULATION (from your engine)
# -----------------------------
st.sidebar.header("Detection Inputs")

official_frames = st.sidebar.slider("Official Frames", 10, 500, 100)
test_frames = st.sidebar.slider("Test Frames", 10, 500, 120)
matches = st.sidebar.slider("Matched Frames", 0, official_frames, 60)

# -----------------------------
# CALCULATION
# -----------------------------
if official_frames > 0:
    similarity = (matches / official_frames) * 100
else:
    similarity = 0

# -----------------------------
# DISPLAY METRICS
# -----------------------------
st.metric("Similarity Score", f"{similarity:.2f}%")

if similarity > 60:
    st.error("⚠️ POSSIBLE PIRACY DETECTED")
else:
    st.success("✅ CONTENT LOOKS ORIGINAL")

# -----------------------------
# VISUALIZATION
# -----------------------------
labels = ["Matched Frames", "Unmatched Frames"]
values = [matches, official_frames - matches]

fig, ax = plt.subplots()
ax.bar(labels, values)

ax.set_title("Frame Comparison Analysis")
ax.set_ylabel("Number of Frames")

st.pyplot(fig)

# -----------------------------
# EXTRA INSIGHT PANEL
# -----------------------------
st.markdown("### 🧠 System Insight")
st.write("""
This system compares video frames using structural similarity and fingerprinting techniques 
to detect unauthorized redistribution of sports media content.
""")