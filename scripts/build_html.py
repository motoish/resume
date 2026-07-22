#!/usr/bin/env python3
"""Generate lightweight HTML resumes from RenderCV YAML sources."""

from __future__ import annotations

import html
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install with: python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PRESENT = {
    "english": "present",
    "japanese": "現在",
}

MONTHS_EN = [
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def social_url(network: str, username: str) -> str:
    key = network.lower()
    if key == "github":
        return f"https://github.com/{username}"
    if key == "linkedin":
        return f"https://www.linkedin.com/in/{username}"
    return username


def format_month(date: str, language: str) -> str:
    if not date or date == "present":
        return PRESENT.get(language, "present")
    year, month = date.split("-")[:2]
    month_i = int(month)
    if language == "japanese":
        return f"{int(year)}年{month_i}月"
    return f"{MONTHS_EN[month_i]} {year}"


def format_range(start: str | None, end: str | None, language: str) -> str:
    if not start and not end:
        return ""
    start_s = format_month(start or "", language) if start else ""
    end_s = format_month(end or "present", language)
    if start_s and end_s:
        sep = " – " if language != "japanese" else " ～ "
        return f"{start_s}{sep}{end_s}"
    return start_s or end_s


def render_text_section(entries: list) -> str:
    paragraphs = "".join(f"<p>{esc(item)}</p>" for item in entries if isinstance(item, str))
    return f'<div class="summary">{paragraphs}</div>'


def render_experience(entries: list, language: str) -> str:
    blocks: list[str] = []
    for item in entries:
        if not isinstance(item, dict):
            continue
        title = f"{esc(item.get('position', ''))}, {esc(item.get('company', ''))}"
        date = format_range(item.get("start_date"), item.get("end_date"), language)
        location = item.get("location") or ""
        summary = item.get("summary") or ""
        highlights = item.get("highlights") or []
        lis = "".join(f"<li>{esc(h)}</li>" for h in highlights)
        location_html = f'<p class="entry-sub">{esc(location)}</p>' if location else ""
        summary_html = f'<p class="entry-summary">{esc(summary)}</p>' if summary else ""
        list_html = f"<ul>{lis}</ul>" if lis else ""
        blocks.append(
            f"""
<article class="entry">
  <div class="entry-head">
    <h3 class="entry-title">{title}</h3>
    <p class="entry-meta">{esc(date)}</p>
  </div>
  {location_html}
  {summary_html}
  {list_html}
</article>
""".strip()
        )
    return "\n".join(blocks)


def render_education(entries: list, language: str) -> str:
    blocks: list[str] = []
    for item in entries:
        if not isinstance(item, dict):
            continue
        degree = item.get("degree") or ""
        area = item.get("area") or ""
        institution = item.get("institution") or ""
        title_bits = [b for b in [degree, area] if b]
        title = f"{esc(', '.join(title_bits))} — {esc(institution)}" if title_bits else esc(institution)
        if language == "japanese" and degree and area:
            title = f"{esc(institution)} {esc(degree)}（{esc(area)}）"
        elif language == "japanese":
            title = esc(institution)
        date = format_range(item.get("start_date"), item.get("end_date"), language)
        location = item.get("location") or ""
        highlights = item.get("highlights") or []
        lis = "".join(f"<li>{esc(h)}</li>" for h in highlights)
        location_html = f'<p class="entry-sub">{esc(location)}</p>' if location else ""
        list_html = f"<ul>{lis}</ul>" if lis else ""
        blocks.append(
            f"""
<article class="entry">
  <div class="entry-head">
    <h3 class="entry-title">{title}</h3>
    <p class="entry-meta">{esc(date)}</p>
  </div>
  {location_html}
  {list_html}
</article>
""".strip()
        )
    return "\n".join(blocks)


def render_skills(entries: list) -> str:
    rows: list[str] = []
    for item in entries:
        if not isinstance(item, dict):
            continue
        rows.append(
            f'<li><span class="label">{esc(item.get("label", ""))}</span>'
            f'<span class="details">{esc(item.get("details", ""))}</span></li>'
        )
    return f'<ul class="skills">{"".join(rows)}</ul>'


def render_certificates(entries: list) -> str:
    items: list[str] = []
    for item in entries:
        if isinstance(item, dict):
            if "bullet" in item:
                items.append(f"<li>{esc(item['bullet'])}</li>")
            elif "name" in item:
                items.append(f"<li>{esc(item['name'])}</li>")
        elif isinstance(item, str):
            items.append(f"<li>{esc(item)}</li>")
    return f'<ul class="plain-list">{"".join(items)}</ul>'


def render_bullets(entries: list) -> str:
    items: list[str] = []
    for item in entries:
        if isinstance(item, dict) and "bullet" in item:
            items.append(f"<li>{esc(item['bullet'])}</li>")
        elif isinstance(item, str):
            items.append(f"<li>{esc(item)}</li>")
    return f'<ul class="plain-list">{"".join(items)}</ul>'


def render_section(title: str, entries: list, language: str) -> str:
    if not entries:
        return ""
    first = entries[0]
    if isinstance(first, str):
        body = render_text_section(entries)
    elif isinstance(first, dict) and "company" in first:
        body = render_experience(entries, language)
    elif isinstance(first, dict) and "institution" in first:
        body = render_education(entries, language)
    elif isinstance(first, dict) and "label" in first:
        body = render_skills(entries)
    elif isinstance(first, dict) and ("name" in first or "bullet" in first):
        # certificates vs strengths: both ok as lists; strengths only have bullet
        if "label" not in first and "company" not in first and "institution" not in first:
            if any(isinstance(e, dict) and "name" in e for e in entries):
                body = render_certificates(entries)
            else:
                body = render_bullets(entries)
        else:
            body = render_bullets(entries)
    else:
        body = render_bullets(entries)

    return f"<section>\n  <h2>{esc(title)}</h2>\n  {body}\n</section>"


def build_page(
    *,
    cv: dict,
    language: str,
    lang_code: str,
    pdf_href: str,
    pdf_label: str,
    other_href: str,
    other_label: str,
    current_label: str,
) -> str:
    name = cv.get("name") or ""
    headline = cv.get("headline") or ""
    email = cv.get("email") or ""
    website = cv.get("website") or ""
    socials = cv.get("social_networks") or []
    sections = cv.get("sections") or {}

    contacts: list[str] = []
    if email:
        contacts.append(f'<li><a href="mailto:{esc(email)}">{esc(email)}</a></li>')
    if website:
        label = website.replace("https://", "").replace("http://", "").rstrip("/")
        contacts.append(f'<li><a href="{esc(website)}">{esc(label)}</a></li>')
    for social in socials:
        if not isinstance(social, dict):
            continue
        network = social.get("network") or ""
        username = social.get("username") or ""
        url = social_url(network, username)
        contacts.append(
            f'<li><a href="{esc(url)}">{esc(network)}: {esc(username)}</a></li>'
        )

    section_html = "\n".join(
        render_section(title, entries if isinstance(entries, list) else [], language)
        for title, entries in sections.items()
    )

    return f"""<!doctype html>
<html lang="{esc(lang_code)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(name)} — Resume</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,600&family=Noto+Sans+JP:wght@400;600;700&family=Noto+Serif+JP:wght@600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
  <div class="page">
    <div class="topbar">
      <nav aria-label="Language">
        <a href="{esc(other_href)}">{esc(other_label)}</a>
        <a href="./" aria-current="page">{esc(current_label)}</a>
      </nav>
      <nav aria-label="Downloads">
        <a href="{esc(pdf_href)}">{esc(pdf_label)}</a>
      </nav>
    </div>
    <main class="sheet">
      <header class="identity">
        <h1>{esc(name)}</h1>
        <p class="headline">{esc(headline)}</p>
        <ul class="contacts">
          {"".join(contacts)}
        </ul>
      </header>
      {section_html}
    </main>
    <p class="footer-note">Content sourced from YAML · PDF generated with RenderCV</p>
  </div>
</body>
</html>
"""


def load_cv(path: Path) -> tuple[dict, str]:
    from cv_placeholders import expand_document

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data = expand_document(data)
    cv = data.get("cv") or {}
    language = ((data.get("locale") or {}).get("language")) or "english"
    return cv, language


def main() -> int:
    en_cv, en_lang = load_cv(ROOT / "cv" / "Yuan_Zhang_EN_CV.yaml")
    ja_cv, ja_lang = load_cv(ROOT / "cv" / "Yuan_Zhang_JA_CV.yaml")

    assets = ROOT / "public" / "assets"
    en_dir = ROOT / "public" / "en"
    ja_dir = ROOT / "public" / "ja"
    assets.mkdir(parents=True, exist_ok=True)
    en_dir.mkdir(parents=True, exist_ok=True)
    ja_dir.mkdir(parents=True, exist_ok=True)

    css_src = ROOT / "site" / "styles.css"
    (assets / "styles.css").write_text(css_src.read_text(encoding="utf-8"), encoding="utf-8")

    en_html = build_page(
        cv=en_cv,
        language=en_lang,
        lang_code="en",
        pdf_href="../downloads/Yuan_Zhang_EN_Resume.pdf",
        pdf_label="Download PDF",
        other_href="../ja/",
        other_label="日本語",
        current_label="English",
    )
    ja_html = build_page(
        cv=ja_cv,
        language=ja_lang,
        lang_code="ja",
        pdf_href="../downloads/Yuan_Zhang_JA_Resume.pdf",
        pdf_label="PDFをダウンロード",
        other_href="../en/",
        other_label="English",
        current_label="日本語",
    )

    (en_dir / "index.html").write_text(en_html, encoding="utf-8")
    (ja_dir / "index.html").write_text(ja_html, encoding="utf-8")
    print(f"Wrote {en_dir / 'index.html'}")
    print(f"Wrote {ja_dir / 'index.html'}")
    print(f"Wrote {assets / 'styles.css'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
