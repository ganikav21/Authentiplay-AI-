 AUTHENTIPLAY-AI

AI-powered anti-piracy detection system for digital sports media.

##  Features
- Multi-layer video fingerprinting (SSIM + ORB + Deep Learning)
- Real-time detection simulation
- Real YouTube Data API ingestion (paginated + normalized metadata)
- Explainable AI outputs
- Visual frame matching evidence
- Watermark detection module for source cues
- Risk scoring dashboard
- Tamper-proof forensic reports (SHA-256)

##  Tech Stack
- OpenCV
- TensorFlow (MobileNetV2)
- Streamlit
- Scikit-learn

## Problem
Digital sports media gets redistributed illegally across platforms.

##  Solution
Authentiplay detects, analyzes, and verifies unauthorized video usage in real-time.

## ▶️ Run Locally
```bash
pip install -r requirements.txt
export YOUTUBE_API_KEY=your_key_here
streamlit run app.py

