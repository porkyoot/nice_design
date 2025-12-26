from nicegui import ui
from ...core.definitions import Palette, Shape, Texture, Semantics
from .palette_icon import palette_icon

class theme_icon(ui.element):
    """
    A comprehensive icon that displays a visual representation of a complete theme.
    Combines palette (colors), shape (geometry), and texture (visual effects) by
    composing the other icon components together.
    """
    def __init__(
        self, 
        palette: Palette,
        semantics: Semantics,
        shape: Shape,
        texture: Texture,
        *, 
        size: str = "24px"
    ):
        super().__init__('div')
        
        # Apply base styling
        self.classes('-nd-c-theme-icon')
        self.style(f'width: {size}; height: {size}; position: relative; display: inline-flex; align-items: center; justify-content: center;')
        
        # Create a container with texture effects applied
        with self:
            # Apply texture-based effects to the container
            texture_container = ui.element('div').classes('nd-theme-icon__container')
            
            # Apply texture opacity 
            if texture.opacity < 1.0:
                texture_container.style(f'opacity: {texture.opacity};')
            
            # Apply shadows based on texture
            if texture.shadows and texture.shadow_intensity > 0:
                shadow_size = 'md'
                if texture.shadow_intensity > 1.5:
                    shadow_size = 'xl'
                elif texture.shadow_intensity > 1.0:
                    shadow_size = 'lg'
                elif texture.shadow_intensity < 0.5:
                    shadow_size = 'sm'
                
                texture_container.style(f'filter: drop-shadow(var(--nd-shadow-{shadow_size}));')
            
            # Apply shape-based border and roundness
            border_width = f'{shape.base_border * 0.5}px'  # Scaled for visual balance
            
            # Calculate border radius based on shape.roundness
            # roundness = 0.0 -> sharp (no radius)
            # roundness = 1.0 -> standard (medium radius)
            # roundness = 2.0+ -> very round (approaching circle)
            if shape.roundness == 0:
                border_radius = '0'
            elif shape.roundness >= 2.0:
                border_radius = '50%'  # Circle
            else:
                # Scale border radius with roundness
                radius_value = f'{shape.roundness * 8}px'  # Base of 8px per roundness unit
                border_radius = radius_value
            
            # The palette icon as the core visual
            with texture_container:
                container = ui.element('div').style(f'''
                    position: relative;
                    width: 100%;
                    height: 100%;
                    border-radius: {border_radius};
                    border: {border_width} solid rgba(255, 255, 255, 0.15);
                    overflow: hidden;
                    transition: all var(--nd-transition-speed) ease;
                ''')
                container.classes('-nd-c-theme-icon__palette-container')
                
                with container:
                    # Reuse the palette_icon for color visualization
                    palette_icon(palette, semantics, size=size, circular=False)
