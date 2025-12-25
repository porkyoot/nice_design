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
        minimal: bool = False
    ):
        super().__init__(options=options, label=label, value=value, on_change=on_change)

        # Apply design system classes
        self.classes('nd-select')
        if minimal:
            self.classes('nd-select--minimal')
            self.props('borderless dense')
        else:
            self.props('outlined standout="bg-primary text-white" rounded')

        # Remove Quasar defaults and apply premium props
        self.props('unelevated')

        # Ensure the popup menu is also themed (Quasar uses portal for menus)
        self.props('menu-props="content-class=nd-select-menu"')
