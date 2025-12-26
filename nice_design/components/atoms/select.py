from nicegui import ui
from typing import Any, Optional, Callable

class select(ui.select):
    def __init__(self, 
                 options: Any, 
                 icon_only: bool = False, 
                 prepend: Optional[Callable] = None,
                 on_filter: Optional[Callable] = None,
                 *args, **kwargs):
        
        # Clean up kwargs
        kwargs.pop('with_icons', None)
        self._on_filter_cb = on_filter
        
        # 1. Normalize Options (List -> Dict)
        # We ensure options are stored as: { 'value_id': {'label': 'Name', 'icon': '...', ...} }
        if isinstance(options, list) and options and isinstance(options[0], dict):
            new_options = {}
            for opt in options:
                # Use 'value' or 'label' as the ID key
                key = opt.get('value') or opt.get('label')
                if key is not None:
                    new_options[key] = opt
            options = new_options

        # 2. Fix Initial Value
        # If user passes value={'value': 'yt'...}, extract just 'yt'
        if 'value' in kwargs and isinstance(kwargs['value'], dict):
            kwargs['value'] = kwargs['value'].get('value') or kwargs['value'].get('label')

        super().__init__(options, *args, **kwargs)
        
        # 3. Rich Feature Detection
        def check_rich(opts):
             if not opts: return False
             # Peek at the first item to see if it has 'icon' or 'html'
             first = next(iter(opts.values())) if isinstance(opts, dict) else opts[0]
             return isinstance(first, dict) and ('icon' in first or 'html' in first or 'font' in first)

        self._is_rich = check_rich(options)
        
        # 4. Configure Quasar Props
        if self._is_rich:
            self._setup_rich_slots()
            # CRITICAL: Tell Quasar where to find the text string inside your wrapper
            # NiceGUI wraps your dict as: { value: 'id', label: { YOUR_DATA } }
            self.props('option-label="label.label"')
            
        self.props('outlined rounded standout="bg-primary text-on-primary" popup-content-class="-nd-c-select-menu"')
        self.classes('-nd-c-select')

        # 5. Search / Filter Logic
        if self._on_filter_cb:
            self.props('use-input fill-input input-debounce="0"')
            # Hide selected item while typing to show cursor
            self.props('hide-selected')
            # Server-side filtering: use @input-value not @filter
            # @filter with update() is for client-side filtering only
            self.on('input-value', self._handle_filter)


        if icon_only:
            self.classes('-nd-hide-label -nd-mode-icon-only')
            
        if prepend:
            with self.add_slot('prepend'):
                prepend()

    def _setup_rich_slots(self):
        # SLOT: The Dropdown List
        self.add_slot('option', r'''
            <q-item v-bind="props.itemProps">
                <q-item-section avatar v-if="props.opt.label.icon || props.opt.label.html">
                    <div v-if="props.opt.label.html" v-html="props.opt.label.html"></div>
                    <q-icon v-else :name="props.opt.label.icon" :color="props.opt.label.color" size="sm" />
                </q-item-section>
                <q-item-section>
                    <q-item-label :style="props.opt.label.font ? { 'font-family': props.opt.label.font } : {}">
                        {{ props.opt.label.label }}
                    </q-item-label>
                    <q-item-label caption v-if="props.opt.label.caption">{{ props.opt.label.caption }}</q-item-label>
                </q-item-section>
            </q-item>
        ''')

        # SLOT: The Selected Item (Input Box Display)
        # With hide-selected, this only shows when a value is selected (not while typing)
        self.add_slot('selected-item', r'''
            <div class="row items-center no-wrap -nd-u-gap-2" style="width: 100%;">
                <template v-if="props.opt && props.opt.label">
                    <div v-if="props.opt.label.html" v-html="props.opt.label.html"></div>
                    <q-icon v-else-if="props.opt.label.icon" :name="props.opt.label.icon" :color="props.opt.label.color" size="sm" />
                    <div :style="props.opt.label.font ? { 'font-family': props.opt.label.font } : {}">
                        {{ props.opt.label.label }}
                    </div>
                </template>
            </div>
        ''')

    def _handle_filter(self, e):
        # Handle the search text from the client
        val = (e.args if isinstance(e.args, str) else "").lower()
        
        if self._on_filter_cb:
            new_opts = self._on_filter_cb(val)
            
            # Normalize returned options if they are a list
            if isinstance(new_opts, list) and new_opts and isinstance(new_opts[0], dict):
                new_dict = {}
                for opt in new_opts:
                    key = opt.get('value') or opt.get('label')
                    if key is not None:
                        new_dict[key] = opt
                new_opts = new_dict
            
            # Push updates to the UI
            self.options = new_opts
            self.update()