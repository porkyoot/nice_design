from nicegui import ui
import nice_design as nice
from nice_design.core.engine import ThemeEngine
from nice_design.core.presets import SOLARIZED_PALETTE, SOLARIZED_SEMANTICS, STANDARD_SHAPE, STANDARD_TEXTURE, STANDARD_LAYOUT, STANDARD_ANIMATION, STANDARD_TYPO

# 1. Initialize the Theme Engine
engine = ThemeEngine()

# Create custom shape and texture to demonstrate the new systems
custom_shape = STANDARD_SHAPE
custom_shape.roundness = 1.2
custom_shape.base_border = 1     # 1px base

custom_texture = STANDARD_TEXTURE
custom_texture.texture_cls = 'texture-glossy'
custom_texture.shadow_intensity = 1.2 # Stronger shadows

# Create custom layout (user-adjustable via slider)
custom_layout = STANDARD_LAYOUT
custom_layout.base_space = 1.0

# Create custom animation (user-adjustable via slider)
custom_animation = STANDARD_ANIMATION
custom_animation.transition_speed = 0.6  # Slower, more dramatic transitions

# Customize the palette and semantics
custom_palette = SOLARIZED_PALETTE
custom_semantics = SOLARIZED_SEMANTICS
# Let's make the shadow a dark blue tint instead of pure black
custom_semantics.shadow = "#001a21" 

theme = engine.compile(custom_palette, custom_semantics, custom_shape, custom_texture, custom_layout, custom_animation, STANDARD_TYPO)

# 2. Setup the Design System
nice.setup(theme)

# 3. Build the UI
with ui.column().classes('w-full items-center nd-p-xl nd-gap-xl'):
    
    # Theme Icon Showcase (Comprehensive)
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Theme Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Complete visual representation combining palette, shape, and texture').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
            # Different sizes
            with ui.column().classes('items-center nd-gap-xs'):
                nice.theme_icon(custom_palette, custom_semantics, custom_shape, custom_texture, size="16px")
                ui.label('16px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.theme_icon(custom_palette, custom_semantics, custom_shape, custom_texture, size="24px")
                ui.label('24px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.theme_icon(custom_palette, custom_semantics, custom_shape, custom_texture, size="32px")
                ui.label('32px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.theme_icon(custom_palette, custom_semantics, custom_shape, custom_texture, size="48px")
                ui.label('48px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.theme_icon(custom_palette, custom_semantics, custom_shape, custom_texture, size="64px")
                ui.label('64px').classes('text-xs opacity-40')
    
    # Palette Icon Showcase
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Palette Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Visual representation of the current theme\'s color palette').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
            # Different sizes
            with ui.column().classes('items-center nd-gap-xs'):
                nice.palette_icon(custom_palette, custom_semantics, size="16px")
                ui.label('16px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.palette_icon(custom_palette, custom_semantics, size="24px")
                ui.label('24px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.palette_icon(custom_palette, custom_semantics, size="32px")
                ui.label('32px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.palette_icon(custom_palette, custom_semantics, size="48px")
                ui.label('48px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.palette_icon(custom_palette, custom_semantics, size="64px")
                ui.label('64px').classes('text-xs opacity-40')
    
    # Texture Icon Showcase
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Texture Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Visual representation of the texture\'s surface properties').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
            # Different sizes
            with ui.column().classes('items-center nd-gap-xs'):
                nice.texture_icon(custom_texture, size="16px")
                ui.label('16px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.texture_icon(custom_texture, size="24px")
                ui.label('24px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.texture_icon(custom_texture, size="32px")
                ui.label('32px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.texture_icon(custom_texture, size="48px")
                ui.label('48px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.texture_icon(custom_texture, size="64px")
                ui.label('64px').classes('text-xs opacity-40')
    
    # Shape Icon Showcase
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Shape Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Visual representation of the shape\'s geometric properties').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
            # Different sizes
            with ui.column().classes('items-center nd-gap-xs'):
                nice.shape_icon(custom_shape, size="16px")
                ui.label('16px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.shape_icon(custom_shape, size="24px")
                ui.label('24px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.shape_icon(custom_shape, size="32px")
                ui.label('32px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.shape_icon(custom_shape, size="48px")
                ui.label('48px').classes('text-xs opacity-40')
            
            with ui.column().classes('items-center nd-gap-xs'):
                nice.shape_icon(custom_shape, size="64px")
                ui.label('64px').classes('text-xs opacity-40')

    # Layout Controls
    with nice.card().classes('w-[32rem] nd-gap-md'):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Configuration').classes('text-xs uppercase tracking-widest opacity-40 font-bold ml-1')
        
        nice.select(
            options=[
                {'label': 'Dark Mode', 'value': 'Dark Mode', 'icon': 'mdi-moon-waning-crescent'},
                {'label': 'Light Mode', 'value': 'Light Mode', 'icon': 'mdi-white-balance-sunny'},
                {'label': 'Auto', 'value': 'Auto', 'icon': 'mdi-brightness-auto'}
            ],
            label='System Theme',
            value={'label': 'Dark Mode', 'value': 'Dark Mode', 'icon': 'mdi-moon-waning-crescent'},
            with_icons=True
        ).classes('w-full')
        
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Compact Layout').classes('opacity-60 font-medium')
            nice.select(
                options=[
                    {'label': 'Relaxed', 'value': 'Relaxed', 'icon': 'mdi-arrow-expand-horizontal'},
                    {'label': 'Standard', 'value': 'Standard', 'icon': 'mdi-view-compact'},
                    {'label': 'Minimal', 'value': 'Minimal', 'icon': 'mdi-arrow-collapse-horizontal'}
                ],
                value={'label': 'Standard', 'value': 'Standard', 'icon': 'mdi-view-compact'},
                with_icons=True
            )

        
        with nice.button('Extra Settings', variant='ghost', icon='mdi-dots-horizontal').classes('w-full'):
            with nice.menu():
                nice.menu_item('Export Theme', on_click=lambda: ui.notify('Exporting...'))
                nice.menu_item('Reset Defaults', on_click=lambda: ui.notify('Resetting...'))
                ui.separator().classes('bg-white/10')
                nice.menu_item('Delete System', on_click=lambda: ui.notify('Self-destruct in 3... 2... 1...'))

ui.run(title='Nice Design Tokens', reload=False, show=False)
