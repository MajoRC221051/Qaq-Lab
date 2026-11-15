import base64
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="EMBER", page_icon="🔥", layout="wide", initial_sidebar_state="collapsed")

ASSETS = Path(__file__).parent / "assets"

# ---------- Paleta ----------
BG = "#0B0B0C"        # fondo
SURFACE = "#17120F"   # tarjetas
EMBER = "#E35D0B"     # naranja principal
EMBER_SOFT = "#7A3512"
TEXT = "#F5F1EC"
MUTED = "#8C847C"


@st.cache_data
def gif_b64(name: str) -> str:
    return base64.b64encode((ASSETS / name).read_bytes()).decode()


def inject_css() -> None:
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {{ font-family: 'Outfit', sans-serif; }}

/* Quitar el chrome de Streamlit */
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none !important; }}

.stApp {{
    background:
        radial-gradient(900px 420px at 12% -8%, rgba(227,93,11,.28), transparent 60%),
        radial-gradient(700px 500px at 92% 110%, rgba(227,93,11,.10), transparent 60%),
        {BG};
}}
.block-container {{ max-width: 1180px; padding: 2.2rem 2rem 3rem; }}

/* Marca */
.brand {{ display:flex; align-items:center; gap:.7rem; font-weight:600; letter-spacing:.32em; font-size:1.05rem; color:{TEXT}; }}
.brand i {{ display:inline-flex; gap:3px; align-items:flex-end; height:20px; }}
.brand i b {{ width:3px; background:{MUTED}; border-radius:2px; display:block; }}
.brand i b:nth-child(1) {{ height:12px; }} .brand i b:nth-child(2) {{ height:20px; }} .brand i b:nth-child(3) {{ height:15px; }}

/* Hero */
.hero-title {{ font-size: clamp(2.8rem, 6vw, 4.6rem); font-weight:600; line-height:1.04; letter-spacing:-.02em; color:{TEXT}; margin: 0 0 1.2rem; }}
.hero-sub {{ color:{EMBER}; font-size:1.1rem; font-weight:400; max-width:26ch; line-height:1.45; margin-bottom: 2.4rem; }}

.orb-wrap {{
    position:relative; width:min(100%, 520px); aspect-ratio:1/1; margin-inline:auto;
    border-radius:50%;
    -webkit-mask-image: radial-gradient(circle at center, #000 52%, transparent 71%);
            mask-image: radial-gradient(circle at center, #000 52%, transparent 71%);
}}
.orb-wrap img {{ width:100%; height:100%; object-fit:cover; mix-blend-mode:screen; transform:scale(1.55); }}

/* Botón principal: círculo naranja como en el mockup */
div.stButton > button {{
    background:{EMBER}; color:#fff; border:none; border-radius:999px;
    padding:1.05rem 2.2rem; font-family:'Outfit',sans-serif; font-weight:500; font-size:1.05rem;
    box-shadow: 0 10px 34px rgba(227,93,11,.38);
    transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
}}
div.stButton > button:hover {{ background:#F26A14; color:#fff; transform:translateY(-2px); box-shadow:0 14px 40px rgba(227,93,11,.5); }}
div.stButton > button:focus-visible {{ outline:2px solid {TEXT}; outline-offset:3px; }}
div.stButton > button:active {{ transform:translateY(0); }}

/* Tarjetas del panel */
.greet {{ font-size:2rem; font-weight:600; margin:2rem 0 .2rem; }}
.greet-sub {{ color:{MUTED}; margin-bottom:1.6rem; }}
.stat {{
    background: linear-gradient(150deg, rgba(227,93,11,.22), rgba(255,255,255,.03) 55%), {SURFACE};
    border:1px solid rgba(255,255,255,.06); border-radius:22px; padding:1.6rem 1rem; text-align:center;
}}
.stat .n {{ font-size:2.4rem; font-weight:600; }}
.stat .l {{ color:{MUTED}; font-size:.9rem; }}

@media (prefers-reduced-motion: reduce) {{ div.stButton > button {{ transition:none; }} }}
</style>
""",
        unsafe_allow_html=True,
    )


def landing() -> None:
    st.markdown(
        '<div class="brand"><i><b></b><b></b><b></b></i>EMBER</div>', unsafe_allow_html=True
    )
    st.write("")
    left, right = st.columns([1, 1], gap="large", vertical_alignment="center")

    with left:
        st.markdown(
            """
<h1 class="hero-title">Manage your<br>daily tasks</h1>
<p class="hero-sub">Team and Project management with solution providing App</p>
""",
            unsafe_allow_html=True,
        )
        if st.button("Get Started", key="start"):
            st.session_state.page = "home"
            st.rerun()

    with right:
        st.markdown(
            f'<div class="orb-wrap"><img alt="Esfera de brasas" src="data:image/gif;base64,{gif_b64("ember.gif")}"></div>',
            unsafe_allow_html=True,
        )


def home() -> None:
    top = st.columns([6, 1])
    top[0].markdown('<div class="brand"><i><b></b><b></b><b></b></i>EMBER</div>', unsafe_allow_html=True)
    if top[1].button("Back", key="back"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown('<div class="greet">Hi Ghulam</div><div class="greet-sub">6 tasks are pending</div>', unsafe_allow_html=True)
    st.markdown("### Monthly Review")
    cols = st.columns(4)
    for col, (n, label) in zip(cols, [(22, "Done"), (7, "In progress"), (10, "Ongoing"), (12, "Waiting for review")]):
        col.markdown(f'<div class="stat"><div class="n">{n}</div><div class="l">{label}</div></div>', unsafe_allow_html=True)


inject_css()
st.session_state.setdefault("page", "landing")
{"landing": landing, "home": home}[st.session_state.page]()
