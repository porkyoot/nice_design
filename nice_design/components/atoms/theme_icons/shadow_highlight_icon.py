from nicegui import ui
from ....core.definitions import Texture

class shadow_highlight_icon(ui.element):
    """
    A custom icon that displays the shadow and highlight strength on a circle base.
    Visualizes the depth/elevation of the theme.
    """
    def __init__(
        self, 
        texture: Texture,
        *, 
        size: str = "24px"
    ):
        super().__init__('div')
        
        # Apply base styling
        self.classes('-nd-c-shadow-icon')
        self.style(f'width: {size}; height: {size}; position: relative; display: inline-block;')
        
        # Create the circle element
        with self:
            circle = ui.element('div')
            
            # Determine shadow size based on intensity
            shadow_style = 'none'
            if texture.shadows and texture.shadow_intensity > 0:
                shadow_size = 'md'
                if texture.shadow_intensity > 1.5:
                    shadow_size = 'xl'
                elif texture.shadow_intensity > 1.0:
                    shadow_size = 'lg'
                elif texture.shadow_intensity < 0.5:
                    shadow_size = 'sm'
                
                shadow_style = f'var(--nd-shadow-{shadow_size})'

            # Calculate a simulated highlight opacity based on shadow intensity
            # Stronger shadows usually imply stronger light source -> stronger highlight
            highlight_opacity = 0.1 + (texture.shadow_intensity * 0.2)
            if not texture.shadows:
                highlight_opacity = 0.0
                
            # Inner highlight (inset shadow) simulation
            highlight_style = f'inset 1px 1px 2px rgba(255, 255, 255, {highlight_opacity})'

            circle.style(f'''
                width: 100%;
                height: 100%;
                background: var(--nd-surface-layer);
                border-radius: 50%;
                box-shadow: {shadow_style}, {highlight_style};
                transition: all var(--nd-transition-speed) ease;
            ''')
    
    @staticmethod
    def to_html(texture: Texture, *, size: str = "24px") -> str:
        """Returns the full HTML string for this component."""
        
        shadow_style = 'none'
        if texture.shadows and texture.shadow_intensity > 0:
            shadow_size = 'md'
            if texture.shadow_intensity > 1.5:
                shadow_size = 'xl'
            elif texture.shadow_intensity > 1.0:
                shadow_size = 'lg'
            elif texture.shadow_intensity < 0.5:
                shadow_size = 'sm'
            
            shadow_style = f'var(--nd-shadow-{shadow_size})'
            
        highlight_opacity = 0.1 + (texture.shadow_intensity * 0.2)
        if not texture.shadows:
            highlight_opacity = 0.0
            
        highlight_style = f'inset 1px 1px 2px rgba(255, 255, 255, {highlight_opacity})'

        style = f'''
            width: {size}; 
            height: {size}; 
            background: var(--nd-surface-layer);
            border-radius: 50%;
            display: inline-block;
            box-shadow: {shadow_style}, {highlight_style};
            transition: all var(--nd-transition-speed) ease;
        '''.strip().replace('\n', ' ')
        
        return f'<div class="-nd-c-shadow-icon" style="{style}"></div>'
