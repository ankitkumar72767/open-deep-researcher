from research_graph import create_research_graph
from datetime import datetime
from ocr_utils import extract_text_from_image
from image_utils import analyze_image
from docx_generator import create_docx
from pdf_generator import create_pdf
from graph_builder import build_graph
from utils import extract_pdf_text
from memory import HistoryManager
from citation_utils import generate_citation
from scholar_search import get_arxiv_papers
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from pdf_generator import *
from ppt_generator import *
from auth import *
st.set_page_config(
    
    page_title="Open Deep Research Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ===============================
# 🎨 GLOBAL ADVANCED CSS
# ===============================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
html, body, [class*="css"] {
    color: #e5e7eb !important;
    background-color: #020617 !important;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- MAIN APP ---------- */
.stApp {
    background: radial-gradient(circle at top, #020617, #020617);
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* ---------- HEADINGS ---------- */
.hero-title {
    font-size: 3rem;
    font-weight: 1000;
    background: linear-gradient(90deg, #38bdf8, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ---------- SETTINGS TITLES ---------- */
h1, h2, h3, h4 {
    color: #e5e7eb !important;
}

/* ---------- INPUT ---------- */
.stChatInput textarea {
    background: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 14px;
    border: 1px solid #1f2937;
}

/* ---------- CHAT MESSAGES ---------- */
.stChatMessage {
    background: #020617;
    border-radius: 16px;
    padding: 16px;
    border: 1px solid #1f2937;
}

/* Assistant message */
.stChatMessage[data-testid="chat-message-assistant"] {
    background: #020617;
}

/* User message */
.stChatMessage[data-testid="chat-message-user"] {
    background: #020617;
}

/* ---------- MARKDOWN OUTPUT ---------- */
.stMarkdown, .stMarkdown p, .stMarkdown li {
    color: #e5e7eb !important;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    width: 100%;
    padding: 0.7rem;
    border-radius: 14px;
    font-weight: 600;
    background: linear-gradient(90deg,#2563eb,#22c55e);
    color: white;
    border: none;
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    transform: scale(1.03);
    opacity: 0.9;
}

/* ---------- EXPANDERS ---------- */
details {
    background: #020617;
    border-radius: 12px;
    border: 1px solid #1f2937;
    padding: 10px;
}

/* ---------- STATUS BOX ---------- */
div[data-testid="stStatusWidget"] {
    background: #020617;
    border-radius: 14px;
    border: 1px solid #1f2937;
    color: #e5e7eb;
}
/* ==================================
   OCR + CODE BLOCK DARK THEME FIX
================================== */

.stCodeBlock {
    background: #111827 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #374151 !important;
}

pre {
    background: #111827 !important;
    color: #ffffff !important;
}

code {
    color: #ffffff !important;
}

textarea {
    background: #111827 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
}

/* Scrollbar */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #020617;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 10px;
}

/* Upload Box */

[data-testid="stFileUploader"] {
    border: 1px solid #1f2937 !important;
    border-radius: 16px !important;
    background: #0f172a !important;
}

/* Text Area */

.stTextArea textarea {
    background: #111827 !important;
    color: white !important;
}
 .stTextArea textarea{
    background:#111827 !important;
    color:white !important;
}

[data-testid="stFileUploader"]{
    background:#0f172a !important;
}

.stDownloadButton button{
    background:linear-gradient(90deg,#2563eb,#22c55e)!important;
    color:white!important;
}           
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 IMPORT API KEYS FROM CONFIG
# ==========================================
try:
    from config import GOOGLE_API_KEY, TAVILY_API_KEY,GROQ_API_KEY,OPENROUTER_API_KEY
        
except ImportError:
    st.error("⚠️ config.py file not found! Please create it with your API keys.")
    st.stop()

# ==========================
# LOGIN SYSTEM
# ==========================
# ==========================
# SESSION STATE
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""
if not st.session_state.logged_in:

    st.title("🔐 Open Deep Research Agent")

    tab1, tab2 = st.tabs(
        ["Login", "Register"]
    )

    # Login Tab
    with tab1:

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if login_user(
                username,
                password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    # Register Tab
    with tab2:

        new_user = st.text_input(
            "New Username"
        )

        new_pass = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Register"):

            if register_user(
                new_user,
                new_pass
            ):

                st.success(
                    "Registration Successful"
                )

            else:

                st.error(
                    "User Already Exists"
                )

    st.stop()

# --- INITIALIZATION ---
memory = HistoryManager(
    st.session_state.username
)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

if "image_context" not in st.session_state:
    st.session_state.image_context = ""
if "last_report" not in st.session_state:
    st.session_state["last_report"] = None
# --- SIDEBAR ---
with st.sidebar:

    # ==========================
    # USER INFO
    # ==========================
    st.markdown("### 👤 User Profile")

    st.success(
        f"Welcome, {st.session_state.username}"
    )

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="logout_btn"
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.session_state.messages = []

        st.session_state.pdf_context = ""
        st.session_state.pdf_name = None
        st.session_state.image_context = ""

        st.session_state.pop("last_report", None)
        st.session_state.pop("ocr_text", None)
        st.session_state.pop("image_analysis", None)

        st.rerun()

    st.divider()

    # ==========================
    # TABS
    # ==========================
    tab_settings, tab_upload, tab_history = st.tabs(
        ["⚙️ Settings", "📎 Upload", "📚 History"]
    )
# ==========================
# TAB 1 : SETTINGS
# ==========================
with tab_settings:

    # API STATUS

    if GOOGLE_API_KEY and TAVILY_API_KEY:

        st.success(
            "✅ API Keys Loaded Successfully"
        )

    else:

        st.error(
            "❌ Keys Missing in config.py"
        )

    st.divider()

    # SEARCH MODE

    st.subheader(
        "🔍 Search Focus"
    )

    search_mode = st.radio(
        "Target:",
        [
            "General Web",
            "Academic Papers",
            "Google Scholar",
            "ArXiv"
        ],
        index=0
    )

    st.divider()

    # AI MODEL SELECTION

    st.subheader(
        "🤖 AI Model"
    )

    selected_provider = st.selectbox(
        "Choose Provider",
        [
            "Google Gemini",
            "Groq",
            "OpenRouter"
        ]
    )

    # SHOW ACTIVE MODEL

    if selected_provider == "Google Gemini":

        st.info(
            "Using Gemini 2.5 Flash"
        )

    elif selected_provider == "Groq":

        st.info(
            "Using Llama 3.3 70B (Groq)"
        )

    elif selected_provider == "OpenRouter":

        st.info(
            "Using DeepSeek Chat"
        )

    st.divider()

    
    # ==========================
    # ANALYTICS DASHBOARD
    # ==========================
    st.subheader("📊 Analytics Dashboard")

    total_searches = len(
        memory.load_history()
    )

    total_reports = len(
        memory.load_history()
    )

    pdf_count = (
        1 if st.session_state.pdf_name
        else 0
    )

    image_count = (
        1 if st.session_state.get(
            "image_analysis"
        )
        else 0
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🔍 Searches",
            total_searches
        )

    with col2:

        st.metric(
            "📄 Reports",
            total_reports
        )

    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            "📑 PDFs",
            pdf_count
        )

    with col4:

        st.metric(
            "🖼 Images",
            image_count
        )

    st.metric(
        "👤 Current User",
        st.session_state.username
    )

    st.subheader("📝 Output Length")

    report_type = st.radio(
        "Detail Level:",
        ["Detailed Report", "Short Summary"],
        index=0
    )

    length_map = {
        "Detailed Report": "Detailed",
        "Short Summary": "Short"
    }

    selected_length = length_map[report_type]

# ==========================
# TAB 2 : UPLOAD
# ==========================
with tab_upload:

    # ==========================
    # IMAGE UPLOAD
    # ==========================
    st.subheader("🖼 Upload Image")

    uploaded_image = st.file_uploader(
        "Choose Image",
        type=["png", "jpg", "jpeg"],
        key="image_upload"
    )

    if uploaded_image:

        st.success(
            f"📷 Image Loaded: {uploaded_image.name}"
        )

        if st.button(
            "🔍 Analyze Image",
            use_container_width=True,
            key="analyze_image_btn"
        ):

            temp_image_path = uploaded_image.name

            with open(temp_image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            with st.spinner("Analyzing Image..."):

                image_analysis = analyze_image(
                    temp_image_path,
                    GOOGLE_API_KEY
                )

                ocr_text = extract_text_from_image(
                    temp_image_path
                )

            st.session_state["ocr_text"] = ocr_text
            st.session_state["image_analysis"] = image_analysis

            st.session_state.image_context = f"""
IMAGE ANALYSIS

{image_analysis}

OCR TEXT

{ocr_text}
"""

    # OCR RESULT
    if "ocr_text" in st.session_state:

        st.subheader("OCR Extracted Text")

        st.text_area(
            "OCR Result",
            st.session_state["ocr_text"],
            height=250,
            key="ocr_result"
        )

    # IMAGE ANALYSIS RESULT
    if "image_analysis" in st.session_state:

        st.subheader("Image Analysis")

        st.text_area(
            "Analysis Result",
            st.session_state["image_analysis"],
            height=350,
            key="analysis_result"
        )

    st.divider()

    # ==========================
    # PDF UPLOAD
    # ==========================
    st.subheader("📄 Document Context")

    if not st.session_state.pdf_name:

        uploaded_file = st.file_uploader(
            "Choose PDF",
            type=["pdf"],
            key="pdf_upload"
        )

        if uploaded_file:

            raw_text = extract_pdf_text(
                uploaded_file
            )

            st.session_state.pdf_context = raw_text
            st.session_state.pdf_name = uploaded_file.name

            st.success(
                f"📄 PDF Loaded: {uploaded_file.name}"
            )

    else:

        st.success(
            f"📄 Active File: {st.session_state.pdf_name}"
        )

        if st.button(
            "❌ Remove PDF",
            use_container_width=True,
            key="remove_pdf_btn"
        ):

            st.session_state.pdf_context = ""
            st.session_state.pdf_name = None

            st.rerun()

    st.divider()

    # ==========================
    # ACTION BUTTONS
    # ==========================
    if st.button(
        "🚀 Start New Chat",
        use_container_width=True,
        key="new_chat_btn"
    ):

        st.session_state.messages = []
        st.session_state.pdf_context = ""
        st.session_state.pdf_name = None
        st.session_state.image_context = ""

        st.session_state.pop("ocr_text", None)
        st.session_state.pop("image_analysis", None)
        st.session_state.pop("last_report", None)

        st.rerun()

    if st.button(
        "🧹 Clear History",
        use_container_width=True,
        key="clear_history_btn"
    ):

        memory.clear_history()
        st.success("History Cleared")

    if st.button(
        "🧹 Clear Text",
        use_container_width=True,
        key="clear_text_btn"
    ):

        st.session_state.pop(
            "search_text",
            None
        )

        st.rerun()

    st.divider()
    # ==========================
    # DOWNLOAD REPORT
    # ==========================
    if st.session_state.get("last_report"):

        st.success("✅ Report Ready")

    try:

        docx_file = create_docx(
            st.session_state["last_report"]
        )

        with open(docx_file, "rb") as docx:

            st.download_button(
                "📝 Download DOCX",
                data=docx.read(),
                file_name="research_report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_docx"
            )

        pdf_file = create_pdf(
            st.session_state["last_report"]
        )

        with open(pdf_file, "rb") as pdf:

            st.download_button(
                "📄 Download PDF",
                data=pdf.read(),
                file_name="research_report.pdf",
                mime="application/pdf",
                key="download_pdf"
            )
        # PPT Download
        ppt_file = create_ppt(
            st.session_state["last_report"]
)

        with open(
            ppt_file,
            "rb"
)          as ppt:

            st.download_button(
                "📊 Download PPT",
                ppt.read(),
                file_name="research_report.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
    )
    except Exception as e:

        st.error(
            f"Download Generation Error: {e}"
        )
# TAB 3 : HISTORY
# ==========================
with tab_history:

    st.subheader("📚 Past Researches")
    search_history = st.text_input(
        "🔍 Search History",
        placeholder="Search topic..."
    )
    
    history = memory.load_history()

    if not history:

        st.caption("No History Available")

    else:

        for entry in reversed(history):

            try:

                dt_obj = datetime.strptime(
                    entry["timestamp"],
                    "%Y-%m-%d %H:%M"
                )

                date_label = dt_obj.strftime(
                    "%d %b %Y"
                )

            except:

                date_label = entry["timestamp"]

            short_input = (
                entry["input"][:20] + "..."
                if len(entry["input"]) > 20
                else entry["input"]
            )

            label = f"{date_label} - {short_input}"

            with st.expander(label):

                st.caption(
                    f"📌 Topic: {entry['input']}"
                )

                col1, col2, col3 = st.columns(3)

                # ======================
                # VIEW REPORT
                # ======================
                with col1:

                    if st.button(
                        "👁️ View",
                        key=f"view_{entry['id']}"
                    ):

                        @st.dialog("📜 Research Report")
                        def show_report():

                            st.subheader(
                                entry["input"]
                            )

                            st.markdown(
                                entry["report"]
                            )

                        show_report()

                # ======================
                # RESUME CHAT
                # ======================
                with col2:

                    if st.button(
                        "🔄 Resume",
                        key=f"load_{entry['id']}"
                    ):

                        saved_history = entry.get(
                            "chat_history",
                            None
                        )

                        if saved_history:

                            st.session_state.messages = saved_history

                        else:

                            st.session_state.messages = [
                                {
                                    "role": "user",
                                    "content": entry["input"]
                                },
                                {
                                    "role": "assistant",
                                    "content": entry["report"]
                                }
                            ]

                        st.success(
                            "✅ Chat Loaded"
                        )

                        st.rerun()

                # ======================
                # DELETE REPORT
                # ======================
                with col3:

                    if st.button(
                        "🗑️ Delete",
                        key=f"del_{entry['id']}"
                    ):

                        memory.delete_entry(
                            entry["id"]
                        )

                        st.success(
                            "🗑️ Deleted Successfully"
                        )

                        st.rerun()

# --- MAIN CHAT ---
if not st.session_state.messages:
    st.markdown("""
<div style="text-align:center; margin-top:30px; margin-bottom:10px;">
  <h1 class="hero-title">
    Open Deep Research Agent
  </h1>
  <p style="color:#94a3b8; font-size:1.1rem;">
    What would you like to research today ?
  </p>
</div>
""", unsafe_allow_html=True)

else:
    st.caption("Open Deep Research Agent")
    if st.session_state.pdf_name:
        st.info(f" *Active Context:* {st.session_state.pdf_name}")

# Display Messages
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat Input
placeholder = (
    "Ask a research question..."
    if st.session_state.messages
    else "Enter a topic..."
)

if prompt := st.chat_input(placeholder):

    if (
        selected_provider == "Google Gemini"
        and not GOOGLE_API_KEY
    ):
        st.error("Google API Key Missing")
        st.stop()

    if (
        selected_provider == "Groq"
        and not GROQ_API_KEY
    ):
        st.error("Groq API Key Missing")
        st.stop()

    if (
        selected_provider == "OpenRouter"
        and not OPENROUTER_API_KEY
    ):
        st.error("OpenRouter API Key Missing")
        st.stop()

    if not TAVILY_API_KEY:
        st.error("Tavily API Key Missing")
        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.rerun()

# Backend Execution
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    prompt = st.session_state.messages[-1]["content"]

    recent_messages = st.session_state.messages[:-1]
    formatted_history = []

    for i, msg in enumerate(reversed(recent_messages)):
        role = msg["role"].upper()
        content = msg["content"]

        if i > 2 and len(content) > 500:
            content = content[:200] + "... [Old Context Truncated]"

        formatted_history.insert(
            0,
            f"{role}: {content}"
        )

    final_history_str = "\n".join(formatted_history[-10:])

    final_topic = prompt
    mode = "Text"

    has_pdf = bool(st.session_state.pdf_context)
    has_image = bool(st.session_state.get("image_context", ""))

    if has_pdf and has_image:

        final_topic = f"""
User Question:
{prompt}

PDF Context:
{st.session_state.pdf_context[:10000]}

Image Context:
{st.session_state.image_context}
"""
        mode = "PDF + Image"

    elif has_pdf:

        final_topic = f"""
User Question:
{prompt}

PDF Context:
{st.session_state.pdf_context[:10000]}
"""
        mode = "PDF"

    elif has_image:

        final_topic = f"""
User Question:
{prompt}

Image Context:
{st.session_state.image_context}
"""
        mode = "Image"

    with st.chat_message("assistant", avatar="🤖"):

        try:

            app_graph = build_graph(
                GOOGLE_API_KEY,
                TAVILY_API_KEY,
                GROQ_API_KEY,
                OPENROUTER_API_KEY,
                selected_provider
            )
            status_placeholder = st.status(
                "🤖 Agent Working...",
                expanded=False
            )

            final_state = app_graph.invoke({
                "topic": final_topic,
                "chat_history": final_history_str,
                "summary_length": selected_length,
                "search_mode": search_mode
            })

            report = final_state["final_report"]

            review = final_state.get(
                    "review_feedback",
                    ""
            )

            st.session_state["last_report"] = report
            status_placeholder.update(
                label="Complete",
                state="complete",
                expanded=False
            )

            st.markdown(report)
            st.subheader("📊 Research Knowledge Graph")

            keywords = final_state.get(
                "graph_keywords",
                []
            )

            graph_fig = create_research_graph(
                prompt,
                keywords
            )

            st.plotly_chart(
                graph_fig,
                use_container_width=True,
                key=f"graph_{prompt}_{total_searches}"
            )
            if review:
                st.divider()
                st.subheader("📊 AI Review")
                st.markdown(review)
            full_response = report
            if review:
                full_response += f"\n\nAI Review:\n{review}"
            st.session_state.messages.append({
                "role": "assistant",
                "content":  full_response
            })

            memory.save_entry(
                prompt,
                mode,
                full_response,
                st.session_state.messages
            )
            #st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")
