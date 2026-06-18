from pathlib import Path
from portfolio_data import PROFILE, FEATURED_SERVICES, CASE_STUDIES, PROJECTS

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

DOCS.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

service_cards = "\n".join(
    f"""
    <article class="service-card">
      <h3>{item["title"]}</h3>
      <p>{item["text"]}</p>
    </article>
    """
    for item in FEATURED_SERVICES
)

case_cards = "\n".join(
    f"""
    <article class="case-card">
      <span>Case Study</span>
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
    """
    for title, text in CASE_STUDIES
)

project_cards = "\n".join(
    f"""
    <article class="project-card">
      <p class="project-tags">{item["tags"]}</p>
      <h3>{item["title"]}</h3>
      <p>{item["text"]}</p>
      <a href="{item["link"]}" target="_blank">View project →</a>
    </article>
    """
    for item in PROJECTS
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{PROFILE["name"]} | {PROFILE["title"]}</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>

<header class="hero">
  <nav class="nav">
    <strong>{PROFILE["name"]}</strong>
    <div>
      <a href="#services">Services</a>
      <a href="#portfolio">Portfolio</a>
      <a href="#projects">Projects</a>
      <a href="#contact">Contact</a>
    </div>
  </nav>

  <div class="hero-grid">
    <div>
      <p class="eyebrow">{PROFILE["subtitle"]}</p>
      <h1>{PROFILE["title"]}</h1>
      <p class="hero-text">
        I build automation workflows that transform spreadsheets, PDFs,
        OCR outputs and structured data into professional reports,
        dossiers, manuals and business documents.
      </p>

      <div class="buttons">
        <a href="{PROFILE["github"]}">GitHub</a>
        <a href="{PROFILE["linkedin"]}">LinkedIn</a>
        <a href="{PROFILE["upwork"]}">Upwork</a>
        <a href="{PROFILE["fiverr"]}">Fiverr</a>
        <a href="mailto:{PROFILE["email"]}">Email</a>
      </div>
    </div>

    <div class="hero-panel">
      <p>Document Automation</p>
      <h2>15+</h2>
      <span>workflow demos</span>
      <hr>
      <p>Python • OCR • PDF Reports • Data Analysis</p>
    </div>
  </div>
</header>

<main>

<section id="services" class="section">
  <p class="section-label">Services</p>
  <h2>Core automation services</h2>
  <p class="section-intro">
    I focus on repetitive reporting and document workflows where teams lose time copying,
    formatting and rebuilding the same files every week or month.
  </p>
  <div class="services-grid">
    {service_cards}
  </div>
</section>

<section id="portfolio" class="section alt">
  <p class="section-label">Portfolio</p>
  <h2>15 document automation workflows</h2>
  <p class="section-intro">
    These case studies show how the same automation approach can adapt to different
    industries, formats and business needs.
  </p>
  <div class="case-grid">
    {case_cards}
  </div>
</section>

<section id="projects" class="section">
  <p class="section-label">Projects</p>
  <h2>Selected GitHub projects</h2>
  <p class="section-intro">
    A selection of projects related to document automation, OCR, data analysis,
    reporting and public information workflows.
  </p>
  <div class="project-grid">
    {project_cards}
  </div>
</section>

<section class="section split">
  <div>
    <p class="section-label">What I automate</p>
    <h2>From messy input to polished output</h2>
  </div>
  <div class="checklist">
    <p>PDF reports generated from Excel, CSV or structured data</p>
    <p>OCR and information extraction from documents</p>
    <p>Audit, compliance and traceability documentation</p>
    <p>Business reports, proposals, manuals and technical documentation</p>
    <p>Repetitive document workflows that waste time every month</p>
  </div>
</section>

<section id="contact" class="contact-section">
  <h2>Need to automate a recurring report or document workflow?</h2>
  <p>Send me a message and I can review the process with you.</p>
  <a href="mailto:{PROFILE["email"]}">{PROFILE["email"]}</a>
</section>

</main>

<footer>
  <p>© 2026 {PROFILE["name"]} — Document Automation & Data Analytics</p>
</footer>

</body>
</html>
"""

css = """* {
  box-sizing: border-box;
}

:root {
  --bg: #f7f5fb;
  --ink: #151522;
  --muted: #5a5868;
  --purple: #2b214f;
  --purple-2: #6848a0;
  --card: #ffffff;
  --line: #e8e2f0;
  --soft: #eee8f8;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: var(--bg);
  color: var(--ink);
}

a {
  color: inherit;
}

.hero {
  padding: 28px 8% 76px;
  color: white;
  background:
    radial-gradient(circle at 80% 20%, rgba(255,255,255,.18), transparent 30%),
    linear-gradient(135deg, var(--purple), var(--purple-2));
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 70px;
}

.nav a {
  margin-left: 22px;
  text-decoration: none;
  opacity: .9;
  font-weight: 700;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.4fr .6fr;
  gap: 50px;
  align-items: center;
}

.eyebrow,
.section-label {
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-size: 12px;
  font-weight: 800;
}

h1 {
  font-size: clamp(42px, 6vw, 72px);
  line-height: .95;
  margin: 14px 0 22px;
  max-width: 820px;
}

.hero-text {
  max-width: 760px;
  font-size: 20px;
  line-height: 1.65;
  color: #f1ecff;
}

.buttons {
  margin-top: 32px;
}

.buttons a,
.contact-section a {
  display: inline-block;
  margin: 8px 10px 8px 0;
  padding: 13px 20px;
  border-radius: 999px;
  background: white;
  color: var(--purple);
  text-decoration: none;
  font-weight: 800;
  box-shadow: 0 14px 28px rgba(0,0,0,.16);
}

.hero-panel {
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.25);
  border-radius: 28px;
  padding: 34px;
  backdrop-filter: blur(10px);
}

