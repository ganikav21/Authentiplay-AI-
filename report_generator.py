from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


# ================= PDF REPORT =================
def generate_report(result, filename="authentiplay_report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    # ================= TITLE =================
    content.append(Paragraph("Authentiplay AI Investigation Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # ================= BASIC INFO =================
    content.append(Paragraph(f"Generated: {datetime.now()}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Final Similarity: {result['similarity']}%", styles["Heading2"]))
    content.append(Paragraph(f"Risk Level: {result['risk']}", styles["Heading3"]))
    content.append(Spacer(1, 12))

    # ================= BREAKDOWN =================
    content.append(Paragraph("Feature Breakdown:", styles["Heading2"]))

    content.append(Paragraph(f"Frame Similarity: {result['frame_similarity']}%", styles["Normal"]))
    content.append(Paragraph(f"Thumbnail Similarity: {result['thumbnail_similarity']}%", styles["Normal"]))
    content.append(Paragraph(f"CLIP Similarity: {result['clip_similarity']}%", styles["Normal"]))
    content.append(Paragraph(f"Audio Similarity: {result['audio_similarity']}%", styles["Normal"]))
    content.append(Spacer(1, 12))

    # ================= CLIP INSIGHTS =================
    content.append(Paragraph("CLIP Reasoning:", styles["Heading2"]))

    content.append(Paragraph(f"Video 1: {result.get('clip_label_1', [])}", styles["Normal"]))
    content.append(Paragraph(f"Video 2: {result.get('clip_label_2', [])}", styles["Normal"]))
    content.append(Paragraph(f"Common: {result.get('clip_common', [])}", styles["Normal"]))
    content.append(Spacer(1, 12))

    # ================= PROPAGATION =================
    prop = result.get("propagation", {})

    content.append(Paragraph("Propagation Analysis:", styles["Heading2"]))
    content.append(Paragraph(f"Origin: {prop.get('origin','Unknown')}", styles["Normal"]))
    content.append(Paragraph(f"Nodes: {prop.get('nodes', [])}", styles["Normal"]))

    doc.build(content)

    return filename