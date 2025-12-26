from nicegui import ui
from typing import Optional
from ....core.definitions import Texture

class texture_icon(ui.element):
    """
    A custom HTML/CSS icon that displays a visual representation of a texture.
    Features a circle styled like a card showing the texture's visual properties
    (opacity, shadows, glossy/flat effects).
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
        self.classes('-nd-c-texture-icon')
        self.style(f'width: {size}; height: {size}; position: relative;')
        
        # Create the circle element
        with self:
            circle = ui.element('div').classes('-nd-c-texture-icon__circle')
            
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
                circle.style('background: var(--nd-surface-layer);')
            
            # Apply shadows based on intensity
            if texture.shadows_enabled and texture.shadow_intensity > 0:
                shadow_size = 'md'
                if texture.shadow_intensity > 1.5:
                    shadow_size = 'xl'
                elif texture.shadow_intensity > 1.0:
                    shadow_size = 'lg'
                elif texture.shadow_intensity < 0.5:
                    shadow_size = 'sm'
                
                circle.style(f'box-shadow: var(--nd-shadow-{shadow_size}) !important;')
            
            # Apply border and transitions
            # Apply shape-based border and roundness
            border_width_px = f"{max(1.0, float(texture.border_width) * 0.5)}px"
            
            if texture.roundness == 0:
                border_radius = '0'
            elif texture.roundness >= 2.0:
                border_radius = '50%'
            else:
                radius_percent = (texture.roundness / 2.0) * 50
                border_radius = f'{radius_percent}%'

            circle.style(f'''
                position: relative;
                border: {border_width_px} solid rgba(255, 255, 255, 0.1);
                border-radius: {border_radius};
                width: 100%;
                height: 100%;
                overflow: hidden;
                transition: all var(--nd-transition-speed) ease;
            ''')
            
            with circle:
                 # Apply highlight density if applicable
                if texture.highlight_intensity > 0:
                    # Add a subtle gloss effect
                    ui.element('div').style(f'''
                        position: absolute;
                        top: 0; left: 0; width: 100%; height: 50%;
                        background: linear-gradient(to bottom, rgba(255,255,255,{0.1 * texture.highlight_intensity}), transparent);
                        pointer-events: none;
                        z-index: 10;
                    ''')
            
            # Add hover effect
            circle.classes('-nd-c-texture-icon__circle--interactive')

    @staticmethod
    def to_html(texture: Texture, *, size: str = "24px") -> str:
        """Returns the full HTML string for this component."""
        
        # Wrapper styles
        wrapper_style = f'width: {size}; height: {size}; position: relative; display: inline-block;'
        
        # Circle styles
        circle_style = ''
        
        # Opacity/Backdrop
        if texture.opacity < 1.0:
            circle_style += f'background: rgba(128, 128, 128, {texture.opacity}); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);'
        else:
             circle_style += 'background: var(--nd-surface-layer);'
             
        # Shadows
        if texture.shadows_enabled and texture.shadow_intensity > 0:
            shadow_size = 'md'
            if texture.shadow_intensity > 1.5:
                shadow_size = 'xl'
            elif texture.shadow_intensity > 1.0:
                shadow_size = 'lg'
            elif texture.shadow_intensity < 0.5:
                shadow_size = 'sm'
            circle_style += f' box-shadow: var(--nd-shadow-{shadow_size}) !important;'
            
        # Shape styling
        border_width_px = f"{max(1.0, float(texture.border_width) * 0.5)}px"
        
        if texture.roundness == 0:
            border_radius = '0'
        elif texture.roundness >= 2.0:
            border_radius = '50%'
        else:
            radius_percent = (texture.roundness / 2.0) * 50
            border_radius = f'{radius_percent}%'

        # Border and general
        circle_style += f' position: relative; border: {border_width_px} solid rgba(255, 255, 255, 0.1); border-radius: {border_radius}; width: 100%; height: 100%; overflow: hidden; transition: all var(--nd-transition-speed) ease;'
        
        # Clean up
        circle_style = circle_style.replace('\n', ' ').strip()
        
        # Gloss effect HTML if highlight_intensity is high
        gloss_html = ""
        if texture.highlight_intensity > 0:
             gloss_html = f'<div style="position: absolute; top: 0; left: 0; width: 100%; height: 50%; background: linear-gradient(to bottom, rgba(255,255,255,{0.1 * texture.highlight_intensity}), transparent); pointer-events: none; z-index: 10;"></div>'

        # The circle div
        circle_html = f'<div class="-nd-c-texture-icon__circle {texture.texture_cls}" style="{circle_style}">{gloss_html}</div>'
        
        return f'<div class="-nd-c-texture-icon" style="{wrapper_style}">{circle_html}</div>'
