# streamlit_app.py
import streamlit as st
import pandas as pd
import os
import base64
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---- Intent Classification Setup ----
# Define intents and example patterns
template_intents = {
    'long_range': [
        'long range', 'distance driving', '200 miles', 'best for long trips', 'range max'
    ],
    'budget': [
        'under 40k', 'under $40k', 'cheap ev', 'affordable ev', 'budget electric'
    ],
    'family': [
        'family', 'big', 'space', 'kids', 'family car'
    ],
    'phev': [
        'phev', 'plug-in hybrid', 'hybrid', 'short range hybrid'
    ],
    'small': [
        'small', 'compact', 'city driving', 'tiny', 'urban'
    ],
    'policy': [
        'policy', 'infrastructure', 'government', 'subsidies', 'incentives'
    ],
    'fleet': [
        'fleet', 'replace my fleet', 'upgrade fleet', 'fleet management'
    ]
}
# Responses for each intent
intent_responses = {
    'long_range': '✅ Recommended for long range: Tesla Model 3 Long Range (~358 miles) or Hyundai Ioniq 6 (~361 miles).',
    'budget': '💰 Budget-friendly EVs: Nissan Leaf, Chevy Bolt, Hyundai Kona Electric (all under $40k).',
    'family': '👨‍👩‍👧‍👦 Best for families: Tesla Model Y, Kia EV6, or Hyundai Ioniq 5 for space and safety.',
    'phev': '🔌 PHEVs such as Chrysler Pacifica or Toyota Prius Prime offer short electric range with backup gas.',
    'small': '🏙️ Compact EVs: Mini Electric, Fiat 500e for easy city driving.',
    'policy': '📢 Policy Advice: Invest in fast-charging infrastructure, battery recycling incentives, and clean energy subsidies.',
    'fleet': '🚚 Fleet Advice: Transition to BEVs like Tesla Model Y or Kia EV6 for lower total cost of ownership.',
    'unknown': "🚘 I'm an EV assistant. Ask me about EV models, price, range, fleets, or policy."
}
# Prepare training data
patterns = []
labels = []
for intent, pats in template_intents.items():
    for pat in pats:
        patterns.append(pat)
        labels.append(intent)
# Train vectorizer & classifier
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(patterns)
clf = LogisticRegression(max_iter=200)
clf.fit(X_train, labels)

def classify_intent(message):
    X_msg = vectorizer.transform([message])
    pred = clf.predict(X_msg)[0]
    return pred if pred in intent_responses else 'unknown'

# ---- Streamlit UI ----
st.set_page_config(page_title="EV Market Chatbot", page_icon="🚗")
st.title("🚗 EV Market Advisor Chatbot")

# Onboarding
with st.expander("ℹ️ How This Assistant Helps"):
    st.markdown("""
    **This assistant uses EV market data (180k+ vehicles) to provide:
    - EV recommendations by budget, range, family, or fleet
    - Policy insights for government planning
    - Fleet upgrade strategies
    **Limitations:** no real-time availability, location-specific prices, or mechanical/legal advice.
    """)

# Sidebar quick filters
st.sidebar.header("🔍 Quick Recommendations")
if st.sidebar.button("Long Range EVs"):
    st.sidebar.success(intent_responses['long_range'])
if st.sidebar.button("Budget EVs (<$40k)"):
    st.sidebar.success(intent_responses['budget'])
if st.sidebar.button("Family EVs"):
    st.sidebar.success(intent_responses['family'])

# EV Image Cards
ev_dir = os.path.join(os.path.dirname(__file__), 'images')
st.subheader("🚗 Top EV Picks")
ev_cards = [
    {
        'name':'Tesla Model 3','range':'358 mi','price':'$39,990',
        'img':os.path.join(ev_dir,'tesla_model_3.jpg')
    },
    {
        'name':'Hyundai Ioniq 5','range':'303 mi','price':'$41,650',
        'img':os.path.join(ev_dir,'hyundai_ioniq_5.jpg')
    },
    {
        'name':'Chevy Bolt','range':'259 mi','price':'$26,500',
        'img':os.path.join(ev_dir,'chevy_bolt.jpg')
    }
]
cols = st.columns(len(ev_cards))
for col, ev in zip(cols, ev_cards):
    with col:
        st.image(ev['img'], caption=f"{ev['name']} — Range: {ev['range']} | Price: {ev['price']}", use_container_width=True)

# Chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
st.markdown('---')
st.subheader('🗂️ Chat History')
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# Export chat
if st.button('⬇️ Export Chat History'):
    df = pd.DataFrame(st.session_state.messages)
    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ev_chat_history.csv">Download chat history</a>'
    st.markdown(href, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask about EVs..."):
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    intent = classify_intent(prompt)
    reply = intent_responses.get(intent, intent_responses['unknown'])
    st.session_state.messages.append({'role':'assistant','content':reply})
    with st.chat_message('assistant'):
        st.markdown(reply)
    st.markdown('**Was this helpful?**')
    col1, col2 = st.columns(2)
    with col1:
        st.button('👍 Yes', key=f'yes_{len(st.session_state.messages)}')
    with col2:
        st.button('👎 No', key=f'no_{len(st.session_state.messages)}')
