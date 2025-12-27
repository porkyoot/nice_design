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
        rotate_icon: bool = False,
        *args, **kwargs
    ):
        super().__init__(text, icon=icon, on_click=on_click, *args, **kwargs)
        
        if variant == 'secondary':
            self.props('color=secondary')
            
        elif variant == 'ghost':
            self.props('outline color=primary')
            
        # Handle rotate_icon logic with a semantic class
        if rotate_icon:
            self.classes('nd-btn-rotate')
            self.on('click', lambda: self.classes(toggle='nd-btn-rotated'))