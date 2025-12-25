from nicegui import ui
from typing import Optional, Literal

# Mirroring NiceGUI's API structure
class button(ui.button):
    def __init__(
        self, 
        text: str = '', 
        variant: Literal['primary', 'secondary', 'ghost'] = 'primary',
        icon: Optional[str] = None,
        on_click = None,
        rotate_icon: bool = False
    ):
        super().__init__(text, icon=icon, on_click=on_click)
        
        # Apply design system classes
        # We use .classes() to add our custom styles
        self.classes('-nd-c-btn')
        self.classes(f'-nd-c-btn--{variant}')
        
        # Remove Quasar defaults to prevent styling conflicts
        self.props('unelevated no-caps')
        
        # If ghost, we use the 'flat' prop as a base but our CSS takes over
        if variant == 'ghost':
            self.props('outline')

        if rotate_icon:
            self.classes('-nd-c-btn--rotate')
            self.on('click', lambda: self.classes(toggle='-nd-c-btn--rotated'))