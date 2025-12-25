from nicegui import ui

class AppCard(ui.card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes("nds-card")
        self.props('unelevated')
