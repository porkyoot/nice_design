from nicegui import ui
from typing import Any, Dict, List, Optional, Callable, Union
from nice_design.components.atoms.button import button
from nice_design.components.atoms.menu import menu, menu_item

class select_menu(button):
    def __init__(self, 
                 options: Union[List, Dict], 
                 value: Any = None, 
                 on_change: Optional[Callable] = None, 
                 label: str = None, 
                 width: str = None,
                 **kwargs):
        
        # 1. Compatibility: Consume legacy 'with_icons' argument
        kwargs.pop('with_icons', None)
        
        # Parse options
        self.options_map = {}
        if isinstance(options, list):
             if options and isinstance(options[0], dict):
                  # List of dicts
                  for opt in options:
                      val = opt.get('value')
                      if val is not None:
                           self.options_map[val] = opt
             else:
                  # Simple list
                  for opt in options:
                       self.options_map[opt] = {'label': str(opt)}
        elif isinstance(options, dict):
             # Dict
             for k, v in options.items():
                 if isinstance(v, dict):
                      self.options_map[k] = v
                 else:
                      self.options_map[k] = {'label': str(v)}
        
        self._value = value
        self._on_change_handler = on_change
        self._placeholder = label
        
        # Initial Appearance
        initial_text, initial_icon = self._get_label_icon(value)
        
        # Determine icon_right
        icon_right = kwargs.pop('icon_right', 'arrow_drop_down')
        
        # Filter kwargs for button
        # button class signature: (text, variant, icon, on_click, rotate_icon)
        # It does NOT accept **kwargs.
        btn_kwargs = {}
        if 'variant' in kwargs:
            btn_kwargs['variant'] = kwargs.pop('variant')
        if 'rotate_icon' in kwargs:
            btn_kwargs['rotate_icon'] = kwargs.pop('rotate_icon')
        
        # We assume any other kwargs are intended for button props or ignored. 
        # Since button doesn't take kwargs, we must rely on .props() or properties for others.
        # But for now, let's just pass what button accepts.
            
        super().__init__(text=initial_text, icon=initial_icon, on_click=self.open_curr_menu, **btn_kwargs)
        
        # Apply icon_right
        if icon_right:
            self.props(f'icon-right="{icon_right}"')
        
        if width:
            self.style(f'width: {width}')
            
        # Add Menu
        with self:
             with menu() as self._menu_component:
                 self._render_menu_items()

    def _get_label_icon(self, value):
        if value is not None and value in self.options_map:
            opt = self.options_map[value]
            return opt.get('label', str(value)), opt.get('icon')
        # Use placeholder if available
        return (self._placeholder if self._placeholder else '', None)

    def open_curr_menu(self):
        self._menu_component.open()

    def _render_menu_items(self):
        self._menu_component.clear()
        with self._menu_component:
            for val, details in self.options_map.items():
                
                # Function factory to capture value
                def make_handler(v):
                    return lambda: self.set_value(v)
                
                lbl = details.get('label', str(val))
                icn = details.get('icon')
                clr = details.get('color')
                
                # Create item
                # We use properties to add icon/logic
                m = menu_item(on_click=make_handler(val))
                with m:
                     # Since we are using slots/internal structure, we might need to handle content
                     # If we just passed 'text' to menu_item, it creates default structure.
                     # We want richer structure if icons/colors present, 
                     # AND we want "selected" styling.
                     
                     m.style('min-width: 150px')
                     
                     # Highlight if selected
                     is_selected = (val == self._value)
                     if is_selected:
                         m.classes('bg-primary text-white')
                         
                     # Icon section
                     if icn:
                         with ui.element('q-item-section').props('avatar'):
                              ui.icon(icn, color=clr if not is_selected else None) 
                              # Note: if selected, text is white, icon should probably be white too or inherit.
                     
                     # Label section
                     with ui.element('q-item-section'):
                          ui.label(lbl)
                          
    def set_value(self, new_value: Any):
        if self._value != new_value:
            self._value = new_value
            
            # Update Trigger Button
            text, icon = self._get_label_icon(new_value)
            self.text = text
            self.icon = icon # Updates property
            
            # Re-render menu to update selection highlight
            self._render_menu_items()
            
            # Trigger Callback
            if self._on_change_handler:
                # Mimic event object with .value
                class EventMock:
                    def __init__(self, v, s):
                        self.value = v
                        self.sender = s
                self._on_change_handler(EventMock(new_value, self))

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self.set_value(new_value)
