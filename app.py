import base64
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Ember",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
INVESTIGATIONS_PATH = DATA_DIR / "investigations.csv"
BASSII_TESTS_PATH = DATA_DIR / "bassii_sibal_tests_EN.csv"
ACCIDENT_CASES_PATH = DATA_DIR / "accident_cases.csv"

BASSII_REPORT_URL = "https://ntrs.nasa.gov/citations/20210011385"
SAME_PSI_URL = "https://psi.nasa.gov/physci/repo/data/investigations/PSI-102"

GIF_CANDIDATES = [
    ASSETS_DIR / "ember.gif.gif",
    ASSETS_DIR / "ember.gif",
    ASSETS_DIR / "ember_gif.gif",
    BASE_DIR / "ember.gif.gif",
    BASE_DIR / "ember.gif",
    BASE_DIR / "ember_gif.gif",
]

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
a.nav-item:hover { color: var(--text); }
.em a.nav-item { color: var(--muted) !important; }
.em a.nav-item:hover { color: var(--text) !important; }
.em a.nav-item.active { color: var(--ember) !important; }
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
.grid5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 18px; }
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

.library-header { padding: 64px 0 40px; }
.library-header h1 { color: var(--text); font-size: clamp(2.2rem, 4vw, 3.6rem); line-height: 1.08;
  margin-bottom: 18px; }
.library-header p { color: var(--muted); max-width: 48rem; font-size: 1.04rem; }
.results-count { color: var(--muted); margin: 28px 0 18px; font-size: 0.9rem; }

.investigation-card { min-height: 370px; background: var(--card); border: 1px solid var(--border);
  border-radius: 20px; padding: 28px; margin-bottom: 24px; font-family: Inter, Arial, sans-serif;
  color: var(--text); display: flex; flex-direction: column; }
.investigation-card:hover { border-color: rgba(242,92,5,0.45); }
.psi-id { color: var(--ember-light); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.12em;
  margin-bottom: 12px; }
