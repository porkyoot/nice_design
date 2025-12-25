from .definitions import Theme, Palette, Shape, Texture, Layout, Animation, Typography, CompiledTheme
from .registry import ThemeRegistry

class ThemeEngine:
    def __init__(self):
        self.registry = ThemeRegistry()
        self.registry.discover_plugins()

    def compile(self, palette: Palette, shape: Shape, texture: Texture, layout: Layout, animation: Animation, typo: Typography) -> CompiledTheme:
        # 1. Calculate Radii based on Shape's Roundness
        base_radius = 0.5 # rem
        radii = {
            'sm': f"{base_radius * 0.5 * shape.roundness}rem",
            'md': f"{base_radius * shape.roundness}rem",
            'lg': f"{base_radius * 2 * shape.roundness}rem",
            'full': '9999px' if shape.roundness > 0 else '0px'
        }

        # 2. Calculate Spacing based on Layout's base_space
        bs = layout.base_space
        radii.update({
            'space-xs': f"{bs * 0.25}rem",
            'space-sm': f"{bs * 0.5}rem",
            'space-md': f"{bs * 1.0}rem",
            'space-lg': f"{bs * 1.5}rem",
            'space-xl': f"{bs * 2.0}rem",
        })

        # 3. Calculate Borders based on Shape's base_border (px)
        bb = shape.base_border
        radii.update({
            'border-xs': '0px',
            'border-sm': f"{bb}px",
            'border-md': f"{bb * 2}px",
            'border-lg': f"{bb * 4}px",
            'border-xl': f"{bb * 8}px",
        })

        # 4. Calculate Shadow Color (convert hex to rgb comma string)
        def hex_to_rgb_commas(hex_color):
            h = hex_color.lstrip('#')
            if len(h) == 3: h = ''.join([c*2 for c in h])
            r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            return f"{r}, {g}, {b}"

        shadow_rgb = hex_to_rgb_commas(palette.shadow)
        radii['shadow-color'] = shadow_rgb

        # 5. Calculate Shadows based on Texture's Intensity
        si = texture.shadow_intensity
        if not texture.shadows:
            si = 0
            
        s_col = "var(--nd-shadow-color)"
        radii.update({
            'shadow-xs': f"0 1px 2px 0 rgba({s_col}, {0.05 * si:.2f})",
            'shadow-sm': f"0 1px 3px 0 rgba({s_col}, {0.1 * si:.2f}), 0 1px 2px -1px rgba({s_col}, {0.1 * si:.2f})",
            'shadow-md': f"0 4px 6px -1px rgba({s_col}, {0.1 * si:.2f}), 0 2px 4px -2px rgba({s_col}, {0.1 * si:.2f})",
            'shadow-lg': f"0 10px 15px -3px rgba({s_col}, {0.1 * si:.2f}), 0 4px 6px -4px rgba({s_col}, {0.1 * si:.2f})",
            'shadow-xl': f"0 20px 25px -5px rgba({s_col}, {0.1 * si:.2f}), 0 8px 10px -6px rgba({s_col}, {0.1 * si:.2f})",
        })

        # 6. Add Transition Speed from Animation
        radii['transition-speed'] = f"{animation.transition_speed}s"

        # 7. Calculate Colors (Handling Opacity for Glass/Ghost textures)
        def mix(hex_color, opacity):
            if opacity >= 1.0: return hex_color
            return f"color-mix(in srgb, {hex_color}, transparent {int((1-opacity)*100)}%)"

        def get_color(color_list, index, default):
            try:
                return color_list[index]
            except IndexError:
                return default

        colors = {
            'primary': palette.primary,
            'secondary': palette.secondary,
            'foreground-1': mix(get_color(palette.foregrounds, 0, '#ffffff'), texture.opacity),
            'foreground-2': mix(get_color(palette.foregrounds, 1, '#f0f0f0'), texture.opacity),
            'foreground-3': mix(get_color(palette.foregrounds, 2, '#e0e0e0'), texture.opacity),
            'background-1': mix(get_color(palette.backgrounds, 0, '#000000'), texture.opacity),
            'background-2': mix(get_color(palette.backgrounds, 1, '#111111'), texture.opacity),
            'background-3': mix(get_color(palette.backgrounds, 2, '#222222'), texture.opacity),
            'highlight': palette.highlight,
        }
        
        # Add named colors from palette
        for color_name, color_value in palette.colors.items():
            colors['color-' + color_name] = color_value
        
        for s_type, s_color in palette.status.items():
            colors['status-' + s_type] = s_color

        radii['font-main'] = typo.font_main
        radii['font-mono'] = typo.font_mono

        # 8. Determine CSS Classes from Texture
        css_classes = [texture.texture_cls]
        if not texture.shadows:
            css_classes.append('no-shadows')

        return CompiledTheme(colors=colors, layout=radii, classes=css_classes)