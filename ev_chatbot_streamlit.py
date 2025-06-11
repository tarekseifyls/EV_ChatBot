# streamlit_app.py
import streamlit as st
import pandas as pd
import os
import base64
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---- Define Intents and Example Patterns ----
template_intents = {
    'greeting': [
        'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'
    ],
    'farewell': [
        'bye', 'goodbye', 'see you', 'farewell', 'later'
    ],
    'recommendation': [
        'recommend', 'best', 'buy', 'choose', 'under', 'family', 'space',
        'wanna buy', 'purchase', 'looking to buy', 'interested in buying',
        'suggest an EV', 'which EV', 'what EV should I buy'
    ],
    'selling': [
        'sell', 'selling', 'trade-in', 'sell my EV', 'want to sell', 'list my car'
    ],
    'policy': [
        'policy', 'policies', 'infrastructure', 'charging infrastructure',
        'expand charging', 'deploy chargers', 'support EV adoption',
        'government policies', 'subsidies', 'incentives', 'regulations'
    ],
    'fleet': [
        'fleet', 'replace my fleet', 'upgrade fleet', 'fleet management', 'commercial use'
    ]
}

# ---- Responses for Each Intent ----
intent_responses = {
    'greeting': '👋 Hello! I am your EV market advisor. How can I help today?',
    'farewell': '👋 Goodbye! Come back anytime for more EV insights.',
    'recommendation': lambda msg: (
        '✅ Long Range Picks: Tesla Model 3 Long Range (~358 miles) or Hyundai Ioniq 6 (~361 miles).'
        if any(x in msg.lower() for x in ['long range','200','distance']) else
        '💰 Budget EVs: Nissan Leaf, Chevy Bolt, Hyundai Kona Electric (all under $40k).'
        if any(x in msg.lower() for x in ['under 40k','budget','cheap']) else
        '👨‍👩‍👧‍👦 Family EVs: Tesla Model Y, Kia EV6, Hyundai Ioniq 5 — spacious and safe.'
        if any(x in msg.lower() for x in ['family','space','kids']) else
        '🔌 PHEVs: Chrysler Pacifica or Toyota Prius Prime — short-range electric with gas backup.'
        if any(x in msg.lower() for x in ['phev','hybrid']) else
        '🏙️ Compact EVs: Mini Electric, Fiat 500e — perfect for urban driving.'
        if any(x in msg.lower() for x in ['small','compact','city']) else
        '🚘 Balanced Pick: Tesla Model 3 — strong range, performance, and value.'
    ),
    'selling': '💸 To sell your EV: list it on major marketplaces, get a battery health report, and price competitively.',
    'policy': '📢 Policy Insight: Invest in fast-charging station rollouts, battery recycling programs, and clean energy incentives.',
    'fleet': '🚚 Fleet Advice: Upgrade to BEVs like Tesla Model Y or Kia EV6 for lower long-term costs and improved reliability.',
    'unknown': "🤔 I didn't catch that. Ask me about EV models, prices, range, fleets, or policies."
}

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
def get_response(message):
    intent = classify_intent(message)
    # If response is callable (recommendation), call with message
    resp = intent_responses.get(intent)
    if callable(resp):
        return resp(message)
    return resp

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
        - Selling your EV
        - EV policy & infrastructure planning
        - Fleet upgrade strategies

        **Limitations:** No real-time availability, location-specific prices, or mechanical/legal advice.
        """
    )

# Sidebar Quick Filters
st.sidebar.header("🔍 Quick Recommendations")
if st.sidebar.button("Long Range EVs"):
    st.sidebar.success(get_response('long range'))
if st.sidebar.button("Budget EVs (<$40k)"):
    st.sidebar.success(get_response('under 40k'))
if st.sidebar.button("Family EVs"):
    st.sidebar.success(get_response('family'))
if st.sidebar.button("Sell My EV"):
    st.sidebar.success(get_response('selling'))

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

# Chat History & Export
if 'messages' not in st.session_state:
    st.session_state.messages = []
st.markdown('---')
st.subheader('🗂️ Chat History')
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
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
    reply = get_response(prompt)
    st.session_state.messages.append({'role':'assistant','content':reply})
    with st.chat_message('assistant'):
        st.markdown(reply)
    st.markdown('**Was this helpful?**')
    col1, col2 = st.columns(2)
    with col1:
        st.button('👍 Yes', key=f'yes_{len(st.session_state.messages)}')
    with col2:
        st.button('👎 No', key=f'no_{len(st.session_state.messages)}')
