from nicegui import ui

def configure_global_styles():
    """
    Configures global defaults for NiceGUI components using the native default_props API.
    """
    # Use ui.button.default_props('unelevated no-caps') to style all buttons.
    ui.button.default_props('unelevated no-caps')

    # Use ui.input.default_props('outlined dense') for inputs.
    ui.input.default_props('outlined dense')

    # Use ui.select.default_props('outlined dense behavior="menu"').
    ui.select.default_props('outlined dense behavior="menu"')

    # Use ui.card.default_props('flat bordered').
    ui.card.default_props('flat bordered')
