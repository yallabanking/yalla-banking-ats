# YALLA BANKING ATS SCORE - Project Structure

## 📁 Complete File Structure

```
yalla_banking_ats_score/
│
├── 📄 app.py                          # Main Streamlit application (21KB)
│   ├── Drag & Drop file upload interface
│   ├── Radial gauge visualization
│   ├── Score breakdown display
│   ├── Tabbed detailed analysis
│   └── PDF report download
│
├── 📄 cv_parser.py                    # CV text extraction engine (3.4KB)
│   ├── parse_pdf() - Extract text from PDF using pdfplumber
│   ├── parse_docx() - Extract text from DOCX using python-docx
│   ├── Readability detection
│   ├── Table and image detection
│   └── Error handling for corrupted files
│
├── 📄 ats_scorer.py                   # ATS scoring logic (13KB)
│   ├── check_readability() - 25 points
│   ├── check_sections() - 25 points
│   ├── check_keywords() - 30 points
│   ├── check_contact_info() - 20 points
│   ├── Banking keywords database
│   ├── Certifications detection
│   ├── Action verbs analysis
│   └── Weak phrases detection
│
├── 📄 report_generator.py             # PDF report generation (10KB)
│   ├── generate_report() - Create PDF with ReportLab
│   ├── Radial gauge drawing
│   ├── Progress bars
│   ├── Color-coded sections
│   └── Professional formatting
│
├── 📄 index.html                      # Standalone HTML version (35KB)
│   ├── Complete client-side application
│   ├── PDF.js for PDF parsing
│   ├── Mammoth.js for DOCX parsing
│   ├── jsPDF for report generation
│   └── No server required
│
├── 📄 requirements.txt                # Python dependencies (102B)
│   ├── streamlit>=1.28.0
│   ├── pdfplumber>=0.10.0
│   ├── python-docx>=1.0.0
│   ├── reportlab>=4.0.0
│   ├── plotly>=5.17.0
│   └── PyPDF2>=3.0.0
│
├── 📄 sample_cv.docx                  # Sample CV for testing
│   └── Complete banking professional CV
│
├── 📄 README.md                       # Documentation
│   ├── Project overview
│   ├── Installation instructions
│   ├── Usage guide
│   ├── Customization tips
│   └── Tech stack details
│
├── 📄 setup.sh                        # Linux/Mac setup script
│   ├── Virtual environment creation
│   ├── Dependency installation
│   └── Quick start instructions
│
├── 📄 setup.bat                       # Windows setup script
│   ├── Virtual environment creation
│   ├── Dependency installation
│   └── Quick start instructions
│
├── 📄 .gitignore                      # Git ignore rules
│
└── 📁 .vscode/                        # VS Code configuration
    ├── settings.json                  # Python & editor settings
    └── launch.json                    # Debug configurations
```

## 🚀 Quick Start Guide

### For Visual Studio Code:

1. **Open the project folder in VS Code**
   - File → Open Folder → Select `yalla_banking_ats_score`

2. **Run setup (first time only)**
   - Linux/Mac: `chmod +x setup.sh && ./setup.sh`
   - Windows: Double-click `setup.bat`
   - Or manually: See README.md

3. **Run the application**
   - Press F5 and select "Run Streamlit App"
   - Or open terminal: `streamlit run app.py`
   - Browser opens at: http://localhost:8501

4. **Alternative: HTML Version**
   - Simply open `index.html` in any browser
   - No installation required

## 📊 Scoring Breakdown

### Readability (25 points)
- Text extraction success: 0-10 pts
- No tables detected: 0-8 pts
- No images detected: 0-7 pts

### Sections (25 points)
- Summary/Objective: 5 pts
- Work Experience: 5 pts
- Education: 5 pts
- Skills: 5 pts
- Contact Information: 5 pts

### Keywords (30 points)
- Banking keywords found: 0-15 pts
- Certifications detected: 0-10 pts
- Job description match: 0-30 pts (if JD provided)

### Contact Info (20 points)
- Email address: 7 pts
- Phone number: 7 pts
- LinkedIn profile: 6 pts

## 🎨 Customization Points

### Add Custom Keywords
File: `ats_scorer.py` → Line ~20
```python
BANKING_KEYWORDS = [
    "your", "custom", "keywords", "here"
]
```

### Modify Section Patterns
File: `ats_scorer.py` → Line ~10
```python
SECTION_PATTERNS = {
    "Your Section": [r"(?i)\b(your|patterns)\b"],
}
```

### Adjust Score Weights
File: `ats_scorer.py` → Function `calculate_ats_score()`
- Modify return values in each `check_*()` function

### Change Color Scheme
File: `app.py` → CSS section (top of file)
```css
--navy: #1E3A8A;
--green: #22C55E;
--orange: #F59E0B;
--red: #EF4444;
```

## 🧪 Testing

### Test with Sample CV
1. Run the application
2. Upload `sample_cv.docx`
3. Expected score: ~85/100 (Excellent)

### Test with Job Description
1. Upload any CV
2. Paste a job description in the text area
3. Click "Analyze My CV"
4. Check "Keyword Analysis" tab for match percentage

## 📦 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Docker (create Dockerfile)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Cloud Deployment
- **Streamlit Cloud**: Push to GitHub, connect to streamlit.io
- **Heroku**: Use Procfile with `web: streamlit run app.py`
- **AWS/Azure**: Deploy as container or VM

## 🔧 Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### PDF Not Parsing
- Ensure PDF is text-based, not scanned images
- Try converting to DOCX first

### Dependencies Issues
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📚 Additional Resources

- Streamlit Docs: https://docs.streamlit.io
- PDFPlumber: https://github.com/jsvine/pdfplumber
- python-docx: https://python-docx.readthedocs.io
- ReportLab: https://www.reportlab.com/docs/

---

**Project Size**: ~93KB (excluding dependencies)
**Lines of Code**: ~2,500
**Python Version**: 3.8+
**License**: Educational/Professional Use
