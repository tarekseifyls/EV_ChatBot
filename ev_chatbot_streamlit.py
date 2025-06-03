# streamlit_app.py
import streamlit as st

# ---- Chatbot Logic ----
def intent_classifier(message):
    msg = message.lower()
    if any(x in msg for x in ["recommend", "best", "buy", "choose", "under"]):
        return "recommendation"
    elif any(x in msg for x in ["policy", "infrastructure", "government"]):
        return "policy"
    elif any(x in msg for x in ["fleet", "replace", "upgrade"]):
        return "fleet"
    return "general"

def recommend_ev(message):
    msg = message.lower()
    if "long range" in msg or "200" in msg or "high range" in msg:
        return "I recommend the Tesla Model 3 Long Range (~358 miles) or Hyundai Ioniq 6 (~361 miles). Both are ideal for distance driving."
    elif "cheap" in msg or "affordable" in msg or "under 40k" in msg or "under $40k" in msg or "budget" in msg:
        return "Consider the Nissan Leaf, Chevy Bolt, or Hyundai Kona Electric — all are priced under $40,000 and perform well for everyday use."
    elif "family" in msg or "big" in msg:
        return "Try the Tesla Model Y or Kia EV6. Both offer great space and safety for families."
    elif "phev" in msg:
        return "Plug-in hybrids like the Chrysler Pacifica or Toyota Prius Prime are good for mixed use but have limited electric range."
    elif "small" in msg:
        return "The Mini Electric or Fiat 500e are compact and ideal for city driving."
    else:
        return "For a balanced option, Tesla Model 3 offers great range, performance, and value in the EV space."

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
        return "Governments should focus on charging infrastructure, battery recycling incentives, and phasing out fossil subsidies."
    elif intent == "fleet":
        return "Fleet managers should prioritize BEVs with high uptime and low cost of ownership, such as the Tesla Model Y or Kia EV6."
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

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
