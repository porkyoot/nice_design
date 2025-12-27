from typing import Optional, Dict, Any
from pathlib import Path
from nicegui import ui, app
from .core.engine import ThemeEngine
from .core.registry import ThemeRegistry
from .core.definitions import Theme, CompiledTheme
from .core.manager import theme_manager

# Standard Exports
from .components.atoms.button import button
from .components.atoms.card import card
from .components.atoms.select import select
from .components.atoms.menu import menu, menu_item
from .components.atoms.icon import icon
from .components.atoms.theme_icons.palette_icon import palette_icon
from .components.atoms.theme_icons.theme_icon import theme_icon
from .components.atoms.theme_icons.texture_icon import texture_icon
from .components.atoms.theme_icons.shape_icon import shape_icon
from .components.atoms.theme_icons.border_icon import border_icon
from .components.atoms.theme_icons.shadow_highlight_icon import shadow_highlight_icon
from .components.atoms.slider import slider, split_slider, palette_slider
from .components.atoms.multi_button import multi_button
from .components.atoms.select_button import select_button
from .components.molecules.theme_selector import theme_selector

# Singleton Engine, Registry, and Manager
engine = ThemeEngine()
registry = ThemeRegistry()

def configure_defaults():
    """Configures global defaults via ThemeManager."""
    theme_manager.configure_defaults()

def load_design_system():
    """Injects the library's CSS and discovered theme assets into the NiceGUI head."""
    # 1. Core library assets
    css_path = Path(__file__).parent / 'assets' / 'css'
    for css_file in ['global.css', 'textures.css', 'atoms.css', 'quasar_overrides.css']:
        full_path = css_path / css_file
        if full_path.exists():
            with open(full_path) as f:
                ui.add_head_html(f"<style>{f.read()}</style>")
        
    # 2. MDI Icons
    ui.add_head_html('<link href="https://cdn.jsdelivr.net/npm/@mdi/font@7.2.96/css/materialdesignicons.min.css" rel="stylesheet">')

    # 3. Discovered Theme Assets (from /themes folder)
    themes_dir = Path(__file__).parent / "themes"
    
    # Auto-serve the themes directory for assets (fonts, images)
    if themes_dir.exists():
        app.add_static_files('/nd_themes', str(themes_dir))
        
    registry.discover_plugins()
    
    # Inject Texture CSS from themes/textures/*.css
    texture_css = registry.get_texture_css()
    if texture_css:
        ui.add_head_html(f"<style>{texture_css}</style>")
        
    # Inject Font CSS from themes/fonts/
    font_css = registry.get_font_css()
    if font_css:
        ui.add_head_html(f"<style>{font_css}</style>")

def apply_theme(theme: Theme):
    """Applies a theme using the ThemeManager."""
    theme_manager.apply_theme(theme)

def setup(theme: Optional[Theme] = None):
    """
    Initializes the design system and optionally applies a theme.
    """
    # 1. Load static assets & discover themes
    load_design_system()
    
    # 2. Configure component defaults
    theme_manager.configure_defaults()
    
    # 3. Apply initial theme if provided
    if theme:
        theme_manager.apply_theme(theme)