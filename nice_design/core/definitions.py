from dataclasses import dataclass, field
from typing import Literal, Dict, List, Optional

@dataclass
class Palette:
    """
    Consolidated Palette category: Primitives + Semantic Roles.
    """
    name: str
    mode: Literal['dark', 'light']
    
    # Primitives (Rainbow) - e.g. {'blue': '#...', 'cyan': '#...'}
    colors: Dict[str, str] = field(default_factory=dict)
    
    # 1. Main Accents & Contrast
    primary: str = "#000000"
    on_primary: str = "#ffffff"
    secondary: str = "#ffffff"
    on_secondary: str = "#000000"
    
    # 2. Surfaces (Backgrounds)
    surface_base: str = "#000000"     # Deepest/App background
    surface_layer: str = "#111111"    # Cards/Floating surfaces
    surface_overlay: str = "#222222"  # Modals/Dropdowns
    
    # 3. Content (Foregrounds)
    content_main: str = "#ffffff"     # High contrast text
    content_muted: str = "#aaaaaa"    # Medium contrast
    content_subtle: str = "#666666"   # Low contrast/Disabled
    
    # 4. Semantic Status Colors & Contrast
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
class Texture:
    """
    Consolidated Texture category: Surface effects + Geometric shape.
    """
    name: str = "default"
    texture_cls: str = "-nd-t-flat" 
    
    # 1. Surface Effects
    opacity: float = 1.0           # 0.0 to 1.0 (glassmorphism)
    shadow_intensity: float = 1.0  # multiplier
    highlight_intensity: float = 1.0 # multiplier
    
    # 2. Geometric Shape
    roundness: float = 1.0         # 0.0 to 2.5 (multiplier)
    border_width: int = 1          # base border width in px
    
    # Flags
    shadows_enabled: bool = True

@dataclass
class Typography:
    """
    Consolidated Typography category.
    """
    name: str = "default"
    font_main: str = "sans-serif"
    font_secondary: str = "sans-serif"
    font_mono: str = "monospace"
    scale_ratio: float = 1.25 # Ratio between h1, h2, etc.
    title_transform: str = "none" # lowercase, none, capitalize, uppercase

@dataclass
class Layout:
    """
    Consolidated Layout category: Spacing + Animation.
    """
    name: str = "default"
    base_space: float = 1.0        # rem multiplier
    transition_speed: float = 0.3  # seconds

@dataclass
class Theme:
    """
    The central Theme object, strictly divided into 4 categorical pillars.
    """
    name: str
    palette: Palette
    texture: Texture = field(default_factory=Texture)
    typography: Typography = field(default_factory=Typography)
    layout: Layout = field(default_factory=Layout)
    prefix: str = "nd"

@dataclass
class CompiledTheme:
    colors: Dict[str, str]
    layout: Dict[str, str] # Note: This maps CSS variable suffixes to values
    classes: List[str]