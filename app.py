import base64
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Ember",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent
GIF_CANDIDATES = ["ember.gif.gif", "ember.gif", "ember_gif.gif"]

CSS = """
<style>
:root {
  --bg: #090909; --bg-soft: #111111; --card: #1A1A1A;
  --ember: #F25C05; --ember-light: #FF7A1A;
  --text: #F4F4F2; --muted: #9A9A9A; --border: rgba(255,255,255,0.08);
}
header[data-testid="stHeader"], footer, #MainMenu, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] { display: none !important; }
html, body, .stApp { background: var(--bg) !important; }
.stApp {
  background:
    radial-gradient(700px 420px at 85% 6%, rgba(242,92,5,0.13), transparent 70%),
    var(--bg) !important;
}
.block-container { max-width: 1180px !important; padding: 2rem 1.5rem 3rem !important; }
.em, .em * { box-sizing: border-box; font-family: Inter, Arial, sans-serif; }
.em { color: var(--text); line-height: 1.6; }
.em a { text-decoration: none; }
.em h1, .em h2, .em h3, .em p { margin: 0; }

.nav { display: flex; justify-content: space-between; align-items: center; gap: 24px;
  padding: 18px 0 22px; border-bottom: 1px solid var(--border); flex-wrap: wrap; }
.brand { font-weight: 800; letter-spacing: 0.22em; font-size: 1.05rem; color: var(--text); }
.nav-links { display: flex; gap: 28px; flex-wrap: wrap; align-items: center; }
.nav-item { font-size: 0.92rem; color: var(--muted); display: inline-flex; align-items: center; gap: 8px; }
.nav-item.active { color: var(--ember); font-weight: 600; border-bottom: 2px solid var(--ember); padding-bottom: 2px; }
.nav-item small { font-size: 0.68rem; color: #6d6d6d; border: 1px solid var(--border);
  border-radius: 999px; padding: 1px 8px; }

.hero { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 56px; align-items: center;
  min-height: 78vh; padding: 56px 0; }
.eyebrow { color: var(--ember-light); font-size: 0.78rem; letter-spacing: 0.18em; font-weight: 600; margin-bottom: 22px; }
.hero h1 { font-size: clamp(2.4rem, 5.2vw, 4.2rem); line-height: 1.05; font-weight: 700;
  letter-spacing: -0.02em; margin-bottom: 26px; }
.hero p.lead { color: var(--muted); font-size: 1.1rem; max-width: 34em; margin-bottom: 36px; }
.cta-row { display: flex; align-items: center; gap: 22px; flex-wrap: wrap; }
.btn { background: var(--ember); color: #0b0b0b !important; font-weight: 700; padding: 14px 28px;
  border-radius: 999px; display: inline-block; box-shadow: 0 8px 30px rgba(242,92,5,0.28); }
.btn:hover { background: var(--ember-light); }
.btn:focus-visible { outline: 2px solid var(--text); outline-offset: 3px; }
.scope-note { color: var(--muted); font-size: 0.88rem; }

.visual { background: var(--card); border: 1px solid var(--border); border-radius: 24px; padding: 14px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.5), 0 0 90px rgba(242,92,5,0.16); }
.visual img { width: 100%; height: auto; display: block; border-radius: 14px; }
.visual-empty { aspect-ratio: 16 / 9; border-radius: 14px; display: flex; align-items: center;
  justify-content: center; color: var(--muted); font-size: 0.85rem; text-align: center; padding: 20px;
  background: radial-gradient(circle at 60% 45%, rgba(242,92,5,0.14), #0d0d0d 65%); }

.section { padding: 72px 0 8px; }
.section h2 { font-size: clamp(1.6rem, 3vw, 2.2rem); font-weight: 700; letter-spacing: -0.01em; margin-bottom: 20px; }
.about { background: var(--bg-soft); border: 1px solid var(--border); border-radius: 24px;
  padding: 48px; margin-top: 40px; scroll-margin-top: 24px; }
.about p { color: #cfcfcc; font-size: 1.05rem; max-width: 52em; }

.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 32px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35); }
.card.accent { border-top: 2px solid var(--ember); }
.card h3 { font-size: 1.15rem; font-weight: 650; margin-bottom: 12px; line-height: 1.3; }
.card p { color: var(--muted); font-size: 0.96rem; }
.step-n { color: var(--ember-light); font-weight: 700; font-size: 0.95rem; margin-bottom: 14px; }
.step-t { font-size: 1.1rem; font-weight: 650; margin-bottom: 10px; }

.plan { padding: 24px; }
.plan h3 { font-size: 1.02rem; margin-bottom: 8px; }
.status { display: inline-block; font-size: 0.72rem; padding: 3px 12px; border-radius: 999px; margin-bottom: 14px;
  border: 1px solid var(--border); color: var(--muted); }
.status.on { color: var(--ember-light); border-color: rgba(242,92,5,0.5); background: rgba(242,92,5,0.1); }
.plan.off { opacity: 0.8; }

.scope { margin-top: 72px; background: linear-gradient(135deg, rgba(242,92,5,0.10), rgba(26,26,26,1) 55%);
  border: 1px solid rgba(242,92,5,0.28); border-radius: 22px; padding: 40px; }
.scope h2 { font-size: 1.3rem; margin-bottom: 12px; }
.scope p { color: #cfcfcc; max-width: 52em; }

.footer { margin-top: 80px; padding-top: 28px; border-top: 1px solid var(--border);
  color: var(--muted); font-size: 0.88rem; text-align: center; }

@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; gap: 36px; min-height: auto; padding: 36px 0; }
  .grid3, .grid4 { grid-template-columns: 1fr; }
  .about, .scope { padding: 28px; }
  .nav-links { gap: 16px 20px; }
}
@media (min-width: 901px) and (max-width: 1100px) {
  .grid4 { grid-template-columns: repeat(2, 1fr); }
}
</style>
"""


