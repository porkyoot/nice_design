from .definitions import Theme, Palette, Skin, Typography

class ThemeEngine:
    def compile(self, palette: Palette, skin: Skin, typo: Typography) -> Theme:
        # 1. Calculate Radii based on Skin's Roundness
        base_radius = 0.5 # rem
        radii = {
            'sm': f"{base_radius * 0.5 * skin.roundness}rem",
            'md': f"{base_radius * skin.roundness}rem",
            'lg': f"{base_radius * 2 * skin.roundness}rem",
            'full': '9999px' if skin.roundness > 0 else '0px'
        }

        # 2. Calculate Colors (Handling Opacity for Glass/Ghost skins)
        def mix(hex_color, opacity):
            if opacity >= 1.0: return hex_color
            # Returns a CSS color-mix for native transparency
            return f"color-mix(in srgb, {hex_color}, transparent {int((1-opacity)*100)}%)"

        colors = {
            'primary': palette.primary,
            'secondary': palette.secondary,
            'accent': palette.accent,
            'surface-1': mix(palette.surfaces.get('1', '#ffffff'), skin.opacity),
            'surface-2': mix(palette.surfaces.get('2', '#f0f0f0'), skin.opacity),
            'surface-3': mix(palette.surfaces.get('3', '#e0e0e0'), skin.opacity),
        }
        
        # Map statuses
        for s_type, s_color in palette.status.items():
            colors[f'status-{s_type}'] = s_color

        radii['font-main'] = typo.font_family
        radii['font-mono'] = typo.mono_family

        # 3. Determine CSS Classes
        css_classes = [skin.texture_cls]
        if not skin.shadows:
            css_classes.append('no-shadows')

        return Theme(colors=colors, layout=radii, classes=css_classes)