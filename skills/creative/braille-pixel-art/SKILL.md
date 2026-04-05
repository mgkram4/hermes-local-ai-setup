---
name: braille-pixel-art
description: Create stunning terminal pixel art using Unicode braille patterns (U+2800-U+28FF). Achieve 8x resolution compared to traditional ASCII art with smooth curves, detailed portraits, and Rich color markup.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ASCII-Art, Braille, Terminal-Art, Pixel-Art, Unicode, Rich-Markup, TUI]
    related_skills: [ascii-video, popular-web-designs]
---

# Braille Pixel Art — High-Resolution Terminal Art

Create beautiful, high-resolution terminal art using Unicode braille patterns. This technique achieves **8x the resolution** of traditional ASCII art by using braille characters (U+2800-U+28FF), where each character cell contains 8 individually controllable "pixels" (dots).

## Why Braille Art?

| Technique | Resolution per Cell | Best For |
|-----------|---------------------|----------|
| Traditional ASCII (`#`, `@`, `.`) | 1 pixel | Simple shapes, text art |
| Block Elements (`█`, `▄`, `▀`) | 2-4 pixels | Bars, basic graphics |
| **Braille Patterns** | **8 pixels** | Portraits, smooth curves, detailed art |

Braille art is the **gold standard** for terminal pixel art because:
- **8 dots per character** (2 columns × 4 rows) = 8x resolution
- **256 unique patterns** (U+2800 to U+28FF) for precise control
- **Smooth curves and gradients** impossible with traditional ASCII
- **Rich color markup** for themed, colorful displays

## Braille Character Grid

Each braille character is a 2×4 grid of dots:

```
┌───┬───┐
│ 1 │ 4 │  ← Row 0
├───┼───┤
│ 2 │ 5 │  ← Row 1
├───┼───┤
│ 3 │ 6 │  ← Row 2
├───┼───┤
│ 7 │ 8 │  ← Row 3
└───┴───┘
  L   R
```

The Unicode codepoint is calculated as: `U+2800 + (dot_bits)`

Where dot bits are:
- Dot 1 = 0x01, Dot 2 = 0x02, Dot 3 = 0x04, Dot 7 = 0x40 (left column)
- Dot 4 = 0x08, Dot 5 = 0x10, Dot 6 = 0x20, Dot 8 = 0x80 (right column)

### Common Braille Patterns

| Pattern | Unicode | Hex | Description |
|---------|---------|-----|-------------|
| ⠀ | U+2800 | 0x00 | Empty (all dots off) |
| ⠁ | U+2801 | 0x01 | Dot 1 only |
| ⠃ | U+2803 | 0x03 | Dots 1,2 |
| ⠇ | U+2807 | 0x07 | Dots 1,2,3 (left column top 3) |
| ⡇ | U+2847 | 0x47 | Full left column |
| ⠸ | U+2838 | 0x38 | Dots 4,5,6 (right column top 3) |
| ⢸ | U+28B8 | 0xB8 | Full right column |
| ⣿ | U+28FF | 0xFF | All 8 dots (full block) |
| ⣀ | U+28C0 | 0xC0 | Bottom row only |
| ⠛ | U+281B | 0x1B | Top 4 dots |
| ⣤ | U+28E4 | 0xE4 | Bottom 6 dots |

## Creating Braille Art

### Method 1: Manual Character Selection

For small icons or symbols, manually select braille characters:

```
[#FFD700]⠀⠀⠀⢀⣤⣤⣤⣤⡀⠀⠀⠀[/]
[#FFD700]⠀⠀⢀⣾⣿⚡⣿⣿⚡⣷⡀⠀⠀[/]
[#FFD700]⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀[/]
```

### Method 2: Python Braille Renderer

