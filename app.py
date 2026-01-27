import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

st.set_page_config(
    page_title="Haven",
    page_icon="🫂",
    layout="centered"
)
# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# SIDEBAR

with st.sidebar:
    st.markdown("### 🎨 Appearance")
    st.session_state.dark_mode = st.toggle("Dark mode 🌙")
    st.divider()

    if st.button("🧹 Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("🔒 Conversations are not saved or stored.")

# THEME STYLES


if not st.session_state.dark_mode:
    # LIGHT MODE 
    st.markdown("""
    <style>
    /* App background + global text */
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
        color: #0f172a !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #cbd5e1;
    }

    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
    }

    /* Chat bubbles */
    [data-testid="stChatMessage"][aria-label="user"] {
        background-color: #dbeafe;
        color: #0f172a;
        border-radius: 14px;
        padding: 0.75rem;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] {
        background-color: #ffffff;
        color: #0f172a;
        border-radius: 14px;
        padding: 0.75rem;
        border: 1px solid #e5e7eb;
    }

    /* Input box */
    textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        caret-color: #0f172a !important;
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }

    textarea::placeholder {
        color: #475569 !important;
    }

    /* Buttons (global) */
    button {
        background-color: #e0f2fe !important;
        color: #0f172a !important;
        border-radius: 10px !important;
        border: 1px solid #bae6fd !important;
    }

    button:hover {
        background-color: #bae6fd !important;
    }

    /* Expander arrow + text */
    details summary {
        color: #0f172a !important;
        font-weight: 600;
    }

    /* Header icons (deploy, collapse, menu dots) */
    header * {
        color: #0f172a !important;
    }

    /* Markdown + captions */
    .stMarkdown, .stCaption {
        color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

else:
    # DARK MODE 
    st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    [data-testid="stChatMessage"] {
        background-color: #020617;
        color: #e5e7eb;
        border-radius: 14px;
        padding: 0.75rem;
    }

    textarea {
        background-color: #020617 !important;
        color: #e5e7eb !important;
        caret-color: #e5e7eb !important;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# MODEL
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=st.secrets["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile"
)

SYSTEM_PROMPT = """
You are Haven — a calm, emotionally intelligent companion for university students.

Your role:
* Listen deeply before responding
* Validate emotions without judging
* Offer gentle, realistic guidance
* Sound like a caring senior, not a therapist

You help with:
1. Academic stress (exams, assignments, fear of failure)
2. Emotional pain (loneliness, relationships, burnout)
3. Motivation (small wins, self-belief, grounding)

Behavior rules:
- Keep replies short (2–4 sentences).
- Use soft, human language.
- If overwhelmed → grounding (breathing, senses).
- If angry → patience, no confrontation.
- If self-harm is mentioned → gently guide toward help.

Grounding examples:
* “Let’s take one slow breath together.”
* “Name 3 things you can see around you.”

Crisis handling:
If user mentions self-harm or hopelessness:
* Acknowledge pain
* Encourage reaching out to a real human
* Share emergency numbers calmly (112 / campus counselor)

Never sound robotic. Never rush them.
You are here to sit with them, not fix them instantly.
"""

st.title("🫂 Your Mental Health Haven")
st.caption("A quiet place to breathe and talk.")

if not st.session_state.messages:
    st.info("You can talk about exams, stress, relationships — or just how today feels.")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# USER INPUT

user_input = st.chat_input("I’m listening…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for msg in st.session_state.messages[-6:]:
        messages.append(
            HumanMessage(msg["content"]) if msg["role"] == "user"
            else AIMessage(msg["content"])
        )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = llm.invoke(messages).content

        typed = ""
        for word in response.split():
            typed += word + " "
            placeholder.markdown(typed)
            time.sleep(0.05)

    st.session_state.messages.append({"role": "assistant", "content": response})

# GROUNDING

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🫁 Take a breath"):
        st.toast("Inhale slowly… hold… exhale", duration=4)

# EMERGENCY CONTACT
with st.expander("🆘 Need immediate help?"):
    st.warning("**Emergency contact for territory of India:** 112\n\n**Police:** 100")

st.caption("⚠️ This application does not replace professional mental health care.")
