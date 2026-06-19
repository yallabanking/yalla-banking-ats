"""
YALLA BANKING ATS SCORE - Main Streamlit Application
A professional ATS compatibility checker for banking & finance CVs.
"""

import streamlit as st
import plotly.graph_objects as go
import time
from cv_parser import parse_cv
from ats_scorer import calculate_ats_score
from report_generator import generate_report

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="YALLA BANKING ATS SCORE",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --accent-blue: #3b82f6;
        --accent-purple: #8b5cf6;
        --accent-pink: #ec4899;
        --accent-green: #10b981;
        --accent-orange: #f59e0b;
        --accent-red: #ef4444;
    }

    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0a0a0f 0%, #12121a 100%);
    }

    #MainMenu, header, footer { visibility: hidden; }

    .app-header {
        background: linear-gradient(135deg, rgba(59,130,246,0.1) 0%, rgba(139,92,246,0.1) 50%, rgba(236,72,153,0.1) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 3rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }

    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: 50%;
        transform: translateX(-50%);
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(139,92,246,0.15), transparent 70%);
        pointer-events: none;
    }

    .app-header h1 {
        color: #FFFFFF;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.7) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .app-header p {
        color: rgba(255,255,255,0.7);
        font-size: 1rem;
        margin: 0.75rem 0 0 0;
        font-weight: 400;
    }

    .upload-container {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }

    .upload-container:hover {
        border-color: rgba(139,92,246,0.3);
        background: rgba(255,255,255,0.05);
    }

    .score-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        margin-bottom: 1.5rem;
    }

    .score-card h3 {
        color: rgba(255,255,255,0.7);
        font-weight: 600;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.9rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        background: rgba(255,255,255,0.06);
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(139,92,246,0.15);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        color: #fff;
    }

    .metric-label {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.5);
        font-weight: 500;
        margin-top: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-bar {
        height: 4px;
        border-radius: 2px;
        background: rgba(255,255,255,0.1);
        margin-top: 0.75rem;
        overflow: hidden;
    }

    .metric-bar-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
    }

    .tip-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }

    .tip-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
    }

    .tip-card:hover {
        background: rgba(255,255,255,0.06);
        transform: translateX(4px);
    }

    .tip-category {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #8b5cf6;
        background: rgba(139,92,246,0.1);
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        display: inline-block;
        margin-bottom: 0.5rem;
    }

    .tip-text {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .section-found {
        color: #10b981;
        font-weight: 600;
        background: rgba(16,185,129,0.1);
        border: 1px solid rgba(16,185,129,0.3);
        padding: 0.5rem 1rem;
        border-radius: 100px;
        font-size: 0.8rem;
    }

    .section-missing {
        color: #ef4444;
        font-weight: 600;
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.3);
        padding: 0.5rem 1rem;
        border-radius: 100px;
        font-size: 0.8rem;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeIn 0.5s ease forwards;
    }

    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        color: white;
        border: none;
        padding: 1.25rem 2.5rem;
        border-radius: 100px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }

    .stDownloadButton > button:hover {
        box-shadow: 0 20px 40px rgba(139,92,246,0.3);
        transform: translateY(-2px);
    }

    /* File uploader styling */
    .stFileUploader {
        background: transparent;
    }

    .stFileUploader > div {
        border: 2px dashed rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        padding: 2.5rem 2rem !important;
        background: rgba(255,255,255,0.02) !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader > div:hover {
        border-color: rgba(139,92,246,0.5) !important;
        background: rgba(255,255,255,0.04) !important;
    }

    /* Text inputs */
    .stTextArea textarea {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(139,92,246,0.5) !important;
        box-shadow: 0 0 0 4px rgba(139,92,246,0.1) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 100px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button:hover {
        box-shadow: 0 20px 40px rgba(139,92,246,0.3) !important;
        transform: translateY(-2px) !important;
    }

    /* Text colors */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .stMarkdown p {
        color: rgba(255,255,255,0.7) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.03);
        border-radius: 100px;
        padding: 0.5rem;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 100px;
        padding: 0.75rem 1.5rem;
        color: rgba(255,255,255,0.5);
        font-weight: 600;
        font-size: 0.85rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(139,92,246,0.3);
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="app-header">
    <p style="font-size:0.8rem;color:rgba(255,255,255,0.5);margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.1em">ATS Compatibility Checker</p>
    <h1>YALLA BANKING ATS SCORE</h1>
    <p>Analyze your CV with advanced ATS algorithms. Get instant feedback and actionable insights.</p>
</div>
""",
    unsafe_allow_html=True,
)


# ─── Session State ────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "parsed_cv" not in st.session_state:
    st.session_state.parsed_cv = None
if "filename" not in st.session_state:
    st.session_state.filename = None


# ─── Upload Section ───────────────────────────────────────────────────────────
col_upload, col_jd = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown("### 📄 Upload Your CV")
    uploaded_file = st.file_uploader(
        "Drop your CV here (PDF or DOCX)",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )

with col_jd:
    st.markdown("### 📋 Job Description (Optional)")
    job_description = st.text_area(
        "Paste the job description to check keyword match:",
        height=170,
        placeholder="Paste the job posting here for accurate keyword matching...",
        label_visibility="collapsed",
    )


# ─── Analyze Button ───────────────────────────────────────────────────────────
if uploaded_file is not None:
    st.markdown("---")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze_clicked = st.button(
            "🔍 Analyze My CV",
            use_container_width=True,
            type="primary",
        )

    if analyze_clicked:
        with st.spinner("Analyzing your CV against ATS standards..."):
            # Parse the file
            file_bytes = uploaded_file.read()
            parsed = parse_cv(file_bytes, uploaded_file.name)
            st.session_state.parsed_cv = parsed
            st.session_state.filename = uploaded_file.name

            if not parsed["is_readable"]:
                st.error(
                    f"❌ {parsed.get('error', 'Could not extract text from the file.')}"
                )
            else:
                # Calculate score
                results = calculate_ats_score(parsed, job_description)
                st.session_state.results = results

                # Small delay for animation effect
                time.sleep(0.5)
                st.rerun()


# ─── Display Results ──────────────────────────────────────────────────────────
if st.session_state.results is not None:
    results = st.session_state.results
    parsed = st.session_state.parsed_cv

    # ─── Score Dashboard ──────────────────────────────────────────────────
    st.markdown("---")

    col_gauge, col_metrics = st.columns([1, 2], gap="large")

    with col_gauge:
        # Radial gauge using Plotly
        score = results["total_score"]
        color = results["color"]
        level = results["level"]

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                number={
                    "font": {"size": 50, "color": color, "family": "Inter"},
                    "suffix": "",
                },
                gauge={
                    "shape": "angular",
                    "bar": {"color": color, "thickness": 15},
                    "bgcolor": "rgba(255,255,255,0.05)",
                    "borderwidth": 0,
                    "axis": {
                        "range": [0, 100],
                        "tickwidth": 0,
                        "tickcolor": "#12121a",
                        "tickfont": {"size": 10, "color": "rgba(255,255,255,0.4)"},
                    },
                    "steps": [
                        {"range": [0, 35], "color": "rgba(239,68,68,0.2)"},
                        {"range": [35, 55], "color": "rgba(245,158,11,0.2)"},
                        {"range": [55, 80], "color": "rgba(16,185,129,0.2)"},
                        {"range": [80, 100], "color": "rgba(16,185,129,0.3)"},
                    ],
                    "threshold": {
                        "line": {"color": color, "width": 4},
                        "thickness": 0.8,
                        "value": score,
                    },
                },
                domain={"x": [0, 1], "y": [0, 1]},
            )
        )

        fig.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": "Inter"},
            annotations=[
                dict(
                    text=f"<b>{level}</b>",
                    x=0.5,
                    xref="paper",
                    y=0.15,
                    yref="paper",
                    showarrow=False,
                    font={"size": 16, "color": color, "family": "Inter"},
                ),
                dict(
                    text="ATS SCORE",
                    x=0.5,
                    xref="paper",
                    y=0.0,
                    yref="paper",
                    showarrow=False,
                    font={"size": 11, "color": "#94A3B8", "family": "Inter"},
                ),
            ],
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_metrics:
        st.markdown("#### Score Breakdown")

        breakdown = results["breakdown"]

        # Metric cards row
        mcol1, mcol2, mcol3, mcol4 = st.columns(4, gap="small")

        metrics_data = [
            (
                "Readability",
                breakdown["readability"]["score"],
                breakdown["readability"]["max"],
            ),
            ("Sections", breakdown["sections"]["score"], breakdown["sections"]["max"]),
            ("Keywords", breakdown["keywords"]["score"], breakdown["keywords"]["max"]),
            (
                "Contact Info",
                breakdown["contact"]["score"],
                breakdown["contact"]["max"],
            ),
        ]

        for col, (label, sc, mx) in zip([mcol1, mcol2, mcol3, mcol4], metrics_data):
            pct = (sc / mx * 100) if mx > 0 else 0
            if pct >= 80:
                bar_color = "#22C55E"
            elif pct >= 55:
                bar_color = "#F59E0B"
            else:
                bar_color = "#EF4444"

            with col:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: {bar_color}">{sc}<span style="font-size:1rem;color:#94A3B8">/{mx}</span></div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-bar">
                        <div class="metric-bar-fill" style="width:{pct}%;background:{bar_color}"></div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Sections found/missing
        st.markdown("")
        st.markdown("#### Section Detection")
        found_sections = breakdown["sections"].get("found", {})
        if found_sections:
            sec_cols = st.columns(len(found_sections))
            for col, (section, found) in zip(sec_cols, found_sections.items()):
                with col:
                    if found:
                        st.markdown(
                            f'<div class="section-found">✓ {section}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div class="section-missing">✗ {section}</div>',
                            unsafe_allow_html=True,
                        )

    # ─── Detailed Analysis ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📊 Detailed Analysis")

    tab1, tab2, tab3 = st.tabs(
        ["📝 Recommendations", "🔑 Keyword Analysis", "📄 File Info"]
    )

    with tab1:
        all_tips = results["all_tips"]
        if not all_tips:
            st.success("🎉 Excellent! Your CV passes all major ATS checks. Keep it up!")
        else:
            st.info(f"Found **{len(all_tips)}** areas for improvement:")
            for category, tip in all_tips:
                st.markdown(
                    f"""
                <div class="tip-card">
                    <span class="tip-category">{category}</span>
                    <div class="tip-text">{tip}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    with tab2:
        kw_analysis = breakdown["keywords"].get("analysis", {})

        if kw_analysis.get("jd_match_percentage", 0) > 0:
            st.markdown(
                f"**Job Description Match: {kw_analysis['jd_match_percentage']}%**"
            )

            matched = kw_analysis.get("jd_matched_keywords", [])
            missing = kw_analysis.get("jd_missing_keywords", [])

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                if matched:
                    st.markdown("**✅ Matched Keywords:**")
                    for kw in matched[:15]:
                        st.markdown(f"- {kw}")
            with col_m2:
                if missing:
                    st.markdown("**❌ Missing Keywords (Add These):**")
                    for kw in missing[:15]:
                        st.markdown(f"- {kw}")
        else:
            found_kw = kw_analysis.get("found_banking_keywords", [])
            found_certs = kw_analysis.get("found_certifications", [])
            found_verbs = kw_analysis.get("found_action_verbs", [])
            weak_phrases = kw_analysis.get("weak_phrases_found", [])

            col_k1, col_k2 = st.columns(2)
            with col_k1:
                if found_kw:
                    st.markdown("**Banking Keywords Found:**")
                    for kw in found_kw[:15]:
                        st.markdown(f"- {kw}")
                if found_certs:
                    st.markdown("**Certifications Detected:**")
                    for c in found_certs:
                        st.markdown(f"- {c.upper()}")
            with col_k2:
                if found_verbs:
                    st.markdown("**Strong Action Verbs Used:**")
                    for v in found_verbs[:10]:
                        st.markdown(f"- {v}")
                if weak_phrases:
                    st.markdown("**⚠️ Weak Phrases to Replace:**")
                    for w in weak_phrases:
                        st.markdown(f"- ~~{w}~~ → Use strong action verbs instead")

    with tab3:
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("File Name", st.session_state.filename)
            st.metric("Word Count", results["word_count"])
        with info_col2:
            st.metric("Pages", results["page_count"])
            st.metric("File Readable", "Yes" if parsed["is_readable"] else "No")

        if parsed.get("has_tables"):
            st.warning(
                "⚠️ Tables detected in your CV. ATS systems may not parse tables correctly."
            )
        if parsed.get("has_images"):
            st.warning(
                "⚠️ Images detected. Remove images and graphics for better ATS compatibility."
            )

    # ─── Download Report ──────────────────────────────────────────────────
    st.markdown("---")

    report_bytes = generate_report(results)

    st.download_button(
        label="📥 Download ATS Report (PDF)",
        data=report_bytes,
        file_name=f"ATS_Report_{st.session_state.filename.rsplit('.', 1)[0]}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

else:
    # ─── Landing State ────────────────────────────────────────────────────
    st.markdown("")
    st.markdown("")

    col_info1, col_info2, col_info3 = st.columns(3, gap="medium")

    with col_info1:
        st.markdown(
            """
        <div class="score-card" style="text-align:center;padding:2.5rem 2rem">
            <div style="width:64px;height:64px;margin:0 auto 1.5rem;background:linear-gradient(135deg,#3b82f6,#8b5cf6);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.75rem">📄</div>
            <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:0.75rem;color:#fff">Upload</h3>
            <p style="color:rgba(255,255,255,0.7);font-size:0.9rem">Drop your CV in PDF or DOCX format</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_info2:
        st.markdown(
            """
        <div class="score-card" style="text-align:center;padding:2.5rem 2rem">
            <div style="width:64px;height:64px;margin:0 auto 1.5rem;background:linear-gradient(135deg,#8b5cf6,#ec4899);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.75rem">🔍</div>
            <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:0.75rem;color:#fff">Analyze</h3>
            <p style="color:rgba(255,255,255,0.7);font-size:0.9rem">Advanced ATS compatibility scanning</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_info3:
        st.markdown(
            """
        <div class="score-card" style="text-align:center;padding:2.5rem 2rem">
            <div style="width:64px;height:64px;margin:0 auto 1.5rem;background:linear-gradient(135deg,#ec4899,#f59e0b);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.75rem">📊</div>
            <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:0.75rem;color:#fff">Improve</h3>
            <p style="color:rgba(255,255,255,0.7);font-size:0.9rem">Get actionable insights & recommendations</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        """
    <div class="score-card" style="text-align:center;padding:3rem 2rem">
        <h3 style="font-size:1.5rem;font-weight:700;margin-bottom:1.5rem;font-family:'Space Grotesk',sans-serif;background:linear-gradient(135deg,#3b82f6,#8b5cf6,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">How It Works</h3>
        <p style="color:rgba(255,255,255,0.7);max-width:700px;margin:0 auto;line-height:1.8">
            <strong style="color:#fff">YALLA BANKING ATS SCORE</strong> analyzes your CV the same way Applicant Tracking Systems do.
            It checks <strong style="color:#fff">readability</strong> (can the ATS read your file?), <strong style="color:#fff">section structure</strong>
            (are standard headings present?), <strong style="color:#fff">keyword matching</strong> (do your skills match the job?),
            and <strong style="color:#fff">contact information</strong> (can recruiters reach you?). Get a score out of 100 with
            specific tips to improve your CV's chances of passing ATS filters.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
