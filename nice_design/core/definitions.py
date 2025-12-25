from dataclasses import dataclass, field
from typing import Literal, Dict

@dataclass
class Palette:
    """Defines the raw colors."""
    name: str
    primary: str
    secondary: str
    colors: Dict[str, str]    # Named colors: blue, cyan, green, yellow, orange, red, magenta, purple
    surfaces: Dict[str, str]  # {'1': '#...', '2': '#...'}
    backgrounds: Dict[str, str]  # {'1': '#...', '2': '#...'} - solid backgrounds
    status: Dict[str, str]    # {'success': '...', 'error': '...'}
    shadow: str = "#000000"   # Default shadow color

@dataclass
class Skin:
    """Defines the physical look (Texture & Shape)."""
    name: str
    # 0.0 = Sharp, 1.0 = Standard, 2.0 = Round
    roundness: float = 1.0  
    # 0.0 = Transparent, 1.0 = Solid. Used for glassmorphism calculation.
    opacity: float = 1.0    
    # Base spacing unit in rem (standard is 1.0)
    base_space: float = 1.0
    # Base border width in px
    base_border: int = 1
    # Shadow intensity multiplier (0.0 to 1.0)
    shadow_intensity: float = 1.0
    # Base transition speed in seconds
    transition_speed: float = 0.3
    # CSS class to inject for texture (e.g., 'texture-glossy')
    texture_cls: str = 'texture-flat' 
    shadows: bool = True

@dataclass
class Typography:
    font_family: str
    mono_family: str
    scale_ratio: float = 1.25 # Ratio between h1, h2, etc.

@dataclass
class Theme:
    """The compiled result object used by components."""
    colors: Dict[str, str]  # Compiled CSS variables
    layout: Dict[str, str]  # Compiled Spacing/Radii
    classes: list[str]      # Global classes to apply to Body