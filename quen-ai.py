import streamlit as st
import requests
import json
import base64
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Qwen AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

BACKGROUND_FILE = (
    BASE_DIR / "assets" / "ai-background.jpg"
)

HISTORY_FILE = (
    BASE_DIR / "chat_history.json"
)


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_BASE_URL = "http://localhost:11434"

OLLAMA_TAGS_URL = (
    OLLAMA_BASE_URL + "/api/tags"
)

OLLAMA_CHAT_URL = (
    OLLAMA_BASE_URL + "/api/chat"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = {}

if "delete_target" not in st.session_state:
    st.session_state.delete_target = None


# ============================================================
# LOAD CHAT HISTORY
# ============================================================

def load_history():

    if not HISTORY_FILE.exists():
        return {}

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except Exception:
        return {}


if not st.session_state.saved_chats:

    st.session_state.saved_chats = load_history()


# ============================================================
# SAVE CHAT HISTORY
# ============================================================

def save_history():

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                st.session_state.saved_chats,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception:
        return False


# ============================================================
# GET OLLAMA MODELS
# ============================================================

def get_models():

    try:

        response = requests.get(
            OLLAMA_TAGS_URL,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        result = []

        for item in data.get("models", []):

            name = item.get("name")

            if name:
                result.append(name)

        return result

    except Exception:

        return []


models = get_models()


# ============================================================
# SELECT DEFAULT MODEL
# ============================================================

if models:

    if (
        st.session_state.selected_model is None
        or
        st.session_state.selected_model not in models
    ):

        # Prefer Qwen if available
        qwen_models = [
            model
            for model in models
            if "qwen" in model.lower()
        ]

        if qwen_models:

            st.session_state.selected_model = (
                qwen_models[0]
            )

        else:

            st.session_state.selected_model = (
                models[0]
            )


# ============================================================
# READ BACKGROUND IMAGE
# ============================================================

def load_background():

    if not BACKGROUND_FILE.exists():
        return ""

    try:

        with open(
            BACKGROUND_FILE,
            "rb"
        ) as file:

            encoded = base64.b64encode(
                file.read()
            ).decode("utf-8")

        return encoded

    except Exception:

        return ""


background_base64 = load_background()


# ============================================================
# THEME
# ============================================================

dark_mode = (
    st.session_state.theme == "dark"
)


if dark_mode:

    PAGE_BG = "#07142f"

    SIDEBAR_BG = (
        "rgba(5, 10, 30, 0.90)"
    )

    CARD_BG = (
        "rgba(9, 17, 43, 0.82)"
    )

    INPUT_BG = (
        "rgba(9, 17, 43, 0.95)"
    )

    TEXT = "#f8fafc"

    MUTED = "#94a3b8"

    BORDER = (
        "rgba(255,255,255,0.13)"
    )

    OVERLAY = (
        "rgba(4, 9, 30, 0.55)"
    )

else:

    PAGE_BG = "#edf1f8"

    SIDEBAR_BG = (
        "rgba(255,255,255,0.93)"
    )

    CARD_BG = (
        "rgba(255,255,255,0.88)"
    )

    INPUT_BG = (
        "rgba(255,255,255,0.96)"
    )

    TEXT = "#1e293b"

    MUTED = "#64748b"

    BORDER = (
        "rgba(30,41,59,0.13)"
    )

    OVERLAY = (
        "rgba(245,248,255,0.48)"
    )


# ============================================================
# BACKGROUND URL
# ============================================================

if background_base64:

    background_url = (
        "data:image/jpeg;base64,"
        + background_base64
    )

else:

    background_url = ""


# ============================================================
# GLOBAL CSS
#
# IMPORTANT:
# This is a normal string, NOT an f-string.
# Therefore CSS braces are safe.
# ============================================================

CSS = """
<style>

/* ==========================================================
   GLOBAL
========================================================== */

html,
body,
.stApp {

    font-size: 13px;
}


/* ==========================================================
   APPLICATION BACKGROUND
========================================================== */

.stApp {

    min-height: 100vh;

    background-color:
        __PAGE_BG__;

    background-image:
        linear-gradient(
            __OVERLAY__,
            __OVERLAY__
        ),
        url("__BACKGROUND__");

    background-size:
        cover;

    background-position:
        center center;

    background-attachment:
        fixed;

    background-repeat:
        no-repeat;

    color:
        __TEXT__;
}


/* ==========================================================
   STREAMLIT HEADER
========================================================== */

[data-testid="stHeader"] {

    background:
        transparent !important;

    height:
        0 !important;
}


[data-testid="stToolbar"] {

    visibility:
        hidden !important;
}


#MainMenu {

    visibility:
        hidden;
}


footer {

    visibility:
        hidden;
}


/* ==========================================================
   MAIN CONTENT
========================================================== */

.main .block-container {

    max-width:
        1450px;

    padding-top:
        18px;

    padding-bottom:
        120px;
}


/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"] {

    background:
        __SIDEBAR_BG__ !important;

    backdrop-filter:
        blur(20px);

    -webkit-backdrop-filter:
        blur(20px);

    border-right:
        1px solid
        __BORDER__;
}


/* ==========================================================
   BRAND
========================================================== */

.brand {

    display:
        flex;

    align-items:
        center;

    gap:
        10px;

    padding:
        5px 4px 18px 4px;
}


.brand-logo {

    width:
        40px;

    height:
        40px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        12px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );

    color:
        white;

    font-size:
        19px;

    box-shadow:
        0 8px 24px
        rgba(37,99,235,0.30);
}


.brand-name {

    color:
        __TEXT__;

    font-size:
        17px;

    font-weight:
        750;
}


.brand-description {

    color:
        __MUTED__;

    font-size:
        10px;

    margin-top:
        2px;
}


/* ==========================================================
   SECTION LABEL
========================================================== */

.section-label {

    color:
        __MUTED__;

    font-size:
        10px;

    font-weight:
        700;

    letter-spacing:
        0.08em;

    text-transform:
        uppercase;

    margin:
        16px 3px 8px 3px;
}


/* ==========================================================
   SIDEBAR BUTTONS
========================================================== */

section[data-testid="stSidebar"]
.stButton > button {

    min-height:
        34px !important;

    height:
        34px !important;

    padding:
        4px 8px !important;

    border-radius:
        9px !important;

    color:
        __TEXT__ !important;

    background:
        rgba(255,255,255,0.055) !important;

    border:
        1px solid
        __BORDER__ !important;

    font-size:
        11px !important;
}


section[data-testid="stSidebar"]
.stButton > button:hover {

    background:
        rgba(99,102,241,0.16) !important;

    border-color:
        #6366f1 !important;
}


/* ==========================================================
   MODEL SELECTBOX
========================================================== */

div[data-baseweb="select"] > div {

    min-height:
        35px;

    border-radius:
        9px;

    background:
        __INPUT_BG__ !important;

    border:
        1px solid
        __BORDER__ !important;
}


/* ==========================================================
   CHAT HEADER
========================================================== */

.chat-header {

    padding:
        12px 16px;

    border-radius:
        14px;

    background:
        __CARD_BG__;

    backdrop-filter:
        blur(18px);

    -webkit-backdrop-filter:
        blur(18px);

    border:
        1px solid
        __BORDER__;

    box-shadow:
        0 8px 28px
        rgba(0,0,0,0.14);

    margin-bottom:
        12px;
}


.chat-model-name {

    color:
        __TEXT__;

    font-size:
        15px;

    font-weight:
        750;
}


.status {

    display:
        flex;

    align-items:
        center;

    gap:
        6px;

    margin-top:
        3px;

    color:
        #22c55e;

    font-size:
        10px;
}


.status-dot {

    width:
        6px;

    height:
        6px;

    border-radius:
        50%;

    background:
        #22c55e;

    box-shadow:
        0 0 8px
        rgba(34,197,94,0.75);
}


/* ==========================================================
   WELCOME
========================================================== */

.welcome {

    text-align:
        center;

    padding:
        42px 20px 28px 20px;

    border-radius:
        18px;

    background:
        rgba(5,10,30,0.22);

    backdrop-filter:
        blur(7px);
}


.welcome-logo {

    width:
        62px;

    height:
        62px;

    margin:
        auto;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        18px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );

    color:
        white;

    font-size:
        28px;

    box-shadow:
        0 12px 35px
        rgba(37,99,235,0.30);
}


.welcome-title {

    color:
        __TEXT__;

    font-size:
        24px;

    font-weight:
        750;

    margin-top:
        14px;
}


.welcome-subtitle {

    color:
        __MUTED__;

    font-size:
        12px;

    margin-top:
        5px;
}


/* ==========================================================
   CHAT MESSAGE
========================================================== */

[data-testid="stChatMessage"] {

    background:
        __CARD_BG__ !important;

    backdrop-filter:
        blur(18px);

    -webkit-backdrop-filter:
        blur(18px);

    border:
        1px solid
        __BORDER__;

    border-radius:
        15px;

    padding:
        10px 14px;

    margin:
        7px 0;

    box-shadow:
        0 6px 24px
        rgba(0,0,0,0.10);
}


/* ==========================================================
   CHAT MESSAGE TEXT
========================================================== */

[data-testid="stChatMessage"] p {

    color:
        __TEXT__ !important;

    font-size:
        13px !important;

    line-height:
        1.55 !important;
}


[data-testid="stChatMessage"] strong {

    color:
        __TEXT__ !important;

    font-size:
        13px;
}


/* ==========================================================
   FIXED CHAT INPUT
========================================================== */

[data-testid="stChatInput"] {

    position:
        fixed !important;

    left:
        calc(50% + 70px) !important;

    bottom:
        18px !important;

    transform:
        translateX(-50%) !important;

    width:
        min(
            820px,
            calc(100vw - 520px)
        ) !important;

    z-index:
        9999 !important;

    background:
        __INPUT_BG__ !important;

    backdrop-filter:
        blur(20px);

    -webkit-backdrop-filter:
        blur(20px);

    border:
        1px solid
        __BORDER__ !important;

    border-radius:
        15px !important;

    box-shadow:
        0 12px 45px
        rgba(0,0,0,0.28) !important;
}


[data-testid="stChatInput"] textarea {

    color:
        __TEXT__ !important;

    font-size:
        13px !important;
}


/* ==========================================================
   RIGHT PANEL
========================================================== */

.right-title {

    color:
        __TEXT__;

    font-size:
        20px;

    font-weight:
        750;

    margin:
        2px 0 14px 0;
}


.right-section {

    padding:
        12px;

    margin-bottom:
        10px;

    border-radius:
        13px;

    background:
        __CARD_BG__;

    backdrop-filter:
        blur(18px);

    -webkit-backdrop-filter:
        blur(18px);

    border:
        1px solid
        __BORDER__;

    box-shadow:
        0 6px 22px
        rgba(0,0,0,0.10);
}


.right-section-title {

    color:
        __TEXT__;

    font-size:
        12px;

    font-weight:
        750;

    margin-bottom:
        8px;
}


/* ==========================================================
   RIGHT PANEL BUTTONS
========================================================== */

.stButton > button {

    min-height:
        34px !important;

    border-radius:
        9px !important;

    font-size:
        11px !important;

    color:
        __TEXT__ !important;

    background:
        rgba(255,255,255,0.055) !important;

    border:
        1px solid
        __BORDER__ !important;
}


.stButton > button:hover {

    border-color:
        #6366f1 !important;
}


/* ==========================================================
   DIVIDER
========================================================== */

hr {

    border-color:
        __BORDER__;

    margin:
        9px 0;
}


/* ==========================================================
   MOBILE
========================================================== */

@media (max-width: 900px) {

    [data-testid="stChatInput"] {

        left:
            50% !important;

        width:
            calc(100vw - 28px) !important;
    }

    .main .block-container {

        padding-bottom:
            105px;
    }

}

</style>
"""


# ============================================================
# REPLACE CSS VARIABLES
# ============================================================

CSS = CSS.replace(
    "__PAGE_BG__",
    PAGE_BG
)

CSS = CSS.replace(
    "__OVERLAY__",
    OVERLAY
)

CSS = CSS.replace(
    "__BACKGROUND__",
    background_url
)

CSS = CSS.replace(
    "__SIDEBAR_BG__",
    SIDEBAR_BG
)

CSS = CSS.replace(
    "__CARD_BG__",
    CARD_BG
)

CSS = CSS.replace(
    "__INPUT_BG__",
    INPUT_BG
)

CSS = CSS.replace(
    "__TEXT__",
    TEXT
)

CSS = CSS.replace(
    "__MUTED__",
    MUTED
)

CSS = CSS.replace(
    "__BORDER__",
    BORDER
)


# ============================================================
# APPLY CSS
# ============================================================

st.markdown(
    CSS,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.html(
        """
        <div class="brand">

            <div class="brand-logo">
                🤖
            </div>

            <div>
                <div class="brand-name">
                    Qwen AI
                </div>

                <div class="brand-description">
                    Local AI Assistant
                </div>
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "＋  New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.chat_title = (
            "New Chat"
        )

        st.rerun()


    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">'
        'Chat History'
        '</div>',
        unsafe_allow_html=True
    )


    if st.session_state.saved_chats:

        titles = list(
            st.session_state.saved_chats.keys()
        )

        titles.reverse()


        for index, title in enumerate(titles):

            col1, col2 = st.columns(
                [5, 1],
                gap="small"
            )


            # -----------------------------------------------
            # OPEN CHAT
            # -----------------------------------------------

            with col1:

                if st.button(
                    "💬 " + title,
                    key=f"history_open_{index}",
                    use_container_width=True
                ):

                    chat = (
                        st.session_state
                        .saved_chats[title]
                    )


                    st.session_state.messages = (
                        chat.get(
                            "messages",
                            []
                        )
                    )


                    st.session_state.chat_title = (
                        title
                    )


                    saved_model = chat.get(
                        "model"
                    )


                    if (
                        saved_model
                        and saved_model in models
                    ):

                        st.session_state.selected_model = (
                            saved_model
                        )


                    st.rerun()


            # -----------------------------------------------
            # DELETE
            # -----------------------------------------------

            with col2:

                if st.button(
                    "🗑",
                    key=f"history_delete_{index}",
                    help="Delete chat"
                ):

                    st.session_state.delete_target = (
                        title
                    )

                    st.rerun()


            # -----------------------------------------------
            # CONFIRM DELETE
            # -----------------------------------------------

            if (
                st.session_state.delete_target
                == title
            ):

                st.warning(
                    "Delete this conversation?"
                )


                yes_col, no_col = st.columns(
                    2
                )


                with yes_col:

                    if st.button(
                        "Delete",
                        key=f"confirm_delete_{index}",
                        use_container_width=True
                    ):

                        if title in (
                            st.session_state
                            .saved_chats
                        ):

                            del (
                                st.session_state
                                .saved_chats[title]
                            )


                        save_history()


                        if (
                            st.session_state.chat_title
                            == title
                        ):

                            st.session_state.messages = []

                            st.session_state.chat_title = (
                                "New Chat"
                            )


                        st.session_state.delete_target = (
                            None
                        )

                        st.rerun()


                with no_col:

                    if st.button(
                        "Cancel",
                        key=f"cancel_delete_{index}",
                        use_container_width=True
                    ):

                        st.session_state.delete_target = (
                            None
                        )

                        st.rerun()

    else:

        st.caption(
            "No conversations yet."
        )


    st.markdown("---")


    # --------------------------------------------------------
    # MODEL SELECTOR
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">'
        'AI Model'
        '</div>',
        unsafe_allow_html=True
    )


    if models:

        selected_index = models.index(
            st.session_state.selected_model
        )


        selected_model = st.selectbox(
            "Select model",
            models,
            index=selected_index,
            label_visibility="collapsed"
        )


        st.session_state.selected_model = (
            selected_model
        )

    else:

        st.error(
            "Ollama model not found."
        )

        st.code(
            "ollama list"
        )


# ============================================================
# MAIN LAYOUT
# ============================================================

left_space, center, right = st.columns(
    [0.12, 6.1, 2.0],
    gap="medium"
)


# ============================================================
# CENTER CHAT
# ============================================================

with center:

    current_model = (
        st.session_state.selected_model
        or "Qwen AI"
    )


    # --------------------------------------------------------
    # CHAT HEADER
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="chat-header">

            <div class="chat-model-name">
                🤖 {current_model}
            </div>

            <div class="status">

                <span class="status-dot"></span>

                Local model • Ollama

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # WELCOME
    # --------------------------------------------------------

    if not st.session_state.messages:

        st.html(
            """
            <div class="welcome">

                <div class="welcome-logo">
                    ✨
                </div>

                <div class="welcome-title">
                    How can I help you?
                </div>

                <div class="welcome-subtitle">
                    Ask anything. Your conversation
                    runs locally using Ollama.
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # SHOW CONVERSATION
    # --------------------------------------------------------

    for message in st.session_state.messages:

        role = message.get(
            "role",
            "assistant"
        )

        content = message.get(
            "content",
            ""
        )


        if role == "user":

            with st.chat_message(
                "user",
                avatar="👤"
            ):

                st.markdown(
                    "**You**"
                )

                st.markdown(
                    content
                )

        else:

            with st.chat_message(
                "assistant",
                avatar="🤖"
            ):

                st.markdown(
                    "**"
                    + current_model
                    + "**"
                )

                st.markdown(
                    content
                )


    # ========================================================
    # OLLAMA RESPONSE
    # ========================================================

    def ask_qwen(messages):

        payload = {

            "model":
                st.session_state.selected_model,

            "messages":
                messages,

            "stream":
                True
        }


        try:

            response = requests.post(
                OLLAMA_CHAT_URL,
                json=payload,
                stream=True,
                timeout=180
            )


            response.raise_for_status()


            for line in response.iter_lines(
                decode_unicode=True
            ):

                if not line:
                    continue


                try:

                    data = json.loads(line)

                except json.JSONDecodeError:

                    continue


                if "error" in data:

                    yield (
                        "❌ Ollama error: "
                        + str(
                            data["error"]
                        )
                    )

                    return


                message_data = data.get(
                    "message",
                    {}
                )


                content = message_data.get(
                    "content",
                    ""
                )


                if content:

                    yield content


        except requests.exceptions.ConnectionError:

            yield (
                "❌ Cannot connect to Ollama.\n\n"
                "Make sure Ollama is running."
            )


        except requests.exceptions.Timeout:

            yield (
                "⏱️ Qwen took too long "
                "to respond."
            )


        except requests.exceptions.RequestException as error:

            yield (
                "❌ Ollama request failed:\n\n"
                + str(error)
            )


        except Exception as error:

            yield (
                "❌ Unexpected error:\n\n"
                + str(error)
            )


    # ========================================================
    # CHAT INPUT
    # ========================================================

    prompt = st.chat_input(
        "💬 Message Qwen..."
    )


    if prompt:

        # ----------------------------------------------------
        # CREATE CHAT TITLE
        # ----------------------------------------------------

        if not st.session_state.messages:

            title = prompt.strip()


            if len(title) > 35:

                title = (
                    title[:35]
                    + "..."
                )


            st.session_state.chat_title = (
                title
            )


        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )


        # ----------------------------------------------------
        # DISPLAY USER
        # ----------------------------------------------------

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.markdown(
                "**You**"
            )

            st.markdown(
                prompt
            )


        # ----------------------------------------------------
        # QWEN RESPONSE
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            st.markdown(
                "**"
                + current_model
                + "**"
            )


            response = st.write_stream(
                ask_qwen(
                    st.session_state.messages
                )
            )


        # ----------------------------------------------------
        # SAVE RESPONSE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


        # ----------------------------------------------------
        # AUTO SAVE
        # ----------------------------------------------------

        title = (
            st.session_state.chat_title
            or "New Chat"
        )


        st.session_state.saved_chats[
            title
        ] = {

            "messages":
                st.session_state.messages,

            "model":
                st.session_state.selected_model,

            "saved_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }


        save_history()


        st.rerun()


# ============================================================
# RIGHT SETTINGS
# ============================================================

with right:

    st.html(
        """
        <div class="right-title">
            ⚙️ Settings
        </div>
        """
    )


    # ========================================================
    # APPEARANCE
    # ========================================================

    st.html(
        """
        <div class="right-section">

            <div class="right-section-title">
                🎨 Appearance
            </div>

        </div>
        """
    )


    dark_enabled = st.toggle(
        "Dark mode",
        value=dark_mode
    )


    requested_theme = (
        "dark"
        if dark_enabled
        else "light"
    )


    if requested_theme != (
        st.session_state.theme
    ):

        st.session_state.theme = (
            requested_theme
        )

        st.rerun()


    # ========================================================
    # CONVERSATION
    # ========================================================

    st.html(
        """
        <div class="right-section">

            <div class="right-section-title">
                💾 Conversation
            </div>

        </div>
        """
    )


    if st.button(
        "💾 Save Chat",
        use_container_width=True
    ):

        if st.session_state.messages:

            title = (
                st.session_state.chat_title
                or "New Chat"
            )


            st.session_state.saved_chats[
                title
            ] = {

                "messages":
                    st.session_state.messages,

                "model":
                    st.session_state.selected_model,

                "saved_at":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            }


            if save_history():

                st.success(
                    "Chat saved"
                )

        else:

            st.info(
                "No conversation to save."
            )


    if st.button(
        "🗑️ Clear Current Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.chat_title = (
            "New Chat"
        )

        st.rerun()


    # ========================================================
    # MODEL DETAILS
    # ========================================================

    st.html(
        """
        <div class="right-section">

            <div class="right-section-title">
                🧠 Model Details
            </div>

        </div>
        """
    )


    st.markdown(
        "**Model**"
    )

    st.caption(
        current_model
    )


    st.divider()


    st.markdown(
        "**Engine**"
    )

    st.caption(
        "Ollama"
    )


    st.divider()


    st.markdown(
        "**Location**"
    )

    st.caption(
        "Local"
    )


    st.divider()


    st.markdown(
        "**Status**"
    )


    if models:

        st.success(
            "🟢 Connected"
        )

    else:

        st.error(
            "🔴 Ollama unavailable"
        )


    # ========================================================
    # GENERAL
    # ========================================================

    st.html(
        """
        <div class="right-section">

            <div class="right-section-title">
                ℹ️ General
            </div>

        </div>
        """
    )


    st.caption(
        "Local AI chatbot powered by Ollama."
    )

    st.caption(
        "Your conversations stay on this computer."
    )

    st.caption(
        "Saved chats: "
        + str(
            len(
                st.session_state.saved_chats
            )
        )
    )