#!/usr/bin/env python3
"""
OpenAI-style cover image generator
Generates vibrant, complex gradient covers with bold colors and flowing transitions
"""

import numpy as np
from PIL import Image, ImageFilter
import argparse
import random
import colorsys
from scipy.ndimage import gaussian_filter


def generate_bold_color_palette(num_colors=5, base_hue=None, include_white=True):
    """
    Generate bold, vibrant color palette with high saturation
    
    Args:
        num_colors: Number of colors in palette
        base_hue: Base hue (0-1), if None will be random
        include_white: Whether to include white/very light colors
    
    Returns:
        List of (r, g, b) tuples
    """
    colors = []
    
    # Add white or very light color for highlights
    if include_white:
        colors.append((255, 255, 255))
        num_colors -= 1
    
    if base_hue is None:
        base_hue = random.random()
    
    for i in range(num_colors):
        if i == 0:
            # Base color - high saturation
            hue = base_hue
            saturation = random.uniform(0.75, 0.95)
            lightness = random.uniform(0.55, 0.75)
        elif i == 1:
            # Complementary or analogous color
            if random.random() > 0.5:
                # Complementary (opposite on color wheel)
                hue = (base_hue + 0.5) % 1.0
            else:
                # Analogous (nearby on color wheel)
                hue = (base_hue + random.uniform(0.15, 0.25)) % 1.0
            saturation = random.uniform(0.7, 0.95)
            lightness = random.uniform(0.5, 0.7)
        else:
            # Additional colors - varied
            hue = (base_hue + random.uniform(-0.3, 0.3)) % 1.0
            saturation = random.uniform(0.65, 0.95)
            lightness = random.uniform(0.5, 0.75)
        
        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append((int(r * 255), int(g * 255), int(b * 255)))
    
    return colors


def create_complex_gradient(width, height, colors, num_centers=6):
    """
    Create complex gradient with multiple color centers and smooth blending
    
    Args:
        width: Image width
        height: Image height
        colors: List of (r, g, b) color tuples
        num_centers: Number of color centers
    
    Returns:
        numpy array (height, width, 3)
    """
    # Initialize RGB channels
    img_r = np.zeros((height, width), dtype=np.float32)
    img_g = np.zeros((height, width), dtype=np.float32)
    img_b = np.zeros((height, width), dtype=np.float32)
    weights = np.zeros((height, width), dtype=np.float32)
    
    # Create coordinate grids
    xx, yy = np.meshgrid(np.arange(width), np.arange(height))
    
    # Generate color centers with strategic placement
    centers = []
    
    # Place some centers at corners and edges
    edge_positions = [
        (0, 0), (width, 0), (0, height), (width, height),  # Corners
        (width//2, 0), (width, height//2), (width//2, height), (0, height//2)  # Edge midpoints
    ]
    
    for i in range(num_centers):
        if i < len(edge_positions) and random.random() > 0.3:
            # Use edge position with some randomness
            base_x, base_y = edge_positions[i % len(edge_positions)]
            x = base_x + random.uniform(-width*0.2, width*0.2)
            y = base_y + random.uniform(-height*0.2, height*0.2)
        else:
            # Random position
            x = random.uniform(-width * 0.2, width * 1.2)
            y = random.uniform(-height * 0.2, height * 1.2)
        
        # Pick color
        color = colors[i % len(colors)]
        
        # Varied influence radius
        radius = random.uniform(min(width, height) * 0.4, max(width, height) * 0.9)
        
        # Varied strength
        strength = random.uniform(0.7, 1.3)
        
        centers.append((x, y, color, radius, strength))
    
    # Blend colors from all centers
    for cx, cy, color, radius, strength in centers:
        # Calculate distance from center
        dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
        
        # Create smooth falloff with varied exponent
        exponent = random.uniform(1.5, 2.5)
        weight = np.exp(-(dist / radius) ** exponent) * strength
        
        # Add weighted color
        img_r += color[0] * weight
        img_g += color[1] * weight
        img_b += color[2] * weight
        weights += weight
    
    # Normalize by total weights
    weights = np.maximum(weights, 1e-6)
    img_r /= weights
    img_g /= weights
    img_b /= weights
    
    # Stack channels
    img_array = np.stack([img_r, img_g, img_b], axis=2)
    
    # Clip to valid range
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    
    return img_array


def add_flow_distortion(img_array, strength=0.05):
    """
    Add flowing distortion to create organic, complex patterns
    
    Args:
        img_array: numpy array (height, width, 3)
        strength: Distortion strength (0-1)
    
    Returns:
        Distorted numpy array
    """
    height, width = img_array.shape[:2]
    
    # Create flow field using sine waves
    x = np.linspace(0, 4 * np.pi, width)
    y = np.linspace(0, 4 * np.pi, height)
    xx, yy = np.meshgrid(x, y)
    
    # Create distortion offsets
    offset_x = np.sin(yy + np.cos(xx)) * strength * width
    offset_y = np.cos(xx + np.sin(yy)) * strength * height
    
    # Create new coordinate grids
    new_x = np.clip(np.arange(width)[np.newaxis, :] + offset_x, 0, width - 1).astype(int)
    new_y = np.clip(np.arange(height)[:, np.newaxis] + offset_y, 0, height - 1).astype(int)
    
    # Apply distortion
    distorted = np.zeros_like(img_array)
    for i in range(3):
        distorted[:, :, i] = img_array[new_y, new_x, i]
    
    return distorted


def apply_multi_scale_blur(img_array, base_sigma=40, num_scales=3):
    """
    Apply multi-scale blur for ultra-smooth gradients
    
    Args:
        img_array: numpy array (height, width, 3)
        base_sigma: Base blur strength
        num_scales: Number of blur scales
    
    Returns:
        Blurred numpy array
    """
    result = img_array.astype(np.float32)
    
    for scale in range(num_scales):
        sigma = base_sigma * (1.5 ** scale)
        blurred = np.zeros_like(result)
        
        for i in range(3):
            blurred[:, :, i] = gaussian_filter(result[:, :, i], sigma=sigma)
        
        # Blend with original
        alpha = 0.3 / (scale + 1)
        result = result * (1 - alpha) + blurred * alpha
    
    return np.clip(result, 0, 255).astype(np.uint8)


def enhance_vibrancy(img_array, saturation_boost=1.25, contrast_boost=1.15):
    """
    Enhance color vibrancy and contrast for bold look
    
    Args:
        img_array: numpy array (height, width, 3)
        saturation_boost: Saturation multiplier
        contrast_boost: Contrast multiplier
    
    Returns:
        Enhanced numpy array
    """
    img = Image.fromarray(img_array)
    
    from PIL import ImageEnhance
    
    # Boost saturation significantly
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation_boost)
    
    # Boost contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast_boost)
    
    # Slight brightness boost
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.03)
    
    return np.array(img)


