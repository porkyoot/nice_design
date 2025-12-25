from nicegui import ui

class menu(ui.menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply design system classes
        self.classes('nd-menu')
        
        # Premium props for the Quasar q-menu
        self.props('transition-show="jump-down" transition-hide="jump-up"')

class menu_item(ui.menu_item):
     def __init__(self, text: str = '', on_click = None, *, auto_close: bool = True):
        super().__init__(text, on_click, auto_close=auto_close)
        self.classes('nd-menu-item')
