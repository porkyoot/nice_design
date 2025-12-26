from nicegui import ui
from typing import Optional, Callable, Any, Dict

class slider(ui.slider):
    """
    Standard slider component aligned with Nice Design system.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props('color="primary" label-always')
        self.classes('w-full')


class dual_slider(ui.element):
    """
    A centered 'dual' slider that fills from zero outwards.
    Useful for complementary values like shadow/highlight.
    
    Visual Structure:
    [Layer 0] Custom Track (Background)
    [Layer 1] Center Marker
    [Layer 2] Fill Bar (Dynamic)
    [Layer 3] Interactive Slider (Transparent track/selection)
    """
    def __init__(self, 
                 min: float = -1.0, 
                 max: float = 1.0, 
                 step: float = 0.1, 
                 value: float = 0.0,
                 color_left: str = 'primary',
                 color_right: str = 'secondary',
                 on_change: Optional[Callable] = None):
        super().__init__('div')
        self.classes('relative-position w-full flex items-center justify-center my-2')
        self.style('height: 40px; min-width: 120px;') # Ensure touch target size

        self._min = min
        self._max = max
        self._color_left = color_left
        self._color_right = color_right
        self._on_change = on_change
        self._value = value

        with self:
            # 1. Background Track
            ui.element('div').classes('absolute bg-grey-3 rounded-full').style(
                'left: 0; right: 0; top: 50%; height: 4px; transform: translateY(-50%); z-index: 0;'
            )

            # 2. Center Marker
            self.center_marker = ui.element('div').classes('absolute bg-grey-5').style(
                'left: 50%; top: 50%; height: 8px; width: 2px; transform: translate(-50%, -50%); z-index: 0;'
            )

            # 3. Dynamic Fill Bar
            self.fill_bar = ui.element('div').classes('absolute rounded-full pointer-events-none').style(
                'top: 50%; transform: translateY(-50%); height: 4px; z-index: 1; transition: all 0.1s ease;'
            )

            # 4. The Interactive Slider
            # We hide the native track and selection so we can render our own.
            self.slider = ui.slider(min=min, max=max, step=step, value=value, on_change=self._handle_change)
            self.slider.classes('w-full absolute inset-0 z-10')
            # 'selection-color="transparent"' hides the left-fill
            # 'track-color="transparent"' hides the background track
            self.slider.props('selection-color="transparent" track-color="transparent" label-always thumb-size="16px"')
            
        # Initial Render
        self._update_presentation(value)

    def _handle_change(self, e):
        self._value = e.value
        self._update_presentation(e.value)
        if self._on_change:
            self._on_change(e)

    def _resolve_color(self, color_name: str) -> str:
        """Helper to resolve Quasar/NiceDesign color names to CSS vars."""
        # Check standard palette names
        if color_name in ['primary', 'secondary', 'accent', 'positive', 'negative', 'info', 'warning']:
            return f'var(--nd-{color_name})'
        # Basic Colors
        if color_name in ['red', 'green', 'blue', 'orange', 'purple', 'grey']:
            # Quasar defines text-red, etc. but for background CSS we usually need var or hex.
            # NiceDesign might not have vars for these.
            # Fallback to name (browser handles 'red', 'blue')
            return color_name
        return color_name

    def _update_presentation(self, value):
        range_span = self._max - self._min
        if range_span == 0:
            norm = 0.5
        else:
            norm = (value - self._min) / range_span

        # Determine "Zero" position in the normalized 0..1 range
        if self._min <= 0 <= self._max:
            zero_norm = (0 - self._min) / range_span
        elif 0 < self._min:
            zero_norm = 0.0 # Zero is to the left
        else: # 0 > max
            zero_norm = 1.0 # Zero is to the right
            
        zero_norm = max(0.0, min(1.0, zero_norm))

        # Update Center Marker Position
        self.center_marker.style(f'left: {zero_norm * 100}%; top: 50%; height: 8px; width: 2px; transform: translate(-50%, -50%); z-index: 0;')

        # Calculate Fill Bar
        if norm >= zero_norm:
            # Positive / Right relative to zero
            left_pct = zero_norm * 100
            width_pct = (norm - zero_norm) * 100
            active_color = self._color_right
        else:
            # Negative / Left relative to zero
            left_pct = norm * 100
            width_pct = (zero_norm - norm) * 100
            active_color = self._color_left

        css_color = self._resolve_color(active_color)
        
        self.fill_bar.style(
            f'left: {left_pct}%; width: {width_pct}%; background-color: {css_color}; '
            f'top: 50%; transform: translateY(-50%); height: 4px; z-index: 1; transition: all 0.1s ease;'
        )

        # Optional: Update Thumb Color dynamically? 
        # ui.slider color prop affects thumb and selection.
        # We can update the slider color prop.
        self.slider.props(f'color="{active_color}"')


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
                self.slider_left.props(f'reverse label-always color="{color_left}" track-size="4px" thumb-size="16px"')
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
                self.slider_right.props(f'label-always color="{color_right}" track-size="4px" thumb-size="16px"')
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
