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
from .components.atoms.multi_button import multi_button
from .components.atoms.select_button import select_button
from .components.molecules.theme_selector import theme_selector

# Singleton Engine & Registry
engine = ThemeEngine()
registry = ThemeRegistry()

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
    # The registry discovers fonts and generates @font-face CSS during discover_plugins()
    font_css = registry.get_font_css()
    if font_css:
        ui.add_head_html(f"<style>{font_css}</style>")

def apply_theme(theme: CompiledTheme, initial: bool = False):
    """Applies the compiled theme to the UI via CSS variables.
    
    Args:
        theme: The compiled theme to apply
        initial: If True, uses static CSS injection (for initial setup before event loop starts).
                 If False, uses JavaScript to update CSS variables dynamically.
    """
    # Build CSS variables
    css_vars = {}
    
    # Apply Colors first (including those from palette.colors)
    for name, value in theme.colors.items():
        css_vars[f'--nd-{name}'] = value
    
    # Apply Layout variables in proper order
    # First, set shadow-color (needed by other shadow variables)
    if 'shadow-color' in theme.layout:
        css_vars[f'--nd-shadow-color'] = theme.layout['shadow-color']
    
    # Then process all other layout variables
    for name, value in theme.layout.items():
        if name == 'shadow-color':
            continue  # Already processed above
        elif name.startswith('font-'):
            css_vars[f'--nd-{name}'] = value
        elif name.startswith('space-'):
            css_vars[f'--nd-{name}'] = value
        elif name.startswith('border-'):
            css_vars[f'--nd-{name}'] = value
        elif name.startswith('shadow-'):
            css_vars[f'--nd-{name}'] = value
        elif name == 'transition-speed':
            css_vars[f'--nd-transition-speed'] = value
        else:
            css_vars[f'--nd-radius-{name}'] = value
    
    if initial:
        # Initial setup: Use static CSS injection
        # Add Quasar brand sync to the static vars
        if theme.colors.get('primary'):
            css_vars['--q-primary'] = theme.colors['primary']
        if theme.colors.get('secondary'):
            css_vars['--q-secondary'] = theme.colors['secondary']
            
        css_vars_str = "\n  ".join([f"{k}: {v};" for k, v in css_vars.items()])
        ui.add_head_html(f"<style>:root {{\n  {css_vars_str}\n}}</style>")
        
        # Apply body classes
        if theme.classes:
            ui.query('body').classes(' '.join(theme.classes))
    else:
        # Dynamic update: Use JavaScript to update CSS variables
        import json
        vars_json = json.dumps(css_vars)
        ui.run_javascript(f'''
            const root = document.documentElement;
            const vars = {vars_json};
            for (const [key, value] of Object.entries(vars)) {{
                root.style.setProperty(key, value);
            }}
            
            // Sync Quasar brand colors with our theme values directly
            if (vars['--nd-primary']) {{
                root.style.setProperty('--q-primary', vars['--nd-primary']);
            }}
            if (vars['--nd-secondary']) {{
                root.style.setProperty('--q-secondary', vars['--nd-secondary']);
            }}
        ''')
        
        # Update body classes for texture
        if theme.classes:
            # Remove previous texture classes and add new ones
            ui.run_javascript(f'''
                const body = document.body;
                // Remove previous texture classes (anything starting with -nd-t- or texture-)
                body.classList.forEach(cls => {{
                    if (cls.startsWith('-nd-t-') || cls.startsWith('texture-') || cls === 'no-shadows') {{
                        body.classList.remove(cls);
                    }}
                }});
                // Add new classes
                {json.dumps(theme.classes)}.forEach(cls => body.classList.add(cls));
            ''')

def setup(theme: Optional[CompiledTheme] = None):
    """
    Convenience function to load the system and optionally apply a theme.
    """
    # IMPORTANT: Inject theme CSS variables FIRST, before loading component CSS
    # This ensures variables are available when atoms.css (which references them) is parsed
    if theme:
        # Build and inject CSS variables
        css_vars = {}
        
        # Apply Colors first
        for name, value in theme.colors.items():
            css_vars[f'--nd-{name}'] = value
        
        # Apply Layout variables in proper order
        # First, set shadow-color (needed by other shadow variables)
        if 'shadow-color' in theme.layout:
            css_vars[f'--nd-shadow-color'] = theme.layout['shadow-color']
        
        # Then process all other layout variables
        for name, value in theme.layout.items():
            if name == 'shadow-color':
                continue  # Already processed above
            elif name.startswith('font-'):
                css_vars[f'--nd-{name}'] = value
            elif name.startswith('space-'):
                css_vars[f'--nd-{name}'] = value
            elif name.startswith('border-'):
                css_vars[f'--nd-{name}'] = value
            elif name.startswith('shadow-'):
                css_vars[f'--nd-{name}'] = value
            elif name == 'transition-speed':
                css_vars[f'--nd-transition-speed'] = value
            else:
                css_vars[f'--nd-radius-{name}'] = value
        
        # Add Quasar brand sync
        if theme.colors.get('primary'):
            css_vars['--q-primary'] = theme.colors['primary']
        if theme.colors.get('secondary'):
            css_vars['--q-secondary'] = theme.colors['secondary']

        # Inject CSS variables BEFORE loading design system CSS
        css_vars_str = "\n  ".join([f"{k}: {v};" for k, v in css_vars.items()])
        ui.add_head_html(f"<style>:root {{\n  {css_vars_str}\n}}</style>")
        
        # Generate utility classes
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
        
        ui.add_head_html(f"<style>{chr(10).join(utils)}</style>")
    
    # NOW load the design system (which loads atoms.css that references these variables)
    load_design_system()
    
    # Apply body classes for texture if theme was provided
    if theme and theme.classes:
        ui.query('body').classes(' '.join(theme.classes))