from nicegui import ui
from ..atoms.select import select
from ..atoms.button import button
from ..atoms.menu import menu
from ..atoms.icon import icon as IconAtom
from typing import List, Callable, Optional, Any

class ThemeConfig(ui.row):
    """
    A molecule that uses a static theme icon as a trigger for a sophisticated
    configuration menu, utilizing only design system atoms.
    """
    def __init__(
        self, 
        themes: List[Any], 
        *,
        fonts: List[Any] = None,
        on_theme_change: Optional[Callable[[str], None]] = None,
        on_mode_toggle: Optional[Callable[[bool], None]] = None,
        on_texture_change: Optional[Callable[[str], None]] = None,
        on_font_change: Optional[Callable[[str], None]] = None,
        is_dark: bool = True
    ):
        super().__init__()
        self.classes('items-center nd-gap-sm')
        
        self.themes = themes
        self.fonts = fonts or [
            {'label': 'Inter', 'value': 'Inter', 'icon': 'mdi-alphabetical-variant'},
            {'label': 'Roboto', 'value': 'Roboto', 'icon': 'mdi-alphabetical-variant'},
            {'label': 'Outfit', 'value': 'Outfit', 'icon': 'mdi-alphabetical-variant'},
            {'label': 'Fira Code', 'value': 'Fira Code', 'icon': 'mdi-code-tags'}
        ]
        self.on_theme_change = on_theme_change
        self.on_mode_toggle = on_mode_toggle
        self.on_texture_change = on_texture_change
        self.on_font_change = on_font_change
        self.is_dark = is_dark
        
        # 1. Create the Trigger (Minimal Select)
        self.trigger = select(
            options=[], 
            minimal=True
        )
        # Add icon via slot (new pattern)
        with self.trigger.add_slot('prepend'):
            IconAtom('mdi-palette-outline').classes('nd-select__icon').style('color: var(--nd-magenta) !important')
        
        # 2. Build the Sophisticated Menu
        with self.trigger:
            with menu().classes('nd-p-md nd-gap-md') as self.config_menu:
                
                # Row 1: Mode Toggle and Texture Select
                with ui.row().classes('w-full items-center justify-between nd-gap-md'):
                    # Mode Button (Sun/Moon)
                    self.mode_btn = button(
                        variant='ghost',
                        icon='mdi-white-balance-sunny' if self.is_dark else 'mdi-moon-waning-crescent',
                        on_click=self.toggle_mode
                    ).classes('w-10 h-10 rounded-full')
                    self._update_mode_btn_color()

                    # Texture Select (Minimal) - icons shown in options via with_icons
                    textures = [
                        {'label': 'flat', 'value': 'flat', 'icon': 'mdi-format-color-fill'},
                        {'label': 'glossy', 'value': 'glossy', 'icon': 'mdi-glass-variant'},
                        {'label': 'glass', 'value': 'glass', 'icon': 'mdi-blur'},
                        {'label': 'simple', 'value': 'simple', 'icon': 'mdi-circle-outline'}
                    ]
                    self.texture_select = select(
                        options=textures,
                        value=None, 
                        minimal=True,
                        on_change=lambda e: self._handle_texture_change(e.value),
                        with_icons=True
                    )
                    self.texture_select.props('option-value="value" option-label="label" emit-value map-options')
                    self.texture_select.value = 'flat'

                ui.separator().classes('bg-white/10')

                # Row 2: Palette Selection (Normal Select)
                with ui.column().classes('w-full nd-gap-xs'):
                    ui.label('PALETTE').classes('text-[10px] font-bold opacity-40 tracking-widest ml-1')
                    initial_palette = self.themes[0] if self.themes else None
                    palette_value = initial_palette['value'] if isinstance(initial_palette, dict) else initial_palette
                    
                    self.palette_select = select(
                        options=self.themes,
                        value=None,
                        on_change=lambda e: self._handle_theme_change(e.value),
                        with_icons=True
                    )
                    self.palette_select.classes('w-full')
                    self.palette_select.props('option-value="value" option-label="label" emit-value map-options')
                    self.palette_select.value = palette_value

                # Row 3: Font Selection (Normal Select)
                with ui.column().classes('w-full nd-gap-xs'):
                    ui.label('TYPOGRAPHY').classes('text-[10px] font-bold opacity-40 tracking-widest ml-1')
                    initial_font = self.fonts[0] if self.fonts else None
                    font_value = initial_font['value'] if isinstance(initial_font, dict) else initial_font
                    
                    self.font_select = select(
                        options=self.fonts,
                        value=None,
                        on_change=lambda e: self._handle_font_change(e.value),
                        with_icons=True
                    )
                    self.font_select.classes('w-full')
                    self.font_select.props('option-value="value" option-label="label" emit-value map-options')
                    self.font_select.value = font_value

    def toggle_mode(self):
        self.is_dark = not self.is_dark
        self._update_mode_appearance()
        if self.on_mode_toggle:
            self.on_mode_toggle(self.is_dark)

    def _update_mode_appearance(self):
        # Update Icon
        icon_name = 'mdi-white-balance-sunny' if self.is_dark else 'mdi-moon-waning-crescent'
        self.mode_btn.props(f'icon={icon_name}')
        self._update_mode_btn_color()

    def _update_mode_btn_color(self):
        # Sun uses Orange/Yellow style, Moon uses Accent color
        if self.is_dark:
            self.mode_btn.style('color: #fdb813 !important; border-color: #fdb813 !important')
        else:
            self.mode_btn.style('color: var(--nd-purple) !important; border-color: var(--nd-purple) !important')

    def _handle_theme_change(self, theme_name: str):
        if self.on_theme_change:
            self.on_theme_change(theme_name)

    def _handle_texture_change(self, texture: str):
        if self.on_texture_change:
            self.on_texture_change(texture)

    def _handle_font_change(self, font: str):
        if self.on_font_change:
            self.on_font_change(font)