```python
def pixel_to_braille(pixels: list[list[bool]], width: int, height: int) -> str:
    """Convert a 2D pixel grid to braille characters.
    
    Args:
        pixels: 2D list of booleans (True = dot on)
        width: Width in pixels (will be divided by 2 for braille)
        height: Height in pixels (will be divided by 4 for braille)
    
    Returns:
        String of braille characters
    """
    result = []
    
    # Process in 2x4 blocks
    for y in range(0, height, 4):
        row = []
        for x in range(0, width, 2):
            # Calculate braille character for this 2x4 block
            char_code = 0x2800
            
            # Dot positions: (x_offset, y_offset, bit_value)
            dots = [
                (0, 0, 0x01), (1, 0, 0x08),  # Row 0
                (0, 1, 0x02), (1, 1, 0x10),  # Row 1
                (0, 2, 0x04), (1, 2, 0x20),  # Row 2
                (0, 3, 0x40), (1, 3, 0x80),  # Row 3
            ]
            
            for dx, dy, bit in dots:
                px, py = x + dx, y + dy
                if py < height and px < width and pixels[py][px]:
                    char_code |= bit
            
            row.append(chr(char_code))
        result.append(''.join(row))
    
    return '\n'.join(result)
```

### Method 3: Image to Braille Converter

```python
from PIL import Image

def image_to_braille(image_path: str, width: int = 60, threshold: int = 128) -> str:
    """Convert an image to braille art.
    
    Args:
        image_path: Path to image file
        width: Output width in characters (actual pixel width = width * 2)
        threshold: Brightness threshold (0-255) for dot activation
    
    Returns:
        Braille art string
    """
    img = Image.open(image_path).convert('L')  # Grayscale
    
    # Calculate dimensions (2 pixels per braille column, 4 per row)
    pixel_width = width * 2
    aspect = img.height / img.width
    pixel_height = int(pixel_width * aspect)
    # Round to multiple of 4 for clean braille rows
    pixel_height = (pixel_height // 4) * 4
    
    img = img.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
    
    pixels = [[img.getpixel((x, y)) < threshold 
               for x in range(pixel_width)] 
              for y in range(pixel_height)]
    
    return pixel_to_braille(pixels, pixel_width, pixel_height)
```

## Rich Color Markup

Combine braille art with Rich markup for stunning colored displays:

### Color Syntax

```
[#RRGGBB]braille text[/]           # Hex color
[bold #FFD700]text[/]              # Bold + color
[dim #555577]text[/]               # Dimmed color
[italic dim #555577]text[/]        # Italic + dim
```

### Gradient Techniques

Create depth with color gradients from top to bottom:

```
[#FFD700]⠀⠀⠀⠀⠀⢀⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀[/]     ← Brightest (highlight)
[#C9A227]⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀[/]     ← Mid-bright
[#8B7500]⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀[/]     ← Mid-dark
[#555577]⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀[/]     ← Darkest (shadow)
```

### Character Portraits Template

A 16-line portrait template with frame:

```yaml
pixel_art: |
  [dim #2A2A50]┌────────────────────────┐[/]
  [dim #2A2A50]│[/]  [#COLOR1]⠀⠀⠀⠀⠀⢀⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR2]⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR3]⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR4]⠀⠀⠀⢿⣿◉⣿⣿⣿◉⣿⡿⠀⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR5]⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR6]⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR7]⠀⠀⠀⢀⣴⣿⣿⚕⣿⣿⣦⡀⠀⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR8]⠀⠀⣰⣿⣿⡿⠛⠛⠛⢿⣿⣿⣆⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [#COLOR9]⠀⢠⣿⣿⠃⠀⠀⠀⠀⠀⠘⣿⣿⡄⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [dim #COLOR10]⠀⣿⣿⡇⠀⣿⣿⣿⣿⠀⢸⣿⣿⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [dim #COLOR11]⠀⠹⣿⣷⣄⠀⠀⠀⠀⣠⣾⣿⠏⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [dim #COLOR12]⠀⠀⠈⠻⣿⣿⣶⣶⣿⣿⠟⠁⠀⠀[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]    [bold #COLOR1]⚕ NAME ⚕[/]    [dim #2A2A50]│[/]
  [dim #2A2A50]│[/]  [dim #555577]Title or Description[/]  [dim #2A2A50]│[/]
  [dim #2A2A50]└────────────────────────┘[/]
```

## Design Principles

### 1. Start with Silhouette
Draw the outline first using full blocks (`⣿`) and empty spaces (`⠀`).

