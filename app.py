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
  --bg: #090909;
  --bg-soft: #111111;
  --card: #1A1A1A;
  --ember: #F25C05;
  --ember-light: #FF7A1A;
  --text: #F4F4F2;
  --muted: #9A9A9A;
  --border: rgba(255,255,255,0.08);
}

header[data-testid="stHeader"],
footer,
#MainMenu,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
  display: none !important;
}

html,
body,
.stApp {
  background: var(--bg) !important;
}

.stApp {
  background:
    radial-gradient(
      700px 420px at 85% 6%,
      rgba(242,92,5,0.13),
      transparent 70%
    ),
    var(--bg) !important;
}

.block-container {
  max-width: 1180px !important;
  padding: 2rem 1.5rem 3rem !important;
}

.em,
.em * {
  box-sizing: border-box;
  font-family: Inter, Arial, sans-serif;
}

.em {
  color: var(--text);
  line-height: 1.6;
}

.em a {
  text-decoration: none;
}

.em h1,
.em h2,
.em h3,
.em p {
  margin: 0;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 18px 0 22px;
  border-bottom: 1px solid var(--border);
  flex-wrap: wrap;
}

.brand {
  font-weight: 800;
  letter-spacing: 0.22em;
  font-size: 1.05rem;
  color: var(--text);
}

.nav-links {
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
  align-items: center;
}

.nav-item {
  font-size: 0.92rem;
  color: var(--muted);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

a.nav-item:hover {
  color: var(--text);
}

.nav-item.active {
  color: var(--ember);
  font-weight: 600;
  border-bottom: 2px solid var(--ember);
  padding-bottom: 2px;
}

.nav-item small {
  font-size: 0.68rem;
  color: #6d6d6d;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 1px 8px;
}

.hero {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 56px;
  align-items: center;
  min-height: 78vh;
  padding: 56px 0;
}

.eyebrow {
  color: var(--ember-light);
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  font-weight: 600;
  margin-bottom: 22px;
}

.hero h1 {
  font-size: clamp(2.4rem, 5.2vw, 4.2rem);
  line-height: 1.05;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 26px;
}

.hero p.lead {
  color: var(--muted);
  font-size: 1.1rem;
  max-width: 34em;
  margin-bottom: 36px;
}

.cta-row {
  display: flex;
  align-items: center;
  gap: 22px;
  flex-wrap: wrap;
}

.btn {
  background: var(--ember);
  color: #0b0b0b !important;
  font-weight: 700;
  padding: 14px 28px;
  border-radius: 999px;
  display: inline-block;
  box-shadow: 0 8px 30px rgba(242,92,5,0.28);
}

.btn:hover {
  background: var(--ember-light);
}

.btn:focus-visible {
  outline: 2px solid var(--text);
  outline-offset: 3px;
}

.scope-note {
  color: var(--muted);
  font-size: 0.88rem;
}

.visual {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 14px;
  box-shadow:
    0 24px 60px rgba(0,0,0,0.5),
    0 0 90px rgba(242,92,5,0.16);
}

.visual img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 14px;
}

.visual-empty {
  aspect-ratio: 16 / 9;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--muted);
  font-size: 0.85rem;
  text-align: center;
  padding: 20px;
  background:
    radial-gradient(
      circle at 60% 45%,
      rgba(242,92,5,0.14),
      #0d0d0d 65%
    );
}

.section {
  padding: 72px 0 8px;
}

.section h2 {
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 700;
  letter-spacing: -0.01em;
  margin-bottom: 20px;
}

.about {
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 48px;
  margin-top: 40px;
  scroll-margin-top: 24px;
}

.about p {
  color: #cfcfcc;
  font-size: 1.05rem;
  max-width: 52em;
}

