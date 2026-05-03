import os
import glob
import json
from flask import Flask, render_template, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
from datetime import datetime

app = Flask(__name__)

PAPERS_DIR = os.path.join(os.path.dirname(__file__), "papers")
REVIEWED_DIR = os.path.join(os.path.dirname(__file__), "reviewed")
METADATA_FILE = os.path.join(os.path.dirname(__file__), "papers_metadata.json")

os.makedirs(PAPERS_DIR, exist_ok=True)
os.makedirs(REVIEWED_DIR, exist_ok=True)

# Paper metadata - in production this would be a database
PAPERS_METADATA = {
    "paper_001.pdf": {
        "title": "Deep Learning for Natural Language Processing",
        "authors": "Dr. Alice Chen, Dr. Wei Zhang",
        "abstract": "This paper presents novel approaches to NLP using transformer-based deep learning architectures.",
        "keywords": ["deep learning", "NLP", "transformers", "BERT"]
    },
    "paper_002.pdf": {
        "title": "Scalable Distributed Systems Architecture",
        "authors": "Prof. Bob Martinez, Dr. Priya Sharma",
        "abstract": "We propose a new framework for building highly scalable distributed systems using microservice patterns.",
        "keywords": ["distributed systems", "microservices", "scalability", "cloud"]
    },
    "paper_003.pdf": {
        "title": "Quantum Computing Applications in Cryptography",
        "authors": "Dr. Sarah Kim, Prof. James Wilson",
        "abstract": "An exploration of quantum computing's implications for modern cryptographic systems and post-quantum security.",
        "keywords": ["quantum computing", "cryptography", "security", "post-quantum"]
    },
}


def find_latest_reviewed(filename):
    pattern = os.path.join(REVIEWED_DIR, f"*_{filename}")
    matches = glob.glob(pattern)
    if matches:
        return max(matches, key=os.path.getmtime)
    legacy = os.path.join(REVIEWED_DIR, f"reviewed_{filename}")
    return legacy if os.path.exists(legacy) else None


def get_papers():
    papers = []
    for filename in sorted(os.listdir(PAPERS_DIR)):
        if filename.endswith(".pdf"):
            reviewed_file = find_latest_reviewed(filename)
            meta = PAPERS_METADATA.get(filename, {
                "title": filename.replace(".pdf", "").replace("_", " ").title(),
                "authors": "Unknown",
                "abstract": "",
                "keywords": []
            })
            papers.append({
                "filename": filename,
                "title": meta["title"],
                "authors": meta["authors"],
                "abstract": meta["abstract"],
                "keywords": meta.get("keywords", []),
                "reviewed": reviewed_file is not None,
                "reviewed_filename": os.path.basename(reviewed_file) if reviewed_file else None,
                "size": os.path.getsize(os.path.join(PAPERS_DIR, filename))
            })
    return papers


@app.route("/")
def index():
    papers = get_papers()
    reviewed_count = sum(1 for p in papers if p["reviewed"])
    return render_template("index.html", papers=papers, reviewed_count=reviewed_count, total_count=len(papers))