### 2. Add Detail with Partial Fills
Use partial braille characters for edges and curves:
- `⡇` / `⢸` for vertical edges
- `⣀` / `⠛` for horizontal edges
- `⠁`, `⠈`, `⡀`, `⢀` for single-dot details

### 3. Use Iconic Symbols
Embed Unicode symbols for recognizable features:
- `◉` or `●` for eyes
- `⚡` for lightning/energy
- `⚕` for medical/Hermes caduceus
- `🔱` for trident
- `☀` for sun
- `🌊` for water

### 4. Frame Your Art
Use box-drawing characters for professional framing:
- `┌`, `┐`, `└`, `┘` for corners
- `─`, `│` for edges
- `╔`, `╗`, `╚`, `╝` for double-line frames

### 5. Color Theming
Choose a color palette that matches the subject:
- **Gold theme**: `#FFD700`, `#C9A227`, `#8B7500` (Hermes)
- **Blue theme**: `#1E90FF`, `#87CEEB`, `#4169E1` (Poseidon)
- **Red theme**: `#DC143C`, `#8B0000`, `#CD5C5C` (Ares)
- **Purple theme**: `#9B59B6`, `#DDA0DD`, `#663399` (Hades)
- **Green theme**: `#32CD32`, `#90EE90`, `#228B22` (Artemis)

## Example: Creating a God Portrait

### Step 1: Define the Color Palette

```yaml
colors:
  highlight: "#FFD700"    # Brightest areas
  primary: "#C9A227"      # Main color
  secondary: "#8B7500"    # Darker areas
  shadow: "#555577"       # Shadows
  frame: "#2A2A50"        # Frame color
```

### Step 2: Build the Portrait Layer by Layer

```
# Layer 1: Frame
[dim #2A2A50]┌────────────────────────┐[/]
[dim #2A2A50]│                        │[/]
...
[dim #2A2A50]└────────────────────────┘[/]

# Layer 2: Head/Hair (top, brightest)
[#555577]⠀⠀⠀⠀⠀⢀⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀[/]

# Layer 3: Face (mid-section, primary colors)
[#FFD700]⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀[/]

# Layer 4: Eyes (using special symbols)
[#FFEC8B]⠀⠀⠀⢿⣿[/][bold #FFD700]◉[/][#FFEC8B]⣿⣿⣿[/][bold #FFD700]◉[/][#FFEC8B]⣿⡿⠀⠀⠀[/]

# Layer 5: Body (lower section, darker)
[dim #555577]⠀⣿⣿⡇⠀⣿⣿⣿⣿⠀⢸⣿⣿⠀[/]

# Layer 6: Name plate
[bold #FFD700]⚕ HERMES ⚕[/]
```

### Step 3: Add Iconic Elements

Insert recognizable symbols that represent the character:
- Hermes: `⚕` (caduceus), `⚡` (speed)
- Zeus: `⚡` (lightning), `☁` (clouds)
- Poseidon: `🔱` (trident), `🌊` (waves)
- Apollo: `☀` (sun), `🎵` (music)
- Artemis: `🏹` (bow), `🌙` (moon)

## Testing Your Art

### In Python with Rich

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

art = """[#FFD700]⠀⠀⠀⠀⠀⢀⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀[/]
[#C9A227]⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀[/]
[#FFD700]⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀[/]"""

console.print(Panel(art, title="Braille Art Test"))
```

### In Terminal

```bash
echo -e "\e[38;2;255;215;0m⠀⠀⠀⠀⠀⢀⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀\e[0m"
```

## Resources

- **Unicode Braille Chart**: https://www.unicode.org/charts/PDF/U2800.pdf
- **Rich Library**: https://rich.readthedocs.io/
- **Textual TUI**: https://textual.textualize.io/

## Tips for Hermes Agents

1. **Start simple**: Begin with 8-10 line portraits before attempting larger pieces
2. **Test incrementally**: Render after each major change to catch issues early
3. **Use consistent spacing**: Braille characters are fixed-width; maintain alignment
4. **Layer colors logically**: Highlight → Primary → Secondary → Shadow (top to bottom)
5. **Include fallbacks**: Some terminals may not render all braille characters correctly
6. **Document your palette**: Include color codes in comments for future editing
