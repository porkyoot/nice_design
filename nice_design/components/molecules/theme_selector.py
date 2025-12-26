from typing import Optional, Callable, Dict, Any
from nicegui import ui
import copy

from nice_design.components.atoms.select_button import select_button
from nice_design.components.atoms.menu import menu
from nice_design.components.atoms.select import select
from nice_design.components.atoms.theme_icon import theme_icon
from nice_design.components.atoms.palette_icon import palette_icon
from nice_design.components.atoms.texture_icon import texture_icon

from nice_design.core.presets import (
    SOLARIZED_PALETTE, 
    SOLARIZED_SEMANTICS, 
    STANDARD_SHAPE, 
    STANDARD_SHAPE, 
    STANDARD_TEXTURE,
    STANDARD_LAYOUT,
)
from nice_design.core.definitions import Palette, Texture, Shape, Layout
from nice_design.components.atoms.slider import slider, split_slider

# --- Mock Data for Selects ---
# In a real app, these would come from the ThemeEngine registry or a configuration object

# Palettes
PALETTE_OPTIONS = {}

# Solarized (Default)
PALETTE_OPTIONS['Solarized'] = {
    'palette': SOLARIZED_PALETTE,
    'semantics': SOLARIZED_SEMANTICS
}

# Dracula-ish (Mock)
DRACULA_PALETTE = copy.deepcopy(SOLARIZED_PALETTE)
DRACULA_PALETTE.name = "dracula"
DRACULA_PALETTE.colors = {
    'blue': '#8be9fd', 'cyan': '#8be9fd', 'green': '#50fa7b', 
    'yellow': '#f1fa8c', 'orange': '#ffb86c', 'red': '#ff5555', 
    'magenta': '#ff79c6', 'purple': '#bd93f9'
}
DRACULA_SEMANTICS = copy.deepcopy(SOLARIZED_SEMANTICS)
DRACULA_SEMANTICS.name = "dracula"
DRACULA_SEMANTICS.surface_base = '#282a36'
DRACULA_SEMANTICS.content_main = '#f8f8f2'
PALETTE_OPTIONS['Dracula'] = {'palette': DRACULA_PALETTE, 'semantics': DRACULA_SEMANTICS}

# Textures
TEXTURE_OPTIONS = {}

# Standard (Flat)
TEXTURE_OPTIONS['Flat'] = STANDARD_TEXTURE

# Glassy
GLASSY_TEXTURE = copy.deepcopy(STANDARD_TEXTURE)
GLASSY_TEXTURE.name = 'glassy'
GLASSY_TEXTURE.opacity = 0.6
GLASSY_TEXTURE.texture_cls = 'texture-glassy'
TEXTURE_OPTIONS['Glassy'] = GLASSY_TEXTURE

# Glossy (High Shadow)
GLOSSY_TEXTURE = copy.deepcopy(STANDARD_TEXTURE)
GLOSSY_TEXTURE.name = 'glossy'
GLOSSY_TEXTURE.shadow_intensity = 1.5
GLOSSY_TEXTURE.opacity = 0.95
TEXTURE_OPTIONS['Glossy'] = GLOSSY_TEXTURE


