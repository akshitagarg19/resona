import streamlit as st
import base64
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Resona",
    page_icon="🐧",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. Helper Function to Load & Encode Background Image
# -----------------------------------------------------------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    bg_base64 = get_base64_image("background.jpg")
    bg_style = f"""
        background-image: url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    """
except FileNotFoundError:
    bg_style = "background-color: #0b1329;"

# -----------------------------------------------------------------------------
# 3. Custom Visual Styling
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        {bg_style}
    }}

    [data-testid="stBottom"], 
    [data-testid="stBottomBlockContainer"], 
    footer, 
    .reportview-container {{
        background: transparent !important;
        background-color: transparent !important;
    }}

    .resona-header-container {{
        margin-bottom: 15px;
    }}

    .resona-main-title {{
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #1e3a8a;
        line-height: 1.1;
        margin: 0px;
        text-shadow: 0px 1px 4px rgba(255, 255, 255, 0.8);
    }}

    .resona-sub-title {{
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-top: 5px;
        margin-bottom: 0px;
        text-shadow: 0px 1px 4px rgba(255, 255, 255, 0.8);
    }}

    .stApp p, .stApp span, .stApp label, .stCaptionContainer {{
        color: #1e3a8a !important;
        font-weight: 600;
    }}

    .stButton button {{
        background-color: rgba(224, 242, 254, 0.9) !important;
        color: #1e3a8a !important;
        border: 1px solid rgba(56, 189, 248, 0.6) !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 15px rgba(5, 10, 25, 0.1);
        transition: all 0.2s ease;
    }}

    .stButton button p, .stButton button span {{
        color: #1e3a8a !important;
    }}

    .stButton button:hover {{
        background-color: rgba(186, 230, 253, 1) !important;
        border-color: rgba(30, 58, 138, 0.5) !important;
    }}

    .stChatMessage {{
        background-color: rgba(11, 19, 41, 0.88) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0px 6px 24px rgba(5, 10, 25, 0.5);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #e0f2fe !important;
    }}

    .stChatMessage p {{
        color: #e0f2fe !important;
    }}

    .stChatInputContainer {{
        border-radius: 20px !important;
        background-color: rgba(224, 242, 254, 0.75) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(56, 189, 248, 0.6) !important;
        box-shadow: 0px 4px 20px rgba(5, 10, 25, 0.15);
    }}

    .stChatInputContainer textarea {{
        color: #0f172a !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 4. System Prompt & Gemini Client Initialization
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """You are Resona, an empathetic, non-judgmental listener designed to help users process their emotions and thoughts using simple, direct language suitable for someone who may be stressed or overwhelmed. Respond supportively and kindly in English or Hinglish depending on what the user uses, keeping your replies clear and concise. You must never provide a medical diagnosis, psychological treatment, or clinical advice, and you must never claim to replace a qualified professional; if a user exhibits signs of severe crisis or distress, gently encourage them to reach out to a trusted professional, support system, or helpline."""

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# -----------------------------------------------------------------------------
# 5. Chat Session State Management & Page Flow State
# -----------------------------------------------------------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there. I'm Resona. If you're feeling stressed, overwhelmed, or just need a quiet space to talk without any judgment, I'm here to listen. What's on your mind today?"
        }
    ]

# -----------------------------------------------------------------------------
# 6. Two-Page Navigation Handling
# -----------------------------------------------------------------------------
if not st.session_state.started:
    st.markdown(
        """
        <div class="resona-header-container" style="margin-top: 50px;">
            <div class="resona-main-title">Resona - We hear you!</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption("A quiet, non-judgmental space to express what you're feeling.")

    st.markdown(
        """
        <div style="
            background: rgba(224, 242, 254, 0.75);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            margin: 25px 0px 30px 0px;
            text-align: center;
            border: 1px solid rgba(56, 189, 248, 0.5);
            box-shadow: 0px 6px 20px rgba(5, 10, 25, 0.1);
        ">
            <p style="font-style: italic; font-size: 1.05rem; color: #1e3a8a !important; margin: 0; line-height: 1.5;">
                Take all the time you need. There is no rush, no pressure, and no right way to feel. Step inside whenever you are ready.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Start", use_container_width=True):
        st.session_state.started = True
        st.rerun()

else:
    st.markdown(
        """
        <div class="resona-header-container">
            <div class="resona-main-title">Resona - We hear you!</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption("A quiet, non-judgmental space to express what you're feeling.")

    st.markdown(
        """
        <div style="
            background: rgba(224, 242, 254, 0.75);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 18px 20px;
            margin: 15px 0px 15px 0px;
            text-align: center;
            border: 1px solid rgba(56, 189, 248, 0.5);
            box-shadow: 0px 6px 20px rgba(5, 10, 25, 0.1);
        ">
            <p style="font-style: italic; font-size: 1.1rem; color: #1e3a8a !important; margin: 0; line-height: 1.5; font-weight: 700;">
                “What you seek is seeking you.”
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Interactive Virtual Hug Button with st.toast
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🤗 Receive Virtual Hug", use_container_width=True):
            st.toast("Sending you virtual hugs!! 🤗❤️")

    # Chat History & User Input
    for message in st.session_state.messages:
        avatar_icon = "🐧" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    if user_input := st.chat_input("Type how you're feeling (in English or Hinglish)..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🐧"):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error details: {e}")
