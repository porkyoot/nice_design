import importlib.metadata
from .definitions import Palette, Shape, Texture

class ThemeRegistry:
    def __init__(self):
        self._palettes = {}
        self._shapes = {}
        self._textures = {}
        
    def discover_plugins(self):
        """Scans the installed python environment for plugins."""
        
        # 1. Discover Palettes
        # We look for the group 'nice_design.palettes'
        try:
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

            # 2. Discover Shapes
            if hasattr(entry_points, 'select'):
                 shapes = entry_points.select(group='nice_design.shapes')
            else:
                 shapes = entry_points.get('nice_design.shapes', [])

            for ep in shapes:
                try:
                    shape_obj = ep.load()
                    if isinstance(shape_obj, Shape):
                        print(f"Loaded External Shape: {shape_obj.name}")
                        self._shapes[shape_obj.name] = shape_obj
                except Exception as e:
                    print(f"Failed to load shape {ep.name}: {e}")

            # 3. Discover Textures
            if hasattr(entry_points, 'select'):
                 textures = entry_points.select(group='nice_design.textures')
            else:
                 textures = entry_points.get('nice_design.textures', [])

            for ep in textures:
                try:
                    texture_obj = ep.load()
                    if isinstance(texture_obj, Texture):
                        print(f"Loaded External Texture: {texture_obj.name}")
                        self._textures[texture_obj.name] = texture_obj
                except Exception as e:
                    print(f"Failed to load texture {ep.name}: {e}")
        except Exception as e:
            print(f"Error during plugin discovery: {e}")

    def get_palette(self, name: str) -> Palette:
        return self._palettes.get(name)

    def get_shape(self, name: str) -> Shape:
        return self._shapes.get(name)

    def get_texture(self, name: str) -> Texture:
        return self._textures.get(name)

    def list_palettes(self) -> list[str]:
        return list(self._palettes.keys())

    def list_shapes(self) -> list[str]:
        return list(self._shapes.keys())

    def list_textures(self) -> list[str]:
        return list(self._textures.keys())