# YALLA BANKING ATS SCORE

Professional ATS (Applicant Tracking System) Compatibility Checker for Banking & Finance CVs.

## 📁 Project Structure

```
yalla_banking_ats_score/
├── app.py                 # Main Streamlit application
├── cv_parser.py          # PDF & DOCX text extraction engine
├── ats_scorer.py         # ATS scoring logic (4 criteria / 100 points)
├── report_generator.py   # PDF report generation with recommendations
├── index.html            # Standalone HTML version (no server needed)
├── requirements.txt      # Python dependencies
└── .vscode/             # VS Code configuration
```

## 🚀 Quick Start

### Option 1: Streamlit Version (Python)

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
   Or use VS Code's "Run Streamlit App" debug configuration (F5).

4. **Open in browser:**
   Navigate to `http://localhost:8501`

### Option 2: HTML Version (No Setup)

Simply open `index.html` in any modern web browser. No server or installation required.

## 📊 Scoring System (100 Points Total)

| Criterion | Weight | What It Checks |
|-----------|--------|----------------|
| **Readability** | 25 pts | Text extraction, standard fonts, no excessive images/tables |
| **Sections** | 25 pts | Standard headings (Summary, Experience, Education, Skills, Contact) |
| **Keywords** | 30 pts | Banking/finance terms, certifications, action verbs, JD match |
| **Contact Info** | 20 pts | Email, phone, LinkedIn profile presence |

### Score Levels:
- **80-100**: Excellent (Green)
- **55-79**: Good (Orange)
- **35-54**: Needs Improvement (Dark Orange)
- **0-34**: Poor (Red)

## ✨ Features

### Core Functionality
- ✅ Drag & drop CV upload (PDF/DOCX)
- ✅ Real-time ATS compatibility analysis
- ✅ Dynamic radial gauge with color-coded scores
- ✅ Detailed breakdown by category
- ✅ Section detection (Summary, Experience, Education, Skills, Contact)
- ✅ Keyword matching against job descriptions
- ✅ Banking/finance industry-specific keywords
- ✅ Certification detection (CFA, CMA, CPA, etc.)
- ✅ Action verb analysis vs weak phrases
- ✅ Contact information validation

### Reports & Recommendations
- 📄 Downloadable PDF report with full analysis
- 💡 Actionable tips for CV improvement
- 🔍 Keyword match analysis (when job description provided)
- 📊 Visual score breakdown with progress bars

## 🛠️ Tech Stack

### Streamlit Version
- **Frontend/Backend**: Streamlit
- **PDF Parsing**: pdfplumber, PyPDF2
- **DOCX Parsing**: python-docx
- **Visualization**: Plotly
- **Report Generation**: ReportLab

### HTML Version
- **PDF Parsing**: PDF.js
- **DOCX Parsing**: Mammoth.js
- **Report Generation**: jsPDF
- **UI**: Pure HTML/CSS/JavaScript

## 📝 Usage Tips

1. **Upload CV**: Drag & drop or click to upload your CV (PDF or DOCX)
2. **Job Description** (Optional): Paste the job posting for keyword matching
3. **Analyze**: Click "Analyze My CV" to get your ATS score
4. **Review Results**: Check the detailed breakdown and recommendations
5. **Download Report**: Save the PDF report for reference

## 🔧 Customization

### Adding Custom Keywords
Edit `ats_scorer.py` to add industry-specific keywords:

```python
BANKING_KEYWORDS = [
    "your", "custom", "keywords", "here"
]
```

### Modifying Section Patterns
Update section detection regex in `ats_scorer.py`:

```python
SECTION_PATTERNS = {
    "Your Section": [r"(?i)\b(your|patterns)\b"],
}
```

### Adjusting Score Weights
Modify the scoring logic in `calculate_ats_score()` function in `ats_scorer.py`.

## 📦 Dependencies

```
streamlit>=1.28.0
pdfplumber>=0.10.0
python-docx>=1.0.0
reportlab>=4.0.0
plotly>=5.17.0
PyPDF2>=3.0.0
```

## 🎨 Color Scheme

- **Primary**: Navy Blue (#1E3A8A)
- **Success**: Green (#22C55E)
- **Warning**: Orange (#F59E0B)
- **Error**: Red (#EF4444)
- **Background**: Light Gray (#F8FAFC)

## 📄 License

This project is created for educational and professional use.

## 🤝 Support

For issues or questions, please refer to the code comments or modify as needed for your specific requirements.

---

**Built with ❤️ for Banking & Finance Professionals**
