from .definitions import Theme
from typing import Optional

class StatusStyles:
    """
    Logic layer to map status strings to theme semantic colors.
    """
    @staticmethod
    def get_color(theme: Theme, status: str) -> str:
        # 1. Try semantic status (error, warning, success, info)
        # 1. Try semantic status (error, warning, success, info)
        if status == 'success': return theme.semantics.success
        if status == 'error': return theme.semantics.error
        if status == 'warning': return theme.semantics.warning
        if status == 'info': return theme.semantics.info
        
        # 2. Fallback to palette colors if status matches a color name
        if status in theme.palette.colors:
            return theme.palette.colors[status]
            
        # 3. Default fallback
        return theme.semantics.secondary

class CategoryStyles:
    """
    Logic layer to map file categories to theme colors.
    """
    @staticmethod
    def get_color(theme: Theme, category: str) -> str:
        category = category.lower()
        colors = theme.palette.colors
        
        # Map common categories to palette colors
        # Adjust these mappings as needed or move to a config
        mapping = {
            'image': 'purple',
            'video': 'magenta',
            'audio': 'cyan',
            'document': 'blue',
            'archive': 'red',
            'folder': 'yellow',
            'unknown': 'base' 
        }
        
        color_name = mapping.get(category)
        
        if color_name and color_name in colors:
            return colors[color_name]
            
        return theme.semantics.secondary
