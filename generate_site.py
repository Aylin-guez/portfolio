from pathlib import Path
import html
import shutil

from portfolio_data import (
    CASE_STUDIES,
    DEFAULT_GITHUB_URL,
    ENGINE_PRODUCTS_ROOT,
    FEATURED_SERVICES,
    HOME_FEATURED_SLUGS,
    PORTFOLIO_CATEGORIES,
    PROFILE,
    PROJECTS,
    TEXT,
    WHAT_I_BUILD,
    PROBLEMS,
    PROBLEMS_ES,
    SOLUTIONS,
    SOLUTIONS_ES,
    INDUSTRIES,
    INDUSTRIES_ES,
    TECH_STACK,
)

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SHOWCASES = DOCS / "showcases"
ASSETS = DOCS / "assets"
ENGINE_PRODUCTS = Path(ENGINE_PRODUCTS_ROOT)
HERO_LOGO_SOURCE = Path(r"E:\datosperfil.png")


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def copy_showcase_assets() -> None:
    SHOWCASES.mkdir(parents=True, exist_ok=True)
    for item in CASE_STUDIES:
        slug = item["slug"]
        source = ENGINE_PRODUCTS / slug / "showcase"
        target = SHOWCASES / slug
        target.mkdir(parents=True, exist_ok=True)
        if not source.exists():
            continue
        for png in sorted(source.glob("page_*.png")):
            shutil.copy2(png, target / png.name)


def copy_brand_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    if HERO_LOGO_SOURCE.exists():
        shutil.copy2(HERO_LOGO_SOURCE, ASSETS / HERO_LOGO_SOURCE.name)


def product_by_slug(slug: str) -> dict:
    return next(item for item in CASE_STUDIES if item["slug"] == slug)


def image_path(item: dict) -> str:
    return f"showcases/{item['slug']}/page_01_cover.png"


def showcase_path(item: dict) -> str:
    return f"showcases/{item['slug']}/index.html"


def render_product_card(item: dict, t: dict) -> str:
    title = esc(item["title"])
    return f"""
    <article class="case-card">
      <a class="case-image-link" href="{showcase_path(item)}" aria-label="{esc(t['view_showcase'])}: {title}">
        <img src="{image_path(item)}" alt="{title} showcase preview" loading="lazy" />
      </a>
      <div class="case-content">
        <p class="case-category">{esc(item['category'])}</p>
        <h3>{title}</h3>
        <p>{esc(item['description'])}</p>
      </div>
      <div class="case-actions">
        <a class="button-primary" href="{showcase_path(item)}">{esc(t['view_showcase'])}</a>
        <a class="button-secondary" href="{DEFAULT_GITHUB_URL}" target="_blank" rel="noreferrer">{esc(t['github'])}</a>
      </div>
    </article>
    """


def render_showcase_page(item: dict) -> str:
    source = SHOWCASES / item["slug"]
    images = sorted(path.name for path in source.glob("page_*.png"))
    image_markup = "\n".join(
        f'<img src="{name}" alt="{esc(item["title"])} page {index}" loading="lazy" />'
        for index, name in enumerate(images, start=1)
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(item['title'])} | Showcase</title>
  <link rel="stylesheet" href="../../style.css" />
</head>
<body id="top">
  <main class="showcase-page">
    <nav class="showcase-nav">
      <a href="../../index.html#portfolio">Back to portfolio</a>
      <a href="{DEFAULT_GITHUB_URL}" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
    <header class="showcase-header">
      <p class="section-label">{esc(item['category'])}</p>
      <h1>{esc(item['title'])}</h1>
      <p>{esc(item['description'])}</p>
    </header>
    <section class="showcase-grid">
      {image_markup}
    </section>
  </main>