.grid3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.grid4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.grid5 {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

.card.accent {
  border-top: 2px solid var(--ember);
}

.card h3 {
  font-size: 1.15rem;
  font-weight: 650;
  margin-bottom: 12px;
  line-height: 1.3;
}

.card p {
  color: var(--muted);
  font-size: 0.96rem;
}

.step-n {
  color: var(--ember-light);
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 14px;
}

.step-t {
  font-size: 1.1rem;
  font-weight: 650;
  margin-bottom: 10px;
}

.plan {
  padding: 24px;
}

.plan h3 {
  font-size: 1.02rem;
  margin-bottom: 8px;
}

.status {
  display: inline-block;
  font-size: 0.72rem;
  padding: 3px 12px;
  border-radius: 999px;
  margin-bottom: 14px;
  border: 1px solid var(--border);
  color: var(--muted);
}

.status.on {
  color: var(--ember-light);
  border-color: rgba(242,92,5,0.5);
  background: rgba(242,92,5,0.1);
}

.plan.off {
  opacity: 0.8;
}

.scope {
  margin-top: 72px;
  background:
    linear-gradient(
      135deg,
      rgba(242,92,5,0.10),
      rgba(26,26,26,1) 55%
    );
  border: 1px solid rgba(242,92,5,0.28);
  border-radius: 22px;
  padding: 40px;
}

.scope h2 {
  font-size: 1.3rem;
  margin-bottom: 12px;
}

.scope p {
  color: #cfcfcc;
  max-width: 52em;
}

.library-header {
  padding: 64px 0 40px;
}

.library-header h1 {
  color: var(--text);
  font-size: clamp(2.2rem, 4vw, 3.6rem);
  line-height: 1.08;
  margin-bottom: 18px;
}

.library-header p {
  color: var(--muted);
  max-width: 48rem;
  font-size: 1.04rem;
}

.results-count {
  color: var(--muted);
  margin: 28px 0 18px;
  font-size: 0.9rem;
}

.investigation-card {
  min-height: 370px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px;
  margin-bottom: 24px;
  font-family: Inter, Arial, sans-serif;
  color: var(--text);
  display: flex;
  flex-direction: column;
}

.investigation-card:hover {
  border-color: rgba(242,92,5,0.45);
}

.psi-id {
  color: var(--ember-light);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  margin-bottom: 12px;
}

.investigation-card h3 {
  color: var(--text);
  font-size: 1.18rem;
  line-height: 1.35;
  margin: 0 0 14px;
}

.investigation-card p {
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.55;
  margin: 0;
}

.card-meta {
  color: #ccccca;
  font-size: 0.82rem;
  margin-bottom: 16px;
  line-height: 1.55;
}

.resource-list {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin: 18px 0;
}

.resource-tag {
  color: #c7c7c4;
  background: #111111;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.72rem;
}

.coverage {
  border-top: 1px solid var(--border);
  padding-top: 16px;
  margin-top: auto;
  color: #cfcfcc;
  font-size: 0.85rem;
}

.card-actions {
  display: flex;
  gap: 18px;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 18px;
}

.source-link {
  color: var(--ember-light) !important;
  font-size: 0.86rem;
  font-weight: 600;
}

.source-link:hover {
  color: var(--text) !important;
}

.source-link.secondary {
  color: #cfcfcc !important;
}

.detail-back {
  display: inline-block;
  color: var(--ember-light) !important;
  font-size: 0.88rem;
  font-weight: 600;
  margin: 28px 0;
}

.detail-panel {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 22px;
  padding: 38px;
}

.detail-panel h1 {
  font-size: clamp(1.8rem, 3.5vw, 3rem);
  line-height: 1.15;
  margin-bottom: 18px;
}

.detail-panel h2 {
  font-size: 1.2rem;
  margin: 34px 0 12px;
}

.detail-panel p {
  color: #cfcfcc;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 28px 0;
}

.detail-item {
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px;
}

.detail-label {
  color: var(--muted);
  font-size: 0.72rem;
  margin-bottom: 5px;
}

.detail-value {
  color: var(--text);
  font-size: 0.9rem;
  word-break: break-word;
}

div[data-testid="stTextInput"] input {
  background: var(--bg-soft);
  color: var(--text);
  border: 1px solid var(--border);
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div {
  background: var(--bg-soft);
  color: var(--text);
  border-color: var(--border);
}

.footer {
  margin-top: 80px;
  padding-top: 28px;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.88rem;
  text-align: center;
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
    gap: 36px;
    min-height: auto;
    padding: 36px 0;
  }

  .grid3,
  .grid4,
  .grid5,
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .about,
  .scope,
  .detail-panel {
    padding: 28px;
  }

  .nav-links {
    gap: 16px 20px;
  }
}

@media (min-width: 901px) and (max-width: 1100px) {
  .grid4,
  .grid5 {
    grid-template-columns: repeat(2, 1fr);
  }

  .detail-grid {
    grid-template-columns: repeat(2, 1fr);
  }
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
        '<div class="visual-empty">'
        'Visual not found. Place ember.gif.gif inside the assets folder.'
        '</div>'
    )


def html(block: str) -> str:
    return "\n".join(
        line.strip()
        for line in block.splitlines()
        if line.strip()
    )


def get_query_value(
    name: str,
    default: str = "",
) -> str:
    value = st.query_params.get(name, default)

    if isinstance(value, list):
        return value[0] if value else default

    return value


def render_nav(active_page: str) -> str:
    home_class = (
        "nav-item active"
        if active_page == "home"
        else "nav-item"
    )

    library_class = (
        "nav-item active"
        if active_page == "library"
        else "nav-item"
    )

    return html(
        f"""
        <div class="nav">
          <span class="brand">EMBER</span>

          <div class="nav-links">
            <a
              class="{home_class}"
              href="?page=home"
              target="_self"
            >
              Home
            </a>

            <a
              class="{library_class}"
              href="?page=library"
              target="_self"
            >
              Library
            </a>

            <span class="nav-item">
              Experiment Explorer <small>Planned</small>
            </span>

            <span class="nav-item">
              Accident Cases <small>Planned</small>
            </span>

            <span class="nav-item">
              Data Lab <small>Planned</small>
            </span>
          </div>
        </div>
        """
    )


hero = f"""
<div class="hero">
  <div>
    <div class="eyebrow">
      NASA PSI EXPERIMENTAL DATA
    </div>

    <h1>
      Find the experiment behind the question.
    </h1>

    <p class="lead">
      Ember organizes experimental conditions and documented
      outcomes so research students can locate relevant evidence
      without searching through disconnected reports.
    </p>

    <div class="cta-row">
      <a class="btn" href="#about">
        Understand Ember
      </a>

      <span class="scope-note">
        Prototype scope: BASS-II / SIBAL
      </span>
    </div>
  </div>

  <div class="visual">
    {load_gif_html()}
  </div>
</div>
"""

body = html(
    """
    <div class="about" id="about">
      <h2>From scattered reports to usable evidence</h2>

      <p>
        Ember organizes experimental information from NASA’s
        Physical Sciences Informatics platform for research
        students. The prototype begins with BASS-II/SIBAL and
        connects variables such as material, oxygen concentration,
        airflow, sample geometry, sample reuse, ignition status,
        and documented outcome. Its purpose is to make relevant
        experiments easier to find and compare while keeping the
        original source, missing information, and limits of
        interpretation visible.
      </p>
    </div>

    <div class="section">
      <div class="grid3">
        <div class="card accent">
          <h3>Search by experimental conditions</h3>

          <p>
            Locate experiments using variables such as material,
            oxygen concentration, airflow, geometry, ignition
            status, and documented outcome.
          </p>
        </div>

        <div class="card accent">
          <h3>Compare documented results</h3>

          <p>
            Review how different experimental conditions and
            observed outcomes are represented in the available
            records without converting descriptive evidence into
            unsupported predictions.
          </p>
        </div>

        <div class="card accent">
          <h3>Keep the source visible</h3>

          <p>
            Preserve the connection between every result, its
            original report, missing fields, and the limitations
            that affect its interpretation.
          </p>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>How Ember works</h2>

      <div class="grid3">
        <div class="card">
          <div class="step-n">01</div>
          <div class="step-t">Define the conditions</div>

          <p>
            Select the variables that are relevant to the
            research question.
          </p>
        </div>

        <div class="card">
          <div class="step-n">02</div>
          <div class="step-t">Review matching experiments</div>

          <p>
            Examine the documented conditions, observations,
            and available outcomes.
          </p>
        </div>

        <div class="card">
          <div class="step-n">03</div>
          <div class="step-t">Verify the evidence</div>

          <p>
            Consult the source and consider missing information
            before drawing conclusions.
          </p>
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

        <div class="card plan off">
          <span class="status">Planned</span>
          <h3>Experiment Explorer</h3>
          <p>Search and filter PSI experiments.</p>
        </div>

        <div class="card plan off">
          <span class="status">Planned</span>
          <h3>Accident Cases</h3>

          <p>
            Review documented cases and their relevant variables.
          </p>
        </div>

        <div class="card plan off">
          <span class="status">Planned</span>
          <h3>Data Lab</h3>

          <p>
            Explore selected records through tables and
            descriptive visualizations.
          </p>
        </div>
      </div>
    </div>

    <div class="scope">
      <h2>Prototype scope</h2>

      <p>
        The current prototype uses the available BASS-II/SIBAL
        records to demonstrate how PSI information can be organized
        and explored. It does not estimate fire risk, replace the
        original scientific reports, or generalize results to
        experimental conditions that were not tested.
      </p>
    </div>

    <div class="footer">
      Ember — Experimental evidence organized for research.
    </div>
    """
)


@st.cache_data(show_spinner=False)
def load_investigations() -> pd.DataFrame:
    if not INVESTIGATIONS_PATH.is_file():
        raise FileNotFoundError(
            f"Missing file: {INVESTIGATIONS_PATH}. "
            "Place investigations.csv inside the data folder."
        )

    dataframe = pd.read_csv(
        INVESTIGATIONS_PATH
    ).fillna("")

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

    missing_columns = required_columns.difference(
        dataframe.columns
    )

    if missing_columns:
        missing_text = ", ".join(
            sorted(missing_columns)
        )

        raise ValueError(
            f"Missing columns in investigations.csv: "
            f"{missing_text}"
        )

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
        pd.to_numeric(
            dataframe["ember_record_count"],
            errors="coerce",
        )
        .fillna(0)
        .astype(int)
    )

    return dataframe


