from nicegui import ui
import nice_design as nice
from nice_design.core.engine import ThemeEngine
from nice_design.core.presets import SOLARIZED_PALETTE, STANDARD_SKIN, STANDARD_TYPO

# 1. Initialize the Theme Engine
engine = ThemeEngine()

# Create a custom skin to demonstrate the new systems
custom_skin = STANDARD_SKIN
custom_skin.texture_cls = 'texture-glossy'
custom_skin.roundness = 1.2
custom_skin.base_space = 1.0
custom_skin.base_border = 1     # 1px base
custom_skin.shadow_intensity = 1.2 # Stronger shadows
custom_skin.transition_speed = 0.6  # Slower, more dramatic transitions

# Customize the palette with a themed shadow
custom_palette = SOLARIZED_PALETTE
# Let's make the shadow a dark blue tint instead of pure black
custom_palette.shadow = "#001a21" 

theme = engine.compile(custom_palette, custom_skin, STANDARD_TYPO)

# 2. Setup the Design System
nice.setup(theme)

# 3. Build the UI
with ui.column().classes('w-full items-center nd-p-xl nd-gap-xl'):
    
    # Hero Card
    with nice.card().classes('w-[32rem] items-center nd-gap-lg nd-shadow-xl'):
        with ui.avatar('mdi-layers', color='primary', text_color='white').classes('shadow-xl'):
            ui.icon('mdi-palette')
        ui.label('Nice Design System').classes('text-4xl font-extrabold tracking-tight')
        ui.label('Standardized Design Tokens').classes('text-lg opacity-60 text-center')
        
        with ui.row().classes('nd-gap-md w-full justify-center'):
            nice.button('Primary Action', variant='primary', icon='mdi-rocket')
            nice.button('Secondary', variant='secondary', icon='mdi-cog')

    # Token Showcase Row
    with ui.row().classes('nd-gap-xl'):
        # Border Showcase
        with nice.card().classes('nd-gap-md nd-p-lg'):
            ui.label('Border System').classes('text-sm font-bold uppercase opacity-40')
            with ui.row().classes('nd-gap-sm'):
                ui.label('SM').classes('nd-p-sm nd-border-sm border-white/20 rounded')
                ui.label('MD').classes('nd-p-sm nd-border-md border-white/20 rounded')
                ui.label('LG').classes('nd-p-sm nd-border-lg border-white/20 rounded')
        
        # Shadow Showcase
        with nice.card().classes('nd-gap-md nd-p-lg'):
            ui.label('Shadow System').classes('text-sm font-bold uppercase opacity-40')
            with ui.row().classes('nd-gap-md'):
                ui.label('SM').classes('nd-p-sm bg-white/5 nd-shadow-sm rounded')
                ui.label('MD').classes('nd-p-sm bg-white/5 nd-shadow-md rounded')
                ui.label('LG').classes('nd-p-sm bg-white/5 nd-shadow-lg rounded')

    # Layout Controls
    with nice.card().classes('w-[32rem] nd-gap-md'):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Configuration').classes('text-xs uppercase tracking-widest opacity-40 font-bold ml-1')
            nice.ThemeSelector(
                themes=['Solarized Dark', 'Nordic Night', 'Cyberpunk', 'Minimalist'],
                on_theme_change=lambda t: ui.notify(f"Theme changed to: {t}"),
                on_mode_toggle=lambda dark: ui.notify(f"Dark mode: {dark}")
            )
        
        nice.select(
            options=['Dark Mode', 'Light Mode', 'Auto'],
            label='System Theme',
            value='Dark Mode'
        ).classes('w-full')
        
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Compact Layout').classes('opacity-60 font-medium')
            nice.select(
                options=['Relaxed', 'Standard', 'Minimal'],
                value='Standard',
                minimal=True,
                icon='mdi-tune',
                icon_color='var(--nd-primary)'
            )
        
        with nice.button('Extra Settings', variant='ghost', icon='mdi-dots-horizontal').classes('w-full'):
            with nice.menu():
                nice.menu_item('Export Theme', on_click=lambda: ui.notify('Exporting...'))
                nice.menu_item('Reset Defaults', on_click=lambda: ui.notify('Resetting...'))
                ui.separator().classes('bg-white/10')
                nice.menu_item('Delete System', on_click=lambda: ui.notify('Self-destruct in 3... 2... 1...'))

ui.run(title='Nice Design Tokens', reload=False, show=False)
