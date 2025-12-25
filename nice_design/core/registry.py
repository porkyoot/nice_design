import importlib.metadata
from .definitions import Palette, Skin

class ThemeRegistry:
    def __init__(self):
        self._palettes = {}
        self._skins = {}
        
    def discover_plugins(self):
        """Scans the installed python environment for plugins."""
        
        # 1. Discover Palettes
        # We look for the group 'nice_design.palettes'
        entry_points = importlib.metadata.entry_points()
        
        # Python 3.10+ syntax safely accessing the group
        if hasattr(entry_points, 'select'):
             palettes = entry_points.select(group='nice_design.palettes')
        else:
             palettes = entry_points.get('nice_design.palettes', [])

        for ep in palettes:
            try:
                # The entry point loads the Plugin Function or Object
                plugin_obj = ep.load()
                if isinstance(plugin_obj, Palette):
                    print(f"Loaded External Palette: {plugin_obj.name}")
                    self._palettes[plugin_obj.name] = plugin_obj
            except Exception as e:
                print(f"Failed to load palette {ep.name}: {e}")

        # 2. Discover Skins (same logic)
        if hasattr(entry_points, 'select'):
             skins = entry_points.select(group='nice_design.skins')
        else:
             skins = entry_points.get('nice_design.skins', [])

        for ep in skins:
            try:
                skin_obj = ep.load()
                if isinstance(skin_obj, Skin):
                    self._skins[skin_obj.name] = skin_obj
            except Exception:
                pass

    def get_palette(self, name: str) -> Palette:
        return self._palettes.get(name)