def load_gif_html() -> str:
    for name in GIF_CANDIDATES:
        path = BASE_DIR / name
        if path.is_file():
            data = base64.b64encode(path.read_bytes()).decode()
            return f'<img src="data:image/gif;base64,{data}" alt="Animated visual of a sample burning">'
    return '<div class="visual-empty">Visual not found. Place ember.gif.gif next to app.py.</div>'


def html(block: str) -> str:
    return "\n".join(line.strip() for line in block.splitlines() if line.strip())


nav = html("""
<div class="nav">
  <span class="brand">EMBER</span>
  <div class="nav-links">
    <span class="nav-item active">Home</span>
    <span class="nav-item">Experiment Explorer <small>Planned</small></span>
    <span class="nav-item">Accident Cases <small>Planned</small></span>
    <span class="nav-item">Data Lab <small>Planned</small></span>
  </div>
</div>
""")

hero = f"""
<div class="hero">
  <div>
    <div class="eyebrow">NASA PSI EXPERIMENTAL DATA</div>
    <h1>Find the experiment behind the question.</h1>
    <p class="lead">Ember organizes experimental conditions and documented outcomes so research students can locate relevant evidence without searching through disconnected reports.</p>
    <div class="cta-row">
      <a class="btn" href="#about">Understand Ember</a>
      <span class="scope-note">Prototype scope: BASS-II / SIBAL</span>
    </div>
  </div>
  <div class="visual">{load_gif_html()}</div>
</div>
"""

body = html("""
<div class="about" id="about">
  <h2>From scattered reports to usable evidence</h2>
  <p>Ember organizes experimental information from NASA’s Physical Sciences Informatics platform for research students. The prototype begins with BASS-II/SIBAL and connects variables such as material, oxygen concentration, airflow, sample geometry, sample reuse, ignition status, and documented outcome. Its purpose is to make relevant experiments easier to find and compare while keeping the original source, missing information, and limits of interpretation visible.</p>
</div>

<div class="section">
  <div class="grid3">
    <div class="card accent">
      <h3>Search by experimental conditions</h3>
      <p>Locate experiments using variables such as material, oxygen concentration, airflow, geometry, ignition status, and documented outcome.</p>
    </div>
    <div class="card accent">
      <h3>Compare documented results</h3>
      <p>Review how different experimental conditions and observed outcomes are represented in the available records without converting descriptive evidence into unsupported predictions.</p>
    </div>
    <div class="card accent">
      <h3>Keep the source visible</h3>
      <p>Preserve the connection between every result, its original report, missing fields, and the limitations that affect its interpretation.</p>
    </div>
  </div>
</div>

<div class="section">
  <h2>How Ember works</h2>
  <div class="grid3">
    <div class="card">
      <div class="step-n">01</div>
      <div class="step-t">Define the conditions</div>
      <p>Select the variables that are relevant to the research question.</p>
    </div>
    <div class="card">
      <div class="step-n">02</div>
      <div class="step-t">Review matching experiments</div>
      <p>Examine the documented conditions, observations, and available outcomes.</p>
    </div>
    <div class="card">
      <div class="step-n">03</div>
      <div class="step-t">Verify the evidence</div>
      <p>Consult the source and consider missing information before drawing conclusions.</p>
    </div>
  </div>
</div>

<div class="section">
  <h2>Planned platform structure</h2>
  <div class="grid4">
    <div class="card plan">
      <span class="status on">Available</span>
      <h3>Home</h3>
      <p>Project purpose and scope.</p>
    </div>
    <div class="card plan off">
      <span class="status">Planned</span>
      <h3>Experiment Explorer</h3>
      <p>Search and filter PSI experiments.</p>
    </div>
    <div class="card plan off">
      <span class="status">Planned</span>
      <h3>Accident Cases</h3>
      <p>Review documented cases and their relevant variables.</p>
    </div>
    <div class="card plan off">
      <span class="status">Planned</span>
      <h3>Data Lab</h3>
      <p>Explore selected records through tables and descriptive visualizations.</p>
    </div>
  </div>
</div>

<div class="scope">
  <h2>Prototype scope</h2>
  <p>The current prototype uses the available BASS-II/SIBAL records to demonstrate how PSI information can be organized and explored. It does not estimate fire risk, replace the original scientific reports, or generalize results to experimental conditions that were not tested.</p>
</div>

<div class="footer">Ember — Experimental evidence organized for research.</div>
""")

st.markdown(CSS, unsafe_allow_html=True)
st.markdown(f'<div class="em">{nav}{hero}{body}</div>', unsafe_allow_html=True)
