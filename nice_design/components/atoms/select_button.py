from nicegui import ui
from typing import Optional

class select_button(ui.button):
    """
    A button styled exactly like a Select component.
    Useful for triggering menus or other interactions while maintaining the Select visual language.
    Contains logic for toggling the chevron rotation.
    """
    def __init__(self, label: str = '', icon: Optional[str] = None, icon_right: str = 'arrow_drop_down', **kwargs):
        super().__init__(text=label, icon=icon, **kwargs)
        
        # Apply strict styling classes
        self.classes('-nd-c-select-button')
        
        # Structure the button to allow space-between alignment
        self.props(f'unelevated no-caps align="between" icon-right="{icon_right}"')
        
        # Internal state for rotation
        self._is_rotated = False
        
        # Bind click to toggle
        self.on('click', self.toggle_rotation)

    def set_label(self, text: str):
        self.text = text
        
    def set_icon(self, icon: str):
        self.icon = icon

    def toggle_rotation(self):
        """Toggles the rotation state of the right icon."""
        self._is_rotated = not self._is_rotated
        self._update_rotation_class()
        
    def reset_rotation(self):
        """Resets rotation to default (0 deg). Useful when menu closes."""
        self._is_rotated = False
        self._update_rotation_class()
        
    def _update_rotation_class(self):
        if self._is_rotated:
            self.classes(add='-nd-state-rotated')
        else:
            self.classes(remove='-nd-state-rotated')
