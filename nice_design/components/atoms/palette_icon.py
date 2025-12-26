from nicegui import ui
from typing import Optional, Dict
from nice_design.core.definitions import Palette, Semantics

class palette_icon(ui.element):
    """
    A custom SVG icon that displays a visual representation of a theme palette.
    Features two half-disks in the center (background and foreground) surrounded by 
    arcs of the 8 named colors.
    """
    def __init__(
        self, 
        palette: Palette,
        semantics: Semantics,
        *, 
        size: str = "24px",
        circular: bool = True
    ):
        super().__init__('svg')
        
        # Extract colors from the palette and semantics
        background_color = semantics.surface_base
        foreground_color = semantics.content_main
        colors = palette.colors
        
        # Set SVG attributes
        self._props['viewBox'] = '0 0 24 24'
        self._props['xmlns'] = 'http://www.w3.org/2000/svg'
        self.classes('-nd-c-theme-icon')
        self.style(f'width: {size}; height: {size};')
        
        if circular:
            self.style('border-radius: 50%;')
        
        # Generate the SVG content
        self._generate_icon(background_color, foreground_color, colors)
    
    def _generate_icon(self, bg_color: str, fg_color: str, colors: Dict[str, str]):
        """Generate the SVG elements for the theme icon."""
        
        # Color order for the arcs (clockwise from top)
        color_names = ['blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'magenta', 'purple']
        
        # Center point
        cx, cy = 12, 12
        
        # Radii
        outer_radius = 22  # Extend beyond viewport to fill corners (clipped by container)
        inner_radius = 6  # Smaller inner radius makes arcs thicker
        center_radius = inner_radius  # Make center fill to the arcs with no gap
        
        # Calculate arc segments (8 segments, 360/8 = 45 degrees each)
        segment_angle = 45
        
        svg_content = []
        
        # Draw the 8 colored arcs
        for i, color_name in enumerate(color_names):
            color = colors.get(color_name, '#888888')
            
            # Calculate start and end angles (in degrees, starting from top)
            start_angle = i * segment_angle - 90  # -90 to start from top
            end_angle = start_angle + segment_angle
            
            # Convert to radians
            import math
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calculate arc path points
            x1_outer = cx + outer_radius * math.cos(start_rad)
            y1_outer = cy + outer_radius * math.sin(start_rad)
            x2_outer = cx + outer_radius * math.cos(end_rad)
            y2_outer = cy + outer_radius * math.sin(end_rad)
            
            x1_inner = cx + inner_radius * math.cos(start_rad)
            y1_inner = cy + inner_radius * math.sin(start_rad)
            x2_inner = cx + inner_radius * math.cos(end_rad)
            y2_inner = cy + inner_radius * math.sin(end_rad)
            
            # Create arc path
            path_d = f"""
                M {x1_outer:.2f},{y1_outer:.2f}
                A {outer_radius},{outer_radius} 0 0 1 {x2_outer:.2f},{y2_outer:.2f}
                L {x2_inner:.2f},{y2_inner:.2f}
                A {inner_radius},{inner_radius} 0 0 0 {x1_inner:.2f},{y1_inner:.2f}
                Z
            """.strip()
            
            svg_content.append(f'<path d="{path_d}" fill="{color}" />')
        
        # Draw center background half-disk (left side)
        svg_content.append(f'''
            <path d="M {cx},{cy - center_radius} 
                     A {center_radius},{center_radius} 0 0 0 {cx},{cy + center_radius} 
                     L {cx},{cy} Z" 
                  fill="{bg_color}" />
        '''.strip())
        
        # Draw center foreground half-disk (right side)
        svg_content.append(f'''
            <path d="M {cx},{cy - center_radius} 
                     A {center_radius},{center_radius} 0 0 1 {cx},{cy + center_radius} 
                     L {cx},{cy} Z" 
                  fill="{fg_color}" />
        '''.strip())
        
        # Add a subtle center line
        svg_content.append(f'''
            <line x1="{cx}" y1="{cy - center_radius}" 
                  x2="{cx}" y2="{cy + center_radius}" 
                  stroke="rgba(255,255,255,0.2)" 
                  stroke-width="0.5" />
        '''.strip())
        
        # Set the SVG content
        self._props['innerHTML'] = '\n'.join(svg_content)

