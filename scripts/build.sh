#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v rendercv >/dev/null 2>&1; then
  echo "rendercv not found. Install with: python3 -m pip install 'rendercv[full]==2.8'" >&2
  exit 1
fi

rm -rf rendercv_output/en rendercv_output/ja
mkdir -p rendercv_output/en rendercv_output/ja
mkdir -p public/en public/ja public/downloads public/assets

rendercv render cv/Yuan_Zhang_EN_CV.yaml
rendercv render cv/Yuan_Zhang_JA_CV.yaml

EN_PDF="$(find rendercv_output/en -maxdepth 1 -name '*.pdf' | head -n 1)"
JA_PDF="$(find rendercv_output/ja -maxdepth 1 -name '*.pdf' | head -n 1)"

if [[ -z "${EN_PDF}" || -z "${JA_PDF}" ]]; then
  echo "Missing RenderCV PDF artifacts under rendercv_output/" >&2
  ls -R rendercv_output >&2 || true
  exit 1
fi

cp "${EN_PDF}" public/downloads/Yuan_Zhang_EN_Resume.pdf
cp "${JA_PDF}" public/downloads/Yuan_Zhang_JA_Resume.pdf

python3 scripts/build_html.py

# Ensure root redirect exists (do not overwrite customizations if already present)
if [[ ! -f public/index.html ]]; then
  cat > public/index.html <<'EOF'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=./en/">
    <link rel="canonical" href="./en/">
    <title>Yuan Zhang Resume</title>
  </head>
  <body>
    <p><a href="./en/">Open English resume</a></p>
  </body>
</html>
EOF
fi

echo "Build complete:"
echo "  public/index.html"
echo "  public/en/index.html"
echo "  public/ja/index.html"
echo "  public/assets/styles.css"
echo "  public/downloads/Yuan_Zhang_EN_Resume.pdf"
echo "  public/downloads/Yuan_Zhang_JA_Resume.pdf"
