from nicegui import ui
import nice_design
from nice_design.core.engine import ThemeEngine
from nice_design.core.presets import SOLARIZED_PALETTE, STANDARD_SKIN, STANDARD_TYPO

# 1. Initialize the Theme Engine
engine = ThemeEngine()

# Create a custom glossy skin for the demo
glossy_skin = STANDARD_SKIN
glossy_skin.texture_cls = 'texture-glossy'
glossy_skin.roundness = 1.5

theme = engine.compile(SOLARIZED_PALETTE, glossy_skin, STANDARD_TYPO)

# 2. Setup the Design System
nice_design.setup(theme)

# 3. Build the UI using NDS components
with nice_design.AppCard().classes('absolute-center w-[28rem] p-10 items-center gap-8'):
    with ui.column().classes('items-center w-full gap-2'):
        with ui.avatar('palette', color='primary', text_color='white').classes('shadow-xl'):
            ui.icon('style')
        ui.label('Nice Design System').classes('text-4xl font-extrabold tracking-tight')
        ui.label('Example of a styleable button system').classes('text-lg opacity-60 text-center')
    
    with ui.row().classes('gap-4 w-full justify-center'):
        nice_design.NDSButton('Brand Action', variant='primary', icon='rocket')
        nice_design.NDSButton('Settings', variant='secondary', icon='settings')
    
    with ui.column().classes('w-full gap-2 mt-4'):
        ui.label('Ghost Variant').classes('text-xs uppercase tracking-widest opacity-40 font-bold ml-1')
        nice_design.NDSButton('View Documentation', variant='ghost', icon='menu_book').classes('w-full')

ui.run(title='Styleable Button Example')
