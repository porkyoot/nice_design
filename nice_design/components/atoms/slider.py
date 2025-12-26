from nicegui import ui
from typing import Optional, Callable, Any, Dict

class slider(ui.slider):
    """
    Standard slider component aligned with Nice Design system.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props('color="primary" label')
        self.classes('w-full')





class split_slider(ui.element):
    """
    A unified slider component with TWO distinct handles, splitting from a central zero.
    Controls TWO independent values (Left Value and Right Value).
    
    Structure:
    [ Left Slider (Max -> 0) ] | [ Right Slider (0 -> Max) ]
    
    The Left Slider is visually reversed so that its '0' is at the right end (center of component).
    """
    def __init__(self,
                 limit: float = 100.0,
                 step: float = 1.0,
                 value_left: float = 0.0,
                 value_right: float = 0.0,
                 color_left: str = 'primary',
                 color_right: str = 'secondary',
                 on_change: Optional[Callable[[Dict[str, float]], None]] = None):
        super().__init__('div')
        self.classes('relative-position w-full flex items-center justify-center my-2 gap-0 row no-wrap')
        # self.style('height: 40px;') 

        self._limit = limit
        self._step = step
        self._value_left = value_left
        self._value_right = value_right
        self._color_left = color_left
        self._color_right = color_right
        self._on_change = on_change
        
        with self:
            # --- Left Side Container ---
            # Flex-1 to take 50% width
            with ui.row().classes('col flex items-center justify-end relative-position px-0').style('height: 48px;'):
                # Track Background (Fake continuous track)
                # We need a track that runs along the middle.
                # Since Quasar slider has its own track, we rely on it, but we need to ensure they join nicely.
                # Actually, standard quasar track is fine.
                
                # Left Slider (Reverse Mode)
                # Range 0 to Limit. 
                # Reverse=True means Min (0) is at Right, Max (Limit) is at Left.
                # Selection fills from Min (Right/Center) to Thumb.
                self.slider_left = ui.slider(min=0, max=limit, step=step, value=value_left, on_change=self._handle_change_left)
                # 'reverse' prop makes 0 be at the right side.
                self.slider_left.props(f'reverse label color="{color_left}" track-size="4px" thumb-size="16px"')
                self.slider_left.classes('w-full')
                # Remove padding to make it touch the center
                # Quasar sliders have padding. We might need negative margins?
                # Let's try standard first.
                
            # --- Center Divider ---
            ui.element('div').classes('bg-grey-4').style('width: 2px; height: 12px; z-index: 10;')

            # --- Right Side Container ---
            with ui.row().classes('col flex items-center justify-start relative-position px-0').style('height: 48px;'):
                # Right Slider (Normal Mode)
                # Range 0 to Limit.
                # Min (0) is at Left (Center).
                # Selection fills from Min (Left/Center) to Thumb.
                self.slider_right = ui.slider(min=0, max=limit, step=step, value=value_right, on_change=self._handle_change_right)
                self.slider_right.props(f'label color="{color_right}" track-size="4px" thumb-size="16px"')
                self.slider_right.classes('w-full')

    def _handle_change_left(self, e):
        self._value_left = e.value
        self._notify()

    def _handle_change_right(self, e):
        self._value_right = e.value
        self._notify()
        
    def _notify(self):
        if self._on_change:
            self._on_change({'left': self._value_left, 'right': self._value_right})


class palette_slider(ui.element):
    """
    A horizontal color selection bar resembling a slider.
    Displays a set of colors and emphasizes the selected one by expanding it.
    Ideal for selecting a color from a palette (e.g., 8 accent colors).
    
    Visual Structure:
    [  ][  ][    SELECTED    ][  ][  ]
    """
    def __init__(self, 
                 colors: list,
                 value: Optional[str] = None, 
                 height: str = '12px',
                 on_change: Optional[Callable[[str], None]] = None):
        super().__init__('div')
        # Container styling
        self.classes('relative w-full rounded-full overflow-hidden flex row no-wrap shadow-sm cursor-pointer')
        self.style(f'height: {height};')
        
        # Validations
        if not colors:
             colors = ['#cccccc'] # Fallback
             
        self._colors = colors
        self._value = value if value in colors else colors[0]
        self._on_change = on_change
        self._items = {} # Map color -> element
        
        self._render_items()

    def _render_items(self):
        with self:
            for color in self._colors:
                # We use specific flex styles for animation
                # Flex-1 for unselected, Flex-4 for selected
                is_selected = (color == self._value)
                flex_val = '4' if is_selected else '1'
                
                item = ui.element('div').classes('h-full transition-all duration-300 ease-out relative hover:opacity-90')
                item.style(f'background-color: {color}; flex: {flex_val};')
                
                # Selection indicator
                if is_selected:
                    self._inject_indicator(item)
                    
                # Click event
                # Note: Capture color in lambda default arg
                item.on('click', lambda _, c=color: self.set_value(c))
                
                self._items[color] = item

    def _inject_indicator(self, container):
        with container:
            # A subtle dot to indicate active state clearly
             ui.element('div').classes('absolute-center w-1.5 h-1.5 rounded-full bg-white/90 shadow-sm ring-1 ring-black/10')

    def set_value(self, value: str):
        if value == self._value:
            return
        if value not in self._items:
            # If for some reason the value is not in our keys (e.g. hex case difference), try to find it or ignore
            # Simple check:
            if value not in self._colors:
                return
            
        self._value = value
        
        # Update styles efficiently
        for color, item in self._items.items():
            item.clear() # Remove any indicators
            
            if color == self._value:
                # Expand
                item.style(f'background-color: {color}; flex: 4;')
                self._inject_indicator(item)
            else:
                # Contract
                item.style(f'background-color: {color}; flex: 1;')
                
        if self._on_change:
            self._on_change(value)

