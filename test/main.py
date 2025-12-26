from typing import Dict, Any, Optional
from nicegui import ui
import nice_design as nice
import copy
from nice_design.core.engine import ThemeEngine
from nice_design.core.presets import SOLARIZED_PALETTE, STANDARD_TEXTURE, STANDARD_LAYOUT, STANDARD_TYPO

# 1. Initialize the Theme Engine
engine = ThemeEngine()

# Create custom texture (includes shape) to demonstrate the new systems
custom_texture = STANDARD_TEXTURE
custom_texture.roundness = 1.2
custom_texture.border_width = 1     
custom_texture.texture_cls = 'texture-glossy'
custom_texture.shadow_intensity = 1.2 # Stronger shadows
custom_texture.highlight_intensity = 1.1 # Subtle highlight

# Create custom layout (includes animation)
custom_layout = STANDARD_LAYOUT
custom_layout.base_space = 1.0
custom_layout.transition_speed = 0.6  # Slower, more dramatic transitions

# Customize the palette
custom_palette = copy.deepcopy(SOLARIZED_PALETTE)
# (Shadow is handled by the theme engine now)

# Compile 4 pillar theme
theme = engine.compile(custom_palette, custom_texture, STANDARD_TYPO, custom_layout)

# 2. Setup the Design System
nice.setup(theme)

# Handle Theme Change
def handle_theme_change(e: Dict[str, Any]):
    # Compile a new theme from the 4 categorical pillars
    new_theme = engine.compile(
        palette=e['palette'],
        texture=e['texture'],
        typo=e['typography'],
        layout=e['layout']
    )
    # Apply it globally
    nice.apply_theme(new_theme)

