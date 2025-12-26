from typing import List, Dict, Any, Optional, Callable
from nicegui import ui
from .button import button

class multi_button(ui.element):
    """
    A segmented button group component that uses nice_design.button atoms.
    Inherits from ui.element to manage a collection of buttons, 
    but styled to feel like a single cohesive atomic component.
    """
    def __init__(
        self, 
        options: List[Dict[str, Any]], 
        value: Any = None, 
        on_change: Optional[Callable] = None
    ):
        super().__init__('div')
        # Cohesive container with items-stretch for full-height buttons
        self.classes('flex items-stretch nd-rounded-md overflow-hidden border border-white/10 nd-gap-0 w-fit h-9')
        self._value = value
        self.on_change = on_change
        self._btn_data: Dict[Any, Dict] = {}
        
        with self:
            for i, opt in enumerate(options):
                # We start with the ghost variant but force 'flat' to avoid Quasar borders
                btn = button(
                    icon=opt.get('icon'),
                    variant='ghost',
                    on_click=lambda o=opt: self.set_value(o['value'])
                ).classes('rounded-none border-none nd-px-md h-full')
                
                # Quasar 'flat' prop removes background and border
                btn.props('flat')
                
                color = opt.get('color')
                if color:
                    btn.style(f'color: {color} !important')
                
                self._btn_data[opt['value']] = {'btn': btn, 'color': color}
                    
        self._update_visuals()

    def set_value(self, val: Any):
        if self._value != val:
            self._value = val
            self._update_visuals()
            if self.on_change:
                self.on_change(val)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.set_value(val)

    def _update_visuals(self):
        for val, btn in self._btn_data.items():
            is_active = (val == self._value)
            b = btn['btn']
            
            # Reset common props/classes
            b.classes('nd-border-none nd-shadow-none shadow-none')
            
            if is_active:
                # Active: background matches custom color if provided, else falls back to primary
                bg_color = btn['color'] if btn['color'] else 'var(--nd-primary)'
                
                b.props('unelevated')
                b.props(remove='flat outline')
                b.classes('-nd-c-btn--primary').classes(remove='-nd-c-btn--ghost')
                b.style(f'color: white !important; background-color: {bg_color} !important; opacity: 1 !important')
            else:
                # Inactive: Flat/Ghost, transparent background
                b.props('flat')
                b.props(remove='unelevated outline')
                b.classes('-nd-c-btn--ghost').classes(remove='-nd-c-btn--primary')
                b.style('background-color: transparent !important')
                if btn['color']:
                    b.style(f'color: {btn["color"]} !important')
                else:
                    b.style(remove='color')
