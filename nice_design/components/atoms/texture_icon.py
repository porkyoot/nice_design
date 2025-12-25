from nicegui import ui
from typing import Optional
from ...core.definitions import Texture

class texture_icon(ui.element):
    """
    A custom HTML/CSS icon that displays a visual representation of a texture.
    Features a circle styled like a card showing the texture's visual properties
    (opacity, shadows, glossy/flat effects).
    """
    def __init__(
        self, 
        texture: Texture,
        *, 
        size: str = "24px"
    ):
        super().__init__('div')
        
        # Apply base styling
        self.classes('nd-texture-icon')
        self.style(f'width: {size}; height: {size}; position: relative;')
        
        # Create the circle element
        with self:
            circle = ui.element('div').classes('nd-texture-icon__circle')
            
            # Apply texture class
            circle.classes(texture.texture_cls)
            
            # Apply opacity
            if texture.opacity < 1.0:
                # Create glassmorphism effect
                circle.style(f'''
                    background: rgba(128, 128, 128, {texture.opacity});
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                ''')
            else:
                # Solid background
                circle.style('background: var(--nd-background-2);')
            
            # Apply shadows based on intensity
            if texture.shadows and texture.shadow_intensity > 0:
                shadow_size = 'md'
                if texture.shadow_intensity > 1.5:
                    shadow_size = 'xl'
                elif texture.shadow_intensity > 1.0:
                    shadow_size = 'lg'
                elif texture.shadow_intensity < 0.5:
                    shadow_size = 'sm'
                
                circle.style(f'box-shadow: var(--nd-shadow-{shadow_size}) !important;')
            
            # Apply border and transitions
            circle.style('''
                border: var(--nd-border-sm) solid rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                width: 100%;
                height: 100%;
                transition: all var(--nd-transition-speed) ease;
            ''')
            
            # Add hover effect to show transition
            circle.classes('nd-texture-icon__circle--interactive')

