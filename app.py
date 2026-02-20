import streamlit as st
import google.generativeai as genai
import plotly.express as px
import pandas as pd
import json
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
    .stChatMessage { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 AI Customer Support Hub</h1>', unsafe_allow_html=True)
st.markdown("### **Prototype → Intelligence → Digital Transformation** | **Streamlit Cloud Ready**")
st.caption("✅ Clean code • No merge conflicts • 100% Cloud compatible")

# ==============================
# GEMINI SETUP
# ==============================

if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = st.secrets.get("GEMINI_API_KEY")

if not st.session_state.gemini_key:
    st.warning("🔑 No Gemini API key found")
    key_input = st.text_input("Enter your Gemini API Key", type="password", key="key_input")
    if st.button("✅ Save Key & Launch"):
        if key_input and key_input.startswith("AIza"):
            st.session_state.gemini_key = key_input
            st.rerun()
        else:
            st.error("Please enter a valid Gemini key")
    st.stop()

genai.configure(api_key=st.session_state.gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

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
    
    proto = st.radio(
        "Select Prototype Stage",
        ["Prototype 1 - Automation",
         "Prototype 2 - Context Intelligence",
         "Prototype 3 - Business Transformation"],
        key="proto_radio"
    )
    st.session_state.prototype = proto

    st.divider()
    
    if st.button("🆕 Start Fresh Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.issue_counts = {"Delivery": 0, "Refund": 0, "Technical": 0, "Other": 0}
        st.session_state.chat_title = None
        st.rerun()

    st.divider()
    st.caption("💡 Works perfectly on Streamlit Cloud")

# ==============================
# MAIN CHAT AREA
# ==============================

title = st.session_state.chat_title or f"Support Chat {datetime.now().strftime('%b %d, %H:%M')}"
st.subheader(f"💬 {title}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your customer support query here..."):
    
    if not is_customer_query(prompt):
        st.error("❌ This AI only handles customer support queries")
        st.stop()
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    issue_type = classify_issue(prompt)
    st.session_state.issue_counts[issue_type] += 1

    # Generate response
    if st.session_state.prototype == "Prototype 1 - Automation":
        system_prompt = "You are a basic automated customer support bot. Respond professionally and concisely to the SINGLE query only."
        gen_input = f"{system_prompt}\n\nCustomer: {prompt}"
    else:
        history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
        if st.session_state.prototype == "Prototype 2 - Context Intelligence":
            system_prompt = "You are an intelligent, context-aware AI customer support agent. Use full conversation history for consistent, personalized replies."
        else:
            system_prompt = "You are a strategic AI customer support agent. Deliver excellent support and contribute to business intelligence."
        gen_input = f"{system_prompt}\n\nFull Conversation:\n{history}"

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

    # Auto title + Export
    if len(st.session_state.messages) == 2 and not st.session_state.chat_title:
        try:
            title_resp = model.generate_content(f"Create a short professional title (max 6 words) for this support chat: {prompt}")
            st.session_state.chat_title = title_resp.text.strip().strip('"\'').title()[:60]
        except:
            st.session_state.chat_title = "Customer Support Session"

    if len(st.session_state.messages) >= 2:
        export_data = {
            "title": st.session_state.chat_title,
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages
        }
        st.download_button(
            label="📥 Export Chat as JSON",
            data=json.dumps(export_data, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name=f"support_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

# ==============================
# PROTOTYPE 3 DASHBOARD (Clean & Fixed)
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

    if total > 0:
        df = pd.DataFrame(list(st.session_state.issue_counts.items()), columns=["Issue Type", "Count"])
        
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                px.bar(df, x="Issue Type", y="Count", color="Issue Type", 
                       title="Issue Distribution", text="Count"), 
                use_container_width=True
            )
        with c2:
            st.plotly_chart(
                px.pie(df, names="Issue Type", values="Count", 
                       title="Issue Share %", hole=0.45), 
                use_container_width=True
            )

        st.markdown("### 💡 AI Business Recommendation")
        try:
            insight = model.generate_content(f"""You are a senior business analyst.
Current session issues: {st.session_state.issue_counts}
Total messages: {len(st.session_state.messages)}
Give ONE powerful, actionable recommendation to reduce these complaints.""")
            st.success(insight.text)
        except:
            st.info("Live insight coming soon...")

# Footer
st.divider()
st.caption("✅ Clean version • No merge conflicts • Ready to deploy")
