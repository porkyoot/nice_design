from typing import Optional, Callable, Dict, Any
from nicegui import ui
import copy

from nice_design.components.atoms.select_button import select_button
from nice_design.components.atoms.menu import menu
from nice_design.components.atoms.select import select
from nice_design.components.atoms.theme_icons.theme_icon import theme_icon
from nice_design.components.atoms.theme_icons.palette_icon import palette_icon
from nice_design.components.atoms.theme_icons.texture_icon import texture_icon
from nice_design.core.fonts import FontManager

from nice_design.core.presets import (
    SOLARIZED_PALETTE, 
    STANDARD_TEXTURE,
    STANDARD_LAYOUT,
    STANDARD_TYPO,
)
from nice_design.core.definitions import Palette, Texture, Layout, Typography, Theme
from nice_design.components.atoms.slider import slider, split_slider, palette_slider

# Use the global registry
import nice_design as nice

class theme_selector(ui.element):
    """
    A molecule that combines a generic select_button and a menu to control the application theme.
    Displays a real-time 'theme_icon' preview of the configured theme.
    Supports 'Theme Bundles' (combinations of 4 pillars) and individual pillar adjustments.
    """
    def __init__(self, on_change: Optional[Callable[[Dict[str, Any]], None]] = None):
        super().__init__('div')
        self.classes('w-fit')
        self._on_change = on_change
        
        # 1. State - Initialized from registry or presets
        self._current_theme_bundle_name = None
        self._current_palette_name = 'solarized'
        self._current_texture_name = 'standard'
        self._current_font_name = 'standard'
        self._current_layout_name = 'standard'
        
        # 2. Category Objects (Working copies)
        self._palette = copy.deepcopy(nice.registry.get_palette('solarized') or SOLARIZED_PALETTE)
        self._texture = copy.deepcopy(nice.registry.get_texture('standard') or STANDARD_TEXTURE)
        self._typography = copy.deepcopy(nice.registry.get_typography('Inter') or STANDARD_TYPO)
        self._layout = copy.deepcopy(nice.registry.get_layout('standard') or STANDARD_LAYOUT)
        
        # 3. Dynamic Font Data
        self._all_font_opts = FontManager.get_font_options(nice.registry.list_typographies())
        
        self._render()

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
                    self._palette,
                    self._texture,
                    size="24px"
                )
        
    def _render_large_preview(self):
        """Renders the large theme icon preview."""
        with ui.row().classes('w-full justify-center py-6 bg-black/5 mb-2'):
             theme_icon(
                self._palette,
                self._texture,
                size="64px"
            )

    def _render(self):
        self.clear()
        
        # Fetch fresh options from registry
        themes = nice.registry.list_themes()
        palettes = nice.registry.list_palettes()
        textures = nice.registry.list_textures()
        layouts = nice.registry.list_layouts()
        fonts = nice.registry.list_typographies()
        
        with self:
            # Main Trigger Button
            self.btn = select_button(
                icon_only=True,
                custom_icon_builder=self._render_trigger_icon
            )
            
            with self.btn:
                with menu().classes('min-w-[280px] nd-p-0') as self.menu:
                    self.menu.on('hide', self.btn.reset_rotation)
                    
                    # 1. Preview
                    self._preview_container = ui.element('div').classes('w-full')
                    with self._preview_container:
                        self._render_large_preview()
                        
                    # 2. Controls Section
                    with ui.column().classes('w-full nd-p-md nd-gap-md'):
                        ui.label('Theme Configuration').classes('text-[10px] font-bold opacity-40 uppercase tracking-widest mb-2')
                        
                        # A. Theme Bundles (Combination Dropdown)
                        if themes:
                             select(
                                 options={t: t.replace('-', ' ').title() for t in themes},
                                 value=self._current_theme_bundle_name,
                                 label='Theme Bundle Preset',
                                 on_change=lambda e: self._update_theme_bundle(e.value)
                             ).classes('w-full mb-2')

                        # Row of Submenu Buttons (The 4 Pillars)
                        with ui.row().classes('w-full nd-gap-sm justify-between'):
                            
                            # --- B. Palette Submenu ---
                            palette_icon_builder = lambda: palette_icon(self._palette, size="24px")
                            with select_button(icon_only=True, custom_icon_builder=palette_icon_builder) as btn_palette:
                                btn_palette.classes('flex-1')
                                with menu().classes('min-w-[240px] nd-p-md nd-gap-md') as m:
                                    m.on('hide', btn_palette.reset_rotation)
                                    ui.label('Palette & Colors').classes('text-xs font-bold opacity-60 mb-2')
                                    
                                    # Primary Accent
                                    ui.label('Primary Accent').classes('text-xs opacity-60 font-bold mb-1')
                                    palette_slider(
                                        colors=list(self._palette.colors.values()) or ["#002b36", "#fdf6e3"],
                                        value=self._palette.primary,
                                        on_change=self._update_primary_accent
                                    )

                                    # Secondary Accent
                                    ui.label('Secondary Accent').classes('text-xs opacity-60 font-bold mb-1')
                                    palette_slider(
                                        colors=list(self._palette.colors.values()) or ["#002b36", "#fdf6e3"],
                                        value=self._palette.secondary,
                                        on_change=self._update_secondary_accent
                                    )

                                    ui.separator().classes('opacity-10 my-1')

                                    # Palette Preset
                                    palette_opts = {}
                                    for name in palettes:
                                        p = nice.registry.get_palette(name)
                                        if p:
                                            html = palette_icon.to_html(p, size="20px")
                                            palette_opts[name] = {'label': name.title(), 'html': html}
                                        
                                    p_val = self._current_palette_name if self._current_palette_name in palette_opts else (next(iter(palette_opts.keys())) if palette_opts else None)
                                        
                                    self._palette_select = select(
                                        options=palette_opts,
                                        value=p_val,
                                        label='Palette Preset',
                                        with_icons=True,
                                        on_change=lambda e: self._update_palette(e.value)
                                    ).classes('w-full')
                            
                            # --- C. Texture Submenu ---
                            texture_icon_builder = lambda: texture_icon(self._texture, size="24px")
                            with select_button(icon_only=True, custom_icon_builder=texture_icon_builder) as btn_texture:
                                btn_texture.classes('flex-1')
                                with menu().classes('min-w-[240px] nd-p-md nd-gap-md') as m:
                                    m.on('hide', btn_texture.reset_rotation)
                                    ui.label('Surface & Shape').classes('text-xs font-bold opacity-60 mb-2')
                                    
                                    # Texture Select
                                    texture_opts = {}
                                    for name in textures:
                                        tex = nice.registry.get_texture(name)
                                        if tex:
                                            html = texture_icon.to_html(tex, size="20px")
                                            texture_opts[name] = {'label': name.title(), 'html': html}

                                    t_val = self._current_texture_name if self._current_texture_name in texture_opts else (next(iter(texture_opts.keys())) if texture_opts else None)

                                    self._texture_select = select(
                                        options=texture_opts,
                                        value=t_val,
                                        label='Texture Base',
                                        with_icons=True,
                                        on_change=lambda e: self._update_texture_preset(e.value)
                                    ).classes('w-full')
                                    
                                    # Shadow / Highlight (Effect Intensities)
                                    with ui.column().classes('w-full nd-gap-sm mt-2'):
                                        ui.row().classes('w-full justify-between text-xs opacity-60 font-bold').style('margin-bottom: -10px').add_slot('default', r'''
                                           <span class="text-blue-400">Shadow</span>
                                           <span class="text-teal-400">Highlight</span>
                                        ''')
                                        self._effect_slider = split_slider(
                                            limit=100,
                                            value_left=self._texture.shadow_intensity * 50, 
                                            value_right=self._texture.highlight_intensity * 50, 
                                            color_left='blue-4',
                                            color_right='teal-4',
                                            on_change=self._update_intensities
                                        )

                                    ui.separator().classes('opacity-10 my-1')
                                    
                                    # Border (Geometric)
                                    with ui.column().classes('w-full nd-gap-xs'):
                                        with ui.row().classes('w-full justify-between'):
                                            ui.label('Border').classes('text-xs opacity-60')
                                            self._border_label = ui.label(f'{self._texture.border_width}px').classes('text-xs font-bold')
                                            
                                        self._border_slider = ui.slider(min=0, max=4, step=1, value=self._texture.border_width,
                                                  on_change=self._update_border).props('markers snap color="primary" label')

                                    # Roundness (Geometric)
                                    with ui.column().classes('w-full nd-gap-xs'):
                                        with ui.row().classes('w-full justify-between'):
                                            ui.label('Roundness').classes('text-xs opacity-60')
                                            self._roundness_label = ui.label(f'{self._texture.roundness:.1f}').classes('text-xs font-bold')
                                            
                                        self._roundness_slider = ui.slider(min=0, max=2.5, step=0.1, value=self._texture.roundness, 
                                                  on_change=self._update_roundness).props('label color="primary"')

                            # --- D. Typography Submenu ---
                            with select_button(icon='mdi-format-font', icon_only=True) as btn_typo:
                                btn_typo.classes('flex-1')
                                with menu().classes('min-w-[240px] nd-p-md nd-gap-md') as m:
                                    m.on('hide', btn_typo.reset_rotation)
                                    ui.label('Typography').classes('text-xs font-bold opacity-60 mb-2')
                                    
                                    f_val = self._current_font_name if self._current_font_name in self._all_font_opts else (next(iter(self._all_font_opts.keys())) if self._all_font_opts else None)

                                    self._font_select = select(
                                        options=self._all_font_opts,
                                        value=f_val,
                                        label='Primary Font',
                                        on_change=lambda e: self._update_font(e.value),
                                        on_filter=self._filter_fonts
                                    ).classes('w-full')

                                    ui.separator().classes('opacity-10 my-1')

                                    # Text Scale
                                    with ui.column().classes('w-full nd-gap-xs'):
                                        with ui.row().classes('w-full justify-between'):
                                            ui.label('Text Scale').classes('text-xs opacity-60')
                                            self._scale_label = ui.label(f'{self._typography.scale_ratio:.2f}').classes('text-xs font-bold')
                                            
                                        self._scale_slider = slider(min=1.0, max=1.6, step=0.05, value=self._typography.scale_ratio,
                                                  on_change=self._update_text_scale).props('label color="primary"')

                            # --- E. Layout Submenu ---
                            with select_button(icon='mdi-view-quilt', icon_only=True) as btn_layout:
                                btn_layout.classes('flex-1')
                                with menu().classes('min-w-[240px] nd-p-md nd-gap-md') as m:
                                    m.on('hide', btn_layout.reset_rotation)
                                    ui.label('Layout & Spacing').classes('text-xs font-bold opacity-60 mb-2')
                                    
                                    layout_opts = {name: name.title() for name in layouts}
                                    l_val = self._current_layout_name if self._current_layout_name in layout_opts else (next(iter(layout_opts.keys())) if layout_opts else None)

                                    self._layout_select = select(
                                        options=layout_opts,
                                        value=l_val,
                                        label='Layout Preset',
                                        on_change=lambda e: self._update_layout_preset(e.value)
                                    ).classes('w-full')
                                    
                                    ui.separator().classes('opacity-10 my-1')
                                    
                                    with ui.column().classes('w-full nd-gap-xs mt-2'):
                                        with ui.row().classes('w-full justify-between'):
                                            ui.label('Spacing Density').classes('text-xs opacity-60')
                                            self._spacing_label = ui.label(f'{self._layout.base_space:.1f}x').classes('text-xs font-bold')
                                            
                                        self._spacing_slider = slider(min=0.5, max=2.0, step=0.1, value=self._layout.base_space,
                                                  on_change=self._update_spacing).props('label color="primary"')

    def _update_theme_bundle(self, bundle_name):
        """Applies a named 'Theme' bundle (combination of 4 pillars)."""
        if not bundle_name: return
        
        theme = nice.registry.get_theme(bundle_name)
        if not theme: return
        
        self._current_theme_bundle_name = bundle_name
        self._palette = copy.deepcopy(theme.palette)
        self._texture = copy.deepcopy(theme.texture)
        self._typography = copy.deepcopy(theme.typography)
        self._layout = copy.deepcopy(theme.layout)
        
        # Update synced select values/labels (optional, for UI consistency)
        self._refresh_components()

    def _update_palette(self, value):
        if value:
            p = nice.registry.get_palette(value)
            if p:
                self._current_palette_name = value
                self._palette = copy.deepcopy(p)
                self._refresh_components()
            
    def _update_primary_accent(self, color):
        self._palette.primary = color
        self._refresh_components()

    def _update_secondary_accent(self, color):
        self._palette.secondary = color
        self._refresh_components()
        
    def _update_texture_preset(self, value):
        if value:
            tex = nice.registry.get_texture(value)
            if tex:
                self._current_texture_name = value
                self._texture = copy.deepcopy(tex)
                self._refresh_components()
            
    def _update_layout_preset(self, value):
        if value:
            lay = nice.registry.get_layout(value)
            if lay:
                self._current_layout_name = value
                self._layout = copy.deepcopy(lay)
                self._refresh_components()
        
    def _update_roundness(self, e):
        self._texture.roundness = e.value
        self._roundness_label.text = f'{e.value:.1f}'
        self._refresh_components()

    def _update_border(self, e):
        val = int(e.value)
        self._texture.border_width = val
        self._border_label.text = f'{val}px'
        self._refresh_components()

    def _update_spacing(self, e):
        self._layout.base_space = e.value
        self._spacing_label.text = f'{e.value:.1f}x'
        self._refresh_components()
        
    def _update_intensities(self, e):
        self._texture.shadow_intensity = e['left'] / 50.0
        self._texture.highlight_intensity = e['right'] / 50.0
        self._refresh_components()

    def _update_font(self, value):
        if value:
            self._current_font_name = value
            # 1. Load font if it's a Google Font
            FontManager.load_font(value)
            
            # 2. Update Typography object
            typo = nice.registry.get_typography(value)
            if typo:
                self._typography.font_main = typo.font_main
            else:
                # Fallback for Google Fonts or others not in registry
                self._typography.font_main = f"'{value}', sans-serif"
            
            self._refresh_components()

    def _filter_fonts(self, val: str):
        """Filters the font options based on search input."""
        if not val:
            return self._all_font_opts
        return {k: v for k, v in self._all_font_opts.items() if val in k.lower()}

    def _update_text_scale(self, e):
        self._typography.scale_ratio = e.value
        self._scale_label.text = f'{e.value:.2f}'
        self._refresh_components()

    def _refresh_components(self):
        """Refreshes the dynamic visualizations and triggers change event."""
        self._update_trigger_icon()
        
        self._preview_container.clear()
        with self._preview_container:
            self._render_large_preview()
            
        if self._on_change:
            self._on_change({
                'palette': self._palette,
                'texture': self._texture,
                'typography': self._typography,
                'layout': self._layout
            })