.investigation-card h3 { color: var(--text); font-size: 1.18rem; line-height: 1.35; margin: 0 0 14px; }
.investigation-card p { color: var(--muted); font-size: 0.92rem; line-height: 1.55; margin: 0; }
.card-meta { color: #ccccca; font-size: 0.82rem; margin-bottom: 16px; line-height: 1.55; }
.resource-list { display: flex; flex-wrap: wrap; gap: 7px; margin: 18px 0; }
.resource-tag { color: #c7c7c4; background: #111111; border: 1px solid var(--border);
  border-radius: 999px; padding: 4px 10px; font-size: 0.72rem; }
.coverage { border-top: 1px solid var(--border); padding-top: 16px; margin-top: auto;
  color: #cfcfcc; font-size: 0.85rem; }
.card-actions { display: flex; gap: 18px; align-items: center; flex-wrap: wrap; margin-top: 18px; }
.source-link { color: var(--ember-light) !important; font-size: 0.86rem; font-weight: 600; }
.source-link:hover { color: var(--text) !important; }
.source-link.secondary { color: #cfcfcc !important; }

.detail-back { display: inline-block; color: var(--ember-light) !important; font-size: 0.88rem;
  font-weight: 600; margin: 28px 0; }
.detail-panel { background: var(--card); border: 1px solid var(--border); border-radius: 22px;
  padding: 38px; }
.detail-panel h1 { font-size: clamp(1.8rem, 3.5vw, 3rem); line-height: 1.15; margin-bottom: 18px; }
.detail-panel h2 { font-size: 1.2rem; margin: 34px 0 12px; }
.detail-panel p { color: #cfcfcc; }
.detail-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 28px 0; }
.detail-item { background: var(--bg-soft); border: 1px solid var(--border); border-radius: 14px; padding: 16px; }
.detail-label { color: var(--muted); font-size: 0.72rem; margin-bottom: 5px; }
.detail-value { color: var(--text); font-size: 0.9rem; word-break: break-word; }

.explorer-header { padding: 64px 0 30px; }
.explorer-header h1 { color: var(--text); font-size: clamp(2.2rem, 4vw, 3.6rem); line-height: 1.08;
  margin-bottom: 18px; }
.explorer-header p { color: var(--muted); max-width: 52rem; font-size: 1.04rem; }
.dataset-strip { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
.dataset-stat { color: #cfcfcc; background: var(--bg-soft); border: 1px solid var(--border);
  border-radius: 999px; padding: 6px 13px; font-size: 0.78rem; }
.question-intro { margin: 18px 0 24px; }
.question-intro h2 { color: var(--text); font-size: 1.35rem; margin-bottom: 8px; }
.question-intro p { color: var(--muted); max-width: 52rem; font-size: 0.93rem; }
.fixed-condition { background: var(--bg-soft); border: 1px solid var(--border); border-radius: 14px;
  padding: 14px 16px; margin: 6px 0 18px; color: #cfcfcc; font-size: 0.88rem; }
.fixed-condition strong { color: var(--text); }
.evidence-summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 34px 0 22px; }
.summary-item { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 18px; }
.summary-label { color: var(--muted); font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase;
  margin-bottom: 7px; }
.summary-value { color: var(--text); font-size: 0.96rem; font-weight: 650; line-height: 1.35; }
.coverage-badge { display: inline-block; border-radius: 999px; padding: 5px 11px; font-size: 0.75rem;
  font-weight: 650; border: 1px solid var(--border); }
.coverage-badge.direct { color: #ff9a52; border-color: rgba(242,92,5,0.55); background: rgba(242,92,5,0.12); }
.coverage-badge.partial { color: #e7b55a; border-color: rgba(231,181,90,0.45); background: rgba(231,181,90,0.09); }
.coverage-badge.documentary { color: #78c8c3; border-color: rgba(120,200,195,0.42); background: rgba(120,200,195,0.08); }
.coverage-badge.outside { color: #d89595; border-color: rgba(216,149,149,0.40); background: rgba(216,149,149,0.08); }
.result-explanation { background: var(--bg-soft); border: 1px solid var(--border); border-radius: 16px;
  padding: 20px; margin-bottom: 22px; }
.result-explanation h3 { color: var(--text); font-size: 1rem; margin-bottom: 8px; }
.result-explanation p { color: #cfcfcc; font-size: 0.9rem; }
.match-card { background: var(--card); border: 1px solid var(--border); border-radius: 18px;
  padding: 24px; margin-bottom: 18px; }
.match-card h3 { color: var(--text); font-size: 1.05rem; margin-bottom: 12px; }
.condition-chips { display: flex; flex-wrap: wrap; gap: 7px; margin: 12px 0 16px; }
.condition-chip { color: #c9c9c6; background: #101010; border: 1px solid var(--border);
  border-radius: 999px; padding: 4px 10px; font-size: 0.72rem; }
.match-card p { color: #cfcfcc; font-size: 0.88rem; margin: 7px 0; }
.match-card .why { color: var(--muted); }
.limitation { border-top: 1px solid var(--border); margin-top: 14px; padding-top: 13px;
  color: var(--muted) !important; font-size: 0.8rem !important; }
.documentary-panel { background: linear-gradient(135deg, rgba(120,200,195,0.07), var(--card) 55%);
  border: 1px solid rgba(120,200,195,0.28); border-radius: 20px; padding: 28px; }
.documentary-panel h2 { color: var(--text); font-size: 1.25rem; margin-bottom: 12px; }
.documentary-panel p { color: #cfcfcc; margin-bottom: 12px; }

.cases-header { padding: 64px 0 32px; }
.cases-header h1 { color: var(--text); font-size: clamp(2.2rem, 4vw, 3.6rem); line-height: 1.08;
  margin-bottom: 18px; }
.cases-header p { color: var(--muted); max-width: 54rem; font-size: 1.04rem; }
.case-count { color: var(--muted); font-size: 0.9rem; margin: 28px 0 14px; }
.case-card { background: var(--card); border: 1px solid var(--border); border-radius: 22px;
  padding: 34px; margin-top: 18px; }
.case-card h2 { color: var(--text); font-size: clamp(1.55rem, 3vw, 2.15rem); line-height: 1.15;
  margin: 0 0 14px; }
.case-card h3 { color: var(--text); font-size: 1rem; margin: 0 0 9px; }
.case-card p { color: #cfcfcc; font-size: 0.91rem; margin: 0; }
.case-meta { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 26px; }
.case-tag { color: #c9c9c6; background: #101010; border: 1px solid var(--border);
  border-radius: 999px; padding: 5px 11px; font-size: 0.73rem; }
.case-overview { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 26px; }
.case-overview-item { background: var(--bg-soft); border: 1px solid var(--border); border-radius: 14px;
  padding: 16px; }
.case-section { border-top: 1px solid var(--border); padding-top: 20px; margin-top: 20px; }
.case-list { display: grid; gap: 8px; }
.case-list-item { color: #cfcfcc; background: #101010; border: 1px solid var(--border);
  border-radius: 12px; padding: 10px 13px; font-size: 0.86rem; }
.psi-connection { background: linear-gradient(135deg, rgba(242,92,5,0.09), rgba(26,26,26,1) 60%);
  border: 1px solid rgba(242,92,5,0.28); border-radius: 16px; padding: 20px; }
.evidence-boundary { color: var(--muted) !important; font-size: 0.84rem !important; }

div[data-testid="stTextInput"] input { background: var(--bg-soft); color: var(--text);
  border: 1px solid var(--border); }
div[data-testid="stNumberInput"] input { background: var(--bg-soft); color: var(--text);
  border-color: var(--border); }
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div { background: var(--bg-soft); color: var(--text);
  border-color: var(--border); }
div[data-testid="stButton"] button { background: var(--ember); color: #0b0b0b; border: 0;
  border-radius: 999px; font-weight: 700; padding-left: 24px; padding-right: 24px; }
div[data-testid="stButton"] button:hover { background: var(--ember-light); color: #0b0b0b; border: 0; }

.stat-hint { color: var(--muted); font-size: 0.74rem; margin-top: 6px; line-height: 1.4; }
.documentary-panel h3, .result-explanation h3 { color: var(--text); font-size: 1rem; margin-bottom: 8px; }
.documentary-panel { margin-bottom: 18px; }
div[data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--border); }
button[data-baseweb="tab"] p { color: var(--muted) !important; font-weight: 600; }
button[data-baseweb="tab"][aria-selected="true"] p { color: var(--ember-light) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--ember) !important; }
div[data-testid="stDownloadButton"] button { background: transparent; color: var(--ember-light);
  border: 1px solid rgba(242,92,5,0.5); border-radius: 999px; font-weight: 600; }
div[data-testid="stDownloadButton"] button:hover { background: rgba(242,92,5,0.12); color: var(--text);
  border-color: var(--ember); }

.footer { margin-top: 80px; padding-top: 28px; border-top: 1px solid var(--border);
  color: var(--muted); font-size: 0.88rem; text-align: center; }

@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; gap: 36px; min-height: auto; padding: 36px 0; }
  .grid3, .grid4, .grid5, .detail-grid, .evidence-summary, .case-overview { grid-template-columns: 1fr; }
  .about, .scope, .detail-panel { padding: 28px; }
  .nav-links { gap: 16px 20px; }
}
@media (min-width: 901px) and (max-width: 1100px) {
  .grid4, .grid5 { grid-template-columns: repeat(2, 1fr); }
  .detail-grid, .evidence-summary, .case-overview { grid-template-columns: repeat(2, 1fr); }
}
</style>
"""


def load_gif_html() -> str:
    for path in GIF_CANDIDATES:
        if path.is_file():
            data = base64.b64encode(path.read_bytes()).decode()
            return (
                '<img src="data:image/gif;base64,'
                f'{data}" alt="Animated visual of a sample burning">'
            )
    return (
        '<div class="visual-empty">Visual not found. Place ember.gif.gif '
        'inside the assets folder.</div>'
    )


def html(block: str) -> str:
    return "\n".join(line.strip() for line in block.splitlines() if line.strip())


def get_query_value(name: str, default: str = "") -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def render_nav(active_page: str) -> str:
    home_class = "nav-item active" if active_page == "home" else "nav-item"
    library_class = "nav-item active" if active_page == "library" else "nav-item"
    explorer_class = "nav-item active" if active_page == "explorer" else "nav-item"
    accidents_class = "nav-item active" if active_page == "accidents" else "nav-item"
    datalab_class = "nav-item active" if active_page == "datalab" else "nav-item"

    return html(
        f"""
        <div class="nav">
          <span class="brand">EMBER</span>
          <div class="nav-links">
            <a class="{home_class}" href="?page=home" target="_self">Home</a>
            <a class="{library_class}" href="?page=library" target="_self">Library</a>
            <a class="{explorer_class}" href="?page=explorer" target="_self">Experiment Explorer</a>
            <a class="{accidents_class}" href="?page=accidents" target="_self">Accident Cases</a>
            <a class="{datalab_class}" href="?page=datalab" target="_self">Data Lab</a>
          </div>
        </div>
        """
    )


hero = html(f"""
<div class="hero">
  <div>
    <div class="eyebrow">NASA PSI EXPERIMENTAL DATA</div>
    <h1>Find the experiment behind the question.</h1>
    <p class="lead">Ember organizes experimental conditions and documented outcomes so research students can locate relevant evidence without searching through disconnected reports.</p>
    <div class="cta-row">
      <a class="btn" href="#about">Understand Ember</a>
      <span class="scope-note">Prototype scope: BASS-II / SIBAL and SAME</span>
    </div>
  </div>
  <div class="visual">{load_gif_html()}</div>
</div>
""")

body = html(
    """
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
      <div class="grid5">
        <div class="card plan">
          <span class="status on">Available</span>
          <h3>Home</h3>
          <p>Project purpose and scope.</p>
        </div>
        <div class="card plan">
          <span class="status on">Available</span>
          <h3>Library</h3>
          <p>Browse PSI investigations and available sources.</p>
        </div>
        <div class="card plan">
          <span class="status on">Available</span>
          <h3>Experiment Explorer</h3>
          <p>Route a research question and review supporting evidence.</p>
        </div>
        <div class="card plan">
          <span class="status on">Available</span>
          <h3>Accident Cases</h3>
          <p>Review documented incidents, operational factors, and evidence limits.</p>
        </div>
        <div class="card plan">
          <span class="status on">Available</span>
          <h3>Data Lab</h3>
          <p>Explore selected records through tables and descriptive visualizations.</p>
        </div>
      </div>
    </div>

    <div class="scope">
      <h2>Prototype scope</h2>
      <p>The current prototype matches questions against available BASS-II/SIBAL records and routes smoke-detection questions to SAME documentation. It does not estimate fire risk, replace the original scientific reports, or generalize results to experimental conditions that were not tested.</p>
    </div>

    <div class="footer">Ember — Experimental evidence organized for research.</div>
    """
)


@st.cache_data(show_spinner=False)
def load_investigations() -> pd.DataFrame:
    if not INVESTIGATIONS_PATH.is_file():
        raise FileNotFoundError(
            f"Missing file: {INVESTIGATIONS_PATH}. "
            "Place investigations.csv inside the data folder."
        )

    dataframe = pd.read_csv(INVESTIGATIONS_PATH).fillna("")

    required_columns = {
        "psi_id",
        "acronym",
        "title",
        "research_area",
        "subresearch_area",
        "project_type",
        "nasa_center",
        "objective_short",
        "available_resources",
        "experimental_table_status",
        "ember_status",
        "ember_record_count",
        "source_url",
    }

    missing_columns = required_columns.difference(dataframe.columns)
    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing columns in investigations.csv: {missing_text}")

    optional_defaults = {
        "flight_platform": "",
        "start_date": "",
        "end_date": "",
        "doi": "",
        "license": "",
        "modeling_table_status": "Not reviewed",
        "related_investigations": "",
    }

    for column, default_value in optional_defaults.items():
        if column not in dataframe.columns:
            dataframe[column] = default_value

    dataframe["ember_record_count"] = (
        pd.to_numeric(dataframe["ember_record_count"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    return dataframe


@st.cache_data(show_spinner=False)
def load_bassii_tests() -> pd.DataFrame:
    if not BASSII_TESTS_PATH.is_file():
        raise FileNotFoundError(
            f"Missing file: {BASSII_TESTS_PATH}. "
            "Place bassii_sibal_tests_EN.csv inside the data folder."
        )

    dataframe = pd.read_csv(BASSII_TESTS_PATH)

    required_columns = {
        "test_id",
        "investigation",
        "material",
        "sample_width_cm",
        "airflow_start_cm_s",
        "airflow_end_cm_s",
        "airflow_profile",
        "oxygen_vol_pct",
        "reused_sample",
        "observed_outcome",
        "ignited_explicit",
        "exclusion_reason",
        "source_page",
        "source_table",
    }

    missing_columns = required_columns.difference(dataframe.columns)
    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"Missing columns in bassii_sibal_tests_EN.csv: {missing_text}"
        )

    numeric_columns = [
        "sample_width_cm",
        "airflow_start_cm_s",
        "airflow_end_cm_s",
        "oxygen_vol_pct",
    ]
    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column], errors="coerce"
        )

    text_columns = [
        "test_id",
        "investigation",
        "material",
        "airflow_profile",
        "reused_sample",
        "observed_outcome",
        "ignited_explicit",
        "exclusion_reason",
        "source_table",
    ]
    for column in text_columns:
        dataframe[column] = dataframe[column].fillna("").astype(str)

    return dataframe


@st.cache_data(show_spinner=False)
def load_accident_cases() -> pd.DataFrame:
    if not ACCIDENT_CASES_PATH.is_file():
        raise FileNotFoundError(
            f"Missing file: {ACCIDENT_CASES_PATH}. "
            "Place accident_cases.csv inside the data folder."
        )

    dataframe = pd.read_csv(
        ACCIDENT_CASES_PATH,
        keep_default_na=False,
    )

    required_columns = {
        "case_id",
        "title",
        "event_date",
        "setting",
        "event_type",
        "crew_affected",
        "outcome",
        "initiating_event",
        "contributing_factors",
        "operational_consequences",
        "response_actions",
        "research_focus",
        "related_psi",
        "relationship_type",
        "psi_relation_note",
        "evidence_level",
        "interpretation_limit",
        "source_title",
        "source_url",
    }

    missing_columns = required_columns.difference(dataframe.columns)
    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"Missing columns in accident_cases.csv: {missing_text}"
        )

    dataframe["crew_affected"] = (
        pd.to_numeric(dataframe["crew_affected"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    return dataframe


def split_pipe_values(value: object) -> list[str]:
    return [
        item.strip()
        for item in str(value).split("|")
        if item.strip()
    ]


FIELD_METADATA = {
    "oxygen_vol_pct": {
        "label": "Oxygen concentration",
        "unit": "vol. %",
        "kind": "numeric",
    },
    "airflow_start_cm_s": {
        "label": "Initial airflow",
        "unit": "cm/s",
        "kind": "numeric",
    },
    "airflow_end_cm_s": {
        "label": "Final airflow",
        "unit": "cm/s",
        "kind": "numeric",
    },
    "sample_width_cm": {
        "label": "Sample width",
        "unit": "cm",
        "kind": "numeric",
    },
    "airflow_profile": {
        "label": "Airflow profile",
        "unit": "",
        "kind": "categorical",
    },
    "reused_sample": {
        "label": "Sample condition",
        "unit": "",
        "kind": "categorical",
    },
    "ignited_explicit": {
        "label": "Explicit ignition",
        "unit": "",
        "kind": "categorical",
    },
    "observed_outcome": {
        "label": "Documented outcome",
        "unit": "",
        "kind": "categorical",
    },
}


def display_condition_value(field: str, value: object) -> str:
    if pd.isna(value) or str(value).strip() == "":
        return "Not reported"

    if field == "reused_sample":
        return "Reused sample" if str(value) == "Yes" else "New sample"

    metadata = FIELD_METADATA[field]
    if metadata["kind"] == "numeric":
        number = float(value)
        formatted = f"{number:.2f}".rstrip("0").rstrip(".")
        unit = metadata["unit"]
        return f"{formatted} {unit}".strip()

    return str(value)


def values_match(field: str, row_value: object, query_value: object) -> bool:
    metadata = FIELD_METADATA[field]
    if pd.isna(row_value) or str(row_value).strip() == "":
        return False

    if metadata["kind"] == "numeric":
        return abs(float(row_value) - float(query_value)) < 1e-9

    return str(row_value).casefold() == str(query_value).casefold()


def outside_numeric_conditions(
    dataframe: pd.DataFrame,
    query: dict[str, object],
) -> list[str]:
    outside = []
    for field, query_value in query.items():
        metadata = FIELD_METADATA[field]
        if metadata["kind"] != "numeric":
            continue

        available = dataframe[field].dropna()
        if available.empty:
            outside.append(metadata["label"])
            continue

        minimum = float(available.min())
        maximum = float(available.max())
        value = float(query_value)
        if value < minimum or value > maximum:
            outside.append(
                f"{metadata['label']} {display_condition_value(field, value)} "
                f"(available range: {display_condition_value(field, minimum)} to "
                f"{display_condition_value(field, maximum)})"
            )

    return outside


def rank_evidence_records(
    dataframe: pd.DataFrame,
    query: dict[str, object],
) -> pd.DataFrame:
    ranked = dataframe.copy()
    exact_counts = pd.Series(0, index=ranked.index, dtype="int64")
    missing_counts = pd.Series(0, index=ranked.index, dtype="int64")
    distances = pd.Series(0.0, index=ranked.index, dtype="float64")

    for field, query_value in query.items():
        metadata = FIELD_METADATA[field]
        missing = ranked[field].isna() | (
            ranked[field].astype(str).str.strip() == ""
        )
        missing_counts += missing.astype(int)

        if metadata["kind"] == "numeric":
            available = ranked[field].dropna()
            field_range = float(available.max() - available.min())
            if field_range == 0:
                field_range = 1.0

            differences = (
                ranked[field].astype(float) - float(query_value)
            ).abs()
            exact_counts += (differences < 1e-9).astype(int)
            distances += differences.fillna(field_range) / field_range
        else:
            matches = (
                ranked[field].astype(str).str.casefold()
                == str(query_value).casefold()
            ) & ~missing
            exact_counts += matches.astype(int)
            distances += (~matches).astype(float)

    ranked["_exact_condition_count"] = exact_counts
    ranked["_missing_condition_count"] = missing_counts
    ranked["_distance"] = distances / max(len(query), 1)

    return ranked.sort_values(
        by=[
            "_exact_condition_count",
            "_missing_condition_count",
            "_distance",
            "test_id",
        ],
        ascending=[False, True, True, True],
    )


def match_evidence(
    dataframe: pd.DataFrame,
    query: dict[str, object],
) -> dict[str, object]:
    if not query:
        return {
            "status": "empty",
            "records": dataframe.iloc[0:0],
            "outside": [],
            "direct_count": 0,
        }

    exact_mask = pd.Series(True, index=dataframe.index)
    for field, query_value in query.items():
        exact_mask &= dataframe[field].apply(
            lambda row_value: values_match(field, row_value, query_value)
        )

    direct = dataframe[exact_mask].copy()
    if not direct.empty:
        return {
            "status": "direct",
            "records": direct.sort_values("test_id"),
            "outside": [],
            "direct_count": len(direct),
        }

    outside = outside_numeric_conditions(dataframe, query)
    ranked = rank_evidence_records(dataframe, query).head(1)
    return {
        "status": "outside" if outside else "partial",
        "records": ranked,
        "outside": outside,
        "direct_count": 0,
    }


def compare_record_to_query(
    row: pd.Series,
    query: dict[str, object],
) -> tuple[list[str], list[str]]:
    matched = []
    different = []

    for field, query_value in query.items():
        metadata = FIELD_METADATA[field]
        row_value = row[field]
        if values_match(field, row_value, query_value):
            matched.append(
                f"{metadata['label']}: "
                f"{display_condition_value(field, row_value)}"
            )
        else:
            different.append(
                f"{metadata['label']}: requested "
                f"{display_condition_value(field, query_value)}; "
                f"test reports {display_condition_value(field, row_value)}"
            )

    return matched, different


def resource_tags(resources_text: str) -> str:
    resources = [
        item.strip()
        for item in str(resources_text).split("|")
        if item.strip()
    ]
    return "".join(
        f'<span class="resource-tag">{escape(resource)}</span>'
        for resource in resources
    )


def investigation_card(row: pd.Series) -> str:
    record_count = int(row["ember_record_count"])
    if record_count > 0:
        coverage = f"{record_count} structured records available in Ember"
    else:
        coverage = escape(str(row["ember_status"]))

    identifier = str(row["psi_id"])
    if str(row["acronym"]).strip():
        identifier = f"{identifier} · {row['acronym']}"

    detail_id = escape(str(row["psi_id"]), quote=True)
    source_url = escape(str(row["source_url"]), quote=True)

    return f"""
    <div class="investigation-card">
      <div class="psi-id">{escape(identifier)}</div>
      <h3>{escape(str(row['title']))}</h3>
      <div class="card-meta">
        {escape(str(row['research_area']))}<br>
        {escape(str(row['subresearch_area']))}<br>
        {escape(str(row['project_type']))}<br>
        {escape(str(row['nasa_center']))}
      </div>
      <p>{escape(str(row['objective_short']))}</p>
      <div class="resource-list">{resource_tags(row['available_resources'])}</div>
      <p>Experimental table: {escape(str(row['experimental_table_status']))}</p>
      <div class="coverage">Ember coverage: {coverage}</div>
      <div class="card-actions">
        <a class="source-link" href="?page=library&amp;psi={detail_id}" target="_self">View investigation</a>
        <a class="source-link secondary" href="{source_url}" target="_blank" rel="noopener noreferrer">Open in NASA PSI</a>
      </div>
    </div>
    """


def detail_item(label: str, value: str) -> str:
    shown_value = value if str(value).strip() else "Not reported"
    return f"""
    <div class="detail-item">
      <div class="detail-label">{escape(label)}</div>
      <div class="detail-value">{escape(str(shown_value))}</div>
    </div>
    """


def render_investigation_detail(row: pd.Series) -> None:
    record_count = int(row["ember_record_count"])
    coverage = (
        f"{record_count} structured records available in Ember"
        if record_count > 0
        else str(row["ember_status"])
    )

    details = "".join(
        [
            detail_item("Research area", row["research_area"]),
            detail_item("Subresearch area", row["subresearch_area"]),
            detail_item("Project type", row["project_type"]),
            detail_item("Flight platform", row["flight_platform"]),
            detail_item("NASA center", row["nasa_center"]),
            detail_item("DOI", row["doi"]),
            detail_item("Start date", row["start_date"]),
            detail_item("End date", row["end_date"]),
            detail_item("License", row["license"]),
        ]
    )

    source_url = escape(str(row["source_url"]), quote=True)

    identifier = str(row["psi_id"])
    if str(row["acronym"]).strip():
        identifier = f"{identifier} · {row['acronym']}"

    panel = f"""
    <a class="detail-back" href="?page=library" target="_self">Back to Library</a>
    <div class="detail-panel">
      <div class="psi-id">{escape(identifier)}</div>
      <h1>{escape(str(row['title']))}</h1>
      <div class="detail-grid">{details}</div>
      <h2>Research objective</h2>
      <p>{escape(str(row['objective_short']))}</p>
      <h2>Available resources</h2>
      <div class="resource-list">{resource_tags(row['available_resources'])}</div>
      <h2>Data availability</h2>
      <p>Experimental table: {escape(str(row['experimental_table_status']))}</p>
      <p>Modeling table: {escape(str(row['modeling_table_status']))}</p>
      <p>Structured records in Ember: {escape(coverage)}</p>
      <h2>Related investigations</h2>
      <p>{escape(str(row['related_investigations']) or 'Not reported')}</p>
      <div class="card-actions">
        <a class="source-link" href="{source_url}" target="_blank" rel="noopener noreferrer">Open in NASA PSI</a>
      </div>
    </div>
    """

    st.markdown(f'<div class="em">{panel}</div>', unsafe_allow_html=True)


def render_home() -> None:
    nav = render_nav("home")
    st.markdown(
        f'<div class="em">{nav}{hero}{body}</div>',
        unsafe_allow_html=True,
    )


def render_library() -> None:
    nav = render_nav("library")
    header = html(
        """
        <div class="library-header">
          <div class="eyebrow">NASA PHYSICAL SCIENCES INFORMATICS</div>
          <h1>PSI Research Library</h1>
          <p>Browse selected NASA PSI investigations and review the evidence available for each project. Ember distinguishes between investigation metadata, reports, analyzed data, publications, and structured experimental records.</p>
        </div>
        """
    )

    st.markdown(
        f'<div class="em">{nav}{header}</div>',
        unsafe_allow_html=True,
    )

    try:
        investigations = load_investigations()
    except (FileNotFoundError, ValueError) as error:
        st.error(str(error))
        return

    selected_psi = get_query_value("psi", "").strip()
    if selected_psi:
        selected_rows = investigations[
            investigations["psi_id"].astype(str).str.casefold()
            == selected_psi.casefold()
        ]
        if selected_rows.empty:
            st.warning("The selected investigation was not found in the catalog.")
        else:
            render_investigation_detail(selected_rows.iloc[0])
            return

    search_column, area_column, type_column = st.columns([2, 1, 1])

    with search_column:
        search = st.text_input(
            "Search",
            placeholder="Search by PSI ID, acronym, or title",
        )

    areas = [
        "All",
        *sorted(
            value
            for value in investigations["research_area"].unique()
            if value
        ),
    ]

    project_types = [
        "All",
        *sorted(
            value
            for value in investigations["project_type"].unique()
            if value
        ),
    ]

    with area_column:
        selected_area = st.selectbox("Research area", areas)

    with type_column:
        selected_type = st.selectbox("Project type", project_types)

    resource_options = sorted(
        {
            resource.strip()
            for resource_text in investigations["available_resources"]
            for resource in str(resource_text).split("|")
            if resource.strip()
        }
    )

    resources_column, coverage_column = st.columns([2, 1])

    with resources_column:
        selected_resources = st.multiselect(
            "Available resources",
            resource_options,
        )

    with coverage_column:
        selected_coverage = st.selectbox(
            "Structured records in Ember",
            ["All", "Available", "Not yet curated"],
        )

    filtered = investigations.copy()

    if search:
        searchable = (
            filtered[["psi_id", "acronym", "title"]]
            .astype(str)
            .agg(" ".join, axis=1)
        )
        filtered = filtered[
            searchable.str.contains(search, case=False, regex=False)
        ]

    if selected_area != "All":
        filtered = filtered[filtered["research_area"] == selected_area]

    if selected_type != "All":
        filtered = filtered[filtered["project_type"] == selected_type]

    if selected_resources:
        filtered = filtered[
            filtered["available_resources"].apply(
                lambda value: all(
                    resource
                    in {
                        item.strip()
                        for item in str(value).split("|")
                        if item.strip()
                    }
                    for resource in selected_resources
                )
            )
        ]

    if selected_coverage == "Available":
        filtered = filtered[filtered["ember_record_count"] > 0]
    elif selected_coverage == "Not yet curated":
        filtered = filtered[filtered["ember_record_count"] == 0]

    st.markdown(
        f'<div class="results-count">{len(filtered)} investigations found</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No investigations match the selected filters.")
        return

    card_columns = st.columns(2)
    for position, (_, row) in enumerate(filtered.iterrows()):
        with card_columns[position % 2]:
            st.markdown(
                investigation_card(row),
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="footer">Ember — Experimental evidence organized for research.</div>',
        unsafe_allow_html=True,
    )


def evidence_summary(
    routed_to: str,
    status_label: str,
    status_class: str,
    reviewed: str,
    found: str,
) -> str:
    return html(f"""
    <div class="evidence-summary">
      <div class="summary-item">
        <div class="summary-label">Routed to</div>
        <div class="summary-value">{escape(routed_to)}</div>
      </div>
      <div class="summary-item">
        <div class="summary-label">Evidence coverage</div>
        <div class="summary-value"><span class="coverage-badge {status_class}">{escape(status_label)}</span></div>
      </div>
      <div class="summary-item">
        <div class="summary-label">Records reviewed</div>
        <div class="summary-value">{escape(reviewed)}</div>
      </div>
      <div class="summary-item">
        <div class="summary-label">Evidence found</div>
        <div class="summary-value">{escape(found)}</div>
      </div>
    </div>
    """)


def match_card(
    row: pd.Series,
    query: dict[str, object],
) -> str:
    matched, different = compare_record_to_query(row, query)
    matched_text = "<br>".join(escape(item) for item in matched)
    different_text = "<br>".join(escape(item) for item in different)

    why_parts = []
    if matched:
        why_parts.append(
            f"<strong>Matched conditions:</strong><br>{matched_text}"
        )
    if different:
        why_parts.append(
            f"<strong>Different conditions:</strong><br>{different_text}"
        )
    why_html = "<br><br>".join(why_parts)

    airflow_start = display_condition_value(
        "airflow_start_cm_s", row["airflow_start_cm_s"]
    )
    airflow_end = display_condition_value(
        "airflow_end_cm_s", row["airflow_end_cm_s"]
    )
    oxygen = display_condition_value(
        "oxygen_vol_pct", row["oxygen_vol_pct"]
    )
    width = display_condition_value(
        "sample_width_cm", row["sample_width_cm"]
    )
    sample_condition = display_condition_value(
        "reused_sample", row["reused_sample"]
    )

    source_page = row["source_page"]
    if pd.notna(source_page):
        try:
            source_page = str(int(float(source_page)))
        except (TypeError, ValueError):
            source_page = str(source_page)
    else:
        source_page = "Not reported"

    limitation = str(row["exclusion_reason"]).strip()
    if not limitation:
        limitation = "No record-specific limitation was reported in the curated table."

    return html(f"""
    <div class="match-card">
      <div class="psi-id">{escape(str(row['test_id']))} · BASS-II</div>
      <h3>{escape(str(row['material']))}</h3>
      <div class="condition-chips">
        <span class="condition-chip">O₂ {escape(oxygen)}</span>
        <span class="condition-chip">Airflow {escape(airflow_start)} → {escape(airflow_end)}</span>
        <span class="condition-chip">{escape(str(row['airflow_profile']))} profile</span>
        <span class="condition-chip">Width {escape(width)}</span>
        <span class="condition-chip">{escape(sample_condition)}</span>
      </div>
      <p><strong>Documented outcome:</strong> {escape(str(row['observed_outcome']))}</p>
      <p><strong>Explicit ignition:</strong> {escape(str(row['ignited_explicit']))}</p>
      <p class="why">{why_html}</p>
      <p><strong>Source:</strong> NASA/TM-20210011385 · {escape(str(row['source_table']))} · p. {escape(source_page)}</p>
      <p class="limitation">{escape(limitation)} This observed outcome is not a fire-risk probability or a universal safety threshold.</p>
      <div class="card-actions">
        <a class="source-link" href="{BASSII_REPORT_URL}" target="_blank" rel="noopener noreferrer">Open source report</a>
      </div>
    </div>
    """)


def render_flame_results(
    tests: pd.DataFrame,
    query: dict[str, object],
) -> None:
    result = match_evidence(tests, query)
    status = str(result["status"])
    records = result["records"]

    if status == "direct":
        status_label = "Direct record evidence"
        status_class = "direct"
        found = f"{len(records)} matching record" + (
            "" if len(records) == 1 else "s"
        )
        explanation = (
            "At least one BASS-II/SIBAL record matches every condition "
            "selected in the submitted question. The result describes "
            "documented tests; it does not predict an untested scenario."
        )
        shown_records = records.head(6)
    elif status == "partial":
        status_label = "Partial record evidence"
        status_class = "partial"
        found = "1 closest documented record"
        explanation = (
            "The selected values fall within the general range represented "
            "by the prototype, but no single record combines every condition. "
            "The closest record is shown below and each difference is "
            "identified explicitly."
        )
        shown_records = records
    else:
        status_label = "Outside current coverage"
        status_class = "outside"
        found = "1 closest record for reference"
        outside_text = "; ".join(result["outside"])
        explanation = (
            "No structured record in this prototype supports all selected "
            f"conditions. Outside coverage: {outside_text}. The closest "
            "record is shown only to identify the current evidence boundary, "
            "not to extrapolate an outcome."
        )
        shown_records = records

    summary = evidence_summary(
        "BASS-II / SIBAL",
        status_label,
        status_class,
        str(len(tests)),
        found,
    )
    explanation_panel = html(f"""
    <div class="result-explanation">
      <h3>Why this result</h3>
      <p>{escape(explanation)}</p>
    </div>
    """)

    st.markdown(
        f'<div class="em">{summary}{explanation_panel}</div>',
        unsafe_allow_html=True,
    )

    for _, row in shown_records.iterrows():
        st.markdown(
            f'<div class="em">{match_card(row, query)}</div>',
            unsafe_allow_html=True,
        )

    if status == "direct" and len(records) > len(shown_records):
        st.caption(
            f"{len(records) - len(shown_records)} additional direct matches "
            "are not displayed in this compact prototype view."
        )


def render_same_results(request: dict[str, object]) -> None:
    focus = str(request.get("focus", "Smoke particle behavior"))
    material = str(request.get("material", "Any documented material"))

    summary = evidence_summary(
        "SAME · PSI-102",
        "Documentary evidence only",
        "documentary",
        "Investigation metadata and reports",
        "1 relevant investigation",
    )

    panel = html(f"""
    <div class="result-explanation">
      <h3>Why this result</h3>
      <p>SAME is relevant because the submitted question concerns {escape(focus.lower())}. The selected material is {escape(material)}. SAME examined smoke-particle behavior and spacecraft detector response under low-gravity conditions.</p>
    </div>
    <div class="documentary-panel">
      <div class="psi-id">PSI-102 · SAME</div>
      <h2>Smoke and Aerosol Measurement Experiment</h2>
      <p><strong>Evidence level:</strong> Investigation metadata and report-level evidence.</p>
      <p><strong>Current limitation:</strong> Structured SAME run records have not been curated in this prototype, so Ember does not claim a condition-level match or generate a detector-performance prediction.</p>
      <p><strong>Related investigation:</strong> SAME-R · PSI-101.</p>
      <div class="card-actions">
        <a class="source-link" href="?page=library&amp;psi=PSI-102" target="_self">View Library record</a>
        <a class="source-link secondary" href="{SAME_PSI_URL}" target="_blank" rel="noopener noreferrer">Open in NASA PSI</a>
      </div>
    </div>
    """)

    st.markdown(
        f'<div class="em">{summary}{panel}</div>',
        unsafe_allow_html=True,
    )


def render_experiment_explorer() -> None:
    nav = render_nav("explorer")

    try:
        tests = load_bassii_tests()
    except (FileNotFoundError, ValueError) as error:
        st.markdown(f'<div class="em">{nav}</div>', unsafe_allow_html=True)
        st.error(str(error))
        return

    oxygen_min = float(tests["oxygen_vol_pct"].min())
    oxygen_max = float(tests["oxygen_vol_pct"].max())
    airflow_min = float(tests["airflow_start_cm_s"].min())
    airflow_max = float(tests["airflow_start_cm_s"].max())

    header = html(f"""
    <div class="explorer-header">
      <div class="eyebrow">EVIDENCE ROUTING AND COVERAGE</div>
      <h1>Experiment Explorer</h1>
      <p>Describe the evidence you need. Ember routes the question to the relevant PSI investigation and shows which conditions are directly represented, partially represented, or outside the current prototype.</p>
      <div class="dataset-strip">
        <span class="dataset-stat">{len(tests)} BASS-II / SIBAL records</span>
        <span class="dataset-stat">O₂ {oxygen_min:.1f}–{oxygen_max:.1f} vol. %</span>
        <span class="dataset-stat">Initial airflow {airflow_min:.1f}–{airflow_max:.1f} cm/s</span>
        <span class="dataset-stat">SAME report routing</span>
      </div>
    </div>
    <div class="question-intro">
      <h2>Build a research question</h2>
      <p>Select only the conditions that matter. Conditions left at Any are not used when comparing records.</p>
    </div>
    """)
    st.markdown(
        f'<div class="em">{nav}{header}</div>',
        unsafe_allow_html=True,
    )

    research_need = st.selectbox(
        "Research need",
        ["Flame behavior", "Smoke and detector response"],
        key="explorer_research_need",
    )

    if research_need == "Flame behavior":
        st.markdown(
            """
            <div class="em"><div class="fixed-condition">
              <strong>Fixed prototype context:</strong> SIBAL fabric, microgravity aboard the ISS, 1 atm, concurrent flow. Only the selected fields below affect matching.
            </div></div>
            """,
            unsafe_allow_html=True,
        )

        oxygen_column, initial_airflow_column = st.columns(2)
        with oxygen_column:
            use_oxygen = st.checkbox(
                "Include oxygen concentration",
                value=True,
                key="explorer_use_oxygen",
            )
            oxygen_value = st.number_input(
                "Oxygen concentration (vol. %)",
                min_value=0.0,
                max_value=100.0,
                value=18.5,
                step=0.1,
                disabled=not use_oxygen,
                key="explorer_oxygen",
            )

        with initial_airflow_column:
            use_initial_airflow = st.checkbox(
                "Include initial airflow",
                value=True,
                key="explorer_use_initial_airflow",
            )
            initial_airflow_value = st.number_input(
                "Initial airflow (cm/s)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.1,
                disabled=not use_initial_airflow,
                key="explorer_initial_airflow",
            )

        final_airflow_column, profile_column = st.columns(2)
        with final_airflow_column:
            use_final_airflow = st.checkbox(
                "Include final airflow",
                value=False,
                key="explorer_use_final_airflow",
            )
            final_airflow_value = st.number_input(
                "Final airflow (cm/s)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.1,
                disabled=not use_final_airflow,
                key="explorer_final_airflow",
            )

        with profile_column:
            profile_options = [
                "Any",
                *sorted(tests["airflow_profile"].dropna().unique()),
            ]
            airflow_profile = st.selectbox(
                "Airflow profile",
                profile_options,
                key="explorer_profile",
            )

        width_column, sample_column = st.columns(2)
        with width_column:
            width_values = sorted(
                float(value)
                for value in tests["sample_width_cm"].dropna().unique()
            )
            width_labels = ["Any", *[f"{value:g} cm" for value in width_values]]
            selected_width = st.selectbox(
                "Sample width",
                width_labels,
                key="explorer_width",
            )

        with sample_column:
            sample_condition = st.selectbox(
                "Sample condition",
                ["Any", "New sample", "Reused sample"],
                key="explorer_sample_condition",
            )

        ignition_column, outcome_column = st.columns(2)
        with ignition_column:
            ignition = st.selectbox(
                "Explicit ignition",
                [
                    "Any",
                    *sorted(tests["ignited_explicit"].dropna().unique()),
                ],
                key="explorer_ignition",
            )

        with outcome_column:
            outcome = st.selectbox(
                "Documented outcome",
                [
                    "Any",
                    *sorted(tests["observed_outcome"].dropna().unique()),
                ],
                key="explorer_outcome",
            )

        if st.button("Find supporting evidence", key="submit_flame_query"):
            query: dict[str, object] = {}
            if use_oxygen:
                query["oxygen_vol_pct"] = float(oxygen_value)
            if use_initial_airflow:
                query["airflow_start_cm_s"] = float(initial_airflow_value)
            if use_final_airflow:
                query["airflow_end_cm_s"] = float(final_airflow_value)
            if airflow_profile != "Any":
                query["airflow_profile"] = airflow_profile
            if selected_width != "Any":
                query["sample_width_cm"] = float(
                    selected_width.replace(" cm", "")
                )
            if sample_condition != "Any":
                query["reused_sample"] = (
                    "Yes" if sample_condition == "Reused sample" else "No"
                )
            if ignition != "Any":
                query["ignited_explicit"] = ignition
            if outcome != "Any":
                query["observed_outcome"] = outcome

            if query:
                st.session_state["explorer_request"] = {
                    "need": "flame",
                    "query": query,
                }
            else:
                st.warning("Select at least one condition before searching.")

        submitted = st.session_state.get("explorer_request", {})
        if submitted.get("need") == "flame":
            render_flame_results(tests, submitted["query"])

    else:
        st.markdown(
            """
            <div class="em"><div class="fixed-condition">
              <strong>Current prototype coverage:</strong> SAME is connected at investigation and report level. Condition-level SAME records have not been curated.
            </div></div>
            """,
            unsafe_allow_html=True,
        )

        focus_column, material_column = st.columns(2)
        with focus_column:
            smoke_focus = st.selectbox(
                "Research focus",
                [
                    "Smoke particle size",
                    "Smoke transport and aging",
                    "Smoke detector response",
                ],
                key="explorer_smoke_focus",
            )

        with material_column:
            smoke_material = st.selectbox(
                "Material of interest",
                [
                    "Any documented material",
                    "Teflon",
                    "Kapton",
                    "Cellulose",
                    "Silicone rubber",
                    "Dibutyl phthalate",
                    "Pyrell (SAME-R)",
                ],
                key="explorer_smoke_material",
            )

        if st.button("Find supporting evidence", key="submit_smoke_query"):
            st.session_state["explorer_request"] = {
                "need": "smoke",
                "focus": smoke_focus,
                "material": smoke_material,
            }

        submitted = st.session_state.get("explorer_request", {})
        if submitted.get("need") == "smoke":
            render_same_results(submitted)

    st.markdown(
        '<div class="footer">Ember — Evidence routing without unsupported prediction.</div>',
        unsafe_allow_html=True,
    )


def case_list(items: list[str]) -> str:
    return "".join(
        f'<div class="case-list-item">{escape(item)}</div>'
        for item in items
    )


def accident_case_card(row: pd.Series) -> str:
    factors = split_pipe_values(row["contributing_factors"])
    consequences = split_pipe_values(row["operational_consequences"])
    responses = split_pipe_values(row["response_actions"])
    research_topics = split_pipe_values(row["research_focus"])

    topic_tags = "".join(
        f'<span class="case-tag">{escape(topic)}</span>'
        for topic in research_topics
    )

    related_psi = str(row["related_psi"]).strip()
    if related_psi == "BASS-II":
        psi_link = (
            '<a class="source-link" href="?page=library&amp;psi=PSI-25" '
            'target="_self">View BASS-II in Library</a>'
        )
    elif related_psi == "SAME":
        psi_link = (
            '<a class="source-link" href="?page=library&amp;psi=PSI-102" '
            'target="_self">View SAME in Library</a>'
        )
    else:
        psi_link = ""

    source_url = escape(str(row["source_url"]), quote=True)
    event_date = escape(str(row["event_date"]))

    return html(f"""
    <div class="case-card">
      <div class="psi-id">{escape(str(row['case_id']))} · {event_date}</div>
      <h2>{escape(str(row['title']))}</h2>
      <div class="case-meta">
        <span class="case-tag">{escape(str(row['setting']))}</span>
        <span class="case-tag">{escape(str(row['event_type']))}</span>
        <span class="case-tag">{escape(str(row['evidence_level']))}</span>
        {topic_tags}
      </div>

      <div class="case-overview">
        <div class="case-overview-item">
          <div class="detail-label">Initiating event</div>
          <div class="detail-value">{escape(str(row['initiating_event']))}</div>
        </div>
        <div class="case-overview-item">
          <div class="detail-label">People affected</div>
          <div class="detail-value">{int(row['crew_affected'])}</div>
        </div>
        <div class="case-overview-item">
          <div class="detail-label">Documented outcome</div>
          <div class="detail-value">{escape(str(row['outcome']))}</div>
        </div>
      </div>

      <div class="case-section">
        <h3>Documented contributing factors</h3>
        <div class="case-list">{case_list(factors)}</div>
      </div>

      <div class="case-section">
        <h3>Operational consequences</h3>
        <div class="case-list">{case_list(consequences)}</div>
      </div>

      <div class="case-section">
        <h3>Response and recovery</h3>
        <div class="case-list">{case_list(responses)}</div>
      </div>

      <div class="case-section psi-connection">
        <h3>Connection to PSI evidence</h3>
        <p><strong>{escape(str(row['relationship_type']))}</strong></p>
        <p>{escape(str(row['psi_relation_note']))}</p>
        <div class="card-actions">{psi_link}</div>
      </div>

      <div class="case-section">
        <h3>Evidence boundary</h3>
        <p class="evidence-boundary">{escape(str(row['interpretation_limit']))}</p>
      </div>

      <div class="card-actions">
        <a class="source-link" href="{source_url}" target="_blank" rel="noopener noreferrer">Open official NASA source</a>
      </div>
    </div>
    """)


def render_accident_cases() -> None:
    nav = render_nav("accidents")

    try:
        cases = load_accident_cases()
    except (FileNotFoundError, ValueError) as error:
        st.markdown(f'<div class="em">{nav}</div>', unsafe_allow_html=True)
        st.error(str(error))
        return

    header = html(f"""
    <div class="cases-header">
      <div class="eyebrow">DOCUMENTED OPERATIONAL CONTEXT</div>
      <h1>Accident Cases</h1>
      <p>Explore documented spacecraft incidents and ground-test failures. Ember separates historical facts, operational lessons, and experimental evidence so case narratives are not treated as probabilities or training labels.</p>
      <div class="dataset-strip">
        <span class="dataset-stat">{len(cases)} NASA-documented cases</span>
        <span class="dataset-stat">Historical evidence</span>
        <span class="dataset-stat">No accident probabilities</span>
      </div>
    </div>
    <div class="question-intro">
      <h2>Choose a research context</h2>
      <p>Filter the cases by operational setting, research focus, or connection to PSI evidence.</p>
    </div>
    """)

    st.markdown(
        f'<div class="em">{nav}{header}</div>',
        unsafe_allow_html=True,
    )

    search_column, focus_column, setting_column = st.columns([1.4, 1, 1])

    with search_column:
        search = st.text_input(
            "Search cases",
            placeholder="Search by case, event, factor, or response",
            key="accident_search",
        )

    focus_options = sorted(
        {
            topic
            for value in cases["research_focus"]
            for topic in split_pipe_values(value)
        }
    )
    with focus_column:
        selected_focus = st.selectbox(
            "Research focus",
            ["All", *focus_options],
            key="accident_focus",
        )

    with setting_column:
        selected_setting = st.selectbox(
            "Operational setting",
            ["All", *sorted(cases["setting"].unique())],
            key="accident_setting",
        )

    selected_psi = st.selectbox(
        "Related PSI evidence",
        ["All", "BASS-II", "SAME", "No direct PSI match"],
        key="accident_psi",
    )

    filtered = cases.copy()

    if search:
        searchable_columns = [
            "title",
            "event_type",
            "initiating_event",
            "contributing_factors",
            "operational_consequences",
            "response_actions",
            "research_focus",
        ]
        searchable = (
            filtered[searchable_columns]
            .astype(str)
            .agg(" ".join, axis=1)
        )
        filtered = filtered[
            searchable.str.contains(search, case=False, regex=False)
        ]

    if selected_focus != "All":
        filtered = filtered[
            filtered["research_focus"].apply(
                lambda value: selected_focus in split_pipe_values(value)
            )
        ]

    if selected_setting != "All":
        filtered = filtered[filtered["setting"] == selected_setting]

    if selected_psi == "No direct PSI match":
        filtered = filtered[filtered["related_psi"].str.strip() == ""]
    elif selected_psi != "All":
        filtered = filtered[filtered["related_psi"] == selected_psi]

    st.markdown(
        f'<div class="case-count">{len(filtered)} relevant case' +
        ('</div>' if len(filtered) == 1 else 's</div>'),
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No documented cases match the selected context.")
        return

    case_ids = filtered["case_id"].tolist()
    labels = {
        row["case_id"]: f"{row['title']} · {row['event_date']}"
        for _, row in filtered.iterrows()
    }
    if st.session_state.get("selected_accident_case") not in case_ids:
        st.session_state["selected_accident_case"] = case_ids[0]
    selected_case = st.selectbox(
        "Select a case for detailed review",
        case_ids,
        format_func=lambda case_id: labels[case_id],
        key="selected_accident_case",
    )

    selected_row = filtered[filtered["case_id"] == selected_case].iloc[0]
    st.markdown(
        f'<div class="em">{accident_case_card(selected_row)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="footer">Historical cases support context and research questions. They are not experimental observations, accident-frequency data, or prediction labels.</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Data Lab
# ---------------------------------------------------------------------------

DL_COLORS = {
    "Flame extinction by quenching": "#F25C05",
    "No ignition": "#78C8C3",
    "Blowoff": "#E7B55A",
    "No blowoff": "#B58BE0",
    "Outcome not specified": "#8A8A88",
    "Reused sample: ignition": "#FF9A52",
    "Reused sample: no ignition": "#4FA39E",
    "Reused sample: one-sided flame": "#D89595",
}
DL_TEXT = "#CFCFCC"
DL_GRID = "rgba(255,255,255,0.07)"

# Observed ranges of the SIBAL subset (Dominio sheet). Used only to draw the
# envelope; they are recomputed from the data below, never typed by hand.
OUTCOME_ORDER = list(DL_COLORS.keys())


@st.cache_data(show_spinner=False)
def load_same_sizes() -> pd.DataFrame:
    path = DATA_DIR / "same_particle_sizes.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Missing file: {path}.")
    frame = pd.read_csv(path)
    frame["change_nm"] = frame["aged_720s_nm"] - frame["base_nm"]
    frame["change_pct"] = frame["change_nm"] / frame["base_nm"] * 100
    return frame


@st.cache_data(show_spinner=False)
def load_saffire() -> pd.DataFrame:
    path = DATA_DIR / "saffire_tests.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Missing file: {path}.")
    frame = pd.read_csv(path)
    for column in ["sample_width_cm", "sample_length_cm", "thickness_mm",
                   "flow_cm_s", "oxygen_vol_pct", "duration_s", "spread_rate_mm_s"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def dl_style(chart):
    import altair as alt  # bundled with Streamlit

    return (
        chart.configure(background="transparent")
        .configure_view(stroke=None)
        .configure_axis(
            labelColor=DL_TEXT, titleColor=DL_TEXT, gridColor=DL_GRID,
            domainColor="rgba(255,255,255,0.2)", tickColor="rgba(255,255,255,0.2)",
            labelFontSize=12, titleFontSize=12, titleFontWeight=600,
        )
        .configure_legend(
            labelColor=DL_TEXT, titleColor=DL_TEXT, labelFontSize=11,
            titleFontSize=11, orient="bottom", columns=2, symbolType="circle",
        )
        .configure_title(color="#F4F4F2", fontSize=14, anchor="start")
    )


def dl_header(title: str, text: str, chips: list[str]) -> str:
    strip = "".join(f'<span class="dataset-stat">{escape(c)}</span>' for c in chips)
    return f"""
    <div class="explorer-header">
      <div class="eyebrow">DESCRIPTIVE DATA EXPLORATION</div>
      <h1>{escape(title)}</h1>
      <p>{escape(text)}</p>
      <div class="dataset-strip">{strip}</div>
    </div>
    """


def dl_note(title: str, text: str, tone: str = "") -> str:
    cls = "result-explanation" if not tone else f"documentary-panel"
    return f'<div class="{cls}"><h3>{escape(title)}</h3><p>{escape(text)}</p></div>'


def dl_stat(label: str, value: str, hint: str = "") -> str:
    hint_html = f'<div class="stat-hint">{escape(hint)}</div>' if hint else ""
    return (
        '<div class="summary-item">'
        f'<div class="summary-label">{escape(label)}</div>'
        f'<div class="summary-value">{escape(value)}</div>{hint_html}</div>'
    )


def spread_offsets(frame: pd.DataFrame) -> pd.Series:
    """Tiny visual offset (<= 0.1 vol. %) for tests that share exact coordinates."""
    key = (
        frame["oxygen_vol_pct"].astype(str) + "|"
        + frame["airflow_start_cm_s"].astype(str) + "|"
        + frame["airflow_end_cm_s"].astype(str)
    )
    rank = frame.groupby(key).cumcount()
    size = key.map(key.value_counts())
    return ((rank - (size - 1) / 2) * 0.07).where(size > 1, 0.0)


def bassii_chart(frame: pd.DataFrame, scenario: dict | None, envelope: dict):
    import altair as alt

    plot = frame.copy()
    plot["o2_plot"] = plot["oxygen_vol_pct"] + spread_offsets(plot)
    plot["airflow_pair"] = (
        plot["airflow_start_cm_s"].map(lambda v: f"{v:g}")
        + " → " + plot["airflow_end_cm_s"].map(lambda v: f"{v:g}") + " cm/s"
    )
    plot["sample"] = plot["reused_sample"].map({"Yes": "Reused sample", "No": "New sample"})
    plot["quality"] = plot["oxygen_caveat"].map(
        {"Yes": "NASA flags this O₂ reading as possibly inaccurate", "No": "No flag"}
    )
    plot["width_label"] = plot["sample_width_cm"].map(lambda v: f"{v:g} cm")

    scale = alt.Scale(domain=OUTCOME_ORDER, range=[DL_COLORS[k] for k in OUTCOME_ORDER])
    x_enc = alt.X(
        "o2_plot:Q", title="Oxygen concentration (vol. %)", axis=alt.Axis(values=list(range(15, 23)), format="d"),
        scale=alt.Scale(domain=[envelope["o2_lo"] - 1.2, envelope["o2_hi"] + 1.2], nice=False, zero=False),
    )
    y_scale = alt.Scale(type="sqrt", domain=[0, envelope["flow_hi"] * 1.12])
    tooltip = [
        alt.Tooltip("test_id:N", title="Test"),
        alt.Tooltip("observed_outcome:N", title="Documented outcome"),
        alt.Tooltip("oxygen_vol_pct:Q", title="O₂ (vol. %)"),
        alt.Tooltip("airflow_pair:N", title="Airflow start → end"),
        alt.Tooltip("airflow_profile:N", title="Profile"),
        alt.Tooltip("width_label:N", title="Sample width"),
        alt.Tooltip("sample:N", title="Sample condition"),
        alt.Tooltip("quality:N", title="Data quality"),
        alt.Tooltip("source_table:N", title="Source table"),
        alt.Tooltip("source_page:Q", title="Report page"),
    ]

    envelope_df = pd.DataFrame([{
        "x0": envelope["o2_lo"], "x1": envelope["o2_hi"],
        "y0": envelope["flow_lo"], "y1": envelope["flow_hi"],
    }])
    box = alt.Chart(envelope_df).mark_rect(
        color="#F25C05", opacity=0.05, stroke="#F25C05", strokeOpacity=0.35,
        strokeDash=[5, 4],
    ).encode(
        x=alt.X("x0:Q", scale=alt.Scale(domain=[envelope["o2_lo"] - 1.2, envelope["o2_hi"] + 1.2], nice=False, zero=False)),
        x2="x1:Q", y=alt.Y("y0:Q", scale=y_scale), y2="y1:Q",
    )

    segment = alt.Chart(plot).mark_rule(strokeWidth=2, opacity=0.55).encode(
        x=x_enc,
        y=alt.Y("airflow_start_cm_s:Q", scale=y_scale, title="Airflow (cm/s, √ scale)"),
        y2="airflow_end_cm_s:Q",
        color=alt.Color("observed_outcome:N", scale=scale, legend=None),
        strokeDash=alt.condition(alt.datum.reused_sample == "Yes", alt.value([4, 3]), alt.value([1, 0])),
        tooltip=tooltip,
    )
    start = alt.Chart(plot).mark_point(filled=True, size=95, opacity=0.95, stroke="#090909", strokeWidth=1).encode(
        x=x_enc, y=alt.Y("airflow_start_cm_s:Q", scale=y_scale),
        color=alt.Color("observed_outcome:N", scale=scale, title="Documented outcome",
                        legend=alt.Legend(orient="bottom", columns=3, symbolType="circle")),
        shape=alt.Shape("reused_sample:N", scale=alt.Scale(domain=["No", "Yes"], range=["circle", "square"]),
                        legend=None),
        tooltip=tooltip,
    )
    end = alt.Chart(plot[plot["airflow_start_cm_s"] != plot["airflow_end_cm_s"]]).mark_point(
        shape="diamond", size=70, filled=False, strokeWidth=2,
    ).encode(
        x=x_enc, y=alt.Y("airflow_end_cm_s:Q", scale=y_scale),
        color=alt.Color("observed_outcome:N", scale=scale, legend=None),
        tooltip=tooltip,
    )
    flagged = alt.Chart(plot[plot["oxygen_caveat"] == "Yes"]).mark_point(
        shape="circle", size=330, filled=False, stroke="#F4F4F2", strokeWidth=1.2, strokeDash=[2, 2],
    ).encode(x=x_enc, y=alt.Y("airflow_start_cm_s:Q", scale=y_scale), tooltip=tooltip)

    layers = [box, segment, start, end, flagged]
    if scenario:
        sc = pd.DataFrame([{"o2": scenario["oxygen_vol_pct"], "flow": scenario["airflow_start_cm_s"],
                            "label": "Your scenario"}])
        layers.append(
            alt.Chart(sc).mark_point(shape="cross", size=260, strokeWidth=3, color="#FFFFFF").encode(
                x="o2:Q", y=alt.Y("flow:Q", scale=y_scale),
                tooltip=[alt.Tooltip("label:N", title=""), alt.Tooltip("o2:Q", title="O₂ (vol. %)"),
                         alt.Tooltip("flow:Q", title="Airflow (cm/s)")],
            )
        )
    return dl_style(alt.layer(*layers).properties(height=430))


def render_bassii_tab(tests: pd.DataFrame) -> None:
    envelope = {
        "o2_lo": float(tests["oxygen_vol_pct"].min()), "o2_hi": float(tests["oxygen_vol_pct"].max()),
        "flow_lo": float(min(tests["airflow_start_cm_s"].min(), tests["airflow_end_cm_s"].min())),
        "flow_hi": float(max(tests["airflow_start_cm_s"].max(), tests["airflow_end_cm_s"].max())),
    }

    st.markdown(
        '<div class="em">'
        + dl_note(
            "What this chart shows",
            "Each mark is one real test from Table 7.1 of the BASS-II summary report. Circles are new samples and "
            "squares are reused samples. When airflow changed during a run, a line joins the starting airflow "
            "(filled mark) to the final airflow (open diamond), because one number cannot describe that test. "
            "Colour is the outcome written in the table.",
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        widths = st.multiselect(
            "Sample width (cm)", sorted(tests["sample_width_cm"].dropna().unique()),
            default=sorted(tests["sample_width_cm"].dropna().unique()), key="dl_width",
        )
    with c2:
        sample_state = st.selectbox("Sample condition", ["All", "New samples only", "Reused samples only"],
                                    key="dl_sample")
    with c3:
        outcomes = st.multiselect(
            "Documented outcome", OUTCOME_ORDER, default=OUTCOME_ORDER, key="dl_outcomes",
        )

    filtered = tests[tests["sample_width_cm"].isin(widths) & tests["observed_outcome"].isin(outcomes)]
    if sample_state == "New samples only":
        filtered = filtered[filtered["reused_sample"] == "No"]
    elif sample_state == "Reused samples only":
        filtered = filtered[filtered["reused_sample"] == "Yes"]

    overlay = st.checkbox("Overlay my scenario on the chart", value=False, key="dl_overlay")
    scenario = None
    if overlay:
        s1, s2 = st.columns(2)
        with s1:
            o2 = st.number_input("Scenario oxygen (vol. %)", min_value=0.0, max_value=100.0,
                                 value=18.7, step=0.1, key="dl_s_o2")
        with s2:
            flow = st.number_input("Scenario initial airflow (cm/s)", min_value=0.0, max_value=500.0,
                                   value=10.0, step=0.5, key="dl_s_flow")
        scenario = {"oxygen_vol_pct": float(o2), "airflow_start_cm_s": float(flow)}
        outside = outside_numeric_conditions(
            tests, {"oxygen_vol_pct": o2, "airflow_start_cm_s": flow}
        )
        if outside:
            st.warning(
                "Outside the tested domain: " + "; ".join(outside)
                + ". Ember does not extrapolate beyond the observed range."
            )
        else:
            near = tests[
                (tests["oxygen_vol_pct"].sub(o2).abs() <= 0.5)
                & (tests["airflow_start_cm_s"].sub(flow).abs() <= 1.0)
            ]
            st.info(
                f"Inside the observed ranges, with {len(near)} test(s) within ±0.5 vol. % O₂ and ±1 cm/s "
                "initial airflow. Being inside both ranges does not mean this exact combination was tested."
            )

    if filtered.empty:
        st.info("No tests match the selected filters.")
        return

    st.altair_chart(bassii_chart(filtered, scenario, envelope), width="stretch", theme=None)
    st.caption(
        f"{len(filtered)} of {len(tests)} tests shown. Shaded rectangle = observed O₂ and airflow ranges; "
        "a point inside it is not evidence that the combination was tested. Dotted white ring = NASA flags the "
        "O₂ reading as possibly inaccurate (GMT45-T1, GMT45-T2). Tests with identical coordinates are offset "
        "by at most 0.1 vol. % so they remain visible; tooltips show the true values. Airflow axis uses a "
        "square-root scale to separate low velocities. Colours are the same as in the outcome bars below."
    )

    left, right = st.columns([1, 1])
    counts = (
        filtered["observed_outcome"].value_counts().rename_axis("outcome").reset_index(name="tests")
    )
    with left:
        import altair as alt

        bars = alt.Chart(counts).mark_bar(cornerRadiusEnd=4).encode(
            y=alt.Y("outcome:N", sort="-x", title=None, axis=alt.Axis(labelLimit=240)),
            x=alt.X("tests:Q", title="Number of tests", axis=alt.Axis(tickMinStep=1, format="d")),
            color=alt.Color("outcome:N", scale=alt.Scale(domain=OUTCOME_ORDER,
                            range=[DL_COLORS[k] for k in OUTCOME_ORDER]), legend=None),
            tooltip=["outcome:N", "tests:Q"],
        ).properties(height=260, title="Documented outcomes (counts, not probabilities)")
        st.altair_chart(dl_style(bars), width="stretch", theme=None)
    with right:
        new = tests[tests["reused_sample"] == "No"]
        quench = int((new["observed_outcome"] == "Flame extinction by quenching").sum())
        st.markdown(
            '<div class="em">'
            + dl_stat("Quenching among new samples", f"{quench} of {len(new)} tests ({quench / len(new):.1%})",
                      "Descriptive frequency of a designed test set.")
            + '<div style="height:14px"></div>'
            + dl_note(
                "How to read the 31.6 %",
                "This is a count inside a set of experiments chosen to explore limits. It is not the probability "
                "that a fire will go out, or that flame spread will stop, in a real cabin. Runs also changed "
                "airflow during the test, so the final event does not say what happened earlier.",
            )
            + "</div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="em"><div class="question-intro"><h2>Traceable records</h2>'
                '<p>Every row keeps its test identifier, report page, table, and the original comment.</p></div></div>',
                unsafe_allow_html=True)
    view = filtered[[
        "test_id", "sample_width_cm", "oxygen_vol_pct", "airflow_start_cm_s", "airflow_end_cm_s",
        "airflow_profile", "reused_sample", "observed_outcome", "ignited_explicit",
        "source_page", "source_table", "original_comment",
    ]].rename(columns={
        "test_id": "Test", "sample_width_cm": "Width (cm)", "oxygen_vol_pct": "O₂ (vol. %)",
        "airflow_start_cm_s": "Start flow (cm/s)", "airflow_end_cm_s": "End flow (cm/s)",
        "airflow_profile": "Profile", "reused_sample": "Reused", "observed_outcome": "Documented outcome",
        "ignited_explicit": "Ignition stated", "source_page": "Page", "source_table": "Table",
        "original_comment": "Original comment",
    })
    st.dataframe(view, hide_index=True, width="stretch")
    st.download_button(
        "Download these records (CSV)", filtered.to_csv(index=False).encode("utf-8"),
        file_name="ember_bassii_sibal_filtered.csv", mime="text/csv", key="dl_dl_bass",
    )


def render_same_tab() -> None:
    import altair as alt

    try:
        sizes = load_same_sizes()
    except FileNotFoundError as error:
        st.error(str(error))
        return

    st.markdown(
        '<div class="em">'
        + dl_note(
            "What this chart shows",
            "Published mass-mean particle diameter of smoke from each material, in the base condition and after "
            "720 seconds of aerosol ageing. Each pair summarises aggregated values from the SAME and SAME-R "
            "reports; it is not an individual particle.",
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    study = st.selectbox("Study", ["All", "SAME", "SAME-R"], key="dl_same_study")
    view = sizes if study == "All" else sizes[sizes["study"] == study]
    long = view.melt(
        id_vars=["study", "material"], value_vars=["base_nm", "aged_720s_nm"],
        var_name="condition", value_name="diameter_nm",
    )
    long["condition"] = long["condition"].map({"base_nm": "Base", "aged_720s_nm": "After 720 s"})
    long["label"] = long["material"] + " · " + long["study"]

    chart = alt.Chart(long).mark_bar(cornerRadiusEnd=3).encode(
        x=alt.X("label:N", title=None, sort=None, axis=alt.Axis(labelAngle=-35, labelLimit=160)),
        xOffset=alt.XOffset("condition:N", sort=["Base", "After 720 s"]),
        y=alt.Y("diameter_nm:Q", title="Mass-mean diameter (nm)"),
        color=alt.Color("condition:N", title="Condition", sort=["Base", "After 720 s"],
                        scale=alt.Scale(domain=["Base", "After 720 s"], range=["#78C8C3", "#F25C05"])),
        tooltip=[alt.Tooltip("label:N", title="Material"), alt.Tooltip("condition:N", title="Condition"),
                 alt.Tooltip("diameter_nm:Q", title="Diameter (nm)")],
    ).properties(height=380)
    st.altair_chart(dl_style(chart), width="stretch", theme=None)

    best = sizes.loc[sizes["change_pct"].idxmax()]
    st.markdown(
        '<div class="em"><div class="evidence-summary">'
        + dl_stat("Pairs compared", str(len(view)), "Selected study filter.")
        + dl_stat("Pairs with larger diameter", f"{int((view['change_nm'] > 0).sum())} of {len(view)}",
                  "Mass-mean diameter only.")
        + dl_stat("Largest relative change", f"{best['material']} · {best['study']}  +{best['change_pct']:.1f} %",
                  "Across all nine pairs.")
        + dl_stat("Smallest relative change", f"+{view['change_pct'].min():.1f} %", "In the selected pairs.")
        + "</div>"
        + dl_note(
            "Limits of this comparison",
            "The diameter increased in all nine selected pairs, but this holds for the mass-mean descriptor only. "
            "For SAME-R Teflon, the geometric diameter Dg falls from 81 nm to 70 nm while the mass-mean diameter "
            "rises from 170 nm to 232 nm. A larger particle does not mean a more toxic smoke or a specific "
            "probability of detection failure.",
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    table = view.rename(columns={
        "study": "Study", "material": "Material", "descriptor": "Descriptor", "base_nm": "Base (nm)",
        "aged_720s_nm": "After 720 s (nm)", "change_nm": "Change (nm)", "change_pct": "Change (%)",
        "source_note": "Source",
    })
    st.dataframe(table, hide_index=True, width="stretch",
                 column_config={"Change (%)": st.column_config.NumberColumn(format="%.1f")})
    st.download_button(
        "Download these records (CSV)", view.to_csv(index=False).encode("utf-8"),
        file_name="ember_same_particle_sizes.csv", mime="text/csv", key="dl_dl_same",
    )


def render_saffire_tab() -> None:
    import altair as alt

    try:
        saffire = load_saffire()
    except FileNotFoundError as error:
        st.error(str(error))
        return

    st.markdown(
        '<div class="em">'
        + dl_note(
            "Why Saffire sits next to BASS-II",
            "Saffire burned larger samples inside the uncrewed Cygnus vehicle. BASS-II used small samples in a "
            "glovebox duct. The two sets cannot be merged into one dataset, but they show how scale and "
            "geometry change what a test can tell you.",
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    rated = saffire.dropna(subset=["spread_rate_mm_s"]).copy()
    rated["label"] = rated["investigation"] + " · test " + rated["test_id"]
    rated["flow"] = rated["flow_cm_s"].map(lambda v: f"{v:g} cm/s")
    rated["scale"] = rated.apply(
        lambda r: "Large sample (40.6 × 94 cm)" if r["sample_width_cm"] == 40.6
        else ("5 × 29 cm sample" if r["sample_width_cm"] == 5 else "Opposed flow, about 10 cm length"),
        axis=1,
    )
    chart = alt.Chart(rated).mark_bar(cornerRadiusEnd=4, color="#F25C05").encode(
        x=alt.X("label:N", title=None, sort=None, axis=alt.Axis(labelAngle=0, labelLimit=140)),
        y=alt.Y("spread_rate_mm_s:Q", title="Reported spread rate (mm/s)"),
        tooltip=[alt.Tooltip("label:N", title="Test"), alt.Tooltip("material:N", title="Material"),
                 alt.Tooltip("flow:N", title="Airflow"), alt.Tooltip("flow_direction:N", title="Direction"),
                 alt.Tooltip("oxygen_vol_pct:Q", title="O₂ (vol. %)"),
                 alt.Tooltip("duration_s:Q", title="Duration (s)"),
                 alt.Tooltip("scale:N", title="Configuration")],
    ).properties(height=320, title="Cotton / fiberglass tests with a reported spread rate")
    st.altair_chart(dl_style(chart), width="stretch", theme=None)

    st.markdown(
        '<div class="em">'
        + dl_note(
            "Limits of this comparison",
            "Tests 2-5 and 2-6 differ by 0.5 mm/s (2.1 vs 2.6 mm/s, +23.8 %) with airflow of 20 and 25 cm/s. Their "
            "duration also differs, and two points cannot establish a general relation between flow and spread "
            "rate. Test 1-2 used opposed flow and a short sample, so it is not directly comparable with the others. "
            "The four silicone configurations did not sustain spread under the published conditions; this does "
            "not make silicone non-flammable in other environments. In the composite test 2-7, the PMMA segment "
            "burned and the Nomex did not ignite, so the components should be read separately.",
        )
        + "</div>",
        unsafe_allow_html=True,
    )
    table = saffire.rename(columns={
        "test_id": "Test", "investigation": "Investigation", "material": "Material",
        "sample_width_cm": "Width (cm)", "sample_length_cm": "Length (cm)", "thickness_mm": "Thickness (mm)",
        "flow_cm_s": "Flow (cm/s)", "flow_direction": "Direction", "oxygen_vol_pct": "O₂ (vol. %)",
        "oxygen_note": "O₂ note", "duration_s": "Duration (s)", "spread_rate_mm_s": "Spread (mm/s)",
        "documented_outcome": "Documented outcome", "source_note": "Source",
    })
    st.dataframe(table, hide_index=True, width="stretch")
    st.download_button(
        "Download these records (CSV)", saffire.to_csv(index=False).encode("utf-8"),
        file_name="ember_saffire_tests.csv", mime="text/csv", key="dl_dl_saffire",
    )


def render_audit_tab(tests: pd.DataFrame) -> None:
    import altair as alt

    total = len(tests)
    new = int((tests["reused_sample"] == "No").sum())
    reused = total - new
    unspecified = int((tests["observed_outcome"] == "Outcome not specified").sum())
    eligible = int(tests["model_eligible"].astype(str).str.lower().eq("true").sum())
    flagged = int((tests["oxygen_caveat"] == "Yes").sum())

    st.markdown(
        '<div class="em"><div class="evidence-summary">'
        + dl_stat("Records transcribed", str(total), "BASS-II rows of Table 7.1.")
        + dl_stat("New / reused samples", f"{new} / {reused}", "Reused samples are context only.")
        + dl_stat("Outcome not specified", f"{unspecified} of {total}", "A dash in the table is not 'spread'.")
        + dl_stat("Eligible for a spread classifier", f"{eligible} of {total}", "No row has an explicit label.")
        + "</div>"
        + '<div class="documentary-panel"><h2>Decision: no sustained-spread classifier from Table 7.1 alone</h2>'
        "<p>A supervised model needs a reliable label for every observation. This table records events such as "
        "quenching, no ignition, and blowoff, which are different mechanisms. It does not state whether sustained "
        "spread occurred in each run, and the label column was left empty on purpose instead of being inferred. "
        "Ember therefore shows comparable tests, counts, coverage, and gaps rather than a probability.</p></div>"
        + "</div>",
        unsafe_allow_html=True,
    )

    reasons = (
        tests["exclusion_reason"].replace("", "No reason recorded").value_counts()
        .rename_axis("reason").reset_index(name="tests")
    )
    chart = alt.Chart(reasons).mark_bar(cornerRadiusEnd=4, color="#E7B55A").encode(
        y=alt.Y("reason:N", sort="-x", title=None, axis=alt.Axis(labelLimit=520)),
        x=alt.X("tests:Q", title="Number of tests", axis=alt.Axis(tickMinStep=1, format="d")),
        tooltip=["reason:N", "tests:Q"],
    ).properties(height=250, title="Why each record is excluded from model training")
    st.altair_chart(dl_style(chart), width="stretch", theme=None)

    left, right = st.columns(2)
    with left:
        st.markdown(
            '<div class="em"><div class="card accent"><h3>What is needed before training</h3>'
            '<div class="case-list">'
            + "".join(f'<div class="case-list-item">{escape(i)}</div>' for i in [
                "Review PSI videos or files and label each test with one uniform sustained-spread rule.",
                "Record stable-regime duration, spread rate, and time of extinction where available.",
                "Keep new and reused samples separate and retain the physical sample identifier.",
                "Split validation by sample or run to avoid leakage; check class balance.",
                "Evaluate probability calibration, not only classification accuracy.",
            ])
            + "</div></div></div>",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            '<div class="em"><div class="card accent"><h3>What Data Lab will not show</h3>'
            '<div class="case-list">'
            + "".join(f'<div class="case-list-item">{escape(i)}</div>' for i in [
                "A fire or spread probability, or a safety percentage.",
                "Interpolation between tests or extrapolation outside the observed ranges.",
                "Lunar, Martian, or Earth-gravity predictions from ISS microgravity tests.",
                "Historical accidents as training data or as comparable records.",
                f"{flagged} records carry an O₂ accuracy flag from NASA and are shown with it.",
            ])
            + "</div></div></div>",
            unsafe_allow_html=True,
        )

    covered = pd.DataFrame([
        ("Material", "SIBAL 75 % cotton / 25 % fiberglass", "Any other material"),
        ("Geometry", "Flat fabric, 0.32 mm thick, 10 cm exposed", "Other geometry or thickness"),
        ("Sample width", "1.2 or 2.2 cm", "Outside 1.2–2.2 cm; no interpolation"),
        ("Oxygen", f"{tests['oxygen_vol_pct'].min():.1f}–{tests['oxygen_vol_pct'].max():.1f} vol. %",
         "Below or above the observed range"),
        ("Airflow", f"{min(tests['airflow_start_cm_s'].min(), tests['airflow_end_cm_s'].min()):g}–"
                    f"{max(tests['airflow_start_cm_s'].max(), tests['airflow_end_cm_s'].max()):g} cm/s profiles",
         "Below or above the observed range"),
        ("Flow direction", "Concurrent", "Opposed or not stated"),
        ("Gravity", "ISS microgravity", "Lunar, Martian, or Earth gravity"),
        ("Pressure", "1 atm", "Any other pressure"),
    ], columns=["Variable", "Directly covered", "Outside the tested domain"])
    st.markdown('<div class="em"><div class="question-intro"><h2>Tested domain of the SIBAL subset</h2>'
                '<p>Ranges are computed from the data. Anything outside them is an evidence gap, not a low-risk case.</p>'
                '</div></div>', unsafe_allow_html=True)
    st.dataframe(covered, hide_index=True, width="stretch")


def render_data_lab() -> None:
    nav = render_nav("datalab")

    try:
        tests = load_bassii_tests()
    except (FileNotFoundError, ValueError) as error:
        st.markdown(f'<div class="em">{nav}</div>', unsafe_allow_html=True)
        st.error(str(error))
        return

    header = dl_header(
        "Data Lab",
        "Explore the structured records behind Ember through tables and descriptive charts. Every mark is a real "
        "record with its source, and every chart states what it can and cannot support.",
        [f"{len(tests)} BASS-II / SIBAL tests", "9 SAME / SAME-R pairs", "9 Saffire tests",
         "Descriptive only: no predictions"],
    )
    st.markdown(f'<div class="em">{nav}{header}</div>', unsafe_allow_html=True)

    tab_bass, tab_same, tab_saffire, tab_audit = st.tabs(
        ["BASS-II · flame spread", "SAME / SAME-R · smoke", "Saffire · scale", "Data audit"]
    )
    with tab_bass:
        render_bassii_tab(tests)
    with tab_same:
        render_same_tab()
    with tab_saffire:
        render_saffire_tab()
    with tab_audit:
        render_audit_tab(tests)

    st.markdown(
        '<div class="footer">Data Lab is descriptive. Counts and frequencies describe designed experiments; '
        'they are not fire probabilities, safety ratings, or predictions for conditions that were not tested.</div>',
        unsafe_allow_html=True,
    )


st.markdown(CSS, unsafe_allow_html=True)

page = get_query_value("page", "home")
if page == "library":
    render_library()
elif page == "explorer":
    render_experiment_explorer()
elif page == "accidents":
    render_accident_cases()
elif page == "datalab":
    render_data_lab()
else:
    render_home()
