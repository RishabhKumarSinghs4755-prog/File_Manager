import streamlit as st
from pathlib import Path
import os

# ---------------------------------------------------------------- page setup
st.set_page_config(page_title="File Manager", page_icon="🗂️", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=IBM+Plex+Sans:wght@400;500&display=swap');

    :root {
        --bg: #14101f;
        --card: #1e1930;
        --line: #342d52;
        --text: #e9e6f5;
        --muted: #9a93b8;
        --amber: #ffb454;
        --lilac: #a99bff;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--text);
    }
    .stApp { background: var(--bg); }
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    .stApp label, .stApp p, .stApp span, .stApp li { color: var(--text); }

    .hero {
        background: linear-gradient(135deg, #251d3f 0%, #1a1530 100%);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 2.2rem 2rem 2rem 2rem;
        margin-bottom: 1.6rem;
        border-bottom: 5px solid var(--amber);
    }
    .hero h1 {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin: 0;
        padding: 0;
    }
    .hero p {
        color: var(--muted);
        margin: 0.5rem 0 0 0;
        font-size: 1.05rem;
    }

    /* tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 0.4rem; border-bottom: 2px solid var(--line); }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 600;
        font-size: 1.02rem;
        padding: 0.6rem 1.1rem;
        color: var(--muted);
    }
    .stTabs [aria-selected="true"] { color: var(--amber); }
    .stTabs [data-baseweb="tab-highlight"] { background-color: var(--amber); height: 4px; }

    /* inputs */
    .stTextInput input, .stTextArea textarea {
        background: var(--card);
        border: 1.5px solid var(--line);
        border-radius: 12px;
        color: var(--text);
    }
    .stTextInput > div > div, .stTextArea > div > div {
        background: transparent;
        border: none;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--lilac);
        box-shadow: 0 0 0 3px rgba(169, 155, 255, 0.28);
    }

    /* radio */
    .stRadio [role="radiogroup"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.8rem 1rem;
    }

    /* code block (file content) */
    .stCode, .stCode pre, [data-testid="stCode"] pre {
        background: var(--card) !important;
        border: 1px solid var(--line);
        border-radius: 12px;
    }
    .stCode code { color: var(--amber) !important; }

    /* expander */
    [data-testid="stExpander"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
    }
    [data-testid="stExpander"] summary { color: var(--text); }
    code { color: var(--amber); background: #2a2342; border-radius: 6px; }

    /* buttons */
    .stButton > button {
        background: var(--amber);
        color: #2a1a05;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.6rem;
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 600;
        transition: background 0.15s ease, transform 0.15s ease;
    }
    .stButton > button p { color: #2a1a05; }
    .stButton > button:hover {
        background: var(--lilac);
        color: #1a1530;
        transform: translateY(-1px);
    }
    .stButton > button:hover p { color: #1a1530; }
    .stButton > button:focus-visible { outline: 3px solid var(--lilac); }

    .foot {
        text-align: center;
        color: var(--muted);
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    </style>
    <div class="hero">
        <h1>File Manager</h1>
        <p>Create, read, update and delete text files from one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- original logic
def createfile():
    try:
        name = st.text_input("please tell your file name:-", key="create_name")
        data = st.text_area("What you want to write:-", key="create_data", height=160)
        if st.button("Create file", key="create_btn"):
            path = Path(name)
            if not path.exists():
                with open(path, 'w') as f:
                    f.write(data)
                st.success("file created successfully")
            else:
                st.error("Error file name already exists")
    except Exception as err:
        st.error(f"an error occured as {err}")


def readfile():
    try:
        name = st.text_input("please tell your file name:-", key="read_name")
        if st.button("Read file", key="read_btn"):
            path = Path(name)
            if path.exists():
                with open(path, 'r') as f:
                    content = f.read()
                    st.markdown("**your file content :-**")
                    st.code(content, language=None)
            else:
                st.error("Error file name do not exists")
    except Exception as err:
        st.error(f"an occured as {err}")


def updatefile():
    try:
        name = st.text_input("please tell your file name:-", key="update_name")
        st.markdown("**operation**")
        operation = st.radio(
            "operation",
            ["1. Renaming the file", "2. Appending the content", "3. Overwriting the file"],
            key="update_choice",
            label_visibility="collapsed",
        )
        choice = int(operation[0])

        new_name = ""
        data = ""
        if choice == 1:
            new_name = st.text_input("Enter the new name of the file:-", key="update_new_name")
        elif choice == 2:
            data = st.text_area("what do you want to append:-", key="update_append", height=140)
        elif choice == 3:
            data = st.text_area("what do you want to overwrite:-", key="update_overwrite", height=140)

        if st.button("Update file", key="update_btn"):
            path = Path(name)
            if path.exists():
                if choice == 1:
                    new_path = Path(new_name)
                    if not new_path.exists():
                        path.rename(new_name)
                        st.success("renamed successfully")
                    else:
                        st.error("file name is already exists")
                elif choice == 2:
                    with open(path, 'a') as f:
                        f.write(" \n" + data)
                    st.success("Successfully appended")
                elif choice == 3:
                    with open(path, 'w') as f:
                        f.write(" \n" + data)
                    st.success("successfully overwritten")
                else:
                    st.error("Invalide choice entered")
            else:
                st.error("Error file name do not exists")
    except Exception as err:
        st.error(f"an error occured as {err}")


def deletefile():
    try:
        name = st.text_input("please tell your file name:-", key="delete_name")
        if st.button("Delete file", key="delete_btn"):
            path = Path(name)
            if path.exists():
                path.unlink()
                st.success("file delete successfully")
            else:
                st.error("Error file name do not exists")
    except Exception as err:
        st.error(f"an error occured as {err}")


# ---------------------------------------------------------------- menu
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["Create a file", "Read a file", "Update a file", "Delete a file"]
)

with tab_create:
    createfile()

with tab_read:
    readfile()

with tab_update:
    updatefile()

with tab_delete:
    deletefile()

# ---------------------------------------------------------------- extras (UI only)
with st.expander("Files in this folder"):
    files = sorted(p.name for p in Path(".").iterdir() if p.is_file() and p.suffix != ".py")
    if files:
        for file_name in files:
            st.markdown(f"- `{file_name}`")
    else:
        st.caption("No files yet. Create one in the first tab.")

st.markdown('<div class="foot">Built with Python and Streamlit</div>', unsafe_allow_html=True)