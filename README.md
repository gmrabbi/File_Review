# AI-Powered File Review & Paper Evaluation System

A modern web-based research paper review platform built using Flask. The system allows reviewers to upload papers, evaluate submissions, generate professional review reports, and merge reviews directly into downloadable PDF files.

Designed for academic conferences, project showcasing events, and peer-review workflows.

---

## Live Demo

🔗 https://file-review-8ig1.onrender.com/

---

## GitHub Repository

🔗 https://github.com/gmrabbi/File_Review

---

# Features

## Core Features

- Upload single or multiple PDF papers
- Review research papers through structured forms
- Generate professional peer-review reports
- Automatically merge review report with original paper
- Download reviewed papers instantly
- Delete uploaded papers and related reviewed files
- Responsive and clean UI

---

## Review System

The review form includes:

- Reviewer information
- Overall evaluation score
- Recommendation system
- Review summary
- Strengths and weaknesses
- Detailed comments to authors

---

## PDF Processing

The system automatically:

1. Creates a formatted review report PDF
2. Merges the review report with the original paper
3. Saves the reviewed version
4. Provides instant download support

---

# Technologies Used

## Backend

- Python
- Flask
- ReportLab
- PyPDF

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

## AI / Data Libraries

- LangChain
- OpenAI SDK
- FAISS

## Deployment

- Render

---

# Python Libraries Used

Some major libraries used in this project:

```txt
Flask
pypdf
reportlab
langchain
langgraph
openai
faiss-cpu
streamlit
pandas
numpy
```

---

# Project Structure

```bash
File_Review/
│
├── papers/                    # Uploaded research papers
├── reviewed/                  # Reviewed and merged PDFs
├── static/                    # CSS, JS, images
├── templates/                 # HTML templates
│
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── papers_metadata.json       # Paper metadata
├── README.md
│
└── ...
```

---

# Installation Guide

## Clone the Repository

```bash
git clone https://github.com/gmrabbi/File_Review.git
cd File_Review
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

```bash
python app.py
```

The application will start at:

```bash
http://127.0.0.1:5000
```

---

# API Routes

| Route | Method | Description |
|------|------|------|
| `/` | GET | Homepage |
| `/review/<filename>` | GET | Review specific paper |
| `/pdf/<filename>` | GET | View uploaded PDF |
| `/submit_review` | POST | Submit review form |
| `/upload_paper` | POST | Upload paper(s) |
| `/download/<filename>` | GET | Download reviewed paper |
| `/delete_paper/<filename>` | DELETE | Delete paper |

---

# How the System Works

## Step 1 — Upload Paper

Users upload research papers in PDF format.

## Step 2 — Review Process

Reviewers evaluate papers using the structured review form.

## Step 3 — Review Report Generation

The system generates a professional PDF review report using ReportLab.

## Step 4 — PDF Merging

The generated review report is merged with the original paper using PyPDF.

## Step 5 — Download

The final reviewed paper becomes available for download.

---

# Security Features

- Secure filename handling
- PDF-only upload validation
- Duplicate filename protection
- Safe file storage management

---

# Future Improvements

- User authentication system
- Admin dashboard
- Database integration
- AI-assisted paper evaluation
- Reviewer assignment system
- Email notification support
- Cloud storage integration
- Review analytics dashboard

---

# Screenshots

Add project screenshots here.

Example:

```md
![Dashboard](screenshots/dashboard.png)
```

---

# Use Cases

- University project showcasing
- Research paper evaluation
- Conference paper review
- Academic peer review workflow
- Competition submission management

---

# Author

## Golam Mostafa Rabby

CSE Undergraduate Student  
:contentReference[oaicite:0]{index=0}

Interested in:
- Machine Learning
- Data Science
- NLP
- IoT Systems
- Web Development

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

Special thanks to the open-source Python community and Flask ecosystem for providing the tools and libraries used in this project.
