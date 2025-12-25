from .theme import Theme

def generate_css(theme: Theme) -> str:
    p = theme.prefix
    pal = theme.palette
    
    lines = [":root {"]

    # --- COLORS: ACCENTS ---
    lines.append("  /* --- Accents --- */")
    lines.append(f"  --{p}-primary: {pal.primary};")
    lines.append(f"  --{p}-secondary: {pal.secondary};")
    lines.append(f"  --{p}-reflection: {pal.reflection};")
    lines.append(f"  --{p}-shadow: {pal.shadow};")

    # --- COLORS: SCALES (List -> Indexed Vars) ---
    lines.append("  /* --- Background Scale (0=Deepest) --- */")
    for i, color in enumerate(pal.background):
        lines.append(f"  --{p}-bg-{i}: {color};")
        
    lines.append("  /* --- Foreground Scale (0=Strongest) --- */")
    for i, color in enumerate(pal.foreground):
        lines.append(f"  --{p}-fg-{i}: {color};")

    # --- COLORS: PALETTE (Dict -> Named Vars) ---
    lines.append("  /* --- Hue Palette --- */")
    for name, hex_val in pal.colors.items():
        lines.append(f"  --{p}-color-{name}: {hex_val};")

    # --- COLORS: STATUS (Dict -> Named Vars) ---
    lines.append("  /* --- Semantic Status --- */")
    for status, hex_val in pal.status.items():
        lines.append(f"  --{p}-status-{status}: {hex_val};")

    # --- SHAPE & TYPOGRAPHY ---
    lines.append("  /* --- Shape & Type --- */")
    lines.append(f"  --{p}-radius-base: {theme.shape.roundness * 0.5}rem;")
    lines.append(f"  --{p}-border-width: {theme.shape.base_border}px;")
    lines.append(f"  --{p}-font-main: {theme.typography.font_main};")
    lines.append(f"  --{p}-font-mono: {theme.typography.font_mono};")

    lines.append("}")
    return "\n".join(lines)