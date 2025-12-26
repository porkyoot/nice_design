from typing import Optional, Dict, Any
from pathlib import Path
from nicegui import ui, app
from .core.engine import ThemeEngine
from .core.registry import ThemeRegistry
from .core.definitions import Theme, CompiledTheme

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
from .components.atoms.select_button import select_button
from .components.molecules.theme_selector import theme_selector

# Singleton Engine & Registry
engine = ThemeEngine()
registry = ThemeRegistry()

def load_design_system():
    """Injects the library's CSS and discovered theme assets into the NiceGUI head."""
    # 1. Core library assets
    css_path = Path(__file__).parent / 'assets' / 'css'
    for css_file in ['global.css', 'textures.css', 'atoms.css']:
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
    # The registry now expects fonts to be served at /nd_themes/fonts/
    registry._font_css = [] # Clear and rebuild if needed
    for font_name in registry.list_typographies():
        # This is a bit of a hacky way to get the filename, 
        # but the registry could store it. 
        # Let's assume the registry has a way to get the font face CSS.
        pass
    
    font_css = registry.get_font_css()
    if font_css:
        ui.add_head_html(f"<style>{font_css}</style>")

def apply_theme(theme: CompiledTheme):
    """Applies the compiled theme to the UI via CSS variables."""
    css_vars = []
    
    # Apply Colors
    for name, value in theme.colors.items():
        css_vars.append(f"--nd-{name}: {value};")
    
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
    
    style_content = ":root {\n  " + "\n  ".join(css_vars) + "\n}\n\n"
    
    # Generate Utility Classes
    utils = []
    scales = ['xs', 'sm', 'md', 'lg', 'xl']
    
    # 1. Spacing Utilities
    for s in scales + ['0']:
        val = f"var(--nd-space-{s})" if s != '0' else "0px"
        utils.append(f".nd-p-{s} {{ padding: {val} !important; }}")
        utils.append(f".nd-pt-{s} {{ padding-top: {val} !important; }}")
        utils.append(f".nd-pb-{s} {{ padding-bottom: {val} !important; }}")
        utils.append(f".nd-pl-{s} {{ padding-left: {val} !important; }}")
        utils.append(f".nd-pr-{s} {{ padding-right: {val} !important; }}")
        utils.append(f".nd-px-{s} {{ padding-left: {val} !important; padding-right: {val} !important; }}")
        utils.append(f".nd-py-{s} {{ padding-top: {val} !important; padding-bottom: {val} !important; }}")
        utils.append(f".nd-m-{s} {{ margin: {val} !important; }}")
        utils.append(f".nd-mx-{s} {{ margin-left: {val} !important; margin-right: {val} !important; }}")
        utils.append(f".nd-my-{s} {{ margin-top: {val} !important; margin-bottom: {val} !important; }}")
        utils.append(f".nd-gap-{s} {{ gap: {val} !important; }}")

    # 2. Radius Utilities
    for s in ['sm', 'md', 'lg', 'full', 'none']:
        val = f"var(--nd-radius-{s})" if s != 'none' else "0px"
        utils.append(f".nd-rounded-{s} {{ border-radius: {val} !important; }}")

    # 3. Border Utilities
    for s in ['sm', 'md', 'lg', 'xl', 'none']:
        val = f"var(--nd-border-{s})" if s != 'none' else "0px"
        utils.append(f".nd-border-{s} {{ border-width: {val} !important; border-style: solid; }}")
        
    style_content += "\n".join(utils)
    ui.add_head_html(f"<style>{style_content}</style>")
    
    if theme.classes:
        ui.query('body').classes(' '.join(theme.classes))

def setup(theme: Optional[CompiledTheme] = None):
    """
    Convenience function to load the system and optionally apply a theme.
    """
    load_design_system()
    if theme:
        apply_theme(theme)