def resource_tags(
    resources_text: str,
) -> str:
    resources = [
        item.strip()
        for item in str(resources_text).split("|")
        if item.strip()
    ]

    return "".join(
        (
            '<span class="resource-tag">'
            f"{escape(resource)}"
            "</span>"
        )
        for resource in resources
    )


def investigation_card(
    row: pd.Series,
) -> str:
    record_count = int(
        row["ember_record_count"]
    )

    if record_count > 0:
        coverage = (
            f"{record_count} structured records "
            "available in Ember"
        )
    else:
        coverage = escape(
            str(row["ember_status"])
        )

    identifier = str(
        row["psi_id"]
    )

    if str(row["acronym"]).strip():
        identifier = (
            f"{identifier} · "
            f"{row['acronym']}"
        )

    detail_id = escape(
        str(row["psi_id"]),
        quote=True,
    )

    source_url = escape(
        str(row["source_url"]),
        quote=True,
    )

    return f"""
    <div class="investigation-card">
      <div class="psi-id">
        {escape(identifier)}
      </div>

      <h3>
        {escape(str(row["title"]))}
      </h3>

      <div class="card-meta">
        {escape(str(row["research_area"]))}<br>
        {escape(str(row["subresearch_area"]))}<br>
        {escape(str(row["project_type"]))}<br>
        {escape(str(row["nasa_center"]))}
      </div>

      <p>
        {escape(str(row["objective_short"]))}
      </p>

      <div class="resource-list">
        {resource_tags(row["available_resources"])}
      </div>

      <p>
        Experimental table:
        {escape(str(row["experimental_table_status"]))}
      </p>

      <div class="coverage">
        Ember coverage: {coverage}
      </div>

      <div class="card-actions">
        <a
          class="source-link"
          href="?page=library&amp;psi={detail_id}"
          target="_self"
        >
          View investigation
        </a>

        <a
          class="source-link secondary"
          href="{source_url}"
          target="_blank"
          rel="noopener noreferrer"
        >
          Open in NASA PSI
        </a>
      </div>
    </div>
    """


