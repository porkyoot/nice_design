from pathlib import Path
from nicegui import ui
from .core.engine import ThemeEngine
from .core.definitions import Theme
from .components.button import NDSButton
from .components.card import AppCard

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

def apply_theme(theme: Theme):
    """Applies the compiled theme to the UI via CSS variables."""
    css_vars = []
    
    # Apply Colors
    for name, value in theme.colors.items():
        css_vars.append(f"--nds-{name}: {value};")
    
    # Extra: Map primary to a readable contrast color if not provided
    if 'primary' in theme.colors:
        css_vars.append("--nds-on-primary: white;")
    
    # Apply Layout (Radii & Fonts)
    for name, value in theme.layout.items():
        if name.startswith('font-'):
            css_vars.append(f"--nds-{name}: {value};")
        else:
            css_vars.append(f"--nds-radius-{name}: {value};")
    
    style_content = ":root {\n  " + "\n  ".join(css_vars) + "\n}"
    ui.add_head_html(f"<style>{style_content}</style>")
    
    # Apply Global Classes to Body using ui.query
    if theme.classes:
        ui.query('body').classes(' '.join(theme.classes))

def setup(theme: Theme = None):
    """
    Convenience function to load the system and optionally apply a theme.
    We use ui.on('connect') or similar if we wanted per-client, 
    but for a simple global setup, we just call the loaders.
    """
    load_design_system()
    if theme:
        apply_theme(theme)