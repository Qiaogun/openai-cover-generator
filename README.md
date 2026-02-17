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

## New: Dynamic Generator UI

A new browser-based dynamic generator is available in `index.html` with a real-time control panel:

- Main hue range (min/max)
- Blur amount
- Opacity
- Animation speed
- Blob count and saturation
- One-click randomize and PNG export

Run locally:

```bash
python -m http.server 8000
# open http://localhost:8000/index.html
```

## Python Static Generator (original)

```bash
python openai-cover-generator/scripts/generate_cover.py -o cover.png -c blue
python openai-cover-generator/scripts/generate_cover.py -c '#FF5733' -r 1:1
```

Options: `-o` output, `-c` theme color, `-r` ratio, `-w` width, `-ht` height

## Download

[**Download openai-cover-generator.zip**](openai-cover-generator.zip)
