from nicegui import ui
from typing import List, Any, Optional, Callable, Dict

class select(ui.select):
    def __init__(self, 
                 options: Any, 
                 icon_only: bool = False, 
                 prepend: Optional[Callable] = None,
                 *args, **kwargs):
        # 1. Compatibility: Consume legacy 'with_icons' argument
        kwargs.pop('with_icons', None)

        # 2. Compatibility: Adapt List[Dict] to Dict[key, Dict] (Rich Options)
        #    If input is [{'label': 'A', 'value': 'a', ...}], convert to {'a': {'label': 'A', 'value': 'a', ...}}
        if isinstance(options, list) and options and isinstance(options[0], dict):
            new_options = {}
            for opt in options:
                key = opt.get('value')
                if key is not None:
                    new_options[key] = opt
            options = new_options

            # 2a. Fix 'value' argument if it was passed as a dict
            if 'value' in kwargs and isinstance(kwargs['value'], dict):
                kwargs['value'] = kwargs['value'].get('value')

        super().__init__(options, *args, **kwargs)
        
        # Check if options is a dictionary of dictionaries (Rich Options)
        # e.g. {'yt': {'label': 'Youtube', 'icon': 'smart_display', 'color': 'red'}}
        is_rich_options = (
            isinstance(options, dict) and 
            options and 
            isinstance(val_iter := next(iter(options.values()), None), dict) and
            ('icon' in val_iter or 'html' in val_iter or 'font' in val_iter)
        )


        if is_rich_options:
            # SLOT: The Dropdown List ('option')
            self.add_slot('option', r'''
                <q-item v-bind="props.itemProps">
                    <q-item-section avatar v-if="props.opt.label.icon || props.opt.label.html">
                        <div v-if="props.opt.label.html" v-html="props.opt.label.html"></div>
                        <q-icon v-else :name="props.opt.label.icon" :color="props.opt.label.color" size="sm" />
                    </q-item-section>
                    <q-item-section>
                        <q-item-label :style="props.opt.label.font ? { 'font-family': props.opt.label.font } : {}">{{ props.opt.label.label }}</q-item-label>
                    </q-item-section>
                </q-item>
            ''')

            # SLOT: The Selected Item ('selected-item')
            self.add_slot('selected-item', r'''
                <div class="row items-center no-wrap -nd-u-gap-2">
                    <div v-if="props.opt.label.html" v-html="props.opt.label.html"></div>
                    <q-icon v-else-if="props.opt.label.icon" :name="props.opt.label.icon" :color="props.opt.label.color" size="sm" />
                    <div :style="props.opt.label.font ? { 'font-family': props.opt.label.font } : {}">{{ props.opt.label.label }}</div>
                </div>
            ''')
            
        self.props('outlined rounded standout="bg-primary text-on-primary" popup-content-class="-nd-c-select-menu"')
        self.classes('-nd-c-select')

        # Handle icon_only mode
        if icon_only:
            self.classes('-nd-hide-label -nd-mode-icon-only')
            
        # Handle prepended custom content (e.g. theme_icon)
        if prepend:
            # We can use the 'prepend' slot of q-field/q-select.
            # NiceGUI allows adding elements to slots using 'with self.add_slot(...)':
            # But wait, self.add_slot(name) returns a 'Slot' context manager.
            # elements added inside are rendered in that slot.
            with self.add_slot('prepend'):
                prepend()
