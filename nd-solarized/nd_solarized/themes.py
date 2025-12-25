from nice_design.core.definitions import Palette, Shape, Texture

SOLARIZED_DARK_PALETTE = Palette(
    name="solarized",
    mode="dark",
    primary="#268bd2",
    secondary="#cb4b16",
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

SOLARIZED_PREMIUM_SHAPE = Shape(
    name="solarized-premium",
    roundness=1.5,
    base_border=1
)

SOLARIZED_PREMIUM_TEXTURE = Texture(
    name="solarized-premium",
    opacity=0.85,
    texture_cls='texture-glossy',
    shadows=True,
    shadow_intensity=1.5
)
