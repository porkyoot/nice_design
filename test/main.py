from nicegui import ui
import nice_design as nice
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
nice.setup(theme)

# 3. Build the UI using lowercase "nice" components (familiar API)
with nice.card().classes('absolute-center w-[28rem] p-10 items-center gap-8'):
    with ui.column().classes('items-center w-full gap-2'):
        with ui.avatar('palette', color='primary', text_color='white').classes('shadow-xl'):
            ui.icon('style')
        ui.label('Nice Design System').classes('text-4xl font-extrabold tracking-tight')
        ui.label('Example of a styleable button system').classes('text-lg opacity-60 text-center')
    
    with ui.row().classes('gap-4 w-full justify-center'):
        nice.button('Brand Action', variant='primary', icon='rocket')
        nice.button('Settings', variant='secondary', icon='settings')
    
    with ui.column().classes('w-full gap-4 mt-2'):
        ui.label('Configuration').classes('text-xs uppercase tracking-widest opacity-40 font-bold ml-1')
        
        # New Select Component
        nice.select(
            options=['Solarized Dark', 'Cyberpunk', 'Nordic', 'Glassmorphism'],
            label='Application Theme',
            value='Solarized Dark'
        ).classes('w-full')
        
        # Minimal Select Demo
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Focus Mode').classes('opacity-60 font-medium')
            nice.select(
                options=['Normal', 'Quiet', 'Zen'],
                value='Normal',
                minimal=True
            )
        
        nice.button('View Documentation', variant='ghost', icon='menu_book').classes('w-full')
        
        with nice.button('More Options', variant='ghost', icon='more_vert').classes('w-full'):
            with nice.menu():
                nice.menu_item('Profile Settings', on_click=lambda: ui.notify('Profile'))
                nice.menu_item('System Status', on_click=lambda: ui.notify('Status'))
                ui.separator().classes('bg-white/10')
                nice.menu_item('Logout', on_click=lambda: ui.notify('Logged out'))

ui.run(title='Styleable Button Example')
