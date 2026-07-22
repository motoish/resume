# Yuan Zhang Resume

Bilingual resume (EN / JA) built with [RenderCV](https://docs.rendercv.com/) (`engineeringclassic` theme).

## URLs

- https://motoish.github.io/resume/ (redirects to EN)
- https://motoish.github.io/resume/en/
- https://motoish.github.io/resume/ja/
- https://motoish.github.io/resume/downloads/Yuan_Zhang_EN_Resume.pdf
- https://motoish.github.io/resume/downloads/Yuan_Zhang_JA_Resume.pdf

## Edit

1. Update `cv/Yuan_Zhang_EN_CV.yaml` and/or `cv/Yuan_Zhang_JA_CV.yaml`
2. Run `./scripts/build.sh`
3. Open `public/en/index.html` / `public/ja/index.html` locally

## Build requirements

```bash
python3 -m pip install 'rendercv[full]==2.8'
./scripts/build.sh
```

## Deploy

Pushes to `main` run GitHub Actions, which builds and publishes the `public/` directory to GitHub Pages.

Enable **Settings → Pages → Build and deployment → GitHub Actions** if not already set.
