from nicegui import ui
from typing import Optional, Union, Callable

class select_button(ui.button):
    """
    A button styled exactly like a Select component.
    Useful for triggering menus or other interactions while maintaining the Select visual language.
    Contains logic for toggling the chevron rotation.
    """
    def __init__(self, 
                 label: str = '', 
                 icon: Optional[str] = None, 
                 icon_right: str = 'arrow_drop_down', 
                 icon_only: bool = False, 
                 custom_icon_builder: Optional[Callable] = None,
                 **kwargs):
        # Default color to None to prevent 'bg-primary' class nicely
        if 'color' not in kwargs:
            kwargs['color'] = 'transparent' # Use transparent so our CSS background takes over
        
        self._icon_only = icon_only
        self._original_label = label
        self._custom_icon_builder = custom_icon_builder
        
        self._custom_label_element = None
        
        # If using a custom builder, we suppress the default label to render it manually
        # alongside the icon for proper grouping and behavior with align="between".
        display_text = '' if (icon_only or custom_icon_builder) else label
        
        # Don't pass icon to super if using custom builder (we insert it manually)
        super_icon = icon if not custom_icon_builder else None
        
        super().__init__(text=display_text, icon=super_icon, **kwargs)
        
        # Apply strict styling classes
        self.classes('-nd-c-select-button')
        
        if icon_only:
            self.classes('-nd-mode-icon-only')
        
        # Structure the button to allow space-between alignment
        self.props(f'unelevated no-caps align="between" icon-right="{icon_right}"')
        
        # Internal state for rotation
        self._is_rotated = False
        
        # Bind click to toggle
        self.on('click', self.toggle_rotation)
        
        # Insert Custom Icon if provided
        if self._custom_icon_builder:
            with self:
                # Group Icon and Label so they stay together on the left.
                # Since the button has align="between", this wrapper will be pushed to the start,
                # and the icon-right (chevron) will be pushed to the end.
                with ui.element('div').classes('row no-wrap items-center'):
                    # Icon Container
                    # 'on-left' adds standard margin-right for separation from text
                    container = ui.element('div').classes('on-left flex flex-center order-first')
                    with container:
                         self._custom_icon_builder()
                    
                    # Manual Label
                    if not icon_only:
                        self._custom_label_element = ui.label(label)

    def set_label(self, text: str):
        self._original_label = text
        if self._icon_only:
            return
            
        if self._custom_label_element:
            self._custom_label_element.text = text
        else:
            self.text = text
        
    def set_icon(self, icon: str):
        if not self._custom_icon_builder:
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
