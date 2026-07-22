#!/usr/bin/env python3
"""Expand dynamic placeholders in RenderCV YAML (e.g. years of experience)."""

from __future__ import annotations

import copy
import re
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: python3 -m pip install pyyaml") from exc

PLACEHOLDER_YEARS = "{{years_of_experience}}"

# Experience-like section keys in EN / JA YAMLs
EXPERIENCE_KEYS = {"experience", "業務経歴"}


def _parse_year_month(value: str) -> tuple[int, int] | None:
    if not value or value == "present":
        return None
    match = re.fullmatch(r"(\d{4})-(\d{2})", value.strip())
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def career_start_from_cv(cv: dict[str, Any]) -> tuple[int, int] | None:
    """Return (year, month) of the earliest experience start_date."""
    sections = cv.get("sections") or {}
    starts: list[tuple[int, int]] = []
    for key, entries in sections.items():
        if key not in EXPERIENCE_KEYS or not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            parsed = _parse_year_month(str(entry.get("start_date") or ""))
            if parsed:
                starts.append(parsed)
    if not starts:
        return None
    return min(starts)


def years_of_experience(
    start: tuple[int, int],
    *,
    today: date | None = None,
) -> int:
    """Rounded whole years from start YYYY-MM to today (for 約N年 / about N years)."""
    today = today or date.today()
    start_year, start_month = start
    total_months = (today.year - start_year) * 12 + (today.month - start_month)
    if total_months < 0:
        return 0
    # Round to nearest year (8y10m → 9)
    return (total_months + 6) // 12


def expand_value(value: Any, years: int) -> Any:
    token = str(years)
    if isinstance(value, str):
        return value.replace(PLACEHOLDER_YEARS, token)
    if isinstance(value, list):
        return [expand_value(item, years) for item in value]
    if isinstance(value, dict):
        return {key: expand_value(item, years) for key, item in value.items()}
    return value


def expand_document(data: dict[str, Any], *, today: date | None = None) -> dict[str, Any]:
    expanded = copy.deepcopy(data)
    cv = expanded.get("cv") or {}
    start = career_start_from_cv(cv)
    if start is None:
        return expanded
    years = years_of_experience(start, today=today)
    expanded["cv"] = expand_value(cv, years)
    return expanded


def load_and_expand(path: Path, *, today: date | None = None) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return expand_document(data, today=today)


def write_expanded_yaml(
    src: Path,
    dest: Path,
    *,
    output_folder: str | None = None,
    today: date | None = None,
) -> int:
    """Expand placeholders and write YAML. Returns computed years (or -1)."""
    data = load_and_expand(src, today=today)
    years = -1
    cv = data.get("cv") or {}
    start = career_start_from_cv(yaml.safe_load(src.read_text(encoding="utf-8")).get("cv") or {})
    if start is not None:
        years = years_of_experience(start, today=today)

    if output_folder is not None:
        settings = data.setdefault("settings", {})
        render_command = settings.setdefault("render_command", {})
        render_command["output_folder"] = output_folder

    dest.parent.mkdir(parents=True, exist_ok=True)
    # Keep unicode / unquoted style reasonably readable
    dest.write_text(
        yaml.safe_dump(
            data,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        ),
        encoding="utf-8",
    )
    return years


def main() -> int:
    """CLI: expand cv/*.yaml into build/cv/ for RenderCV."""
    root = Path(__file__).resolve().parent.parent
    out_dir = root / "build" / "cv"
    pairs = [
        ("Yuan_Zhang_EN_CV.yaml", "en"),
        ("Yuan_Zhang_JA_CV.yaml", "ja"),
    ]
    for name, locale in pairs:
        src = root / "cv" / name
        dest = out_dir / name
        # Relative to build/cv/ → repo rendercv_output/<locale>
        years = write_expanded_yaml(
            src,
            dest,
            output_folder=f"../../rendercv_output/{locale}",
        )
        print(f"Expanded {src.name} → {dest} (years_of_experience={years})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
