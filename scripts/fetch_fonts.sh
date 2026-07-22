#!/usr/bin/env bash
# Download Noto Sans JP (Japanese glyphs) for RenderCV PDFs.
# Prefer static Regular/Bold — variable fonts can embed as Thin in Typst.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-"$ROOT/fonts"}"
MARKER="$DEST/.noto-sans-jp-static-ready"
BASE="https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/SubsetOTF/JP"

mkdir -p "$DEST"

if [[ -f "$MARKER" && -f "$DEST/NotoSansJP-Regular.otf" && -f "$DEST/NotoSansJP-Bold.otf" ]]; then
  echo "Japanese fonts already present in $DEST"
  exit 0
fi

echo "Downloading Noto Sans JP Regular/Bold into $DEST ..."
curl -fsSL -o "$DEST/NotoSansJP-Regular.otf" "$BASE/NotoSansJP-Regular.otf"
curl -fsSL -o "$DEST/NotoSansJP-Bold.otf" "$BASE/NotoSansJP-Bold.otf"

# Remove previous variable-font attempt if present
rm -f "$DEST/NotoSansJP-VariableFont_wght.ttf" "$DEST/.noto-sans-jp-ready"

date -u +"%Y-%m-%dT%H:%M:%SZ" > "$MARKER"
ls -lh "$DEST"/NotoSansJP-*.otf
echo "Done. Font family name: Noto Sans JP"