.hero-panel h2 {
  font-size: 86px;
  margin: 8px 0;
}

.hero-panel span,
.hero-panel p {
  color: #efeaff;
}

.hero-panel hr {
  border: 0;
  border-top: 1px solid rgba(255,255,255,.25);
  margin: 28px 0;
}

.section {
  padding: 70px 8%;
}

.section.alt {
  background: #fff;
}

.section h2 {
  font-size: clamp(32px, 4vw, 48px);
  margin: 8px 0 14px;
  letter-spacing: -1px;
}

.section-intro {
  max-width: 820px;
  color: var(--muted);
  line-height: 1.7;
  font-size: 17px;
  margin-bottom: 30px;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(170px, 1fr));
  gap: 18px;
}

.service-card,
.case-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 24px;
  box-shadow: 0 16px 40px rgba(43, 33, 79, .08);
}

.service-card h3,
.case-card h3 {
  margin: 0 0 12px;
  color: var(--purple);
  font-size: 19px;
}

.service-card p,
.case-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
  font-size: 15px;
}

.case-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(230px, 1fr));
  gap: 18px;
}

.case-card span {
  display: inline-block;
  margin-bottom: 12px;
  color: var(--purple-2);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.split {
  display: grid;
  grid-template-columns: .8fr 1.2fr;
  gap: 50px;
  align-items: start;
}

.checklist {
  background: white;
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 28px;
}

.checklist p {
  margin: 12px 0;
  color: var(--muted);
  line-height: 1.6;
}

.checklist p::before {
  content: "✓";
  color: var(--purple-2);
  font-weight: 900;
  margin-right: 10px;
}

.contact-section {
  margin: 40px 8% 70px;
  padding: 48px;
  border-radius: 30px;
  background: linear-gradient(135deg, var(--purple), var(--purple-2));
  color: white;
}

.contact-section h2 {
  font-size: clamp(28px, 4vw, 44px);
  margin: 0 0 12px;
}

.contact-section p {
  color: #efeaff;
}

footer {
  padding: 28px 8%;
  background: #1f1838;
  color: white;
}

@media (max-width: 1100px) {
  .hero-grid,
  .split {
    grid-template-columns: 1fr;
  }

  .services-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .case-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 700px) {
  .hero {
    padding: 24px 6% 56px;
  }

  .nav {
    align-items: flex-start;
    gap: 18px;
    flex-direction: column;
    margin-bottom: 42px;
  }

  .nav a {
    margin-left: 0;
    margin-right: 16px;
  }

  .section {
    padding: 52px 6%;
  }

  .services-grid,
  .case-grid,
  .project-grid {
    grid-template-columns: 1fr;
  }

  .contact-section {
    margin: 28px 6% 54px;
    padding: 32px;
  }
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}

.project-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 16px 40px rgba(43, 33, 79, .08);
}

.project-tags {
  color: var(--purple-2);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.4px;
  margin: 0 0 14px;
}

.project-card h3 {
  margin: 0 0 12px;
  color: var(--purple);
  font-size: 22px;
}

.project-card p {
  color: var(--muted);
  line-height: 1.6;
}

.project-card a {
  display: inline-block;
  margin-top: 12px;
  font-weight: 800;
  color: var(--purple-2);
  text-decoration: none;
}
}
"""

(DOCS / "index.html").write_text(html, encoding="utf-8")
(DOCS / "style.css").write_text(css, encoding="utf-8")

print("✅ Portfolio v2 generated in docs/")