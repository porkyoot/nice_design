import importlib.metadata
import yaml
import copy
from pathlib import Path
from .definitions import Palette, Shape, Texture, Layout, Typography, Animation, Semantics

class ThemeRegistry:
    def __init__(self):
        self._palettes = {}
        self._semantics = {}
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

            # 2. Discover Semantics
            if hasattr(entry_points, 'select'):
                 semantics = entry_points.select(group='nice_design.semantics')
            else:
                 semantics = entry_points.get('nice_design.semantics', [])

            for ep in semantics:
                try:
                    plugin_obj = ep.load()
                    if isinstance(plugin_obj, Semantics):
                        print(f"Loaded External Semantics: {plugin_obj.name}")
                        self._semantics[plugin_obj.name] = plugin_obj
                except Exception as e:
                    print(f"Failed to load semantics {ep.name}: {e}")

            # 3. Discover Shapes
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

    def get_semantics(self, name: str, mode: str = None) -> Semantics:
        variations = self._semantics.get(name)
        if not variations:
            return None
            
        if mode:
            return variations.get(mode)
            
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
        semantics_templates = {}
        
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

        # 2. Semantics
        if 'semantics' in block and isinstance(block['semantics'], list):
            for s_data in block['semantics']:
                name = s_data.get('name')
                if not name: continue
                
                # Check inheritance
                if name in semantics_templates:
                    base = semantics_templates[name]
                    merged = copy.deepcopy(base)
                    merged.update(s_data)
                    s_data = merged
                
                semantics_templates[name] = s_data
                self._register_component(s_data, Semantics, self._semantics)
        
        # 3. Shapes
        if 'shapes' in block and isinstance(block['shapes'], list):
            for data in block['shapes']:
                self._register_component(data, Shape, self._shapes)
                
        # 4. Textures
        if 'textures' in block and isinstance(block['textures'], list):
            for data in block['textures']:
                self._register_component(data, Texture, self._textures)
                
        # 5. Typographies
        if 'typographies' in block and isinstance(block['typographies'], list):
            for data in block['typographies']:
                self._register_component(data, Typography, self._typographies)
                
        # 6. Animations
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
            elif cls is Semantics:
                # Special storage for Semantics: name -> mode -> instance (since they can be dark/light)
                # Note: Semantics might not have 'mode' explicitly if it's not in the data? 
                # Wait, if Semantics are mode-specific (which they are), they should have a 'mode' field in YAML?
                # The user request didn't explicitly say Semantics has a 'mode' field in definitions.py. 
                # Let's check definitions.py again.
                # I defined `Semantics` without a `mode` field! 
                # This could be a problem if I want to look them up by mode. 
                # However, the `Palette` has `mode`. 
                # Usually Semantics come in pairs with Palette. 
                # If Semantics doesn't have mode, how do I distinguish Solarized Dark vs Light Semantics?
                # Ah, I should probably add `mode` to Semantics or rely on unique names like "solarized-dark", "solarized-light".
                # The `Palette` has `name` and `mode`.
                # If I look at `presets.py`, `SOLARIZED_SEMANTICS` has `name="solarized-dark"`. 
                # So the name itself carries the mode info implicitly?
                # But `ThemeRegistry.get_palette` takes `name` and `mode`.
                # If I want `get_semantics("solarized", "dark")`, I need to structure it.
                # Let's assume Semantics has a 'mode' if I want to store it like Palette.
                # But I didn't add 'mode' to Semantics dataclass in `definitions.py`. 
                # I should probably just store it by name for now, or check if I should add 'mode'.
                # Re-reading `definitions.py`:
                # @dataclass class Semantics: name: str = "default" ...
                # It does NOT have mode.
                # But `SOLARIZED_SEMANTICS` in `presets.py` was constructed with just name="solarized-dark".
                # So logic suggests `get_semantics` will just take a name.
                # Wait, if I have `themes/solarized.yaml` with:
                # palettes: [{name: solarized, mode: dark}, {name: solarized, mode: light}]
                # and semantics? 
                # IF I want to share the "solarized" name but have different semantics for dark/light, I absolutely need `mode` in Semantics, OR use different names like "solarized-dark-semantics".
                # Given `Palette` has mode, `Semantics` should probably too. 
                # I'll add `mode` to Semantics dataclass in `definitions.py` to be safe and consistent.
                
                # FOR NOW in this tool call, I will assume I will add `mode` to Semantics in a follow up, or construct it.
                # Let's assume Semantics SHOULD have mode. 
                # I will modify `definitions.py` right after this to add `mode` to Semantics.
                
                # So here, I will treat Semantics like Palette.
                if not hasattr(instance, 'mode'):
                     # Fallback if I haven't added it yet
                     storage[instance.name] = instance
                     print(f"Registered Semantics: {instance.name}")
                else:
                    if instance.name not in storage:
                        storage[instance.name] = {}
                    storage[instance.name][instance.mode] = instance
                    print(f"Registered Semantics: {instance.name} ({instance.mode})")

            else:
                storage[instance.name] = instance
                print(f"Registered {cls.__name__}: {instance.name}")
                
        except Exception as e:
            print(f"Failed to register {cls.__name__}: {e}")