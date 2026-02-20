import streamlit as st
import google.generativeai as genai
import plotly.express as px
import pandas as pd
import os

# ==============================
# CONFIGURATION
# ==============================

st.set_page_config(
    page_title="AI Customer Support Transformation",
    layout="wide",
    page_icon="🚀"
)

# Modern Header
st.markdown("""
# 🚀 AI Customer Support Innovation Sprint
### Repeat Prototyping → Intelligence → Digital Transformation
---
""")

# ==============================
# GEMINI CONFIG
# ==============================

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ==============================
# SESSION STATE
# ==============================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "issue_counts" not in st.session_state:
    st.session_state.issue_counts = {
        "Delivery": 0,
        "Refund": 0,
        "Technical": 0,
        "Other": 0
    }

# ==============================
# PROTOTYPE SELECTOR (Sidebar)
# ==============================

st.sidebar.title("🧪 Innovation Sprint Stages")

prototype = st.sidebar.radio(
    "Select Stage:",
    [
        "Prototype 1 - Automation",
        "Prototype 2 - Context Intelligence",
        "Prototype 3 - Business Transformation"
    ]
)

user_input = st.text_input("💬 Enter Customer Support Query")

# ==============================
# HELPER FUNCTIONS
# ==============================

def classify_issue(text):
    text = text.lower()
    if "delivery" in text or "delay" in text:
        return "Delivery"
    elif "refund" in text or "money" in text:
        return "Refund"
    elif "error" in text or "not working" in text:
        return "Technical"
    else:
        return "Other"

def is_customer_query(text):
    keywords = ["order","delivery","refund","payment","error",
                "problem","issue","cancel","technical","account"]
    return any(word in text.lower() for word in keywords)

# ==============================
# MAIN LOGIC
# ==============================

if st.button("🚀 Generate AI Response"):

    if not is_customer_query(user_input):
        st.error("❌ This AI only handles customer support queries.")
        st.stop()

    system_prompt = """
    You are an AI Customer Support Assistant.
    Only respond to customer support related queries professionally.
    """

    if prototype == "Prototype 1 - Automation":
        prompt = user_input

    elif prototype == "Prototype 2 - Context Intelligence":
        st.session_state.chat_history.append(user_input)
        prompt = "\n".join(st.session_state.chat_history)

    else:
        st.session_state.chat_history.append(user_input)
        prompt = "\n".join(st.session_state.chat_history)

    response = model.generate_content(system_prompt + prompt)
    reply = response.text

    issue_type = classify_issue(user_input)
    st.session_state.issue_counts[issue_type] += 1

    # ==============================
    # RESPONSE UI
    # ==============================

    st.markdown("## 🤖 AI Response")
    st.success(reply)

    st.markdown(f"### 📌 Detected Issue: `{issue_type}`")

    # ==============================
    # ADVANCED BUSINESS DASHBOARD
    # ==============================

    if prototype == "Prototype 3 - Business Transformation":

        st.markdown("## 📊 Business Intelligence Dashboard")

        df = pd.DataFrame(
            list(st.session_state.issue_counts.items()),
            columns=["Issue Type", "Count"]
        )

        col1, col2 = st.columns(2)

        with col1:
            fig_bar = px.bar(
                df,
                x="Issue Type",
                y="Count",
                color="Issue Type",
                title="Customer Issue Distribution",
                text="Count"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            fig_pie = px.pie(
                df,
                names="Issue Type",
                values="Count",
                title="Issue Share (%)",
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # AI Generated Business Insight
        highest_issue = df.sort_values("Count", ascending=False).iloc[0]["Issue Type"]

        st.warning(f"⚠️ Insight: '{highest_issue}' complaints are trending. Consider operational optimization.")

        st.info("""
        🔹 Digital Transformation Achieved:
        - AI handles queries
        - AI classifies problems
        - AI generates strategic business insights
        """)