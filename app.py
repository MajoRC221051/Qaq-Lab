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

.footer { margin-top: 80px; padding-top: 28px; border-top: 1px solid var(--border);
  color: var(--muted); font-size: 0.88rem; text-align: center; }

@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; gap: 36px; min-height: auto; padding: 36px 0; }
  .grid3, .grid4, .grid5, .detail-grid, .evidence-summary { grid-template-columns: 1fr; }
  .about, .scope, .detail-panel { padding: 28px; }
  .nav-links { gap: 16px 20px; }
}
@media (min-width: 901px) and (max-width: 1100px) {
  .grid4, .grid5 { grid-template-columns: repeat(2, 1fr); }
  .detail-grid, .evidence-summary { grid-template-columns: repeat(2, 1fr); }
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

    return html(
        f"""
        <div class="nav">
          <span class="brand">EMBER</span>
          <div class="nav-links">
            <a class="{home_class}" href="?page=home" target="_self">Home</a>
            <a class="{library_class}" href="?page=library" target="_self">Library</a>
            <a class="{explorer_class}" href="?page=explorer" target="_self">Experiment Explorer</a>
            <span class="nav-item">Accident Cases <small>Planned</small></span>
            <span class="nav-item">Data Lab <small>Planned</small></span>
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


st.markdown(CSS, unsafe_allow_html=True)

page = get_query_value("page", "home")
if page == "library":
    render_library()
elif page == "explorer":
    render_experiment_explorer()
else:
    render_home()
