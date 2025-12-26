from nicegui import ui
from typing import List, Any, Optional, Callable, Dict

class select(ui.select):
    def __init__(self, 
                 options: Any, 
                 icon_only: bool = False, 
                 prepend: Optional[Callable] = None,
                 on_filter: Optional[Callable] = None,
                 *args, **kwargs):
        
        kwargs.pop('with_icons', None)
        self._on_filter_cb = on_filter
        
        # Normalize list of dicts to dict for NiceGUI
        if isinstance(options, list) and options and isinstance(options[0], dict):
            new_options = {}
            for opt in options:
                key = opt.get('value') or opt.get('label')
                if key is not None:
                    new_options[key] = opt
            options = new_options

        # Fix initial value if passed as dict
        if 'value' in kwargs and isinstance(kwargs['value'], dict):
            kwargs['value'] = kwargs['value'].get('value') or kwargs['value'].get('label')

        super().__init__(options, *args, **kwargs)
        
        # Check if options contain rich metadata
        def check_rich(opts):
             if not opts: return False
             first = next(iter(opts.values())) if isinstance(opts, dict) else opts[0]
             return isinstance(first, dict) and ('icon' in first or 'html' in first or 'font' in first)

        self._is_rich = check_rich(options)
        
        if self._is_rich:
            self._setup_rich_slots()
            # Tell Quasar how to extract the label for display
            self.props('option-label="label.label"')
            
        self.props('outlined rounded standout="bg-primary text-on-primary" popup-content-class="-nd-c-select-menu"')
        self.classes('-nd-c-select')

        if self._on_filter_cb:
            self.props('use-input fill-input hide-selected @filter="val => $emit(\'filter\', val)"')
            self.on('filter', self._handle_filter)

        if icon_only:
            self.classes('-nd-hide-label -nd-mode-icon-only')
            
        if prepend:
            with self.add_slot('prepend'):
                prepend()

    def _setup_rich_slots(self):
        # When NiceGUI passes dict options to Quasar:
        # {'key': {'label': 'Font', 'icon': '...', 'font': '...'}}
        # Becomes: {label: {'label': 'Font', ...}, value: 'key'}
        # So props.opt.label IS the rich object
        
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
                </q-item-section>
            </q-item>
        ''')

        self.add_slot('selected-item', r'''
            <div class="row items-center no-wrap -nd-u-gap-2" v-if="props.opt">
                <template v-if="props.opt.label && typeof props.opt.label === 'object'">
                    <div v-if="props.opt.label.html" v-html="props.opt.label.html"></div>
                    <q-icon v-else-if="props.opt.label.icon" :name="props.opt.label.icon" :color="props.opt.label.color" size="sm" />
                    <div :style="props.opt.label.font ? { 'font-family': props.opt.label.font } : {}">
                        {{ props.opt.label.label }}
                    </div>
                </template>
                <template v-else>
                    <div v-if="props.opt.html" v-html="props.opt.html"></div>
                    <q-icon v-else-if="props.opt.icon" :name="props.opt.icon" :color="props.opt.color" size="sm" />
                    <div :style="props.opt.font ? { 'font-family': props.opt.font } : {}">
                        {{ props.opt.label || props.opt }}
                    </div>
                </template>
            </div>
        ''')

    def _handle_filter(self, e):
        val = (e.args if isinstance(e.args, str) else "").lower()
        if self._on_filter_cb:
            new_opts = self._on_filter_cb(val)
            # Normalize if list was returned
            if isinstance(new_opts, list) and new_opts and isinstance(new_opts[0], dict):
                new_dict = {}
                for opt in new_opts:
                    key = opt.get('value') or opt.get('label')
                    if key is not None:
                        new_dict[key] = opt
                new_opts = new_dict
            
            self.options = new_opts
            self.update()