</body>
</html>
"""


def render_service_cards() -> str:
    return "\n".join(
        f"""
        <article class="service-card">
          <h3>{esc(item['title'])}</h3>
          <p>{esc(item['text'])}</p>
        </article>
        """
        for item in FEATURED_SERVICES
    )


def render_build_cards() -> str:
    return "\n".join(
        f"""
        <article class="build-card">
          <div class="build-icon">{esc(item['icon'])}</div>
          <h3>{esc(item['title'])}</h3>
          <p>{esc(item['text'])}</p>
        </article>
        """
        for item in WHAT_I_BUILD
    )


def render_problem_cards(lang: str) -> str:
    problems = PROBLEMS_ES if lang == "es" else PROBLEMS
    return "\n".join(f'<div class="problem-item">{esc(item)}</div>' for item in problems)


def render_solution_cards(lang: str) -> str:
    solutions = SOLUTIONS_ES if lang == "es" else SOLUTIONS
    labels = {"en": ("Problem", "Solution", "Tech"), "es": ("Problema", "Solución", "Tecnologías")}[lang]
    return "\n".join(
        f"""
        <article class="solution-card">
          <h3>{esc(item['title'])}</h3>
          <p><strong>{labels[0]}:</strong> {esc(item['problem'])}</p>
          <p style="margin-top:10px"><strong>{labels[1]}:</strong> {esc(item['solution'])}</p>
          <div class="solution-meta">{labels[2]}: {esc(item['tech'])}</div>
        </article>
        """
        for item in solutions
    )


def render_tag_cards(items: list[str]) -> str:
    return "\n".join(f'<article class="tag-card"><p>{esc(item)}</p></article>' for item in items)


def render_page(lang: str) -> str:
    t = TEXT[lang]
    featured = [product_by_slug(slug) for slug in HOME_FEATURED_SLUGS]

    featured_cards = "\n".join(render_product_card(item, t) for item in featured)

    category_sections = []
    for category in PORTFOLIO_CATEGORIES:
        products = [item for item in CASE_STUDIES if item["category"] == category]
        cards = "\n".join(render_product_card(item, t) for item in products)
        category_sections.append(
            f"""
            <section class="portfolio-category">
              <div class="category-heading">
                <p class="section-label">{esc(category)}</p>
                <h3>{esc(category)}</h3>
              </div>
              <div class="case-grid">
                {cards}
              </div>
            </section>
            """
        )
    portfolio_sections = "\n".join(category_sections)

    project_cards = "\n".join(
        f"""
        <article class="project-card">
          <p class="project-tags">{esc(item['tags'])}</p>
          <h3>{esc(item['title'])}</h3>
          <p>{esc(item['text'])}</p>
          <a class="button-primary project-link" href="{esc(item['link'])}" target="_blank" rel="noreferrer">{esc(t['view_project'])}</a>
        </article>
        """
        for item in PROJECTS
    )
    checklist = "\n".join(f"<p>{esc(item)}</p>" for item in t["checklist"])
    industries = INDUSTRIES_ES if lang == "es" else INDUSTRIES

    return f"""<!DOCTYPE html>
<html lang="{esc(t['lang'])}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(PROFILE['name'])} | {esc(PROFILE['title'])}</title>
  <link rel="icon" type="image/png" href="assets/datosperfil-favicon.png" />
  <link rel="apple-touch-icon" href="assets/datosperfil-favicon.png" />
  <link rel="stylesheet" href="style.css?v=3" />
</head>
<body id="top">
<header class="hero">
  <nav class="nav">
    <a class="brand-mark" href="#top" aria-label="{esc(PROFILE['name'])}">
      <img src="assets/datosperfil.png" alt="{esc(PROFILE['name'])}" loading="eager" />
      <span class="sr-only">{esc(PROFILE['name'])}</span>
    </a>
    <div class="nav-links">
      <a href="#services">{esc(t['nav_services'])}</a>
      <a href="#portfolio">{esc(t['nav_portfolio'])}</a>
      <a href="#projects">{esc(t['nav_projects'])}</a>
      <a href="#contact">{esc(t['nav_contact'])}</a>
      <a href="{esc(t['other_lang_url'])}">{esc(t['other_lang_label'])}</a>
      <button id="theme-toggle" type="button" aria-label="Toggle color theme">&#127769;</button>
    </div>
  </nav>
  <div class="hero-grid">
    <div>
      <p class="eyebrow">{esc(PROFILE['subtitle'])}</p>
      <h1>{esc(PROFILE['title'])}</h1>
      <p class="hero-text">{esc(t['hero_text'])}</p>
      <div class="buttons">
        <a href="#services">{esc(t['nav_services'])}</a>
        <a href="#solutions">{esc(t['solutions_label'])}</a>
        <a href="#portfolio">{esc(t['nav_portfolio'])}</a>
        <a href="{esc(PROFILE['github'])}" target="_blank" rel="noreferrer">GitHub</a>
        <a href="mailto:{esc(PROFILE['email'])}">Email</a>
      </div>
    </div>
    <div class="hero-panel">
      <p>{esc(t['hero_panel_title'])}</p>
      <h2>{esc(t['hero_panel_count'])}</h2>
      <span>{esc(t['hero_panel_label'])}</span>
      <hr>
      <p>{esc(t['hero_panel_stack'])}</p>
    </div>
  </div>
