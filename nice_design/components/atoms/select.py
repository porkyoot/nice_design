from nicegui import ui
from typing import List, Any, Optional

class select(ui.select):
    def __init__(
        self,
        options: List[Any],
        *,
        label: Optional[str] = None,
        value: Any = None,
        on_change = None,
        minimal: bool = False,
        icon: Optional[str] = None,
        icon_color: Optional[str] = None
    ):
        super().__init__(options=options, label=label, value=value, on_change=on_change)

        # Apply design system classes
        self.classes('nd-select')
        if minimal:
            self.classes('nd-select--minimal')
            self.props('borderless dense')
            if icon:
                with self.add_slot('prepend'):
                    i = ui.icon(icon).classes('nd-select__icon')
                    if icon_color:
                        i.style(f'color: {icon_color} !important')
                    else:
                        i.style('color: var(--nd-on-surface) !important')
        else:
            self.props('outlined standout="bg-primary text-white" rounded')

        # Remove Quasar defaults and apply premium props
        self.props('unelevated')
        
        # Ensure the popup menu matches the design system
        self.props('popup-content-class="nd-select-menu"')