# 3. Build the UI
with ui.column().classes('w-full items-center nd-p-xl nd-gap-xl'):
    
    # New Molecule: Theme Selector (Powered by 4 categories)
    l1 = ui.label('Nice Design System').classes('text-4xl font-bold mb-2')
    l1.tag = 'h1'
    l2 = ui.label('The secondary font is used here').classes('text-xl opacity-60 nd-font-secondary mb-8')
    l2.tag = 'h2'
    
    nice.theme_selector(on_change=handle_theme_change)

    
    # Theme Icon Showcase (Comprehensive)
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Theme Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Complete visual representation combining the 4 pillars').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
            # different sizes
            for s in ["16px", "24px", "32px", "48px", "64px"]:
                with ui.column().classes('items-center nd-gap-xs'):
                    nice.theme_icon(custom_palette, custom_texture, size=s)
                    ui.label(s).classes('text-xs opacity-40')
    
    # Palette Icon Showcase
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Palette Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Visual representation of the Palette pillar').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
            for s in ["16px", "24px", "32px", "48px", "64px"]:
                with ui.column().classes('items-center nd-gap-xs'):
                    nice.palette_icon(custom_palette, size=s)
                    ui.label(s).classes('text-xs opacity-40')
    
    # Texture Icon Showcase
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Texture Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Visual representation of the Texture pillar').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
            for s in ["16px", "24px", "32px", "48px", "64px"]:
                with ui.column().classes('items-center nd-gap-xs'):
                    nice.texture_icon(custom_texture, custom_palette, size=s)
                    ui.label(s).classes('text-xs opacity-40')
    
    # Shape Icon Showcase
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
        ui.label('Shape Icon').classes('text-sm font-bold uppercase opacity-40')
        ui.label('Geometric properties (now part of Texture pillar)').classes('text-xs opacity-60 text-center')
        
        with ui.row().classes('nd-gap-xl items-center'):
             for s in ["16px", "24px", "32px", "48px", "64px"]:
                with ui.column().classes('items-center nd-gap-xs'):
                    nice.shape_icon(custom_texture, size=s)
                    ui.label(s).classes('text-xs opacity-40')

    # Component Demo: SelectButton
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
         ui.label('Select Button Component').classes('text-sm font-bold uppercase opacity-40')
         ui.label('A button atom styled exactly like a Select input').classes('text-xs opacity-60 text-center')
         
         with ui.row().classes('w-full items-center justify-between'):
             ui.label('Default State').classes('opacity-60 font-medium')
             nice.select_button(
                 label='Select Option',
                 on_click=lambda: ui.notify('Clicked Select Button')
             ).classes('w-[180px]')

         with ui.row().classes('w-full items-center justify-between'):
             ui.label('With Menu').classes('opacity-60 font-medium')
             btn_menu = nice.select_button(
                 label='Open Menu',
                 icon='menu',
             ).classes('w-[180px]')
             
             with btn_menu:
                 with nice.menu().on('hide', btn_menu.reset_rotation):
                     nice.menu_item('Option 1', on_click=lambda: (btn_menu.set_label('Option 1'), btn_menu.toggle_rotation()))
                     nice.menu_item('Option 2', on_click=lambda: (btn_menu.set_label('Option 2'), btn_menu.toggle_rotation()))

         with ui.row().classes('w-full items-center justify-between'):
             ui.label('Icon Only').classes('opacity-60 font-medium')
             nice.select_button(
                 label='Hidden Label',
                 icon='settings',
                 icon_only=True
             ).classes('w-[180px]')

    # Component Demo: Sliders
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
         ui.label('Slider Variants').classes('text-sm font-bold uppercase opacity-40')
         ui.label('Standard and Dual-Value Sliders').classes('text-xs opacity-60 text-center')

         # Standard Slider
         with ui.column().classes('w-full gap-2'):
             ui.label('Standard Slider').classes('text-xs opacity-60')
             nice.slider(min=0, max=100, value=50).props('label-always color="primary"')
             
         ui.separator().classes('my-2 opacity-10')
         
         # Split Slider
         ui.label('Split Slider (Independent Handles)').classes('text-xs opacity-60')
         ui.label('Two handles, inverted left axis.').classes('text-[10px] opacity-40')
         
         nice.split_slider(
             limit=100,
             value_left=30,
             value_right=60, 
             color_left='purple-4', 
             color_right='cyan-4',
             on_change=lambda e: ui.notify(f"Left: {e['left']}, Right: {e['right']}")
         )


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

        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Icon Only Select').classes('opacity-60 font-medium')
            nice.select(
                options=[
                    {'label': 'Grid', 'value': 'Grid', 'icon': 'mdi-view-grid'},
                    {'label': 'List', 'value': 'List', 'icon': 'mdi-view-list'},
                ],
                value={'label': 'Grid', 'value': 'Grid', 'icon': 'mdi-view-grid'},
                with_icons=True,
                icon_only=True
            )
            
        
        with nice.button('Extra Settings', variant='ghost', icon='mdi-dots-horizontal').classes('w-full'):
            with nice.menu():
                nice.menu_item('Export Theme', on_click=lambda: ui.notify('Exporting...'))
                nice.menu_item('Reset Defaults', on_click=lambda: ui.notify('Resetting...'))
                ui.separator().classes('bg-white/10')
                nice.menu_item('Delete System', on_click=lambda: ui.notify('Self-destruct in 3... 2... 1...'))

    # Component Demo: Custom Icons
    with nice.card().classes('w-[32rem] items-center nd-gap-md nd-p-lg'):
         ui.label('Custom Icon Support').classes('text-sm font-bold uppercase opacity-40')
         ui.label('Using Generic Components (Theme Icon) as Icons').classes('text-xs opacity-60 text-center')
         
         # --- Select Button with Changing Icon ---
         current_theme_var = {'name': 'Theme 1'}
         
         def render_current_icon():
             if current_theme_var['name'] == 'Theme 1':
                 nice.theme_icon(custom_palette, custom_texture, size="24px")
             else:
                 t = copy.deepcopy(custom_texture)
                 t.roundness = 2.0
                 nice.theme_icon(custom_palette, t, size="24px")

         with ui.row().classes('w-full items-center justify-between'):
             ui.label('Select Button').classes('opacity-60 font-medium')
             btn = nice.select_button(
                 label='Theme 1',
                 custom_icon_builder=render_current_icon
             ).classes('w-[180px]')
             
             with btn:
                 with nice.menu().on('hide', btn.reset_rotation):
                     nice.menu_item('Theme 1', on_click=lambda: (
                         current_theme_var.update({'name': 'Theme 1'}), 
                         btn.set_label('Theme 1'), 
                         btn.refresh(), 
                         btn.toggle_rotation()
                     ))
                     nice.menu_item('Theme 2', on_click=lambda: (
                         current_theme_var.update({'name': 'Theme 2'}), 
                         btn.set_label('Theme 2'), 
                         btn.refresh(), 
                         btn.toggle_rotation()
                     ))

         # --- Select Input with Custom Option Icons ---
         def get_icon_html_1():
             return nice.theme_icon.to_html(custom_palette, custom_texture, size="24px")
             
         def get_icon_html_2():
             import copy
             t = copy.deepcopy(custom_texture)
             t.roundness = 2.0 # Circle
             return nice.theme_icon.to_html(custom_palette, t, size="24px")

         with ui.row().classes('w-full items-center justify-between'):
             ui.label('Select Input').classes('opacity-60 font-medium')
             
             nice.select(
                 options={
                    'Theme 1': {'label': 'Theme 1', 'html': get_icon_html_1()},
                    'Theme 2': {'label': 'Theme 2', 'html': get_icon_html_2()}
                 },
                 value='Theme 1'
             ).classes('w-[180px]')

ui.run(title='Nice Design Tokens', reload=False, show=False)