def parse_color(color_str):
    """Parse color from hex string or color name"""
    if color_str.startswith('#'):
        color_str = color_str.lstrip('#')
        r, g, b = tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        return h
    else:
        color_map = {
            'red': 0.0,
            'orange': 0.08,
            'yellow': 0.16,
            'green': 0.33,
            'cyan': 0.5,
            'blue': 0.6,
            'purple': 0.75,
            'pink': 0.9,
            'magenta': 0.83
        }
        return color_map.get(color_str.lower(), random.random())


def main():
    parser = argparse.ArgumentParser(description='Generate bold OpenAI-style cover images')
    parser.add_argument('--output', '-o', default='cover.png', 
                       help='Output filename (default: cover.png)')
    parser.add_argument('--width', '-w', type=int, default=3840,
                       help='Image width (default: 3840 for 4K)')
    parser.add_argument('--height', '-ht', type=int, default=2160,
                       help='Image height (default: 2160 for 4K)')
    parser.add_argument('--ratio', '-r', type=str,
                       help='Aspect ratio (e.g., 16:9, 4:3, 1:1). Overrides height.')
    parser.add_argument('--theme-color', '-c', type=str,
                       help='Base theme color (hex like #FF5733 or name like blue, purple, pink)')
    parser.add_argument('--num-colors', type=int, default=5,
                       help='Number of colors in palette (default: 5)')
    parser.add_argument('--num-centers', type=int, default=6,
                       help='Number of color centers (default: 6)')
    parser.add_argument('--distortion', type=float, default=0.03,
                       help='Flow distortion strength 0-1 (default: 0.03)')
    parser.add_argument('--blur', type=float, default=50,
                       help='Base blur strength (default: 50)')
    parser.add_argument('--saturation', type=float, default=1.25,
                       help='Saturation boost (default: 1.25)')
    parser.add_argument('--contrast', type=float, default=1.15,
                       help='Contrast boost (default: 1.15)')
    parser.add_argument('--no-white', action='store_true',
                       help='Exclude white from color palette')
    parser.add_argument('--seed', type=int,
                       help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
    
    # Calculate dimensions
    width = args.width
    height = args.height
    
    if args.ratio:
        try:
            w_ratio, h_ratio = map(int, args.ratio.split(':'))
            height = int(width * h_ratio / w_ratio)
        except:
            print(f"Warning: Invalid ratio format '{args.ratio}', using default height")
    
    print(f"Generating {width}x{height} bold gradient cover...")
    
    # Parse theme color
    base_hue = None
    if args.theme_color:
        base_hue = parse_color(args.theme_color)
        print(f"Using theme color: {args.theme_color}")
    
    # Generate bold color palette
    print(f"Generating bold color palette with {args.num_colors} colors...")
    colors = generate_bold_color_palette(num_colors=args.num_colors, base_hue=base_hue, 
                                         include_white=not args.no_white)
    print(f"  Colors: {colors}")
    
    # Create complex gradient
    print(f"Creating complex gradient with {args.num_centers} color centers...")
    img_array = create_complex_gradient(width, height, colors, num_centers=args.num_centers)
    
    # Add flow distortion
    if args.distortion > 0:
        print(f"Adding flow distortion (strength={args.distortion})...")
        img_array = add_flow_distortion(img_array, strength=args.distortion)
    
    # Apply multi-scale blur
    print(f"Applying multi-scale blur (base sigma={args.blur})...")
    img_array = apply_multi_scale_blur(img_array, base_sigma=args.blur)
    
    # Enhance vibrancy
    print("Enhancing vibrancy and contrast...")
    img_array = enhance_vibrancy(img_array, saturation_boost=args.saturation, 
                                 contrast_boost=args.contrast)
    
    # Convert to PIL Image
    image = Image.fromarray(img_array)
    
    # Save image
    print("Saving image...")
    image.save(args.output, 'PNG', quality=95)
    print(f"[OK] Bold cover image saved to: {args.output}")
    print(f"  Dimensions: {width}x{height}")
    print(f"  Colors: {len(colors)}")
    print(f"  Centers: {args.num_centers}")


if __name__ == '__main__':
    main()
