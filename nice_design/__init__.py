from pathlib import Path
from nicegui import ui
from .core.engine import ThemeEngine
from .core.definitions import Theme, CompiledTheme
from .components.atoms.button import button
from .components.atoms.card import card
from .components.atoms.select import select
from .components.atoms.menu import menu, menu_item
from .components.atoms.icon import icon
from .components.atoms.palette_icon import palette_icon
from .components.atoms.theme_icon import theme_icon
from .components.atoms.texture_icon import texture_icon
from .components.atoms.shape_icon import shape_icon
from .components.molecules.theme_config import ThemeConfig

def load_design_system():
    """Injects the library's CSS into the NiceGUI head."""
    # Locate CSS relative to this python file
    css_path = Path(__file__).parent / 'assets' / 'css'
    
    # 1. Load Global CSS
    with open(css_path / 'global.css') as f:
        ui.add_head_html(f"<style>{f.read()}</style>")
        
    # 2. Load Textures
    with open(css_path / 'textures.css') as f:
        ui.add_head_html(f"<style>{f.read()}</style>")
        
    # 3. Load Atoms
    with open(css_path / 'atoms.css') as f:
        ui.add_head_html(f"<style>{f.read()}</style>")
        
    # 4. Load MDI Icons
    ui.add_head_html('<link href="https://cdn.jsdelivr.net/npm/@mdi/font@7.2.96/css/materialdesignicons.min.css" rel="stylesheet">')

def apply_theme(theme: CompiledTheme):
    """Applies the compiled theme to the UI via CSS variables."""
    css_vars = []
    
    # Apply Colors
    for name, value in theme.colors.items():
        css_vars.append(f"--nd-{name}: {value};")
    
    # Extra: Map primary to a readable contrast color if not provided
    if 'primary' in theme.colors:
        css_vars.append("--nd-on-primary: white;")
    
    # Apply Layout (Radii, Fonts, Spacing, Borders, Shadows, Transition)
    for name, value in theme.layout.items():
        if name.startswith('font-'):
            css_vars.append(f"--nd-{name}: {value};")
        elif name.startswith('space-'):
            css_vars.append(f"--nd-{name}: {value};")
        elif name.startswith('border-'):
            css_vars.append(f"--nd-{name}: {value};")
        elif name.startswith('shadow-'):
            css_vars.append(f"--nd-{name}: {value};")
        elif name == 'transition-speed':
            css_vars.append(f"--nd-transition-speed: {value};")
        else:
            css_vars.append(f"--nd-radius-{name}: {value};")
    
    style_content = ":root {\n  " + "\n  ".join(css_vars) + "\n}"
    ui.add_head_html(f"<style>{style_content}</style>")
    
    # Apply Global Classes to Body using ui.query
    if theme.classes:
        ui.query('body').classes(' '.join(theme.classes))

def setup(theme: Theme = None):
    """
    Convenience function to load the system and optionally apply a theme.
    """
    load_design_system()
    if theme:
        apply_theme(theme)