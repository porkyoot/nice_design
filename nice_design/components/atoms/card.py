from nicegui import ui

class card(ui.card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes("nd-card")
        # Apply theme shadow
        self.style('box-shadow: var(--nd-shadow-md); transition: box-shadow var(--nd-transition-speed) ease;')
