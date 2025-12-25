from nicegui import ui

# 1. Define options as a Dictionary of Dictionaries
# The KEY ('yt') is what gets saved to select.value
# The VALUE (the dict) is the data payload for the UI
options_data = {
    'yt': {'label': 'Youtube', 'icon': 'smart_display', 'color': 'red'},
    'sp': {'label': 'Spotify', 'icon': 'music_note', 'color': 'green'},
    'fb': {'label': 'Facebook', 'icon': 'facebook', 'color': 'blue'},
}

# 2. Create the select
# We pass the dictionary directly. NiceGUI handles the mapping.
select = ui.select(options_data, value='yt', label="Select Platform").classes('w-64')

# 3. SLOT: The Dropdown List ('option')
# NiceGUI wraps your data so:
# - props.opt.value -> The Key (e.g., 'yt')
# - props.opt.label -> The Data Dict (e.g., {'label': 'Youtube', ...})
select.add_slot('option', r'''
    <q-item v-bind="props.itemProps">
        <q-item-section avatar>
            <q-icon :name="props.opt.label.icon" :color="props.opt.label.color" />
        </q-item-section>
        <q-item-section>
            <q-item-label>{{ props.opt.label.label }}</q-item-label>
        </q-item-section>
    </q-item>
''')

# 4. SLOT: The Selected Item ('selected-item')
# Same logic: Access the data via props.opt.label
select.add_slot('selected-item', r'''
    <q-chip dense :removable="false" :color="props.opt.label.color" text-color="white" class="my-0">
        <q-avatar :icon="props.opt.label.icon" text-color="white" />
        {{ props.opt.label.label }}
    </q-chip>
''')

# 5. Verify the output
# notice we just get the clean ID string 'yt', 'sp', etc.
label = ui.label()
select.on_value_change(lambda e: label.set_text(f"Selected ID: {e.value}"))

ui.run()