</header>
<nav class="section-rail" aria-label="Quick section navigation">
  <a class="section-rail-item" href="#services"><span class="section-rail-dot"></span><em>{esc(t['nav_services'])}</em></a>
  <a class="section-rail-item" href="#problems"><span class="section-rail-dot"></span><em>{esc(t['problems_label'])}</em></a>
  <a class="section-rail-item" href="#solutions"><span class="section-rail-dot"></span><em>{esc(t['solutions_label'])}</em></a>
  <a class="section-rail-item" href="#portfolio"><span class="section-rail-dot"></span><em>{esc(t['nav_portfolio'])}</em></a>
  <a class="section-rail-item" href="#contact"><span class="section-rail-dot"></span><em>{esc(t['nav_contact'])}</em></a>
</nav>
<main>
<section id="services" class="section">
  <p class="section-label">{esc(t['services_label'])}</p>
  <h2>{esc(t['services_title'])}</h2>
  <p class="section-intro">{esc(t['services_intro'])}</p>
  <div class="services-grid">{render_service_cards()}</div>
</section>
<section id="build" class="section alt">
  <p class="section-label">{esc(t['build_label'])}</p>
  <h2>{esc(t['build_title'])}</h2>
  <p class="section-intro">{esc(t['build_intro'])}</p>
  <div class="build-grid">{render_build_cards()}</div>
</section>
<section id="problems" class="section">
  <p class="section-label">{esc(t['problems_label'])}</p>
  <h2>{esc(t['problems_title'])}</h2>
  <p class="section-intro">{esc(t['problems_intro'])}</p>
  <div class="problem-grid">{render_problem_cards(lang)}</div>
</section>
<section id="solutions" class="section alt">
  <p class="section-label">{esc(t['solutions_label'])}</p>
  <h2>{esc(t['solutions_title'])}</h2>
  <p class="section-intro">{esc(t['solutions_intro'])}</p>
  <div class="solution-grid">{render_solution_cards(lang)}</div>
</section>
<section id="industries" class="section">
  <p class="section-label">{esc(t['industries_label'])}</p>
  <h2>{esc(t['industries_title'])}</h2>
  <p class="section-intro">{esc(t['industries_intro'])}</p>
  <div class="tag-grid">{render_tag_cards(industries)}</div>
</section>
<section id="tech" class="section alt">
  <p class="section-label">{esc(t['tech_label'])}</p>
  <h2>{esc(t['tech_title'])}</h2>
  <div class="tag-grid">{render_tag_cards(TECH_STACK)}</div>
</section>
<section id="projects" class="section">
  <p class="section-label">{esc(t['projects_label'])}</p>
  <h2>{esc(t['projects_title'])}</h2>
  <p class="section-intro">{esc(t['projects_intro'])}</p>
  <div class="project-grid">{project_cards}</div>
</section>
<section class="section alt">
  <p class="section-label">{esc(t['portfolio_label'])}</p>
  <h2>{esc(t['featured_title'])}</h2>
  <p class="section-intro">{esc(t['featured_intro'])}</p>
  <div class="case-grid featured-grid">{featured_cards}</div>
</section>
<section id="portfolio" class="section">
  <p class="section-label">{esc(t['portfolio_label'])}</p>
  <h2>{esc(t['portfolio_title'])}</h2>
  <p class="section-intro">{esc(t['portfolio_intro'])}</p>
  {portfolio_sections}
</section>
<section class="section split alt">
  <div>
    <p class="section-label">{esc(t['automate_label'])}</p>
    <h2>{esc(t['automate_title'])}</h2>
  </div>
  <div class="checklist">{checklist}</div>
