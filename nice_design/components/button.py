from nicegui import ui
from typing import Optional, Literal

# Use generic names like "NDSButton" (Nice Design System Button)
class NDSButton(ui.button):
    def __init__(
        self, 
        text: str = '', 
        variant: Literal['primary', 'secondary', 'ghost'] = 'primary',
        icon: Optional[str] = None,
        on_click = None
    ):
        super().__init__(text, icon=icon, on_click=on_click)
        
        # Apply design system classes
        # We use .classes() to add our custom styles
        self.classes('nds-btn')
        self.classes(f'nds-btn--{variant}')
        
        # Remove Quasar defaults to prevent styling conflicts
        self.props('unelevated no-caps')
        
        # If ghost, we use the 'flat' prop as a base but our CSS takes over
        if variant == 'ghost':
            self.props('outline')