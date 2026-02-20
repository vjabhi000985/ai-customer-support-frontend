import streamlit as st
import google.generativeai as genai
import plotly.express as px
import pandas as pd
from datetime import datetime

# ==============================
# PAGE CONFIG & STYLING
# ==============================

st.set_page_config(
    page_title="AI Customer Support Hub",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #00ff88, #00b8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .chat-container { border-radius: 15px; padding: 1rem; background: #0e1117; }
    .stChatMessage { border-radius: 12px !important; }
    .metric-card { background: #1e2530; padding: 1rem; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 AI Customer Support Hub</h1>', unsafe_allow_html=True)
st.markdown("### **Prototype → Intelligence → Digital Transformation** | **Streamlit Cloud Ready**")
st.caption("✅ Fully persistent within your browser session • Streaming • Auto-insights • No file system needed")

# ==============================
# GEMINI SETUP (Cloud-friendly)
# ==============================

<<<<<<< HEAD
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = st.secrets.get("GEMINI_API_KEY")   # Works automatically on Cloud

if not st.session_state.gemini_key:
    st.warning("🔑 No Gemini API key found")
    key_input = st.text_input("Enter your Gemini API Key", type="password", key="key_input")
    if st.button("✅ Save Key & Launch"):
        if key_input.startswith("AIza"):
            st.session_state.gemini_key = key_input
            st.rerun()
        else:
            st.error("Invalid Gemini key format")
    st.stop()

genai.configure(api_key=st.session_state.gemini_key)
=======
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
>>>>>>> 44bf94c8ca54841f8c2c45a81a9fcc4a85fdf5c9
model = genai.GenerativeModel("gemini-2.5-flash")

# ==============================
# SESSION STATE
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "issue_counts" not in st.session_state:
    st.session_state.issue_counts = {"Delivery": 0, "Refund": 0, "Technical": 0, "Other": 0}
if "prototype" not in st.session_state:
    st.session_state.prototype = "Prototype 1 - Automation"
if "chat_title" not in st.session_state:
    st.session_state.chat_title = None

# ==============================
# HELPER FUNCTIONS
# ==============================

def classify_issue(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["delivery", "delay", "ship", "tracking", "arrive", "late", "package"]):
        return "Delivery"
    elif any(k in t for k in ["refund", "money", "return", "cancel", "charge", "payment"]):
        return "Refund"
    elif any(k in t for k in ["error", "not working", "bug", "crash", "login", "technical", "app", "website", "page"]):
        return "Technical"
    return "Other"

def is_customer_query(text: str) -> bool:
    keywords = ["order","delivery","refund","payment","error","problem","issue","cancel",
                "technical","account","tracking","return","ship","charge"]
    return any(word in text.lower() for word in keywords)

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:
    st.title("🧪 Innovation Sprint")
    
    prototype = st.radio(
        "Select Prototype Stage",
        ["Prototype 1 - Automation",
         "Prototype 2 - Context Intelligence",
         "Prototype 3 - Business Transformation"],
        key="proto"
    )
    st.session_state.prototype = prototype

    st.divider()
    
    if st.button("🆕 Start Fresh Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.issue_counts = {"Delivery": 0, "Refund": 0, "Technical": 0, "Other": 0}
        st.session_state.chat_title = None
        st.rerun()

    st.divider()
    st.caption("💡 This version works 100% on Streamlit Community Cloud")

# ==============================
# MAIN CHAT AREA
# ==============================

title = st.session_state.chat_title or f"Support Chat {datetime.now().strftime('%b %d, %H:%M')}"
st.subheader(f"💬 {title}")

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your customer support query here..."):
    
    if not is_customer_query(prompt):
        st.error("❌ This AI only handles customer support queries (orders, delivery, refunds, technical issues, etc.)")
        st.stop()
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Classify & count (for dashboard)
    issue_type = classify_issue(prompt)
    st.session_state.issue_counts[issue_type] += 1

    # Prepare prompt for Gemini
    if prototype == "Prototype 1 - Automation":
        system_prompt = "You are a basic automated customer support bot. Respond professionally and concisely to the SINGLE query only."
        gen_input = f"{system_prompt}\n\nCustomer: {prompt}"
    else:
        # Full conversation history for Proto 2 & 3
        history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
        if prototype == "Prototype 2 - Context Intelligence":
            system_prompt = "You are an intelligent, context-aware AI customer support agent. Use full conversation history for consistent, personalized replies."
        else:
            system_prompt = "You are a strategic AI customer support agent. Deliver excellent support and contribute to business intelligence."
        gen_input = f"{system_prompt}\n\nFull Conversation:\n{history}"

    # Generate streaming response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""
        try:
            response = model.generate_content(gen_input, stream=True)
            for chunk in response:
                if chunk.text:
                    full_reply += chunk.text
                    placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)
        except Exception as e:
            full_reply = f"⚠️ Service temporarily unavailable.\n\n{str(e)}"
            placeholder.markdown(full_reply)

    st.session_state.messages.append({"role": "assistant", "content": full_reply})

    # Auto-generate nice title after first exchange
    if len(st.session_state.messages) == 2 and not st.session_state.chat_title:
        try:
            title_prompt = f"Create a short, professional title (max 6 words) for this support chat based only on the first customer message: {prompt}"
            title_resp = model.generate_content(title_prompt)
            st.session_state.chat_title = title_resp.text.strip().strip('"\'').title()[:60]
        except:
            st.session_state.chat_title = "Customer Support Session"

    # Export button appears after first response
    if len(st.session_state.messages) >= 2:
        export_data = {
            "title": st.session_state.chat_title,
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages
        }
        st.download_button(
            label="📥 Export Chat as JSON",
            data=pd.io.json.dumps(export_data).encode(),
            file_name=f"support_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

# ==============================
# PROTOTYPE 3 DASHBOARD
# ==============================

if st.session_state.prototype == "Prototype 3 - Business Transformation":
    st.divider()
    st.markdown("## 📊 Session Business Intelligence Dashboard")

    total = sum(st.session_state.issue_counts.values())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages Exchanged", len(st.session_state.messages))
    with col2:
        st.metric("Issues Classified", total)
    with col3:
        if total > 0:
            top = max(st.session_state.issue_counts, key=st.session_state.issue_counts.get)
            st.metric("Top Issue", top, f"{st.session_state.issue_counts[top]}")

    if total == 0:
        st.info("Start chatting to see live analytics and AI insights.")
    else:
        df = pd.DataFrame(
            list(st.session_state.issue_counts.items()),
            columns=["Issue Type", "Count"]
        )

        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(df, x="Issue Type", y="Count", color="Issue Type",
                         title="Issue Distribution", text="Count")
            fig1.update_layout(height=380)
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            fig2 = px.pie(df, names="Issue Type", values="Count",
                         title="Issue Share %", hole=0.45)
            fig2.update_layout(height=380)
            st.plotly_chart(fig2, use_container_width=True)

        # AI Strategic Insight for this session
        st.markdown("### 💡 AI Business Recommendation")
        try:
            insight_prompt = f"""You are a senior business analyst.
Current session issues: {st.session_state.issue_counts}
Total messages: {len(st.session_state.messages)}
Give ONE powerful, actionable recommendation to reduce these complaints."""
            insight = model.generate_content(insight_prompt)
            st.success(insight.text)
        except:
            st.info("Live insight coming soon...")

<<<<<<< HEAD
# Footer
st.divider()
st.markdown(
    "<p style='text-align:center;color:#666;'>"
    "✅ 100% Streamlit Community Cloud Compatible • Session-only persistence • "
    "Built for instant deployment</p>",
    unsafe_allow_html=True
)
=======
        # AI Generated Business Insight
        highest_issue = df.sort_values("Count", ascending=False).iloc[0]["Issue Type"]

        st.warning(f"⚠️ Insight: '{highest_issue}' complaints are trending. Consider operational optimization.")

        st.info("""
        🔹 Digital Transformation Achieved:
        - AI handles queries
        - AI classifies problems
        - AI generates strategic business insights
        """)
>>>>>>> 44bf94c8ca54841f8c2c45a81a9fcc4a85fdf5c9
