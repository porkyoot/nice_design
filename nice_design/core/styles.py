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
    lines.append(f"  --{p}-secondary: {sem.secondary};")
    lines.append(f"  --{p}-highlight: {sem.highlight};")
    lines.append(f"  --{p}-shadow: {sem.shadow};")

    # --- COLORS: SCALES (List -> Indexed Vars) ---
    lines.append("  /* --- Background Scale (0=Deepest) --- */")
    for i, color in enumerate(sem.backgrounds):
        lines.append(f"  --{p}-bg-{i}: {color};")
        
    lines.append("  /* --- Foreground Scale (0=Strongest) --- */")
    for i, color in enumerate(sem.foregrounds):
        lines.append(f"  --{p}-fg-{i}: {color};")

    # --- COLORS: PALETTE (Dict -> Named Vars) ---
    lines.append("  /* --- Hue Palette --- */")
    for name, hex_val in pal.colors.items():
        lines.append(f"  --{p}-color-{name}: {hex_val};")

    # --- COLORS: STATUS (Dict -> Named Vars) ---
    lines.append("  /* --- Semantic Status --- */")
    for status, hex_val in sem.status.items():
        lines.append(f"  --{p}-status-{status}: {hex_val};")

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
    add_color_utils('secondary', f"--{p}-secondary")
    add_color_utils('highlight', f"--{p}-highlight")
    
    for i in range(len(sem.backgrounds)):
        add_color_utils(f"bg-{i}", f"--{p}-bg-{i}")
        
    for i in range(len(sem.foregrounds)):
        add_color_utils(f"fg-{i}", f"--{p}-fg-{i}")
        
    for status in sem.status:
        add_color_utils(status, f"--{p}-status-{status}")

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