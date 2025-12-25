from nicegui import ui
from typing import Optional

class icon(ui.icon):
    def __init__(
        self, 
        name: str, 
        *, 
        size: Optional[str] = None, 
        color: Optional[str] = None
    ):
        super().__init__(name, size=size, color=color)
        
        # Apply design system defaults if needed
        # We can add custom logic here if icons need specific shadows or transitions
        self.classes('-nd-c-icon')
