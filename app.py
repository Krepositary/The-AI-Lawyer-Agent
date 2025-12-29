import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx2txt

# ==================================================
# 🔴 GEMINI API KEY (HARDCODED)
# 👉 Replace with your actual Gemini API key
# ==================================================
GEMINI_API_KEY = "AIzaSyAT4yWYWjm37h_H9chBiVmbEshYDM5n6lc"

genai.configure(api_key=GEMINI_API_KEY)

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="LegalAdvisor AI ⚖️",
    page_icon="⚖️",
    layout="wide"
)

# ================== UI STYLING ==================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #141E30, #243B55);
}
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
}
h1, h2, h3 {
    color: #F9FAFB;
}
.feature-card {
    background: rgba(255,255,255,0.12);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
}
.chat-ai {
    background: #22C55E;
    padding: 16px;
    border-radius: 14px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("""
<h1>⚖️ LegalAdvisor – AI Lawyer Agent (Gemini)</h1>
<p style="color:#D1D5DB;font-size:18px;">
AI-powered legal assistant for contracts, compliance, drafting & research
</p>
""", unsafe_allow_html=True)

# ================== AGENT MODE ==================
st.sidebar.header("🧠 Agent Capabilities")
agent_mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "📄 Contract & Clause Analyzer",
        "📚 Case Law Research",
        "💬 Legal Q&A Chat",
        "🛡️ Compliance & Risk Checker",
        "✍️ Document Drafting Assistant"
    ]
)

# ================== FILE TEXT EXTRACTION ==================
def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return " ".join(
            page.extract_text()
            for page in reader.pages
            if page.extract_text()
        )
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)
    else:
        return file.read().decode("utf-8")

# ================== GEMINI CALL ==================
def legal_ai(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# ================== MAIN LAYOUT ==================
left, right = st.columns([1, 1])

with left:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📤 Upload Legal Document (PDF / DOCX / TXT)",
        type=["pdf", "docx", "txt"]
    )

    user_input = st.text_area(
        "📝 Enter Legal Query or Instruction",
        height=180,
        placeholder="Example: Identify risky clauses or draft NDA..."
    )

    run_btn = st.button("🚀 Run LegalAdvisor")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.subheader("📊 AI Legal Output")

    if run_btn:
        if not user_input and not uploaded_file:
            st.warning("Please upload a document or enter a query.")
        else:
            doc_text = ""
            if uploaded_file:
                doc_text = extract_text(uploaded_file)

            final_prompt = f"""
You are a senior AI legal advisor.

AGENT MODE:
{agent_mode}

USER REQUEST:
{user_input}

DOCUMENT CONTENT:
{doc_text[:6000]}

INSTRUCTIONS:
- Simplify legal language
- Clearly flag risks
- Suggest alternative clauses
- Use bullet points
- Avoid jurisdiction-specific advice unless mentioned
"""

            with st.spinner("⚖️ LegalAdvisor is analyzing..."):
                output = legal_ai(final_prompt)

            st.markdown(f"<div class='chat-ai'>{output}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================== FOOTER ==================
st.markdown("""
<hr>
<p style="text-align:center;color:#9CA3AF;">
⚠️ AI-generated legal assistance | Not a substitute for licensed legal advice
</p>
""", unsafe_allow_html=True)