@app.route("/review/<filename>")
def review(filename):
    filepath = os.path.join(PAPERS_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    meta = PAPERS_METADATA.get(filename, {
        "title": filename.replace(".pdf", "").replace("_", " ").title(),
        "authors": "Unknown",
        "abstract": "",
        "keywords": []
    })
    reviewed_file = find_latest_reviewed(filename)
    already_reviewed = reviewed_file is not None
    return render_template("review.html",
                           filename=filename,
                           title=meta["title"],
                           authors=meta["authors"],
                           abstract=meta["abstract"],
                           keywords=meta.get("keywords", []),
                           already_reviewed=already_reviewed)


@app.route("/pdf/<filename>")
def serve_pdf(filename):
    filepath = os.path.join(PAPERS_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath, mimetype="application/pdf")


@app.route("/submit_review", methods=["POST"])
def submit_review():
    data = request.get_json()
    filename = data.get("filename")
    reviewer_name = data.get("reviewer_name", "Anonymous")
    reviewer_email = data.get("reviewer_email", "")
    overall_score = data.get("overall_score", "")
    summary = data.get("summary", "")
    strengths = data.get("strengths", "")
    weaknesses = data.get("weaknesses", "")
    comments = data.get("comments", "")
    recommendation = data.get("recommendation", "")

    if not filename or not summary:
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    paper_path = os.path.join(PAPERS_DIR, filename)
    if not os.path.exists(paper_path):
        return jsonify({"success": False, "error": "Paper not found"}), 404

    meta = PAPERS_METADATA.get(filename, {"title": filename, "authors": ""})

    # Build the review PDF in memory
    review_buffer = io.BytesIO()
    doc = SimpleDocTemplate(review_buffer, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("ReviewTitle", parent=styles["Title"],
                                  fontSize=18, textColor=colors.HexColor("#1a2744"),
                                  spaceAfter=6)
    heading_style = ParagraphStyle("SectionHeading", parent=styles["Heading2"],
                                    fontSize=12, textColor=colors.HexColor("#2563eb"),
                                    spaceBefore=14, spaceAfter=4)
    label_style = ParagraphStyle("Label", parent=styles["Normal"],
                                   fontSize=9, textColor=colors.HexColor("#6b7280"),
                                   spaceAfter=2)
    value_style = ParagraphStyle("Value", parent=styles["Normal"],
                                   fontSize=11, textColor=colors.HexColor("#111827"),
                                   spaceAfter=8)
    body_style = ParagraphStyle("Body", parent=styles["Normal"],
                                  fontSize=10, textColor=colors.HexColor("#374151"),
                                  spaceAfter=6, leading=16)

    story = []

    # Header
    story.append(Paragraph("PEER REVIEW REPORT", title_style))
    story.append(Paragraph("DUET CSE Carnival 2026 — Project Showcasing Event", 
                            ParagraphStyle("Sub", parent=styles["Normal"],
                                           fontSize=10, textColor=colors.HexColor("#6b7280"),
                                           spaceAfter=4)))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=16))

    # Paper info
    story.append(Paragraph("PAPER INFORMATION", heading_style))
    story.append(Paragraph("Title", label_style))
    story.append(Paragraph(meta["title"], value_style))
    story.append(Paragraph("Authors", label_style))
    story.append(Paragraph(meta.get("authors", "N/A"), value_style))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb"), spaceAfter=12))

    # Reviewer info
    story.append(Paragraph("REVIEWER INFORMATION", heading_style))
    story.append(Paragraph("Reviewer Name", label_style))
    story.append(Paragraph(reviewer_name, value_style))
    if reviewer_email:
        story.append(Paragraph("Email", label_style))
        story.append(Paragraph(reviewer_email, value_style))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb"), spaceAfter=12))

    # Scores
    story.append(Paragraph("EVALUATION SCORES", heading_style))
    scores_text = f"Overall Score: {overall_score}/10 &nbsp;&nbsp;&nbsp; Recommendation: {recommendation.upper()}"
    story.append(Paragraph(scores_text, ParagraphStyle("Scores", parent=styles["Normal"],
                                                         fontSize=11, textColor=colors.HexColor("#1a2744"),
                                                         spaceAfter=12, leading=18)))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb"), spaceAfter=12))

    # Review content
    story.append(Paragraph("REVIEW SUMMARY", heading_style))
    story.append(Paragraph(summary, body_style))

    if strengths:
        story.append(Paragraph("STRENGTHS", heading_style))
        story.append(Paragraph(strengths, body_style))

    if weaknesses:
        story.append(Paragraph("WEAKNESSES", heading_style))
        story.append(Paragraph(weaknesses, body_style))

    if comments:
        story.append(Paragraph("DETAILED COMMENTS TO AUTHORS", heading_style))
        story.append(Paragraph(comments, body_style))

    doc.build(story)
    review_buffer.seek(0)

    # Merge review PDF + paper PDF (review first)
    paper_reader = PdfReader(paper_path)
    review_reader = PdfReader(review_buffer)

    merged_buffer = io.BytesIO()
    writer = PdfWriter()
    for page in review_reader.pages:
        writer.add_page(page)
    for page in paper_reader.pages:
        writer.add_page(page)

    writer.write(merged_buffer)
    merged_buffer.seek(0)

    output_filename = f"{overall_score}_{filename}"
    output_path = os.path.join(REVIEWED_DIR, output_filename)
    with open(output_path, "wb") as f:
        f.write(merged_buffer.getvalue())

    merged_buffer.seek(0)
    return send_file(merged_buffer, as_attachment=True, download_name=output_filename, mimetype="application/pdf")


@app.route("/download/<filename>")
def download_reviewed(filename):
    filepath = os.path.join(REVIEWED_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath, as_attachment=True, download_name=filename)


@app.route("/upload_paper", methods=["POST"])
def upload_paper():
    if "paper" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded."}), 400

    files = request.files.getlist("paper")
    uploaded_files = []

    for paper_file in files:
        if paper_file.filename == "":
            continue

        if not paper_file.filename.lower().endswith('.pdf'):
            return jsonify({"success": False, "error": f"Only PDF files are supported. Invalid file: {paper_file.filename}"}), 400

        safe_name = secure_filename(paper_file.filename)
        save_path = os.path.join(PAPERS_DIR, safe_name)
        if os.path.exists(save_path):
            base, ext = os.path.splitext(safe_name)
            counter = 1
            while os.path.exists(save_path):
                safe_name = f"{base}_{counter}{ext}"
                save_path = os.path.join(PAPERS_DIR, safe_name)
                counter += 1

        paper_file.save(save_path)
        uploaded_files.append(safe_name)

    if not uploaded_files:
        return jsonify({"success": False, "error": "No valid files uploaded."}), 400

    return jsonify({"success": True, "message": f"{len(uploaded_files)} paper(s) uploaded successfully.", "files": uploaded_files})


@app.route("/delete_paper/<filename>", methods=["DELETE"])
def delete_paper(filename):
    filepath = os.path.join(PAPERS_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"success": False, "error": "Paper not found"}), 404

    try:
        os.remove(filepath)
        # Also remove any reviewed versions
        for reviewed_file in os.listdir(REVIEWED_DIR):
            if reviewed_file.endswith(f"_{filename}"):
                os.remove(os.path.join(REVIEWED_DIR, reviewed_file))
        return jsonify({"success": True, "message": "Paper deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)