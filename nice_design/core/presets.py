from .definitions import Texture, Layout, Palette, Typography

# Define a standard Solarized Palette (Primitives + Semantics)
SOLARIZED_PALETTE = Palette(
    name="solarized",
    mode="dark",
    colors={
        'base03': '#002b36',
        'base02': '#073642',
        'base01': '#586e75',
        'base00': '#657b83',
        'base0': '#839496',
        'base1': '#93a1a1',
        'base2': '#eee8d5',
        'base3': '#fdf6e3',
        'yellow': '#b58900',
        'orange': '#cb4b16',
        'red': '#dc322f',
        'magenta': '#d33682',
        'violet': '#6c71c4',
        'blue': '#268bd2',
        'cyan': '#2aa198',
        'green': '#859900',
    },
    
    # Accents
    primary="#268bd2",       # Blue
    on_primary="#fdf6e3",    # Base3
    secondary="#cb4b16",     # Orange
    on_secondary="#fdf6e3",  # Base3
    
    # Surfaces
    surface_base='#002b36',   # Base03
    surface_layer='#073642',  # Base02
    surface_overlay='#586e75', # Base01
    
    # Content
    content_main='#93a1a1',   # Base1
    content_muted='#839496',  # Base0
    content_subtle='#657b83', # Base00
    
    # Status
    success='#green',         # This was a placeholder in my head, should use '#859900'
    on_success='#002b36',     # Base03
    
    error='#dc322f',          # Red
    on_error='#fdf6e3',       # Base3
    
    warning='#b58900',        # Yellow
    on_warning='#002b36',     # Base03
    
    info='#268bd2',           # Blue
    on_info='#fdf6e3',        # Base3
    
    # Effects
    highlight="#fdf6e3",      # Base3
    shadow="#002b36"          # Base03
)

# Re-assigning Status colors correctly (fixing the '#green' slip above)
SOLARIZED_PALETTE.success = '#859900'

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

# LEGACY / COMPATIBILITY
SOLARIZED_SEMANTICS = SOLARIZED_PALETTE 
STANDARD_SHAPE = STANDARD_TEXTURE       
STANDARD_ANIMATION = STANDARD_LAYOUT    
