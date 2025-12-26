from nicegui import ui
from ....core.definitions import Palette, Texture, Typography, Layout
from .palette_icon import palette_icon

class theme_icon(ui.element):
    """
    A comprehensive icon that displays a visual representation of a complete theme.
    Combines palette, texture, typography, and layout by composing visuals.
    (Note: Typography and Layout are represented subtly or through spacing).
    """
    def __init__(
        self, 
        palette: Palette,
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
            # Ensure container fills the parent
            texture_container.style('width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;')
            
            # Apply texture opacity 
            if texture.opacity < 1.0:
                texture_container.style(f'opacity: {texture.opacity};')
            
            # Apply shadows based on texture
            if texture.shadows_enabled and texture.shadow_intensity > 0:
                shadow_size = 'md'
                if texture.shadow_intensity > 1.5:
                    shadow_size = 'xl'
                elif texture.shadow_intensity > 1.0:
                    shadow_size = 'lg'
                elif texture.shadow_intensity < 0.5:
                    shadow_size = 'sm'
                
                texture_container.style(f'filter: drop-shadow(var(--nd-shadow-{shadow_size}));')
            
            # Apply shape-based border and roundness (from Texture category)
            border_width_px = f"{max(1.0, float(texture.border_width) * 0.5)}px"  # Scaled for visual balance
            
            # Calculate border radius based on texture.roundness
            if texture.roundness == 0:
                border_radius = '0'
            elif texture.roundness >= 2.0:
                border_radius = '50%'  # Circle
            else:
                radius_percent = (texture.roundness / 2.0) * 50
                border_radius = f'{radius_percent}%'
            
            # The palette icon as the core visual
            with texture_container:
                container = ui.element('div').style(f'''
                    position: relative;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: {border_radius};
                    border: {border_width_px} solid rgba(255, 255, 255, 0.15);
                    overflow: hidden;
                    transition: all var(--nd-transition-speed) ease;
                ''')
                container.classes('-nd-c-theme-icon__palette-container')
                
                with container:
                    # Reuse the palette_icon for color visualization
                    palette_icon(palette, size=size, circular=False)

                    # Apply highlight density if applicable - moved here to be inside clipped container
                    if texture.highlight_intensity > 0:
                        # Add a subtle gloss effect
                        ui.element('div').style(f'''
                            position: absolute;
                            top: 0; left: 0; width: 100%; height: 50%;
                            background: linear-gradient(to bottom, rgba(255,255,255,{0.1 * texture.highlight_intensity}), transparent);
                            pointer-events: none;
                            z-index: 10;
                        ''')

    @staticmethod
    def to_html(
        palette: Palette,
        texture: Texture,
        *, 
        size: str = "24px"
    ) -> str:
        """Returns the full HTML string for this component."""
        
        # Texture styling
        texture_style = 'width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;'
        if texture.opacity < 1.0:
            texture_style += f' opacity: {texture.opacity};'
            
        if texture.shadows_enabled and texture.shadow_intensity > 0:
            shadow_size = 'md'
            if texture.shadow_intensity > 1.5:
                shadow_size = 'xl'
            elif texture.shadow_intensity > 1.0:
                shadow_size = 'lg'
            elif texture.shadow_intensity < 0.5:
                shadow_size = 'sm'
            
            texture_style += f' filter: drop-shadow(var(--nd-shadow-{shadow_size}));'
            
        # Shape styling (from Texture)
        border_width_px = f"{max(1.0, float(texture.border_width) * 0.5)}px"
        
        if texture.roundness == 0:
            border_radius = '0'
        elif texture.roundness >= 2.0:
            border_radius = '50%'
        else:
            radius_percent = (texture.roundness / 2.0) * 50
            border_radius = f'{radius_percent}%'
            
        container_style = f'''
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: {border_radius};
            border: {border_width_px} solid rgba(255, 255, 255, 0.15);
            overflow: hidden;
            transition: all var(--nd-transition-speed) ease;
        '''.strip().replace('\n', ' ')

        # Inner palette icon HTML
        inner_html = palette_icon.to_html(palette, size=size, circular=False)
        
        # Gloss effect HTML if highlight_intensity is high
        gloss_html = ""
        if texture.highlight_intensity > 0:
             gloss_html = f'<div style="position: absolute; top: 0; left: 0; width: 100%; height: 50%; background: linear-gradient(to bottom, rgba(255,255,255,{0.1 * texture.highlight_intensity}), transparent); pointer-events: none; z-index: 10;"></div>'

        # Inner Container (Palette Container)
        html_palette_container = f'<div class="-nd-c-theme-icon__palette-container" style="{container_style}">{inner_html}{gloss_html}</div>'
        
        # Texture Container
        html_texture_container = f'<div class="nd-theme-icon__container" style="{texture_style}">{html_palette_container}</div>'
        
        # Outer Wrapper
        outer_style = f'width: {size}; height: {size}; position: relative; display: inline-flex; align-items: center; justify-content: center;'
        return f'<div class="-nd-c-theme-icon" style="{outer_style}">{html_texture_container}</div>'