class theme_selector(ui.element):
    """
    A molecule that combines a generic select_button and a menu to control the application theme.
    Displays a real-time 'theme_icon' preview of the configured theme.
    """
    def __init__(self, on_change: Optional[Callable[[Dict[str, Any]], None]] = None):
        super().__init__('div')
        self.classes('w-fit')
        self._on_change = on_change
        
        # Initial State
        self._current_palette_name = 'Solarized'
        self._current_texture_name = 'Flat'
        
        # Working copies of objects to allow modification (e.g. roundness)
        self._shape = copy.deepcopy(STANDARD_SHAPE)
        self._texture = copy.deepcopy(TEXTURE_OPTIONS['Flat'])
        self._layout = copy.deepcopy(STANDARD_LAYOUT)
        
        self._render()

    @property
    def current_palette(self):
        return PALETTE_OPTIONS[self._current_palette_name]['palette']
        
    @property
    def current_semantics(self):
        return PALETTE_OPTIONS[self._current_palette_name]['semantics']
        
    def _render_trigger_icon(self):
        """Builder for the select_button icon. Creates a container we can update later."""
        self.trigger_icon_container = ui.element('div').classes('flex items-center justify-center')
        self._update_trigger_icon()
        
    def _update_trigger_icon(self):
        """Updates the content of the trigger icon container."""
        if hasattr(self, 'trigger_icon_container'):
            self.trigger_icon_container.clear()
            with self.trigger_icon_container:
                theme_icon(
                    self.current_palette,
                    self.current_semantics,
                    self._shape,
                    self._texture,
                    size="24px"
                )
        
    def _render_large_preview(self):
        """Renders the large theme icon preview."""
        with ui.row().classes('w-full justify-center py-6 bg-black/5 mb-2'):
             theme_icon(
                self.current_palette,
                self.current_semantics,
                self._shape,
                self._texture,
                size="64px"
            )

    def _render(self):
        self.clear()
        
        with self:
            # Icon Only Button
            # We use our custom builder which creates a container we can update
            self.btn = select_button(
                icon_only=True,
                custom_icon_builder=self._render_trigger_icon
            )
            
            with self.btn:
                # Force menu to be styled appropriately
                with menu().classes('min-w-[280px] nd-p-0') as self.menu:
                    # Sync rotation
                    self.menu.on('hide', self.btn.reset_rotation)
                    
                    # 1. Prominent Theme Icon Preview container
                    self._preview_container = ui.element('div').classes('w-full')
                    with self._preview_container:
                        self._render_large_preview()
                        
                    # 2. Controls Section (Scrollable with NiceGUI)
                    # Use a safer height and move padding inside to ensure bottom elements aren't clipped
                    with ui.scroll_area().classes('w-full h-[50vh]'):
                        with ui.column().classes('w-full p-4 gap-4'):
                            ui.label('Theme Configuration').classes('text-[10px] font-bold opacity-40 uppercase tracking-widest')

                        # Palette Select
                        palette_opts = {}
                        for name, data in PALETTE_OPTIONS.items():
                            html = palette_icon.to_html(data['palette'], data['semantics'], size="20px")
                            palette_opts[name] = {'label': name, 'html': html}
                            
                        select(
                            options=palette_opts,
                            value=self._current_palette_name,
                            label='Palette',
                            with_icons=True,
                            on_change=lambda e: self._update_palette(e.value)
                        ).classes('w-full')
                        
                        # Texture Select
                        texture_opts = {}
                        for name, tex in TEXTURE_OPTIONS.items():
                            html = texture_icon.to_html(tex, size="20px")
                            texture_opts[name] = {'label': name, 'html': html}

                        select(
                            options=texture_opts,
                            value=self._current_texture_name,
                            label='Texture',
                            with_icons=True,
                            on_change=lambda e: self._update_texture(e.value)
                        ).classes('w-full')
                        
                        ui.separator().classes('opacity-10 my-1')

                        # Roundness Slider
                        with ui.column().classes('w-full gap-1'):
                            with ui.row().classes('w-full justify-between'):
                                ui.label('Roundness').classes('text-xs opacity-60')
                                self._roundness_label = ui.label(f'{self._shape.roundness:.1f}').classes('text-xs font-bold')
                                
                            ui.slider(min=0, max=2.5, step=0.1, value=self._shape.roundness, 
                                      on_change=self._update_roundness).props('label-always color="primary"')
                                      
                        # Border Slider
                        with ui.column().classes('w-full gap-1'):
                            with ui.row().classes('w-full justify-between'):
                                ui.label('Border').classes('text-xs opacity-60')
                                self._border_label = ui.label(f'{self._shape.base_border}px').classes('text-xs font-bold')
                                
                            ui.slider(min=0, max=4, step=1, value=self._shape.base_border,
                                      on_change=self._update_border).props('markers snap color="primary"')

                        ui.separator().classes('opacity-10 my-1')
                        
                        # Spacing Slider
                        with ui.column().classes('w-full gap-1'):
                            with ui.row().classes('w-full justify-between'):
                                ui.label('Spacing').classes('text-xs opacity-60')
                                self._spacing_label = ui.label(f'{self._layout.base_space:.1f}x').classes('text-xs font-bold')
                                
                            slider(min=0.5, max=2.0, step=0.1, value=self._layout.base_space,
                                      on_change=self._update_spacing).props('label-always color="primary"')
                                      
                        # Shadow / Highlight (Opacity) Split Slider
                        with ui.column().classes('w-full gap-2'):
                            ui.row().classes('w-full justify-between text-xs opacity-60 font-bold').style('margin-bottom: -10px').add_slot('default', r'''
                               <span class="text-blue-400">Shadow</span>
                               <span class="text-teal-400">Opacity</span>
                            ''')
                            
                            split_slider(
                                limit=100, # Using 0-100 scale for UI control
                                value_left=self._texture.shadow_intensity * 50, # Scale 2.0 -> 100
                                value_right=self._texture.opacity * 100, # Scale 1.0 -> 100
                                color_left='blue-4',
                                color_right='teal-4',
                                on_change=self._update_shadow_opacity
                            )

    def _update_palette(self, value):
        if value:
            self._current_palette_name = value
            self._refresh_components()
        
    def _update_texture(self, value):
        if value:
            self._current_texture_name = value
            # Reset local texture state to the selected preset
            self._texture = copy.deepcopy(TEXTURE_OPTIONS[value])
            self._refresh_components()
        
    def _update_roundness(self, e):
        self._shape.roundness = e.value
        self._roundness_label.text = f'{e.value:.1f}'
        self._refresh_components()

    def _update_border(self, e):
        val = int(e.value)
        self._shape.base_border = val
        self._border_label.text = f'{val}px'
        self._refresh_components()

    def _update_spacing(self, e):
        self._layout.base_space = e.value
        self._spacing_label.text = f'{e.value:.1f}x'
        self._refresh_components()
        
    def _update_shadow_opacity(self, e):
        # Scale back from 0-100 UI to data values
        self._texture.shadow_intensity = e['left'] / 50.0 # 100 -> 2.0
        self._texture.opacity = e['right'] / 100.0 # 100 -> 1.0
        self._refresh_components()

    def _refresh_components(self):
        """Refreshes the dynamic visualizations and triggers change event."""
        # Update UI visualizations
        self._update_trigger_icon()
        
        self._preview_container.clear()
        with self._preview_container:
            self._render_large_preview()
            
        # Notify listener
        if self._on_change:
            self._on_change({
                'palette': self.current_palette,
                'semantics': self.current_semantics,
                'texture': self._texture,
                'shape': self._shape,
                'layout': self._layout
            })
