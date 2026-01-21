# openai cover generator skill

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

## How It Works

1. **Color Palette**: Generates 5 bold, vibrant colors with high saturation (0.75-0.95)
2. **Gradient Centers**: Creates 6 color centers at strategic positions with weighted exponential falloff
3. **Flow Distortion**: Adds organic wave-like patterns using sine/cosine functions
4. **Multi-Scale Blur**: Applies Gaussian blur at multiple scales for ultra-smooth gradients
5. **Vibrancy Boost**: Enhances saturation (1.25x) and contrast (1.15x)

## Usage

```bash
python generate_cover.py -o cover.png -c blue
python generate_cover.py -c #FF5733 -r 1:1
```

Options: `-o` output, `-c` theme color, `-r` ratio, `-w` width, `-ht` height

## Download

[**Download openai-cover-generator.zip**](openai-cover-generator.zip)
