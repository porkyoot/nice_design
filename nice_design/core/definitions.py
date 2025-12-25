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
    
    # 1. Main Accents
    primary: str = "#000000"
    secondary: str = "#ffffff"
    
    # 2. Tonal Scales (Ordered by intensity)
    # Backgrounds: 0=Deepest/Base, 1=Surface, 2=Overlay, etc.
    backgrounds: List[str] = field(default_factory=list)
    
    # Foregrounds: 0=Strongest, 1=Normal, 2=Muted, 3=Faint
    foregrounds: List[str] = field(default_factory=list)
    
    # 3. Semantic Status Colors
    # e.g. {'success': '#...', 'error': '#...', 'warning': '#...'}
    status: Dict[str, str] = field(default_factory=dict)
    
    # 4. Effects
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
    texture_cls: str = 'texture-flat' 
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