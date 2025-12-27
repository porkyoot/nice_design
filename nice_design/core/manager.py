from typing import Optional
from nicegui import ui
import json
from .definitions import Theme
from .styles import generate_theme_css

class ThemeManager:
    """
    Central manager for the Nice Design system.
    Handles theme application, dynamic CSS injection, and global component defaults.
    """
    def __init__(self):
        self.current_theme: Optional[Theme] = None
        
    def apply_theme(self, theme: Theme):
        """
        Generates and injects the theme's CSS variables and utility classes.
        Also establishes the 'Variable Bridge' to Quasar and handles body classes.
        """
        self.current_theme = theme
        p = theme.prefix
        pal = theme.palette
        
        # 2. Quasar Color Integration
        ui.colors(
            primary=pal.primary,
            secondary=pal.secondary,
            accent=pal.highlight,
            positive=pal.success,
            negative=pal.error,
            warning=pal.warning,
            info=pal.info
        )
        core_css = generate_theme_css(theme)
        full_css = core_css
        
        # 3. Dynamic Style Update
        css_json = json.dumps(full_css)
        js_apply_css = f'''
            let style = document.getElementById("nd-dynamic-theme");
            if (!style) {{
                style = document.createElement("style");
                style.id = "nd-dynamic-theme";
                document.head.appendChild(style);
            }}
            style.textContent = {css_json};
        '''
        
        # 4. Handle Body Classes (for Textures and Mode)
        classes = [theme.texture.texture_cls]
        if not theme.texture.shadows_enabled:
            classes.append('no-shadows')
            
        classes_json = json.dumps(classes)
        js_apply_classes = f'''
            const body = document.body;
            body.classList.forEach(cls => {{
                if (cls.startsWith('texture-') || cls === 'no-shadows' || cls.startsWith('mode-')) {{
                    body.classList.remove(cls);
                }}
            }});
            {classes_json}.forEach(cls => body.classList.add(cls));
        '''

        from nicegui import core
        if core.loop and core.loop.is_running():
            ui.run_javascript(js_apply_css)
            ui.run_javascript(js_apply_classes)
        else:
            # During startup, inject via head HTML to ensure it's present on first load
            ui.add_head_html(f'<style id="nd-dynamic-theme">{full_css}</style>')
            # For classes, we can't easily target 'body' directly via add_head_html before it exists,
            # but we can inject a script that runs on load.
            ui.add_head_html(f'<script>document.addEventListener("DOMContentLoaded", () => {{ {js_apply_classes} }});</script>')
        
    def configure_defaults(self):
        """
        Configures global defaults for NiceGUI components.
        Ensures consistent look and feel and primary color usage.
        """
        # Buttons: primary color
        ui.button.default_props('color=primary')
        
        # Inputs/Selects: Primary color
        input_props = 'color=primary'
        ui.input.default_props(input_props)
        ui.number.default_props(input_props)
        ui.select.default_props(input_props)
        
        # Sliders: Themed color
        ui.slider.default_props('color=primary')
        
        # Expansion Items: Popup layout
        ui.expansion.default_props('popup')

theme_manager = ThemeManager()
