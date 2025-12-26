from .definitions import Shape, Texture, Layout, Animation, Palette, Typography, Semantics

# Define a standard Solarized Palette (Primitives)
SOLARIZED_PALETTE = Palette(
    name="solarized-dark",
    mode="dark",
    colors={
        'blue': '#268bd2',
        'cyan': '#2aa198',
        'green': '#859900',
        'yellow': '#b58900',
        'orange': '#cb4b16',
        'red': '#dc322f',
        'magenta': '#d33682',
        'purple': '#6c71c4',
    }
)

# Define standard Solarized Semantics (Roles)
SOLARIZED_SEMANTICS = Semantics(
    name="solarized-dark",
    mode="dark",
    
    # Accents
    primary="#268bd2",
    on_primary="#ffffff",
    secondary="#2aa198",
    on_secondary="#ffffff", 
    
    # Surfaces
    surface_base='#002b36',   # Base03
    surface_layer='#073642',  # Base02
    surface_overlay='#586e75', # Base01
    
    # Content
    content_main='#fdf6e3',   # Base3
    content_muted='#93a1a1',  # Base1
    content_subtle='#586e75', # Base01
    
    # Status
    success='#859900',
    on_success='#002b36',
    
    error='#dc322f',
    on_error='#ffffff',
    
    warning='#b58900',
    on_warning='#002b36',
    
    info='#268bd2',
    on_info='#ffffff',
    
    # Effects
    highlight="#ffffff",
    shadow="#000000"
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
    font_main="Inter, Roboto, sans-serif",
    font_secondary="Roboto, sans-serif",
    font_mono="Fira Code, monospace",
    scale_ratio=1.25
)
