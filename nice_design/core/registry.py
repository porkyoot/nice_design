import importlib.metadata
import yaml
import copy
from pathlib import Path
from .definitions import Palette, Shape, Texture, Layout, Typography, Animation

class ThemeRegistry:
    def __init__(self):
        self._palettes = {}
        self._shapes = {}
        self._textures = {}
        self._layouts = {}
        self._typographies = {}
        self._animations = {}
        
    def discover_plugins(self):
        """Scans both entry points and local YAML files."""
        self._discover_entry_points()
        self._discover_yaml_themes()

    def _discover_entry_points(self):
        # 1. Discover Palettes
        try:
            entry_points = importlib.metadata.entry_points()
            
            if hasattr(entry_points, 'select'):
                 palettes = entry_points.select(group='nice_design.palettes')
            else:
                 palettes = entry_points.get('nice_design.palettes', [])

            for ep in palettes:
                try:
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

    def _discover_yaml_themes(self):
        try:
            # Look in ../themes relative to this file
            root_dir = Path(__file__).parent.parent
            themes_dir = root_dir / "themes"
            
            if not themes_dir.exists():
                return

            for yaml_file in themes_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, 'r') as f:
                        data = yaml.safe_load(f)
                        self._process_yaml_data(data)
                        print(f"Loaded YAML Theme: {yaml_file.name}")
                except Exception as e:
                    print(f"Failed to load YAML file {yaml_file.name}: {e}")
        except Exception as e:
             print(f"Error during YAML discovery: {e}")

    def get_palette(self, name: str, mode: str = None) -> Palette:
        # Palettes are stored as dict: name -> mode -> Palette
        variations = self._palettes.get(name)
        if not variations:
            return None
        
        if mode:
            return variations.get(mode)
        
        # Default to 'dark', then 'light', then any
        return variations.get('dark') or variations.get('light') or next(iter(variations.values()))

    def get_shape(self, name: str) -> Shape:
        return self._shapes.get(name)

    def get_texture(self, name: str) -> Texture:
        return self._textures.get(name)

    def get_layout(self, name: str) -> Layout:
        return self._layouts.get(name)

    def get_typography(self, name: str) -> Typography:
        return self._typographies.get(name)

    def get_animation(self, name: str) -> Animation:
        return self._animations.get(name)

    def list_palettes(self) -> list[str]:
        return list(self._palettes.keys())

    def list_shapes(self) -> list[str]:
        return list(self._shapes.keys())

    def list_textures(self) -> list[str]:
        return list(self._textures.keys())

    def _process_yaml_data(self, data):
        if not isinstance(data, dict): return
        
        if 'themes' in data and isinstance(data['themes'], list):
            for theme_block in data['themes']:
                self._process_theme_block(theme_block)
        else:
            # Fallback for old/flat structure (optional)
            self._process_theme_block(data)

    def _process_theme_block(self, block):
        # Local inheritance context for this block
        # name -> properties_dict
        palette_templates = {} 
        
        # 1. Palettes (Nested under 'palettes' list)
        if 'palettes' in block and isinstance(block['palettes'], list):
            for p_data in block['palettes']:
                name = p_data.get('name')
                if not name: continue
                
                # Check inheritance
                if name in palette_templates:
                    # Merge: start with base, update with new
                    base = palette_templates[name]
                    merged = copy.deepcopy(base)
                    merged.update(p_data)
                    p_data = merged
                
                # Update template for future inheritors
                palette_templates[name] = p_data
                
                # Register
                self._register_component(p_data, Palette, self._palettes)
        
        # 2. Shapes
        if 'shapes' in block and isinstance(block['shapes'], list):
            for data in block['shapes']:
                self._register_component(data, Shape, self._shapes)
                
        # 3. Textures
        if 'textures' in block and isinstance(block['textures'], list):
            for data in block['textures']:
                self._register_component(data, Texture, self._textures)
                
        # 4. Typographies
        if 'typographies' in block and isinstance(block['typographies'], list):
            for data in block['typographies']:
                self._register_component(data, Typography, self._typographies)
                
        # 5. Animations
        if 'animations' in block and isinstance(block['animations'], list):
            for data in block['animations']:
                self._register_component(data, Animation, self._animations)

    def _register_component(self, data, cls, storage):
        try:
            instance = cls(**data)
            
            if cls is Palette:
                # Special storage for Palettes: name -> mode -> instance
                if instance.name not in storage:
                    storage[instance.name] = {}
                storage[instance.name][instance.mode] = instance
                print(f"Registered Palette: {instance.name} ({instance.mode})")
            else:
                storage[instance.name] = instance
                print(f"Registered {cls.__name__}: {instance.name}")
                
        except Exception as e:
            print(f"Failed to register {cls.__name__}: {e}")