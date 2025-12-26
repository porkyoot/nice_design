"""Utility functions for the NiceDesign core."""

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple.
    
    Args:
        hex_color: Hex color string (e.g., '#FF5733' or 'FF5733')
        
    Returns:
        Tuple of (r, g, b) values as integers (0-255)
    """
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join([c*2 for c in h])
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
