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
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

def icon(name: str) -> str:
    """Inline SVG icons approximating RenderCV / Font Awesome connections."""
    paths = {
        "email": "M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48H48zM0 176V384c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V176L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z",
        "link": "M579.8 267.7c56.5-56.5 56.5-148.2 0-204.7-50-50-128.8-56.5-186.3-15.4l-1.6 1.1c-14.4 10.3-17.7 30.3-7.4 44.6s30.3 17.7 44.6 7.4l1.6-1.1c32.1-22.9 76-19.3 103.8 8.6 31.5 31.5 31.5 82.5 0 114L422.3 334.8c-31.5 31.5-82.5 31.5-114 0-27.9-27.9-31.5-71.8-8.6-103.8l1.1-1.6c10.3-14.4 6.9-34.4-7.4-44.6s-34.4-6.9-44.6 7.4l-1.1 1.6C189.6 251.2 197.9 345 255 402.1c56.5 56.5 148.2 56.5 204.7 0L579.8 267.7zM60.2 244.3c-56.5 56.5-56.5 148.2 0 204.7 50 50 128.8 56.5 186.3 15.4l1.6-1.1c14.4-10.3 17.7-30.3 7.4-44.6s-30.3-17.7-44.6-7.4l-1.6 1.1c-32.1 22.9-76 19.3-103.8-8.6C74 372 74 321 105.5 289.5L217.7 177.2c31.5-31.5 82.5-31.5 114 0 27.9 27.9 31.5 71.8 8.6 103.9l-1.1 1.6c-10.3 14.4-6.9 34.4 7.4 44.6s34.4 6.9 44.6-7.4l1.1-1.6C450.4 260.8 442.1 167 385 109.9c-56.5-56.5-148.2-56.5-204.7 0L60.2 244.3z",
        "github": "M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8z",
        "linkedin": "M100.3 448H7.4V148.9h92.9zM53.8 108.1C24.1 108.1 0 83.5 0 53.8S24.1 0 53.8 0s53.8 24.1 53.8 53.8-24.1 54.3-53.8 54.3zM447.9 448h-92.7V302.4c0-34.7-.7-79.2-48.3-79.2-48.3 0-55.7 37.7-55.7 76.7V448h-92.8V148.9h89.1v40.8h1.3c12.4-23.5 42.7-48.3 87.9-48.3 94 0 111.3 61.9 111.3 142.3V448z",
    }
    view = {
        "email": "0 0 512 512",
        "link": "0 0 640 512",
        "github": "0 0 496 512",
        "linkedin": "0 0 448 512",
    }
    key = name if name in paths else "link"
    return (
        f'<svg class="icon" viewBox="{view[key]}" aria-hidden="true">'
        f'<path d="{paths[key]}"/></svg>'
    )


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
    dash = " -- " if language == "japanese" else " -- "
    for item in entries:
        if not isinstance(item, dict):
            continue
        position = esc(item.get("position", ""))
        company = esc(item.get("company", ""))
        location = item.get("location") or ""
        title = f'<span class="role">{position}</span>, {company}'
        if location:
            title = f"{title}{dash}{esc(location)}"
        date = format_range(item.get("start_date"), item.get("end_date"), language)
        summary = item.get("summary") or ""
        highlights = item.get("highlights") or []
        lis = "".join(f"<li>{esc(h)}</li>" for h in highlights)
        summary_html = f'<p class="entry-summary">{esc(summary)}</p>' if summary else ""
        list_html = f"<ul>{lis}</ul>" if lis else ""
        blocks.append(
            f"""
<article class="entry">
  <div class="entry-head">
    <h3 class="entry-title">{title}</h3>
    <p class="entry-meta">{esc(date)}</p>
  </div>
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


def section_heading(title: str, language: str) -> str:
    if language == "japanese":
        return title
    # RenderCV shows English section titles in Title Case
    return title.replace("_", " ").strip().title()


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
        if "label" not in first and "company" not in first and "institution" not in first:
            if any(isinstance(e, dict) and "name" in e for e in entries):
                body = render_certificates(entries)
            else:
                body = render_bullets(entries)
        else:
            body = render_bullets(entries)
    else:
        body = render_bullets(entries)

    heading = section_heading(title, language)
    return f"<section>\n  <h2>{esc(heading)}</h2>\n  {body}\n</section>"


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
    from datetime import date

    name = cv.get("name") or ""
    headline = cv.get("headline") or ""
    email = cv.get("email") or ""
    website = cv.get("website") or ""
    socials = cv.get("social_networks") or []
    sections = cv.get("sections") or {}

    today = date.today()
    if language == "japanese":
        updated = f"最終更新：{today.year}年{today.month}月"
    else:
        updated = f"Last updated in {MONTHS_EN[today.month]} {today.year}"

    contacts: list[str] = []
    if email:
        contacts.append(
            f'<li><a href="mailto:{esc(email)}">{icon("email")}'
            f"<span>{esc(email)}</span></a></li>"
        )
    if website:
        label = website.replace("https://", "").replace("http://", "").rstrip("/")
        contacts.append(
            f'<li><a href="{esc(website)}">{icon("link")}'
            f"<span>{esc(label)}</span></a></li>"
        )
    for social in socials:
        if not isinstance(social, dict):
            continue
        network = social.get("network") or ""
        username = social.get("username") or ""
        url = social_url(network, username)
        contacts.append(
            f'<li><a href="{esc(url)}">{icon(network.lower())}'
            f"<span>{esc(username)}</span></a></li>"
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
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
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
        <p class="updated">{esc(updated)}</p>
        <h1>{esc(name)}</h1>
        <p class="headline">{esc(headline)}</p>
        <ul class="contacts">
          {"".join(contacts)}
        </ul>
      </header>
      {section_html}
    </main>
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
