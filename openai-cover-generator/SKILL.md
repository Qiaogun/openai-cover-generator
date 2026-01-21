---
name: openai-cover-generator
description: Generate bold, vibrant OpenAI-style abstract gradient cover images with complex color transitions and flowing effects. Use when users request: (1) Creating eye-catching cover images or backgrounds with vivid gradients, (2) Generating abstract art with bold, saturated colors and smooth transitions, (3) Making social media headers, presentation backgrounds, or promotional graphics with modern aesthetic, (4) Producing images similar to OpenAI's visual style with flowing, organic color gradients and high-contrast effects.
---

# OpenAI Cover Generator

Generate stunning, bold abstract gradient cover images in the style of OpenAI's visual branding. Creates smooth, flowing color gradients with vibrant colors, complex transitions, and organic patterns.

## Quick Start

Generate a bold cover image with default settings (4K resolution, vibrant colors):

```bash
python scripts/generate_cover.py --output my_cover.png --theme-color purple
```

## Common Usage Patterns

**Basic usage with theme color:**
```bash
python scripts/generate_cover.py --theme-color pink --output pink_cover.png
python scripts/generate_cover.py --theme-color blue --output blue_cover.png
python scripts/generate_cover.py --theme-color orange --output orange_cover.png
```

**More complex and vibrant:**
```bash
python scripts/generate_cover.py --theme-color purple --num-centers 8 --saturation 1.35 --output vibrant.png
```

**With flow distortion for organic look:**
```bash
python scripts/generate_cover.py --theme-color pink --distortion 0.05 --blur 60 --output flowing.png
```

**Set aspect ratio:**
```bash
python scripts/generate_cover.py --theme-color blue --ratio 16:9 --output widescreen.png
python scripts/generate_cover.py --theme-color orange --ratio 1:1 --output square.png
```

**Reproducible results:**
```bash
python scripts/generate_cover.py --seed 42 --theme-color pink --output reproducible.png
```

**Exclude white for darker, more saturated look:**
```bash
python scripts/generate_cover.py --theme-color purple --no-white --saturation 1.4 --output dark_bold.png
```

## How It Works

The generator creates complex, vibrant gradients through a multi-stage process:

1. **Generate Bold Color Palette**: Creates 4-5 vibrant colors based on the theme, including:
   - Base color (high saturation)
   - Complementary or analogous colors for contrast
   - Optional white/light color for highlights
   - All colors use high saturation (0.65-0.95) for bold appearance

2. **Create Complex Gradient**: Places 6-8 color centers strategically:
   - Some at corners and edges for structure
   - Others randomly placed for organic variation
   - Each center has varied influence radius and strength
   - Colors blend using smooth exponential falloff

3. **Add Flow Distortion**: Applies sine-wave-based distortion to create flowing, organic patterns (optional but recommended)

4. **Multi-Scale Blur**: Applies Gaussian blur at multiple scales for ultra-smooth transitions while preserving color intensity

5. **Enhance Vibrancy**: Boosts saturation (1.25x default), contrast (1.15x default), and brightness for bold, eye-catching results

## Parameters

All parameters are optional. The script works well with defaults.

### Basic Parameters
- `--output`, `-o`: Output filename (default: `cover.png`)
- `--width`, `-w`: Image width in pixels (default: `3840` for 4K)
- `--height`, `-ht`: Image height in pixels (default: `2160` for 4K)
- `--ratio`, `-r`: Aspect ratio like `16:9`, `4:3`, `1:1` (overrides height)
- `--seed`: Random seed for reproducible results

### Color Parameters
- `--theme-color`, `-c`: Base color as hex (`#FF5733`) or name (`blue`, `purple`, `pink`, `orange`, `green`, `cyan`, `red`, `yellow`, `magenta`)
- `--num-colors`: Number of colors in palette (default: `5`, range: 3-7)
- `--no-white`: Exclude white from palette for darker, more saturated look

### Complexity Parameters
- `--num-centers`: Number of color centers (default: `6`, range: 4-10)
  - More centers = more complex, varied gradients
  - Fewer centers = simpler, bolder transitions
- `--distortion`: Flow distortion strength 0-1 (default: `0.03`)
  - 0 = no distortion (pure gradients)
  - 0.03-0.05 = subtle organic flow
  - 0.1+ = strong wavy patterns

### Enhancement Parameters
- `--blur`: Base blur strength (default: `50`, range: 30-80)
  - Lower = sharper color transitions
  - Higher = smoother, more diffused gradients
- `--saturation`: Saturation boost (default: `1.25`, range: 1.0-1.5)
  - 1.0 = no boost
  - 1.25 = vibrant (recommended)
  - 1.4+ = extremely bold
- `--contrast`: Contrast boost (default: `1.15`, range: 1.0-1.3)

## Installation Requirements

The script requires these Python packages:

```bash
pip install numpy pillow scipy
```

If the user's environment doesn't have these packages, install them before running the script.

## Tips for Best Results

### Color Themes
- **Purple**: Creates pink-purple-blue palettes, often with complementary orange/yellow
- **Pink**: Generates vibrant pink-magenta palettes with green or cyan complements
- **Blue**: Produces blue-cyan palettes with orange/yellow contrasts
- **Orange**: Creates warm orange-red-yellow palettes with blue/cyan accents

### Achieving Different Styles

**Bold and vibrant (like OpenAI style):**
```bash
--num-centers 7 --saturation 1.3 --contrast 1.15 --distortion 0.03
```

**Soft and dreamy:**
```bash
--num-centers 4 --saturation 1.1 --blur 70 --distortion 0.02
```

**Complex and organic:**
```bash
--num-centers 9 --distortion 0.05 --blur 55
```

**High contrast:**
```bash
--saturation 1.4 --contrast 1.25 --no-white
```

### Experimentation
- Use `--seed` with same parameters to regenerate identical images
- Try different `--num-centers` values (6-8 works best for complexity)
- Adjust `--distortion` for more/less organic flow
- Increase `--saturation` for bolder colors
- The randomness creates unique results each time - generate multiple versions and pick the best!

## Workflow

When a user requests a cover image:

1. Determine requirements:
   - Theme color preference
   - Aspect ratio (16:9 for presentations, 1:1 for social media, etc.)
   - Desired vibe (bold/soft, simple/complex)
   - Output filename

2. Check dependencies:
   - Verify numpy, pillow, scipy are installed
   - Install if needed: `pip install numpy pillow scipy`

3. Run the script with appropriate parameters:
   - Start with defaults for first attempt
   - Adjust `--num-centers`, `--saturation`, `--distortion` based on feedback
   - Use `--seed` if user wants to reproduce a specific result

4. Show the generated image path to user

5. If variations needed:
   - Change `--seed` for different random variations
   - Adjust `--num-centers` for complexity
   - Modify `--saturation`/`--contrast` for intensity
   - Try `--no-white` for darker look
   - Increase `--distortion` for more organic flow

## Examples

**Vibrant purple gradient:**
```bash
python scripts/generate_cover.py --theme-color purple --num-centers 7 --saturation 1.3 --seed 123 --output purple_vibrant.png
```

**Soft pink gradient:**
```bash
python scripts/generate_cover.py --theme-color pink --num-centers 5 --blur 70 --saturation 1.15 --output pink_soft.png
```

**Bold orange with flow:**
```bash
python scripts/generate_cover.py --theme-color orange --num-centers 8 --distortion 0.05 --saturation 1.35 --output orange_bold.png
```

**Square format for social media:**
```bash
python scripts/generate_cover.py --theme-color blue --ratio 1:1 --width 2048 --output social_square.png
```
