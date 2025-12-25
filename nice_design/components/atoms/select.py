from nicegui import ui
from typing import List, Any, Optional, Callable, Dict


class select(ui.select):
    def __init__(self, options: Any, *args, **kwargs):
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
            isinstance(next(iter(options.values())), dict) and
            'icon' in next(iter(options.values()))
        )

        if is_rich_options:
            # SLOT: The Dropdown List ('option')
            self.add_slot('option', r'''
                <q-item v-bind="props.itemProps">
                    <q-item-section avatar>
                        <q-icon :name="props.opt.label.icon" :color="props.opt.label.color" />
                    </q-item-section>
                    <q-item-section>
                        <q-item-label>{{ props.opt.label.label }}</q-item-label>
                    </q-item-section>
                </q-item>
            ''')

            # SLOT: The Selected Item ('selected-item')
            self.add_slot('selected-item', r'''
                <div class="row items-center no-wrap -nd-u-gap-2">
                    <q-icon :name="props.opt.label.icon" :color="props.opt.label.color" size="xs" />
                    <div>{{ props.opt.label.label }}</div>
                </div>
            ''')
            
        self.props('outlined rounded standout="bg-primary text-on-primary"')
        self.classes('-nd-c-select')







