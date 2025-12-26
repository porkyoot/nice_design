from .definitions import Theme, Palette, Texture, Layout, Typography, CompiledTheme

class ThemeEngine:
    def __init__(self):
        # We'll need to update registry later
        pass

    def compile(self, palette: Palette, texture: Texture, typo: Typography, layout: Layout) -> CompiledTheme:
        # 1. Calculate Radii based on Texture's Roundness
        # (Roundness is now part of Texture)
        base_radius = 0.5 # rem
        tokens = {
            'sm': f"{base_radius * 0.5 * texture.roundness}rem",
            'md': f"{base_radius * texture.roundness}rem",
            'lg': f"{base_radius * 2 * texture.roundness}rem",
            'full': '9999px' if texture.roundness > 0 else '0px'
        }

        # 2. Calculate Spacing based on Layout's base_space
        bs = layout.base_space
        tokens.update({
            'space-xs': f"{bs * 0.25}rem",
            'space-sm': f"{bs * 0.5}rem",
            'space-md': f"{bs * 1.0}rem",
            'space-lg': f"{bs * 1.5}rem",
            'space-xl': f"{bs * 2.0}rem",
        })

        # 3. Calculate Borders based on Texture's border_width (px)
        bw = texture.border_width
        tokens.update({
            'border-xs': '0px',
            'border-sm': f"{bw}px",
            'border-md': f"{bw * 2}px",
            'border-lg': f"{bw * 4}px",
            'border-xl': f"{bw * 8}px",
        })

        # 4. Calculate Shadow Color and Values
        def hex_to_rgb(hex_color):
            h = hex_color.lstrip('#')
            if len(h) == 3: h = ''.join([c*2 for c in h])
            r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            return r, g, b

        r, g, b = hex_to_rgb(palette.shadow)
        # Store as comma-separated for potential direct use
        tokens['shadow-color'] = f"{r}, {g}, {b}"

        # 5. Calculate Shadows based on Texture's Intensity
        # Generate complete shadow values using the shadow-color variable for dynamism
        si = texture.shadow_intensity
        if not texture.shadows_enabled:
            si = 0
            
        # Generate complete shadow definitions using var(--nd-shadow-color)
        # Geometrically scaling shadows with intensity (si) for visible depth
        tokens.update({
            'shadow-xs': f"0 {1*si:.1f}px {2*si:.1f}px 0 rgba(var(--nd-shadow-color), {0.4 * si:.2f})",
            'shadow-sm': f"0 {1*si:.1f}px {3*si:.1f}px 0 rgba(var(--nd-shadow-color), {0.5 * si:.2f}), 0 {1*si:.1f}px {2*si:.1f}px -1px rgba(var(--nd-shadow-color), {0.4 * si:.2f})",
            'shadow-md': f"0 {4*si:.1f}px {6*si:.1f}px -1px rgba(var(--nd-shadow-color), {0.5 * si:.2f}), 0 {2*si:.1f}px {4*si:.1f}px -2px rgba(var(--nd-shadow-color), {0.45 * si:.2f})",
            'shadow-lg': f"0 {10*si:.1f}px {15*si:.1f}px -3px rgba(var(--nd-shadow-color), {0.6 * si:.2f}), 0 {4*si:.1f}px {6*si:.1f}px -4px rgba(var(--nd-shadow-color), {0.5 * si:.2f})",
            'shadow-xl': f"0 {20*si:.1f}px {25*si:.1f}px -5px rgba(var(--nd-shadow-color), {0.7 * si:.2f}), 0 {8*si:.1f}px {10*si:.1f}px -6px rgba(var(--nd-shadow-color), {0.6 * si:.2f})",
        })

        # 6. Add Transition Speed from Layout
        tokens['transition-speed'] = f"{layout.transition_speed}s"

        # 7. Calculate Colors (Handling Opacity for Glass/Ghost textures)
        def mix(hex_color, opacity):
            if opacity >= 1.0: return hex_color
            return f"color-mix(in srgb, {hex_color}, transparent {int((1-opacity)*100)}%)"

        colors = {
            'primary': palette.primary,
            'on-primary': palette.on_primary,
            'secondary': palette.secondary,
            'on-secondary': palette.on_secondary,
            
            'content-main': palette.content_main,
            'content-muted': palette.content_muted,
            'content-subtle': palette.content_subtle,
            
            'surface-base': palette.surface_base,
            'surface-layer': mix(palette.surface_layer, texture.opacity),
            'surface-overlay': mix(palette.surface_overlay, texture.opacity),
            
            'highlight': palette.highlight,

            'status-success': palette.success,
            'on-status-success': palette.on_success,
            'status-error': palette.error,
            'on-status-error': palette.on_error,
            'status-warning': palette.warning,
            'on-status-warning': palette.on_warning,
            'status-info': palette.info,
            'on-status-info': palette.on_info,
        }
        
        # Add named colors from palette
        for color_name, color_value in palette.colors.items():
            colors['color-' + color_name] = color_value

        tokens['font-main'] = typo.font_main
        tokens['font-mono'] = typo.font_mono

        # 8. Determine CSS Classes from Texture
        css_classes = [texture.texture_cls]
        if not texture.shadows_enabled:
            css_classes.append('no-shadows')

        return CompiledTheme(colors=colors, layout=tokens, classes=css_classes)