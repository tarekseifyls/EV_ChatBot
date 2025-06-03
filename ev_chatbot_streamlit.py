# streamlit_app.py
import streamlit as st
import base64
import pandas as pd

# ---- Chatbot Logic ----
def intent_classifier(message):
    msg = message.lower()
    if any(x in msg for x in ["recommend", "best", "buy", "choose", "under", "family", "space"]):
        return "recommendation"
    elif any(x in msg for x in ["policy", "infrastructure", "government"]):
        return "policy"
    elif any(x in msg for x in ["fleet", "replace", "upgrade"]):
        return "fleet"
    return "general"

def recommend_ev(message):
    msg = message.lower()
    if "long range" in msg or "200" in msg or "high range" in msg:
        return "✅ Recommended: Tesla Model 3 Long Range (~358 miles) or Hyundai Ioniq 6 (~361 miles) — ideal for distance driving."
    elif "cheap" in msg or "affordable" in msg or "under 40k" in msg or "under $40k" in msg or "budget" in msg:
        return "💰 Consider: Nissan Leaf, Chevy Bolt, or Hyundai Kona Electric — All priced under $40,000."
    elif "family" in msg or "big" in msg or "space" in msg:
        return "👨‍👩‍👧‍👦 Best for Families: Tesla Model Y, Kia EV6, or Hyundai Ioniq 5 — spacious and highly rated for safety."
    elif "phev" in msg:
        return "🔌 PHEVs: Chrysler Pacifica or Toyota Prius Prime — great for short-range electric and backup gas."
    elif "small" in msg:
        return "🏙️ Small Cars: Mini Electric or Fiat 500e — compact and perfect for urban driving."
    else:
        return "🚘 Balanced Pick: Tesla Model 3 — excellent range, resale value, and performance."

def cluster_matcher(message):
    msg = message.lower()
    if "model y" in msg or "modern" in msg:
        return "Cluster 2"
    elif "model 3" in msg or "older" in msg or "2018" in msg:
        return "Cluster 0"
    elif "pacifica" in msg or "phev" in msg or "short range" in msg:
        return "Cluster 1"
    elif "range" in msg:
        if "200" in msg or "long" in msg:
            return "Cluster 0"
        elif "30" in msg or "short" in msg:
            return "Cluster 1"
        else:
            return "Cluster 2"
    else:
        return "general"

def response_generator(intent, message):
    if intent == "recommendation":
        return recommend_ev(message)
    elif intent == "policy":
        return "📢 Policy Insight: Focus on fast-charging stations, battery recycling programs, and clean energy incentives for EV users."
    elif intent == "fleet":
        return "🚚 Fleet Advice: Upgrade to BEVs like Tesla Model Y or Kia EV6 — lower long-term cost and better range."
    return "Hi! I'm your EV assistant. Ask me about EV models, prices, range, fleets, or policy suggestions."

# ---- Streamlit UI ----
st.set_page_config(page_title="EV Market Chatbot", page_icon="🚗")
st.title("🚗 EV Market Advisor Chatbot")

with st.expander("ℹ️ How This Assistant Helps"):
    st.markdown("""
    ### 📘 Overview
    This chatbot is powered by real-world EV market analysis across 180,000+ vehicles.

    #### ✅ You Can Ask About:
    - Choosing the right EV for your needs
    - Best options for budget, family, or long distance
    - Government EV policies & infrastructure planning
    - Fleet upgrade and transition recommendations

    #### 🚫 Limitations:
    - No real-time vehicle availability or dealership info
    - No region-specific pricing or incentives
    - No mechanical troubleshooting or financial/legal advice

    #### 📊 Market Highlights from Our Findings:
    - **Cluster 2**: Modern BEVs like Model Y, great performance and infrastructure
    - **Cluster 0**: Legacy BEVs like Model 3, good resale and range
    - **Cluster 1**: PHEVs like Pacifica, short-range, suitable for urban fleet use
    - BEVs dominate market share and offer average 200+ mi range
    """)

# Sidebar filters for custom recommendations
st.sidebar.header("🔍 Explore by Need")
if st.sidebar.button("Best Long Range"):
    st.sidebar.success(recommend_ev("long range"))
if st.sidebar.button("Budget EVs (< $40K)"):
    st.sidebar.success(recommend_ev("under 40k"))
if st.sidebar.button("EVs for Families"):
    st.sidebar.success(recommend_ev("family"))

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display full historic chat
st.markdown("---")
st.subheader("🗂️ Chat History")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Download chat history as CSV
if st.button("⬇️ Export Chat History"):
    df = pd.DataFrame(st.session_state.messages)
    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ev_chat_history.csv">Click here to download chat history</a>'
    st.markdown(href, unsafe_allow_html=True)

# Language selector
lang = st.sidebar.selectbox("🌐 Language", ["English", "Français", "العربية"], index=0)
if lang == "Français":
    st.toast("💬 Interface multilingue bientôt disponible !")
elif lang == "العربية":
    st.toast("💬 سيتم دعم اللغة العربية قريباً إن شاء الله")

# Chat Input
if prompt := st.chat_input("Ask me anything about EVs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    intent = intent_classifier(prompt)
    reply = response_generator(intent, prompt)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.markdown("**Was this helpful?**")
    col1, col2 = st.columns(2)
    with col1:
        st.button("👍 Yes", key=f"yes_{len(st.session_state.messages)}")
    with col2:
        st.button("👎 No", key=f"no_{len(st.session_state.messages)}")
