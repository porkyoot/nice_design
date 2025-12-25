from nicegui import ui
from ..atoms.button import button
from ..atoms.menu import menu, menu_item

class ThemeSelector(ui.row):
    """
    A molecule that combines a theme mode toggle (light/dark) 
    and a theme picker menu triggered by a rotating triangle button.
    """
    def __init__(self, themes: list[str] = None, on_mode_toggle=None, on_theme_change=None):
        super().__init__()
        self.classes('items-center nd-gap-sm')
        
        self.is_dark = True
        self.on_mode_toggle = on_mode_toggle
        self.on_theme_change = on_theme_change
        
        # 1. Mode Toggle Button (Atom)
        self.mode_btn = button(
            variant='ghost', 
            icon='mdi-white-balance-sunny', 
            on_click=self.toggle_mode
        )
        self.mode_btn.classes('nd-mode-btn')
        self._apply_mode_style()
        
        # 2. Trigger Button (Atom) with rotating triangle icon
        # We use 'change_history' for a triangle or 'arrow_drop_down' for a more common select feel.
        # The user requested specifically a 'triangle icon'.
        self.trigger_btn = button(
            variant='ghost', 
            icon='mdi-triangle', 
            rotate_icon=True
        )
        self.trigger_btn.classes('nd-theme-trigger')
        
        with self.trigger_btn:
            with menu() as self.theme_menu:
                # Synchronize rotation with menu closing
                self.theme_menu.on('hide', lambda: self.trigger_btn.classes(remove='nd-btn--rotated'))
                
                if themes:
                    for theme in themes:
                        menu_item(theme, on_click=lambda t=theme: self._handle_theme_change(t))
                else:
                    menu_item("No Themes")

    def toggle_mode(self):
        self.is_dark = not self.is_dark
        self._apply_mode_style()
        if self.on_mode_toggle:
            self.on_mode_toggle(self.is_dark)

    def _apply_mode_style(self):
        if self.is_dark:
            # Dark mode -> Sun Icon (Yellow/Orange)
            self.mode_btn.props('icon=mdi-white-balance-sunny')
            self.mode_btn.style('color: #fdb813 !important')
        else:
            # Light mode -> Moon Icon (Indigo/Accent)
            self.mode_btn.props('icon=mdi-moon-waning-crescent')
            self.mode_btn.style('color: var(--nd-accent) !important')

    def _handle_theme_change(self, theme_name: str):
        if self.on_theme_change:
            self.on_theme_change(theme_name)
        self.theme_menu.close()
