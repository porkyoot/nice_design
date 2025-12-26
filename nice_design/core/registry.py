import importlib.metadata
import yaml
import copy
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from .definitions import Palette, Texture, Layout, Typography, Theme

class ThemeRegistry:
    def __init__(self):
        self._palettes = {}    # name -> {mode: Palette}
        self._textures = {}    # name -> Texture
        self._layouts = {}     # name -> Layout
        self._typographies = {} # name -> Typography
        self._themes = {}      # name -> Theme (Combination)
        
        self._font_css = [] # Generated CSS for fonts
        self._texture_css = [] # Generated CSS for textures
        
    def discover_plugins(self):
        """Scans both entry points and local theme folders."""
        self._discover_entry_points()
        self._discover_theme_folders()

    def _discover_entry_points(self):
        entry_points = importlib.metadata.entry_points()
        
        # Discover through entry points
        self._load_entry_point_group(entry_points, 'nice_design.palettes', Palette, self._palettes)
        self._load_entry_point_group(entry_points, 'nice_design.textures', Texture, self._textures)
        self._load_entry_point_group(entry_points, 'nice_design.layouts', Layout, self._layouts)
        self._load_entry_point_group(entry_points, 'nice_design.typographies', Typography, self._typographies)

    def _load_entry_point_group(self, entry_points, group, cls, storage):
        try:
            if hasattr(entry_points, 'select'):
                 items = entry_points.select(group=group)
            else:
                 items = entry_points.get(group, [])

            for ep in items:
                try:
                    obj = ep.load()
                    if isinstance(obj, cls):
                        self._register_instance(obj, storage)
                except Exception as e:
                    print(f"Failed to load {group} {ep.name}: {e}")
        except Exception as e:
            print(f"Error during {group} plugin discovery: {e}")

    def _discover_theme_folders(self):
        """Discovers themes organized by folders: palettes/, textures/, layouts/, fonts/."""
        try:
            root_dir = Path(__file__).parent.parent
            themes_dir = root_dir / "themes"
            
            if not themes_dir.exists():
                return

            # Discover pillars first so bundles can reference them
            self._discover_palettes(themes_dir / "palettes")
            self._discover_layouts(themes_dir / "layouts")
            self._discover_textures(themes_dir / "textures")
            self._discover_fonts(themes_dir / "fonts")
            
            # Discover bundles and named themes in the root themes/ folder
            self._discover_bundles(themes_dir)
            
        except Exception as e:
             print(f"Error during theme folder discovery: {e}")

    def _discover_palettes(self, path: Path):
        if not path.exists(): return
        for yaml_file in path.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        for p_data in data:
                            self._register_raw_data(p_data, Palette, self._palettes)
                    elif isinstance(data, dict):
                        if 'palettes' in data:
                             for p_data in data['palettes']:
                                 self._register_raw_data(p_data, Palette, self._palettes)
                        else:
                             self._register_raw_data(data, Palette, self._palettes)
            except Exception as e:
                print(f"Failed to load palette {yaml_file.name}: {e}")

    def _discover_layouts(self, path: Path):
        if not path.exists(): return
        for yaml_file in path.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        for d in data: self._register_raw_data(d, Layout, self._layouts)
                    else:
                        self._register_raw_data(data, Layout, self._layouts)
            except Exception as e:
                print(f"Failed to load layout {yaml_file.name}: {e}")

    def _discover_textures(self, path: Path):
        if not path.exists(): return
        for css_file in path.glob("*.css"):
            name = css_file.stem
            texture_cls = f"-nd-t-{name}"
            instance = Texture(name=name, texture_cls=texture_cls)
            self._register_instance(instance, self._textures)
            with open(css_file, 'r') as f:
                self._texture_css.append(f.read())

        for yaml_file in path.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        for d in data: self._register_raw_data(d, Texture, self._textures)
                    else:
                        self._register_raw_data(data, Texture, self._textures)
            except Exception as e:
                print(f"Failed to load texture metadata {yaml_file.name}: {e}")

    def _discover_fonts(self, path: Path):
        if not path.exists(): return
        self._font_css = []
        extensions = ('.ttf', '.otf', '.woff', '.woff2')
        for font_file in path.iterdir():
            if font_file.suffix.lower() in extensions:
                font_name = font_file.stem.replace('-', ' ').replace('_', ' ').title()
                family_name = font_name.replace(' ', '')
                
                instance = Typography(name=font_name, font_main=f"'{family_name}', sans-serif")
                self._register_instance(instance, self._typographies)
                
                ext = font_file.suffix.lower()[1:]
                fmt = "truetype" if ext == "ttf" else "opentype" if ext == "otf" else ext
                
                css = f"""
                @font-face {{
                    font-family: '{family_name}';
                    src: url('/nd_themes/fonts/{font_file.name}') format('{fmt}');
                    font-weight: normal;
                    font-style: normal;
                }}
                """
                self._font_css.append(css)

    def _discover_bundles(self, path: Path):
        """Looks for YAML files that specify 'theme' combinations or pillar lists."""
        if not path.exists(): return
        for yaml_file in path.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if not isinstance(data, dict): continue
                    
                    # 1. Check for pillar lists (Legacy Bundle)
                    if 'palettes' in data:
                        for p_data in data['palettes']: self._register_raw_data(p_data, Palette, self._palettes)
                    if 'textures' in data:
                        for d in data['textures']: self._register_raw_data(d, Texture, self._textures)
                    if 'layouts' in data:
                        for d in data['layouts']: self._register_raw_data(d, Layout, self._layouts)
                    if 'typographies' in data:
                        for d in data['typographies']: self._register_raw_data(d, Typography, self._typographies)
                        
                    # 2. Check for 'theme' definition (The Combination Pillar)
                    if 'theme' in data:
                        theme_data = data['theme']
                        theme_name = theme_data.get('name', yaml_file.stem)
                        # Store the raw combination data; we'll resolve it when requested
                        self._themes[theme_name] = theme_data
                        
            except Exception as e:
                print(f"Failed to load bundle {yaml_file.name}: {e}")

    def get_theme(self, name: str) -> Optional[Theme]:
        """Resolves a named theme by combining its referenced pillars."""
        theme_data = self._themes.get(name)
        if not theme_data:
            return None
        
        # Extract Pillar Names
        p_name = theme_data.get('palette')
        t_name = theme_data.get('texture')
        ty_name = theme_data.get('typography') or theme_data.get('font') # support 'font' alias
        l_name = theme_data.get('layout')
        
        # Resolve Objects
        palette = self.get_palette(p_name)
        texture = self.get_texture(t_name) or Texture()
        typography = self.get_typography(ty_name) or Typography()
        layout = self.get_layout(l_name) or Layout()
        
        if not palette:
            print(f"Warning: Theme '{name}' references missing palette '{p_name}'")
            return None
            
        return Theme(
            name=name,
            palette=palette,
            texture=texture,
            typography=typography,
            layout=layout
        )

    def list_themes(self) -> List[str]:
        return list(self._themes.keys())

    def get_font_css(self) -> str:
        return "\n".join(self._font_css)
        
    def get_texture_css(self) -> str:
        return "\n".join(self._texture_css)

    def get_palette(self, name: str, mode: Optional[str] = None) -> Optional[Palette]:
        variations = self._palettes.get(name)
        if not variations: return None
        if mode: return variations.get(mode)
        return variations.get('dark') or variations.get('light') or next(iter(variations.values()))

    def get_texture(self, name: str) -> Optional[Texture]:
        return self._textures.get(name)

    def get_layout(self, name: str) -> Optional[Layout]:
        return self._layouts.get(name)

    def get_typography(self, name: str) -> Optional[Typography]:
        return self._typographies.get(name)

    def list_palettes(self) -> list[str]:
        return list(self._palettes.keys())

    def list_textures(self) -> list[str]:
        return list(self._textures.keys())
    
    def list_layouts(self) -> list[str]:
        return list(self._layouts.keys())
    
    def list_typographies(self) -> list[str]:
        return list(self._typographies.keys())

    def _register_raw_data(self, data, cls, storage):
        try:
            instance = cls(**data)
            self._register_instance(instance, storage)
        except Exception as e:
            print(f"Failed to register {cls.__name__} from data: {e}")

    def _register_instance(self, instance, storage):
        if isinstance(instance, Palette):
            if instance.name not in storage:
                storage[instance.name] = {}
            storage[instance.name][instance.mode] = instance
        else:
            storage[instance.name] = instance