from .definitions import Texture, Layout, Palette, Typography

# Define a standard Solarized Palette (Primitives + Semantics)
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
    },
    
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

# Define a standard Texture (includes Shape)
STANDARD_TEXTURE = Texture(
    name="standard",
    texture_cls='texture-flat',
    opacity=1.0,
    shadow_intensity=1.0,
    highlight_intensity=1.0,
    roundness=1.0,
    border_width=1,
    shadows_enabled=True
)

# Define a standard Layout (includes Animation)
STANDARD_LAYOUT = Layout(
    name="standard",
    base_space=1.0,
    transition_speed=0.3
)

# Define a standard Typography
STANDARD_TYPO = Typography(
    name="standard",
    font_main="Inter, Roboto, sans-serif",
    font_secondary="Roboto, sans-serif",
    font_mono="Fira Code, monospace",
    scale_ratio=1.25
)

# LEGACY / COMPATIBILITY (Optional, but useful if other parts of the system aren't fully migrated yet)
# We can keep these pointing to the same objects if we want to avoid breaking everything at once,
# but since we are refactoring, it's better to clean up.
# For now, I'll just keep the 4 major pillars.
SOLARIZED_SEMANTICS = SOLARIZED_PALETTE # They are now the same object
STANDARD_SHAPE = STANDARD_TEXTURE       # They are now the same object
STANDARD_ANIMATION = STANDARD_LAYOUT    # They are now the same object
