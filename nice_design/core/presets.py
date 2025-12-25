from .definitions import Shape, Texture, Layout, Animation, Palette, Typography

# Define a standard Solarized Dark Palette
SOLARIZED_PALETTE = Palette(
    name="solarized-dark",
    mode="dark",
    primary="#268bd2",
    secondary="#2aa198",
    colors={
        'blue': '#268bd2',
        'cyan': '#2aa198',
        'green': '#859900',
        'yellow': '#b58900',
        'orange': '#cb4b16',
        'red': '#dc322f',
        'magenta': '#d33682',
        'purple': '#6c71c4',
    },
    foregrounds={
        '1': '#fdf6e3',  # Base3 - emphasized content
        '2': '#eee8d5',  # Base2 - body content
        '3': '#93a1a1',  # Base1 - secondary content
    },
    backgrounds={
        '1': '#002b36',  # Base03 - darkest background
        '2': '#073642',  # Base02 - dark background
        '3': '#586e75',  # Base01 - medium (comments)
    },
    status={
        'success': '#859900',
        'error': '#dc322f',
        'warning': '#b58900',
        'info': '#268bd2',
        'debug': '#586e75',  # Base01 - grey for debug/logging
    }
)

# Define a standard Shape
STANDARD_SHAPE = Shape(
    name="standard",
    roundness=1.0,
    base_border=1
)

# Define a standard Texture
STANDARD_TEXTURE = Texture(
    name="standard",
    opacity=1.0,
    shadow_intensity=1.0,
    texture_cls='texture-flat',
    shadows=True
)

# Define a standard Layout (user-adjustable)
STANDARD_LAYOUT = Layout(
    name="standard",
    base_space=1.0
)

# Define a standard Animation (user-adjustable)
STANDARD_ANIMATION = Animation(
    name="standard",
    transition_speed=0.3
)

# Define a standard Typography
STANDARD_TYPO = Typography(
    font_family="Inter, Roboto, sans-serif",
    mono_family="Fira Code, monospace",
    scale_ratio=1.25
)