def detail_item(
    label: str,
    value: str,
) -> str:
    shown_value = (
        value
        if str(value).strip()
        else "Not reported"
    )

    return f"""
    <div class="detail-item">
      <div class="detail-label">
        {escape(label)}
      </div>

      <div class="detail-value">
        {escape(str(shown_value))}
      </div>
    </div>
    """


def render_investigation_detail(
    row: pd.Series,
) -> None:
    record_count = int(
        row["ember_record_count"]
    )

    coverage = (
        f"{record_count} structured records "
        "available in Ember"
        if record_count > 0
        else str(row["ember_status"])
    )

    details = "".join(
        [
            detail_item(
                "Research area",
                row["research_area"],
            ),
            detail_item(
                "Subresearch area",
                row["subresearch_area"],
            ),
            detail_item(
                "Project type",
                row["project_type"],
            ),
            detail_item(
                "Flight platform",
                row["flight_platform"],
            ),
            detail_item(
                "NASA center",
                row["nasa_center"],
            ),
            detail_item(
                "DOI",
                row["doi"],
            ),
            detail_item(
                "Start date",
                row["start_date"],
            ),
            detail_item(
                "End date",
                row["end_date"],
            ),
            detail_item(
                "License",
                row["license"],
            ),
        ]
    )

    source_url = escape(
        str(row["source_url"]),
        quote=True,
    )

    identifier = str(
        row["psi_id"]
    )

    if str(row["acronym"]).strip():
        identifier = (
            f"{identifier} · "
            f"{row['acronym']}"
        )

    panel = f"""
    <a
      class="detail-back"
      href="?page=library"
      target="_self"
    >
      Back to Library
    </a>

    <div class="detail-panel">
      <div class="psi-id">
        {escape(identifier)}
      </div>

      <h1>
        {escape(str(row["title"]))}
      </h1>

      <div class="detail-grid">
        {details}
      </div>

      <h2>Research objective</h2>

      <p>
        {escape(str(row["objective_short"]))}
      </p>

      <h2>Available resources</h2>

      <div class="resource-list">
        {resource_tags(row["available_resources"])}
      </div>

      <h2>Data availability</h2>

      <p>
        Experimental table:
        {escape(str(row["experimental_table_status"]))}
      </p>

      <p>
        Modeling table:
        {escape(str(row["modeling_table_status"]))}
      </p>

      <p>
        Structured records in Ember:
        {escape(coverage)}
      </p>

      <h2>Related investigations</h2>

      <p>
        {
            escape(
                str(row["related_investigations"])
                or "Not reported"
            )
        }
      </p>

      <div class="card-actions">
        <a
          class="source-link"
          href="{source_url}"
          target="_blank"
          rel="noopener noreferrer"
        >
          Open in NASA PSI
        </a>
      </div>
    </div>
    """

    st.markdown(
        f'<div class="em">{panel}</div>',
        unsafe_allow_html=True,
    )


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
          <div class="eyebrow">
            NASA PHYSICAL SCIENCES INFORMATICS
          </div>

          <h1>PSI Research Library</h1>

          <p>
            Browse selected NASA PSI investigations and review
            the evidence available for each project. Ember
            distinguishes between investigation metadata,
            reports, analyzed data, publications, and structured
            experimental records.
          </p>
        </div>
        """
    )

    st.markdown(
        f'<div class="em">{nav}{header}</div>',
        unsafe_allow_html=True,
    )

    try:
        investigations = load_investigations()

    except (
        FileNotFoundError,
        ValueError,
    ) as error:
        st.error(
            str(error)
        )
        return

    selected_psi = get_query_value(
        "psi",
        "",
    ).strip()

    if selected_psi:
        selected_rows = investigations[
            investigations["psi_id"]
            .astype(str)
            .str.casefold()
            == selected_psi.casefold()
        ]

        if selected_rows.empty:
            st.warning(
                "The selected investigation was not "
                "found in the catalog."
            )

        else:
            render_investigation_detail(
                selected_rows.iloc[0]
            )
            return

    (
        search_column,
        area_column,
        type_column,
    ) = st.columns(
        [2, 1, 1]
    )

    with search_column:
        search = st.text_input(
            "Search",
            placeholder=(
                "Search by PSI ID, acronym, or title"
            ),
        )

    areas = [
        "All",
        *sorted(
            value
            for value in investigations[
                "research_area"
            ].unique()
            if value
        ),
    ]

    project_types = [
        "All",
        *sorted(
            value
            for value in investigations[
                "project_type"
            ].unique()
            if value
        ),
    ]

    with area_column:
        selected_area = st.selectbox(
            "Research area",
            areas,
        )

    with type_column:
        selected_type = st.selectbox(
            "Project type",
            project_types,
        )

    resource_options = sorted(
        {
            resource.strip()
            for resource_text in investigations[
                "available_resources"
            ]
            for resource in str(
                resource_text
            ).split("|")
            if resource.strip()
        }
    )

    (
        resources_column,
        coverage_column,
    ) = st.columns(
        [2, 1]
    )

    with resources_column:
        selected_resources = st.multiselect(
            "Available resources",
            resource_options,
        )

    with coverage_column:
        selected_coverage = st.selectbox(
            "Structured records in Ember",
            [
                "All",
                "Available",
                "Not yet curated",
            ],
        )

    filtered = investigations.copy()

    if search:
        searchable = (
            filtered[
                [
                    "psi_id",
                    "acronym",
                    "title",
                ]
            ]
            .astype(str)
            .agg(
                " ".join,
                axis=1,
            )
        )

        filtered = filtered[
            searchable.str.contains(
                search,
                case=False,
                regex=False,
            )
        ]

    if selected_area != "All":
        filtered = filtered[
            filtered["research_area"]
            == selected_area
        ]

    if selected_type != "All":
        filtered = filtered[
            filtered["project_type"]
            == selected_type
        ]

    if selected_resources:
        filtered = filtered[
            filtered[
                "available_resources"
            ].apply(
                lambda value: all(
                    resource
                    in {
                        item.strip()
                        for item in str(
                            value
                        ).split("|")
                        if item.strip()
                    }
                    for resource in selected_resources
                )
            )
        ]

    if selected_coverage == "Available":
        filtered = filtered[
            filtered["ember_record_count"] > 0
        ]

    elif selected_coverage == "Not yet curated":
        filtered = filtered[
            filtered["ember_record_count"] == 0
        ]

    st.markdown(
        (
            '<div class="results-count">'
            f"{len(filtered)} investigations found"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info(
            "No investigations match the selected filters."
        )
        return

    card_columns = st.columns(2)

    for position, (_, row) in enumerate(
        filtered.iterrows()
    ):
        with card_columns[position % 2]:
            st.markdown(
                investigation_card(row),
                unsafe_allow_html=True,
            )

    st.markdown(
        (
            '<div class="footer">'
            "Ember — Experimental evidence "
            "organized for research."
            "</div>"
        ),
        unsafe_allow_html=True,
    )


st.markdown(
    CSS,
    unsafe_allow_html=True,
)

page = get_query_value(
    "page",
    "home",
)

if page == "library":
    render_library()
else:
    render_home()
