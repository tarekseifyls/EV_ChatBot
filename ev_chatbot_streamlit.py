# streamlit_app.py
import streamlit as st

# ---- Chatbot Logic ----
def user_classifier(message):
    message = message.lower()
    if "buy" in message or "choose" in message or "recommend" in message:
        return "buyer"
    elif "infrastructure" in message or "policy" in message or "government" in message:
        return "policymaker"
    elif "fleet" in message or "replace" in message or "upgrade" in message:
        return "fleet_manager"
    else:
        return "general"

def cluster_matcher(message):
    message = message.lower()
    if "model y" in message or "modern" in message:
        return "Cluster 2"
    elif "model 3" in message or "older" in message or "2018" in message:
        return "Cluster 0"
    elif "pacifica" in message or "phev" in message or "short range" in message:
        return "Cluster 1"
    elif "range" in message:
        if "200" in message or "long" in message:
            return "Cluster 0"
        elif "30" in message or "short" in message:
            return "Cluster 1"
        else:
            return "Cluster 2"
    else:
        return "general"

def response_generator(user_type, cluster):
    if user_type == "buyer":
        if cluster == "Cluster 2":
            return "Modern BEVs like Model Y offer ~198 mi range. Ideal for daily use, good resale value, and supported by growing infrastructure."
        elif cluster == "Cluster 0":
            return "Legacy BEVs like Model 3 offer ~235 mi range. Secondhand market is strong but check battery condition."
        elif cluster == "Cluster 1":
            return "PHEVs like Pacifica offer ~33 mi range. Ideal for mixed urban/suburban use. Consider upgrading to BEV in the future."
    elif user_type == "policymaker":
        if cluster == "Cluster 2":
            return "Focus infrastructure spending on Cluster 2 BEVs. Prioritize fast-charging in cities and suburbs."
        elif cluster == "Cluster 1":
            return "Phase out subsidies for PHEVs < 50 mi. Provide upgrade credits for BEVs."
        elif cluster == "Cluster 0":
            return "Support battery swap programs for legacy BEVs. Encourage secondhand warranties."
    elif user_type == "fleet_manager":
        if cluster == "Cluster 1":
            return "PHEVs work for now but are outdated. Upgrade fleets to BEVs for lower cost of ownership."
        elif cluster == "Cluster 2":
            return "Modern BEVs offer better uptime, range, and charging convenience. Ideal for modern fleets."
        elif cluster == "Cluster 0":
            return "Legacy BEVs might work in limited routes. Consider using them until battery efficiency drops."
    return "Hi! I'm your EV market assistant. Ask me anything about buying, policies, or EV fleets."

# ---- Streamlit UI ----
st.set_page_config(page_title="EV Market Chatbot", page_icon="🚗")
st.title("🚗 EV Market Advisor Chatbot")

# Welcome Message
with st.chat_message("assistant"):
    st.markdown("Welcome! I can help you with EV buying advice, policy decisions, and fleet upgrades. Just type your question below.")

# Role Selection
role = st.selectbox("Select your role:", ["buyer", "policymaker", "fleet_manager"])

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Input
if prompt := st.chat_input("Ask me anything about EVs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user_type = role
    cluster = cluster_matcher(prompt)
    reply = response_generator(user_type, cluster)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Optional feedback
    st.markdown("**Was this helpful?**")
    col1, col2 = st.columns(2)
    with col1:
        st.button("👍 Yes", key=f"yes_{len(st.session_state.messages)}")
    with col2:
        st.button("👎 No", key=f"no_{len(st.session_state.messages)}")
