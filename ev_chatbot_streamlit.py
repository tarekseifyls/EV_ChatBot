# streamlit_app.py
import streamlit as st
import pandas as pd
import os
import base64
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---- Define Intents and Example Patterns ----
template_intents = {
    'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
    'farewell': ['bye', 'goodbye', 'see you', 'farewell', 'later'],
    'recommendation': [
        'recommend', 'best', 'buy', 'choose', 'under', 'family', 'space',
        'wanna buy', 'purchase', 'looking to buy', 'interested in buying',
        'suggest an EV', 'which EV', 'what EV should I buy'
    ],
    'policy': ['policy', 'infrastructure', 'government', 'subsidies', 'incentives', 'support EVs', 'regulations'],
    'fleet': ['fleet', 'replace my fleet', 'upgrade fleet', 'fleet management', 'commercial use']
}

# ---- EV Recommendation Logic ----
def recommend_ev(message):
    msg = message.lower()
    if 'long range' in msg or '200' in msg or 'distance' in msg:
        return '✅ Long Range Picks: Tesla Model 3 Long Range (~358 miles) or Hyundai Ioniq 6 (~361 miles).'
    if 'under 40k' in msg or 'budget' in msg or 'cheap' in msg:
        return '💰 Budget EVs: Nissan Leaf, Chevy Bolt, Hyundai Kona Electric (all under $40k).'
    if 'family' in msg or 'space' in msg or 'kids' in msg:
        return '👨‍👩‍👧‍👦 Family EVs: Tesla Model Y, Kia EV6, Hyundai Ioniq 5 — spacious and safe.'
    if 'phev' in msg or 'hybrid' in msg:
        return '🔌 PHEVs: Chrysler Pacifica or Toyota Prius Prime — short electric bursts with gas backup.'
    if 'small' in msg or 'compact' in msg or 'city' in msg:
        return '🏙️ Compact EVs: Mini Electric, Fiat 500e — perfect for urban driving.'
    return '🚘 Balanced Pick: Tesla Model 3 — strong range, performance, and value.'

# ---- Train Intent Classifier ----
patterns = []
labels = []
for intent, pats in template_intents.items():
    for pat in pats:
        patterns.append(pat)
        labels.append(intent)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(patterns)
clf = LogisticRegression(max_iter=200)
clf.fit(X_train, labels)

def classify_intent(message):
    X_msg = vectorizer.transform([message])
    return clf.predict(X_msg)[0]

# ---- Generate Response Based on Intent ----
def response_generator(intent, message):
    if intent == 'greeting':
        return '👋 Hello! I am your EV market advisor. How can I help?'
    if intent == 'farewell':
        return '👋 Goodbye! Feel free to return for more EV advice.'
    if intent == 'recommendation':
        return recommend_ev(message)
    if intent == 'policy':
        return '📢 Policy Insight: Invest in fast-charging infrastructure, battery recycling incentives, and clean energy subsidies.'
    if intent == 'fleet':
        return '🚚 Fleet Advice: Upgrade to BEVs like Tesla Model Y or Kia EV6 for lower long-term cost and better range.'
    return '🤔 I didn\'t catch that. Ask me about EV models, prices, range, fleets, or policies.'

# ---- Streamlit UI ----
st.set_page_config(page_title="EV Market Chatbot", page_icon="🚗")
st.title("🚗 EV Market Advisor Chatbot")

# Onboarding Section
with st.expander("ℹ️ How This Assistant Helps"):
    st.markdown(
        """
        **Powered by analysis of 180,000+ EV records.**

        **Ask about:**
        - EV recommendations by range, budget, family
        - Government EV policies & infrastructure planning
        - Fleet upgrade strategies

        **Limitations:** No real-time availability, location-specific prices, or mechanical/legal advice.
        """
    )

# Sidebar Quick Filters
st.sidebar.header("🔍 Quick Recommendations")
if st.sidebar.button("Long Range EVs"):
    st.sidebar.success(recommend_ev('long range'))
if st.sidebar.button("Budget EVs (<$40k)"):
    st.sidebar.success(recommend_ev('budget'))
if st.sidebar.button("Family EVs"):
    st.sidebar.success(recommend_ev('family'))

# Local Image Cards
ev_dir = os.path.join(os.path.dirname(__file__), 'images')
st.subheader("🚗 Top EV Picks")
ev_cards = [
    {'name':'Tesla Model 3','range':'358 mi','price':'$39,990','img':os.path.join(ev_dir,'tesla_model_3.jpg')},
    {'name':'Hyundai Ioniq 5','range':'303 mi','price':'$41,650','img':os.path.join(ev_dir,'hyundai_ioniq_5.jpg')},
    {'name':'Chevy Bolt','range':'259 mi','price':'$26,500','img':os.path.join(ev_dir,'chevy_bolt.jpg')}
]
cols = st.columns(len(ev_cards))
for col, ev in zip(cols, ev_cards):
    with col:
        st.image(ev['img'], caption=f"{ev['name']} — Range: {ev['range']} | Price: {ev['price']}", use_container_width=True)

# Chat History
if 'messages' not in st.session_state:
    st.session_state.messages = []
st.markdown('---')
st.subheader('🗂️ Chat History')
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# Export Chat History
if st.button('⬇️ Export Chat History'):
    df = pd.DataFrame(st.session_state.messages)
    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ev_chat_history.csv">Download chat history</a>'
    st.markdown(href, unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Ask me anything about EVs..."):
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    intent = classify_intent(prompt)
    reply = response_generator(intent, prompt)
    st.session_state.messages.append({'role':'assistant','content':reply})
    with st.chat_message('assistant'):
        st.markdown(reply)
    st.markdown('**Was this helpful?**')
    col1, col2 = st.columns(2)
    with col1:
        st.button('👍 Yes', key=f'yes_{len(st.session_state.messages)}')
    with col2:
        st.button('👎 No', key=f'no_{len(st.session_state.messages)}')
