# openai cover generator

#### Generate bold, vibrant gradient cover images inspired by OpenAI's design aesthetic.

<table>
<tr>
<td><img src="assets/bold_blue.png" width="300"></td>
<td><img src="assets/bold_orange.png" width="300"></td>
</tr>
<tr>
<td><img src="assets/bold_pink.png" width="300"></td>
<td><img src="assets/openai_blue_cover.png" width="300"></td>
</tr>
</table>

## Dynamic Generator UI (Frontend-only)

`index.html` is a pure frontend dynamic generator with real-time controls:

- Main hue range (min/max)
- Blur amount
- Opacity
- Animation speed
- Blob count and saturation
- Randomize and PNG export

Run locally:

```bash
python -m http.server 8000
# open http://localhost:8000/index.html
```

## Cloudflare Pages CI/CD

This repo includes GitHub Actions workflow:

- File: `.github/workflows/deploy-cloudflare-pages.yml`
- Trigger: push to `main` (and manual dispatch)
- Deploy target: Cloudflare Pages (static frontend, no backend)
- Worker name in `wrangler.toml` is set to `openai-cover-generator` (matching your existing URL).

### Cloudflare Dashboard deploy command (important)

If your Cloudflare build logs show this error:

`It looks like you've run a Workers-specific command in a Pages project.`

Change the deploy command from:

```bash
npx wrangler deploy
```

to:

```bash
npm run deploy
# or: npx wrangler pages deploy .
# workers.dev fallback: npm run deploy:workers
```

This repository now includes a `package.json` deploy script that targets **Pages** instead of Workers.

If you deploy to a Workers URL such as `*.workers.dev`, this repo now also includes a Worker static-assets fallback, so you should still see the same `index.html` app instead of the default Hello World.

### 1) Create a Cloudflare Pages project

- In Cloudflare Dashboard → Pages → Create application → Connect to Git.
- Use this repository and set framework to **None**.
- Build command: leave empty.
- Build output directory: `.`

### 2) Configure GitHub repository secrets

Add these repository secrets:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_PAGES_PROJECT` (your Pages project name)

### 3) Push to main

After pushing to `main`, GitHub Actions automatically deploys the latest static site to Cloudflare Pages.

## Python Static Generator (original)

```bash
python openai-cover-generator/scripts/generate_cover.py -o cover.png -c blue
python openai-cover-generator/scripts/generate_cover.py -c '#FF5733' -r 1:1
```

Options: `-o` output, `-c` theme color, `-r` ratio, `-w` width, `-ht` height

## Download

[**Download openai-cover-generator.zip**](openai-cover-generator.zip)
