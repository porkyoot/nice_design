from nice_design.core.definitions import Palette, Skin

SOLARIZED_DARK_PALETTE = Palette(
    name="solarized-dark-ext",
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

SOLARIZED_PREMIUM_SKIN = Skin(
    name="solarized-premium",
    roundness=1.5,
    opacity=0.85,
    texture_cls='texture-glossy',
    shadows=True,
    shadow_intensity=1.5,
    transition_speed=0.5
)
