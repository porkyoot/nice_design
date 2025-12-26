from .definitions import Theme

def generate_theme_css(theme: Theme) -> str:
    p = theme.prefix
    pal = theme.palette
    sem = theme.semantics
    
    # 1. CSS Variables
    lines = [":root {"]

    # --- COLORS: ACCENTS ---
    lines.append("  /* --- Accents --- */")
    lines.append(f"  --{p}-primary: {sem.primary};")
    lines.append(f"  --{p}-on-primary: {sem.on_primary};")
    lines.append(f"  --{p}-secondary: {sem.secondary};")
    lines.append(f"  --{p}-on-secondary: {sem.on_secondary};")
    lines.append(f"  --{p}-highlight: {sem.highlight};")
    lines.append(f"  --{p}-shadow: {sem.shadow};")

    # --- COLORS: SURFACES ---
    lines.append("  /* --- Surfaces --- */")
    lines.append(f"  --{p}-surface-base: {sem.surface_base};")
    lines.append(f"  --{p}-surface-layer: {sem.surface_layer};")
    lines.append(f"  --{p}-surface-overlay: {sem.surface_overlay};")
        
    lines.append("  /* --- Content --- */")
    lines.append(f"  --{p}-content-main: {sem.content_main};")
    lines.append(f"  --{p}-content-muted: {sem.content_muted};")
    lines.append(f"  --{p}-content-subtle: {sem.content_subtle};")

    # --- COLORS: PALETTE (Dict -> Named Vars) ---
    lines.append("  /* --- Hue Palette --- */")
    for name, hex_val in pal.colors.items():
        lines.append(f"  --{p}-color-{name}: {hex_val};")

    # --- COLORS: STATUS ---
    lines.append("  /* --- Semantic Status --- */")
    lines.append(f"  --{p}-status-success: {sem.success};")
    lines.append(f"  --{p}-on-status-success: {sem.on_success};")
    lines.append(f"  --{p}-status-error: {sem.error};")
    lines.append(f"  --{p}-on-status-error: {sem.on_error};")
    lines.append(f"  --{p}-status-warning: {sem.warning};")
    lines.append(f"  --{p}-on-status-warning: {sem.on_warning};")
    lines.append(f"  --{p}-status-info: {sem.info};")
    lines.append(f"  --{p}-on-status-info: {sem.on_info};")

    # --- SHAPE & TYPOGRAPHY ---
    lines.append("  /* --- Shape & Type --- */")
    lines.append(f"  --{p}-radius-base: {theme.shape.roundness * 0.5}rem;")
    lines.append(f"  --{p}-border-width: {theme.shape.base_border}px;")
    lines.append(f"  --{p}-font-main: {theme.typography.font_main};")
    lines.append(f"  --{p}-font-mono: {theme.typography.font_mono};")
    lines.append("}")

    # 2. Utility Classes
    lines.append("/* --- Utility Classes --- */")
    
    # --- Spacing Utilities ---
    # Sizes: 0, 1, 2, 3, 4, 5, 6, 8, 10, 12
    base_space = theme.layout.base_space
    sizes = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12]
    
    for size in sizes:
        val = f"{size * 0.25 * base_space}rem"
        # Padding
        lines.append(f".-{p}-u-p-{size} {{ padding: {val} !important; }}")
        lines.append(f".-{p}-u-pt-{size} {{ padding-top: {val} !important; }}")
        lines.append(f".-{p}-u-pb-{size} {{ padding-bottom: {val} !important; }}")
        lines.append(f".-{p}-u-pl-{size} {{ padding-left: {val} !important; }}")
        lines.append(f".-{p}-u-pr-{size} {{ padding-right: {val} !important; }}")
        lines.append(f".-{p}-u-px-{size} {{ padding-left: {val} !important; padding-right: {val} !important; }}")
        lines.append(f".-{p}-u-py-{size} {{ padding-top: {val} !important; padding-bottom: {val} !important; }}")
        
        # Margin
        lines.append(f".-{p}-u-m-{size} {{ margin: {val} !important; }}")
        lines.append(f".-{p}-u-mt-{size} {{ margin-top: {val} !important; }}")
        lines.append(f".-{p}-u-mb-{size} {{ margin-bottom: {val} !important; }}")
        lines.append(f".-{p}-u-ml-{size} {{ margin-left: {val} !important; }}")
        lines.append(f".-{p}-u-mr-{size} {{ margin-right: {val} !important; }}")
        lines.append(f".-{p}-u-mx-{size} {{ margin-left: {val} !important; margin-right: {val} !important; }}")
        lines.append(f".-{p}-u-my-{size} {{ margin-top: {val} !important; margin-bottom: {val} !important; }}")
        
        # Gap
        lines.append(f".-{p}-u-gap-{size} {{ gap: {val} !important; }}")

    # --- Color Utilities ---
    # Helper to generate text/bg utils
    def add_color_utils(role, var_name):
        lines.append(f".-{p}-u-text-{role} {{ color: var({var_name}) !important; }}")
        lines.append(f".-{p}-u-bg-{role} {{ background-color: var({var_name}) !important; }}")

    add_color_utils('primary', f"--{p}-primary")
    add_color_utils('on-primary', f"--{p}-on-primary")
    add_color_utils('secondary', f"--{p}-secondary")
    add_color_utils('on-secondary', f"--{p}-on-secondary")
    add_color_utils('highlight', f"--{p}-highlight")
    
    # Surfaces
    add_color_utils('surface-base', f"--{p}-surface-base")
    add_color_utils('surface-layer', f"--{p}-surface-layer")
    add_color_utils('surface-overlay', f"--{p}-surface-overlay")
        
    # Content
    add_color_utils('content-main', f"--{p}-content-main")
    add_color_utils('content-muted', f"--{p}-content-muted")
    add_color_utils('content-subtle', f"--{p}-content-subtle")
        
    # Status
    add_color_utils('success', f"--{p}-status-success")
    add_color_utils('on-success', f"--{p}-on-status-success")
    
    add_color_utils('error', f"--{p}-status-error")
    add_color_utils('on-error', f"--{p}-on-status-error")
    
    add_color_utils('warning', f"--{p}-status-warning")
    add_color_utils('on-warning', f"--{p}-on-status-warning")
    
    add_color_utils('info', f"--{p}-status-info")
    add_color_utils('on-info', f"--{p}-on-status-info")

    # --- Radius Utilities ---
    # sm, md, lg, full, none
    base_r = theme.shape.roundness * 0.5 # rem
    radii = {
        'none': '0px',
        'sm': f"{base_r * 0.5}rem",
        'md': f"{base_r}rem",
        'lg': f"{base_r * 2}rem",
        'full': '9999px'
    }
    
    for size, val in radii.items():
        lines.append(f".-{p}-u-rounded-{size} {{ border-radius: {val} !important; }}")

    # --- Border Utilities ---
    lines.append(f".-{p}-u-border {{ border: var(--{p}-border-width) solid var(--{p}-border-color, currentColor) !important; }}")
    lines.append(f".-{p}-u-border-primary {{ border-color: var(--{p}-primary) !important; }}")

    return "\n".join(lines)