</section>
<section id="contact" class="contact-section">
  <h2>{esc(t['contact_title'])}</h2>
  <p>{esc(t['contact_text'])}</p>
  <a href="mailto:{esc(PROFILE['email'])}">{esc(PROFILE['email'])}</a>
</section>
</main>
<footer><p>2026 {esc(PROFILE['name'])} - {esc(t['footer'])}</p></footer>
<script>
  const button = document.getElementById("theme-toggle");
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {{
    document.body.classList.add("dark");
    button.textContent = String.fromCodePoint(0x2600, 0xFE0F);
  }}
  button.addEventListener("click", () => {{
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    button.textContent = isDark ? String.fromCodePoint(0x2600, 0xFE0F) : String.fromCodePoint(0x1F319);
  }});

  const rail = document.querySelector(".section-rail");
  if (rail) {{
    const toggleRail = () => rail.classList.toggle("is-visible", window.scrollY > 500);
    toggleRail();
    window.addEventListener("scroll", toggleRail, {{ passive: true }});
  }}
</script>
</body>
</html>
"""


CSS = """
*{box-sizing:border-box}
:root{
  --bg:#f7f5fb;--ink:#151522;--muted:#5a5868;--brand:#2b214f;--brand-2:#6848a0;--accent:#7b4cd8;
  --card:#fff;--line:#e8e2f0;--soft:#eee8f8;--shadow:rgba(39,31,69,.10);--glass:rgba(255,255,255,.13)
}
html{scroll-behavior:smooth}body{margin:0;font-family:Arial,sans-serif;background:var(--bg);color:var(--ink)}a{color:inherit}
.hero{padding:28px 8% 76px;color:white;background:radial-gradient(circle at 18% 0%,rgba(255,255,255,.18),transparent 30%),linear-gradient(135deg,var(--brand),var(--brand-2))}
.nav{display:flex;justify-content:space-between;align-items:center;margin-bottom:70px}.nav-links{display:flex;align-items:center;gap:22px;flex-wrap:wrap}.nav a{text-decoration:none;opacity:.92;font-weight:700}
.brand-mark{display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;width:88px;height:88px;padding:6px;border-radius:50%;overflow:hidden;background:rgba(255,255,255,.16);box-shadow:0 10px 22px rgba(0,0,0,.16);text-decoration:none}.brand-mark img{display:block;width:100%;height:100%;object-fit:cover;border-radius:50%;background:#fff}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(280px,.65fr);gap:50px;align-items:center}.eyebrow,.section-label,.case-category,.project-tags{text-transform:uppercase;letter-spacing:1.8px;font-size:12px;font-weight:800}h1{font-size:clamp(42px,6vw,72px);line-height:.96;margin:14px 0 22px;max-width:820px}.hero-text{max-width:780px;font-size:20px;line-height:1.65;color:#f1ecff}.buttons{display:flex;gap:10px;flex-wrap:wrap;margin-top:32px}.buttons a,.contact-section a{display:inline-flex;align-items:center;justify-content:center;min-height:36px;padding:9px 14px;border-radius:999px;background:white;color:var(--brand);text-decoration:none;font-weight:800;font-size:14px;box-shadow:0 14px 28px rgba(0,0,0,.16)}
#theme-toggle{border:0;background:rgba(255,255,255,.18);color:white;border-radius:999px;padding:9px 13px;cursor:pointer;font-size:15px;font-weight:700}.hero-panel{background:var(--glass);border:1px solid rgba(255,255,255,.25);border-radius:28px;padding:34px;backdrop-filter:blur(10px);box-shadow:0 20px 44px rgba(0,0,0,.14)}.hero-panel h2{font-size:64px;margin:8px 0}.hero-panel span,.hero-panel p{color:#efeaff}.hero-panel hr{border:0;border-top:1px solid rgba(255,255,255,.25);margin:28px 0}
.section{padding:78px 8%;position:relative}.section.alt{background:#fff}.section h2{font-size:clamp(32px,4vw,48px);margin:8px 0 14px;letter-spacing:-1px}.section-intro{max-width:840px;color:var(--muted);line-height:1.7;font-size:17px;margin-bottom:34px}.section-label{color:var(--accent)}
.services-grid,.build-grid,.project-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}.service-card,.build-card,.project-card,.solution-card,.tag-card,.case-card,.checklist,.problem-item{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:0 16px 36px var(--shadow)}.service-card,.build-card,.project-card,.solution-card,.checklist{padding:24px}.service-card h3,.build-card h3,.project-card h3,.solution-card h3,.case-card h3{margin:0 0 12px;color:var(--brand)}.service-card p,.build-card p,.project-card p,.solution-card p,.case-card p,.tag-card p{margin:0;color:var(--muted);line-height:1.55;font-size:15px}
.build-card{position:relative;overflow:hidden}.build-card:before{content:"";position:absolute;inset:0 0 auto 0;height:4px;background:linear-gradient(90deg,var(--brand-2),#9b7ee7)}.build-icon{font-size:28px;margin-bottom:12px}.build-card h3{font-size:19px}.build-card p{font-size:14px}.problem-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}.problem-item{padding:16px 18px;color:var(--muted);line-height:1.55;font-size:15px}.problem-item::before{content:"✓";display:inline-grid;place-items:center;width:22px;height:22px;border-radius:999px;margin-right:10px;background:var(--soft);color:var(--brand-2);font-weight:900}.solution-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}.solution-card{display:flex;flex-direction:column;min-height:100%;border-top:4px solid var(--brand-2)}.solution-card h3{font-size:21px}.solution-card strong{color:var(--brand)}.solution-meta{margin-top:auto;padding-top:14px;border-top:1px solid var(--line);font-size:13px;font-weight:800;color:var(--brand-2)}
.tag-grid{display:flex;flex-wrap:wrap;gap:12px}.tag-card{padding:11px 15px;border-radius:999px;box-shadow:none;background:var(--soft)}.tag-card p{font-weight:800;color:var(--brand);font-size:14px}.tag-card p::before{content:"•";margin-right:8px;color:var(--brand-2);font-weight:900}
.portfolio-category{margin-top:42px}.category-heading{display:flex;justify-content:space-between;gap:20px;align-items:end;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:18px}.category-heading h3{margin:0;font-size:26px}.case-grid,.featured-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,280px));justify-content:center;gap:20px}.case-card{overflow:hidden;display:flex;flex-direction:column;min-height:100%;border-radius:12px}.case-image-link{display:block;background:var(--soft);border-bottom:1px solid var(--line)}.case-card img{display:block;width:100%;aspect-ratio:7/5;object-fit:cover;object-position:top center}.case-content{padding:20px 20px 0;flex:1}.case-category{margin:0 0 10px;color:var(--accent)}.case-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:18px 20px 20px}.button-primary,.button-secondary{display:inline-flex;align-items:center;justify-content:center;min-height:34px;padding:8px 12px;border-radius:999px;text-decoration:none;font-weight:800;font-size:12px}.button-primary{background:white;color:var(--brand);box-shadow:0 12px 28px rgba(0,0,0,.12)}.button-secondary{border:1px solid var(--line);color:var(--brand);background:var(--soft)}.project-card .button-primary{margin-top:14px;width:fit-content;background:#fff;color:var(--brand);border:1px solid var(--line);box-shadow:0 10px 22px rgba(39,31,69,.12)}
.split{display:grid;grid-template-columns:.8fr 1.2fr;gap:50px;align-items:start}.checklist p{margin:12px 0;color:var(--muted);line-height:1.6}.checklist p::before{content:"OK";display:inline-block;margin-right:10px;color:var(--brand-2);font-weight:900}.contact-section{margin:40px 8% 70px;padding:48px;border-radius:16px;background:linear-gradient(135deg,var(--brand),var(--brand-2));color:white}.contact-section h2{font-size:clamp(28px,4vw,44px);margin:0 0 12px}.contact-section p{color:#f1ecff}footer{padding:28px 8%;background:#1f1733;color:white}
.showcase-page{padding:28px 6% 70px}.showcase-nav{display:flex;justify-content:space-between;gap:16px;margin-bottom:36px}.showcase-nav a{color:var(--brand);font-weight:800;text-decoration:none}.showcase-header{max-width:900px;margin-bottom:34px}.showcase-header h1{color:var(--brand)}.showcase-header p{color:var(--muted);font-size:18px;line-height:1.65}.showcase-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}.showcase-grid img{width:100%;display:block;border:1px solid var(--line);border-radius:8px;box-shadow:0 16px 36px var(--shadow)}
.section-rail{position:fixed;right:14px;top:50%;transform:translateY(-50%) translateX(16px);z-index:20;display:flex;flex-direction:column;gap:8px;padding:8px 6px;background:rgba(255,255,255,.5);border:1px solid rgba(39,31,69,.12);border-radius:999px;backdrop-filter:blur(10px);box-shadow:0 12px 28px rgba(39,31,69,.12);opacity:0;pointer-events:none;transition:opacity .22s ease,transform .22s ease}.section-rail.is-visible{opacity:1;pointer-events:auto;transform:translateY(-50%)}.section-rail-item{display:flex;align-items:center;gap:10px;justify-content:flex-end;padding:2px 4px;text-decoration:none;white-space:nowrap}.section-rail-dot{display:block;width:8px;height:8px;border-radius:999px;background:var(--brand-2);box-shadow:0 0 0 3px rgba(104,72,160,.12)}.section-rail-item em{font-style:normal;font-size:12px;font-weight:800;color:var(--brand);opacity:0;max-width:0;overflow:hidden;transition:.18s;transform:translateX(6px)}.section-rail:hover .section-rail-item em,.section-rail:focus-within .section-rail-item em{opacity:1;max-width:140px;transform:translateX(0)}
body.dark{--bg:#11101a;--ink:#f7f4ff;--muted:#c8c1d8;--card:#1b1828;--line:#332a4a;--soft:#211b34;--shadow:rgba(0,0,0,.22);background:var(--bg);color:var(--ink)}body.dark .section.alt{background:#151321}body.dark .service-card h3,body.dark .build-card h3,body.dark .solution-card h3,body.dark .case-card h3,body.dark .project-card h3,body.dark .showcase-header h1{color:#efe8ff}body.dark .solution-card strong{color:#efe8ff}body.dark .button-secondary{color:#efe8ff;background:var(--soft)}body.dark .tag-card p{color:#efe8ff}body.dark .problem-item::before{background:#2b2340;color:#d8c8ff}body.dark .section-rail{background:rgba(19,16,29,.72);border-color:rgba(255,255,255,.06)}body.dark .section-rail-dot{background:#cdb8ff;box-shadow:0 0 0 3px rgba(205,184,255,.12)}body.dark .section-rail-item em{color:#efe8ff}
@media (max-width:1100px){.hero-grid,.split{grid-template-columns:1fr}.section-rail{right:10px;top:auto;bottom:12px;transform:translateX(14px);padding:7px 5px;gap:6px}}@media (max-width:760px){.hero{padding:24px 6% 56px}.nav{align-items:flex-start;gap:18px;flex-direction:column;margin-bottom:42px}.nav-links{gap:14px}.brand-mark{width:74px;height:74px;padding:5px}.section{padding:52px 6%}.case-grid,.featured-grid{grid-template-columns:1fr;justify-content:stretch}.case-actions{grid-template-columns:1fr}.contact-section{margin:28px 6% 54px;padding:32px}.section-rail{right:8px;bottom:10px;padding:6px 4px;gap:5px}.section-rail-item em{font-size:11px;max-width:100px}.tag-grid{display:grid;grid-template-columns:1fr 1fr}.tag-card{border-radius:12px}}
"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    copy_showcase_assets()
    copy_brand_assets()
    for item in CASE_STUDIES:
        showcase_dir = SHOWCASES / item["slug"]
        showcase_dir.mkdir(parents=True, exist_ok=True)
        (showcase_dir / "index.html").write_text(render_showcase_page(item), encoding="utf-8")
    (DOCS / "index.html").write_text(render_page("en"), encoding="utf-8")
    (DOCS / "es.html").write_text(render_page("es"), encoding="utf-8")
    (DOCS / "style.css").write_text(CSS, encoding="utf-8")
    print("Portfolio V2 generated from portfolio_data.py into docs/")


if __name__ == "__main__":
    main()
