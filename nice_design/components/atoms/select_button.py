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
                 *args, **kwargs):
        
        # Default color to transparent so our CSS background takes over
        kwargs.setdefault('color', 'transparent')
        
        self._icon_only = icon_only
        self._original_label = label
        self._custom_icon_builder = custom_icon_builder
        
        self._custom_label_element = None
        self._icon_container = None
        
        # If using a custom builder, we suppress the default label to render it manually
        display_text = '' if (icon_only or custom_icon_builder) else label
        
        # Don't pass icon to super if using custom builder
        super_icon = icon if not custom_icon_builder else None
        
        super().__init__(text=display_text, icon=super_icon, *args, **kwargs)
        
        # Apply strict styling classes
        self.classes('nd-select-button')
        
        if icon_only:
            self.classes('nd-mode-icon-only')
        
        # Structure the button to allow space-between alignment
        # unelevated, no-caps are now global defaults but keeping here doesn't hurt if we want to be explicit
        self.props(f'align="between" icon-right="{icon_right}"')
        
        # Internal state for rotation
        self._is_rotated = False
        
        # Bind click to toggle
        self.on('click', self.toggle_rotation)
        
        # Insert Custom Icon if provided
        if self._custom_icon_builder:
            self.style('overflow: visible')
            
            with self:
                with ui.element('div').classes('row no-wrap items-center nd-gap-2').style('overflow: visible'):
                    # Icon Container
                    self._icon_container = ui.element('div').classes('on-left flex flex-center order-first').style('overflow: visible')
                    with self._icon_container:
                         self._custom_icon_builder()
                    
                    # Manual Label
                    if not icon_only:
                        self._custom_label_element = ui.label(label)

    def refresh(self):
        """Re-renders the custom icon content if a builder is present."""
        if self._custom_icon_builder and self._icon_container:
            self._icon_container.clear()
            with self._icon_container:
                self._custom_icon_builder()

    def set_label(self, text: str):
        self._original_label = text
        if self._icon_only:
            return
            
        if self._custom_label_element:
            self._custom_label_element.text = text
        else:
            self.text = text
        
    def set_icon(self, icon: Optional[str]):
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
            self.classes(add='nd-state-rotated')
        else:
            self.classes(remove='nd-state-rotated')
