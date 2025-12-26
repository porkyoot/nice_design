from nicegui import ui
from ....core.definitions import Shape

class border_icon(ui.element):
    """
    A custom icon that displays the border style on a circle base.
    Ignores the shape's roundness and specifically visualizes the border thickness and style.
    """
    def __init__(
        self, 
        shape: Shape,
        *, 
        size: str = "24px"
    ):
        super().__init__('div')
        
        # Apply base styling
        self.classes('-nd-c-border-icon')
        self.style(f'width: {size}; height: {size}; position: relative; display: inline-block;')
        
        # Create the circle element
        with self:
            circle = ui.element('div')
            
            # Apply border width (use base_border to determine thickness)
            # Scaling it slightly for visibility at small sizes if necessary, 
            # but usually 1:1 is best for representation.
            border_width = f'{shape.base_border}px'
            
            circle.style(f'''
                width: 100%;
                height: 100%;
                border: {border_width} solid var(--nd-content-main);
                border-radius: 50%;
                box-sizing: border-box;
                background: transparent;
                transition: all var(--nd-transition-speed) ease;
            ''')
    
    @staticmethod
    def to_html(shape: Shape, *, size: str = "24px") -> str:
        """Returns the full HTML string for this component."""
        border_width = f'{shape.base_border}px'
        
        style = f'''
            width: {size}; 
            height: {size}; 
            border: {border_width} solid var(--nd-content-main);
            border-radius: 50%;
            display: inline-block;
            box-sizing: border-box;
            background: transparent;
            transition: all var(--nd-transition-speed) ease;
        '''.strip().replace('\n', ' ')
        
        return f'<div class="-nd-c-border-icon" style="{style}"></div>'
