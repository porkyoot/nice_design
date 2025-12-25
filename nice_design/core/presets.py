from .definitions import Skin, Palette, Typography

# Define a standard Solarized Dark Palette
SOLARIZED_PALETTE = Palette(
    name="solarized-dark",
    primary="#268bd2",
    secondary="#2aa198",
    accent="#d33682",
    surfaces={
        '1': '#002b36',
        '2': '#073642',
        '3': '#586e75'
    },
    status={
        'success': '#859900',
        'error': '#dc322f',
        'warning': '#b58900',
        'info': '#268bd2'
    }
)

# Define a standard Skin
STANDARD_SKIN = Skin(
    name="standard",
    roundness=1.0,
    opacity=1.0,
    texture_cls='texture-flat',
    shadows=True
)

# Define a standard Typography
STANDARD_TYPO = Typography(
    font_family="Inter, Roboto, sans-serif",
    mono_family="Fira Code, monospace",
    scale_ratio=1.25
)
