from dataclasses import dataclass, field
from typing import Literal, Dict, List

@dataclass
class Palette:
    """
    The core color data. 
    Separates raw ordered scales from semantic roles.
    """
    name: str
    mode: Literal['dark', 'light']
    
    # The Rainbow (Hue Order) for palette pickers
    # e.g. {'blue': '#...', 'cyan': '#...'}
    colors: Dict[str, str]

@dataclass
class Semantics:
    """
    Functional roles mapped from the palette.
    """
    name: str
    mode: Literal['dark', 'light']
    
    # 1. Main Accents & Contrast
    primary: str = "#000000"
    on_primary: str = "#ffffff"
    secondary: str = "#ffffff"
    on_secondary: str = "#000000"
    
    # 2. Surfaces (Backgrounds)
    # Replaces 'backgrounds' list
    surface_base: str = "#000000"     # Deepest/App background
    surface_layer: str = "#111111"    # Cards/Floating surfaces
    surface_overlay: str = "#222222"  # Modals/Dropdowns
    
    # 3. Content (Foregrounds)
    # Replaces 'foregrounds' list
    content_main: str = "#ffffff"     # High contrast text
    content_muted: str = "#aaaaaa"    # Medium contrast
    content_subtle: str = "#666666"   # Low contrast/Disabled
    
    # 4. Semantic Status Colors & Contrast
    # Replaces 'status' dict
    success: str = "#00ff00"
    on_success: str = "#000000"
    
    error: str = "#ff0000"
    on_error: str = "#ffffff"
    
    warning: str = "#ffff00"
    on_warning: str = "#000000"
    
    info: str = "#0000ff"
    on_info: str = "#ffffff"

    # 5. Effects
    highlight: str = "#ffffff"  # For glass/glossy effects
    shadow: str = "#000000"      # Base shadow color

@dataclass
class Shape:
    """Defines geometric properties."""
    name: str = "default"
    # 0.0 = Sharp, 1.0 = Standard, 2.0 = Round
    roundness: float = 1.0  
    # Base border width in px
    base_border: int = 1

@dataclass
class Texture:
    """Defines visual effects and surface properties."""
    name: str = "default"
    # 0.0 = Transparent, 1.0 = Solid. Used for glassmorphism calculation.
    opacity: float = 1.0    
    # Shadow intensity multiplier (0.0 to 1.0)
    shadow_intensity: float = 1.0
    # CSS class to inject for texture (e.g., 'texture-glossy')
    texture_cls: str = '-nd-t-flat' 
    shadows: bool = True

@dataclass
class Layout:
    """Defines spacing and layout properties (user-adjustable)."""
    name: str = "default"
    # Base spacing unit in rem (standard is 1.0)
    base_space: float = 1.0

@dataclass
class Typography:
    name: str = "default"
    font_main: str = "sans-serif"
    font_secondary: str = "sans-serif"
    font_mono: str = "monospace"
    scale_ratio: float = 1.25 # Ratio between h1, h2, etc.

@dataclass
class Animation:
    name: str = "default"
    transition_speed: float = 0.3 # seconds

@dataclass
class Theme:
    palette: Palette
    semantics: Semantics = field(default_factory=Semantics)
    texture: Texture = field(default_factory=Texture)
    shape: Shape = field(default_factory=Shape)
    layout: Layout = field(default_factory=Layout)
    typography: Typography = field(default_factory=Typography)
    animation: Animation = field(default_factory=Animation)
    prefix: str = "nd"

@dataclass
class CompiledTheme:
    colors: Dict[str, str]
    layout: Dict[str, str] # Note: This maps CSS variable suffixes to values
    classes: List[str]