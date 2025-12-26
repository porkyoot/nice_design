from nicegui import ui
from typing import Optional
from ....core.definitions import Texture

class shape_icon(ui.element):
    """
    A custom HTML/CSS icon that displays a visual representation of a shape.
    Features a geometric element showing roundness and border width properties.
    (Category: Texture)
    """
    def __init__(
        self, 
        texture: Texture,
        *, 
        size: str = "24px"
    ):
        super().__init__('div')
        
        # Apply base styling
        self.classes('-nd-c-shape-icon')
        self.style(f'width: {size}; height: {size}; position: relative;')
        
        # Create the shape element
        with self:
            shape_elem = ui.element('div').classes('-nd-c-shape-icon__element')
            
            # Calculate border radius based on roundness
            if texture.roundness == 0:
                border_radius = '0'
            elif texture.roundness >= 2.0:
                border_radius = '50%'  # Circle
            else:
                # Scale between 0% and 50%
                radius_percent = (texture.roundness / 2.0) * 50
                border_radius = f'{radius_percent}%'
            
            # Apply border width
            border_width = f'{texture.border_width}px'
            
            # Style the element
            shape_elem.style(f'''
                width: 100%;
                height: 100%;
                border: {border_width} solid var(--nd-content-main);
                border-radius: {border_radius};
                background: transparent;
                transition: all var(--nd-transition-speed) ease;
            ''')
            
            # Add hover effect
            shape_elem.classes('-nd-c-shape-icon__element--interactive')
