# Yuan Zhang Resume

Bilingual resume (English / Japanese).

| Layer | Role |
|-------|------|
| `cv/*.yaml` | Single content source |
| RenderCV PDF | Formal applications (`engineeringclassic`) |
| Custom HTML + CSS | Online / mobile reading |
| GitHub Actions | Build and deploy `public/` to Pages |

## URLs

**Web (HTML)**

| URL | Description |
|-----|-------------|
| https://motoish.github.io/resume/ | Redirects to English |
| https://motoish.github.io/resume/en/ | English resume (mobile-friendly) |
| https://motoish.github.io/resume/ja/ | Japanese resume (mobile-friendly) |

**PDF (applications)**

| URL | Description |
|-----|-------------|
| https://motoish.github.io/resume/downloads/Yuan_Zhang_EN_Resume.pdf | English PDF |
| https://motoish.github.io/resume/downloads/Yuan_Zhang_JA_Resume.pdf | Japanese PDF |

## Layout

```
resume/
├── cv/
│   ├── Yuan_Zhang_EN_CV.yaml      # English content
│   └── Yuan_Zhang_JA_CV.yaml      # Japanese content
├── site/
│   └── styles.css                # Shared web styles
├── scripts/
│   ├── build.sh                  # Full build (PDF + HTML)
│   └── build_html.py             # YAML → HTML
├── public/
│   ├── index.html                # Root redirect → ./en/
│   ├── en/                       # generated
│   ├── ja/                       # generated
│   ├── assets/                   # generated (copied CSS)
│   └── downloads/                # generated PDFs
├── .github/workflows/deploy.yml
├── README.md
└── LICENSE
```

Generated paths under `public/` (except `public/index.html`) and `rendercv_output/` are gitignored and rebuilt by CI.

## Edit

1. Change content in `cv/Yuan_Zhang_EN_CV.yaml` and/or `cv/Yuan_Zhang_JA_CV.yaml`
2. Optionally adjust `site/styles.css`
3. Run `./scripts/build.sh`
4. Preview `public/en/index.html` and `public/ja/index.html`
