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
        with_icons: bool = False
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
        
        # Ensure the popup menu matches the design system
        self.props('popup-content-class="nd-select-menu"')

        # Add support for icons in options if explicitly requested
        if with_icons:
            self._setup_option_icons()

    def _setup_option_icons(self):
        """
        Sets up Quasar slots for rendering icons in options.
        Requires option-value, option-label, and map-options props to be set.
        """
        # Option slot (dropdown list)
        self.add_slot('option', '''
            <q-item v-bind="scope.itemProps" class="nd-menu-item">
                <q-item-section avatar v-if="scope.opt.icon">
                    <q-icon :name="scope.opt.icon" class="nd-icon" />
                </q-item-section>
                <q-item-section>
                    <q-item-label v-html="scope.opt.label" />
                </q-item-section>
            </q-item>
        ''')
        
        # Selected slot (main display)
        self.add_slot('selected', '''
            <div class="row items-center no-wrap" v-if="scope && scope.opt">
                <q-icon v-if="scope.opt && scope.opt.icon" :name="scope.opt.icon" class="q-mr-sm nd-icon" />
                <div v-if="scope.opt && scope.opt.label" v-html="scope.opt.label"></div>
            </div>
        ''')